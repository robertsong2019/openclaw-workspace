/**
 * OpenClaw Gateway HTTP client.
 *
 * In production, createOpenClawNode() executor is wired to this client
 * so each LangGraph node actually spawns an OpenClaw sub-agent.
 */

export interface OpenClawClientOptions {
  baseUrl: string;
  apiKey?: string;
}

export interface SpawnOptions {
  mode?: "run" | "session";
  runtime?: "subagent" | "acp";
  timeoutSeconds?: number;
}

export type HealthStatus = "ok" | "down";

export interface HealthResult {
  /** "ok" = reachable, 2xx, and gateway self-reports ok !== false */
  status: HealthStatus;
  /** HTTP status code when a response arrived (undefined when unreachable) */
  httpStatus?: number;
  /** gateway-reported `ok` flag, present when body parsed as JSON */
  ok?: boolean;
  /** gateway-reported `status` field, e.g. "live" / "degraded" */
  gatewayStatus?: string;
  /** why the check failed — present iff status === "down" */
  reason?: string;
}

export interface HealthOptions {
  /** abort budget for the whole check; default 2000ms. Never throws. */
  timeoutMs?: number;
}

export class OpenClawClient {
  private baseUrl: string;
  private headers: Record<string, string>;

  constructor({ baseUrl, apiKey }: OpenClawClientOptions) {
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.headers = {
      "Content-Type": "application/json",
      ...(apiKey ? { Authorization: `Bearer ${apiKey}` } : {}),
    };
  }

  /**
   * Spawn an OpenClaw agent and return its result.
   */
  async spawn(task: string, options?: SpawnOptions): Promise<string> {
    let resp: Response;
    try {
      resp = await fetch(`${this.baseUrl}/api/sessions/spawn`, {
        method: "POST",
        headers: this.headers,
        body: JSON.stringify({
          task,
          mode: options?.mode ?? "run",
          runtime: options?.runtime ?? "subagent",
          // explicit check so timeoutSeconds: 0 (valid: no timeout) is not dropped
          ...(options?.timeoutSeconds !== undefined
            ? { timeoutSeconds: options.timeoutSeconds }
            : {}),
        }),
      });
    } catch (err) {
      const reason = err instanceof Error ? err.message : String(err);
      throw new Error(
        `OpenClaw spawn failed: cannot reach gateway at ${this.baseUrl} (${reason})`
      );
    }

    if (!resp.ok) {
      throw new Error(`OpenClaw spawn failed: ${resp.status} ${await resp.text()}`);
    }

    // Read as text first: resp.json() consumes the body, leaving nothing to
    // include in the diagnostic if parsing fails (proxies may answer 2xx HTML).
    const text = await resp.text();
    let data: unknown;
    try {
      data = JSON.parse(text);
    } catch {
      throw new Error(
        `OpenClaw spawn failed: invalid JSON response (status ${resp.status}): ${text.slice(0, 120)}`
      );
    }
    return typeof data === "string" ? data : JSON.stringify(data);
  }

  /**
   * Probe the gateway (GET /healthz). Never throws — always returns a
   * HealthResult so callers can gate spawn() on it without try/catch.
   *
   * Mirrors the real gateway contract: 200 {ok: true, status: "live"}.
   */
  async health(options?: HealthOptions): Promise<HealthResult> {
    const timeoutMs = options?.timeoutMs ?? 2000;
    let resp: Response;
    try {
      resp = await fetch(`${this.baseUrl}/healthz`, {
        headers: this.headers,
        signal: AbortSignal.timeout(timeoutMs),
      });
    } catch (err) {
      const isAbort =
        err instanceof Error && (err.name === "TimeoutError" || err.name === "AbortError");
      const reason = err instanceof Error ? err.message : String(err);
      return {
        status: "down",
        reason: isAbort
          ? `health check timed out after ${timeoutMs}ms`
          : `cannot reach gateway at ${this.baseUrl} (${reason})`,
      };
    }

    const text = await resp.text();
    if (!resp.ok) {
      return { status: "down", httpStatus: resp.status, reason: `${resp.status} ${text.slice(0, 120)}` };
    }

    try {
      const data = JSON.parse(text) as { ok?: unknown; status?: unknown };
      const gatewayStatus = typeof data.status === "string" ? data.status : undefined;
      if (data.ok === false) {
        return { status: "down", httpStatus: resp.status, ok: false, gatewayStatus, reason: `gateway self-reports not-ok (status: ${gatewayStatus ?? "unknown"})` };
      }
      return { status: "ok", httpStatus: resp.status, ok: data.ok === true, gatewayStatus };
    } catch {
      return {
        status: "down",
        httpStatus: resp.status,
        reason: `invalid JSON response (status ${resp.status}): ${text.slice(0, 120)}`,
      };
    }
  }

  /**
   * Create an executor function suitable for createOpenClawNode().
   */
  executor(systemPrompt?: string): (task: string) => Promise<string> {
    return async (task: string) => {
      const fullTask = systemPrompt ? `${systemPrompt}\n\n${task}` : task;
      return this.spawn(fullTask);
    };
  }
}
