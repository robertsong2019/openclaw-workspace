/**
 * createOpenClawNode() — LangGraph.js node factory for OpenClaw agents.
 *
 * Wraps an executor function as a LangGraph.js node that:
 * - Reads the last message or task from state
 * - Injects it into a system prompt template
 * - Calls the executor (mock or real OpenClaw Gateway)
 * - Returns the result to a named state channel + tracks completion
 */

export interface RetryConfig {
  /** Max retry attempts (default: 0 = no retry) */
  maxRetries?: number;
  /** Base delay in ms for exponential backoff (default: 1000) */
  baseDelayMs?: number;
}

export interface OpenClawNodeConfig {
  /** Agent name (used for state tracking) */
  name: string;
  /** System prompt template; {input} is replaced with last message content */
  systemPrompt: string;
  /** Executor function — in production this calls OpenClaw Gateway */
  executor: (task: string) => Promise<string>;
  /** Output state field names (default: [name + "Result"]) */
  produces?: string[];
  /** Retry config for transient executor failures */
  retry?: RetryConfig;
}

export interface AgentState {
  messages?: Array<{ content: string }>;
  task?: string;
  completedSteps?: string[];
  [key: string]: unknown;
}

export function createOpenClawNode(config: OpenClawNodeConfig) {
  const { name, systemPrompt, executor, produces, retry } = config;
  const outputKey = (produces ?? [`${name}Result`])[0];
  const maxRetries = retry?.maxRetries ?? 0;
  const baseDelay = retry?.baseDelayMs ?? 1000;

  const executeWithRetry = async (prompt: string): Promise<string> => {
    let lastError: unknown;
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        return await executor(prompt);
      } catch (err) {
        lastError = err;
        if (attempt < maxRetries) {
          await new Promise((r) => setTimeout(r, baseDelay * Math.pow(2, attempt)));
        }
      }
    }
    throw lastError;
  };

  return async (state: AgentState): Promise<Record<string, unknown>> => {
    const lastMessage = state.messages?.at(-1)?.content ?? state.task ?? "";
    const prompt = systemPrompt.replace(/{input}/g, lastMessage);
    const result = await executeWithRetry(prompt);

    return {
      [outputKey]: result,
      completedSteps: name,
    };
  };
}
