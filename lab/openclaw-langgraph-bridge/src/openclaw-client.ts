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
   * Create an executor function suitable for createOpenClawNode().
   */
  executor(systemPrompt?: string): (task: string) => Promise<string> {
    return async (task: string) => {
      const fullTask = systemPrompt ? `${systemPrompt}\n\n${task}` : task;
      return this.spawn(fullTask);
    };
  }
}
