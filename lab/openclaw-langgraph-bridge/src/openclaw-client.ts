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
    const resp = await fetch(`${this.baseUrl}/api/sessions/spawn`, {
      method: "POST",
      headers: this.headers,
      body: JSON.stringify({
        task,
        mode: options?.mode ?? "run",
        runtime: options?.runtime ?? "subagent",
        ...(options?.timeoutSeconds ? { timeoutSeconds: options.timeoutSeconds } : {}),
      }),
    });

    if (!resp.ok) {
      throw new Error(`OpenClaw spawn failed: ${resp.status} ${await resp.text()}`);
    }

    const data = await resp.json();
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
