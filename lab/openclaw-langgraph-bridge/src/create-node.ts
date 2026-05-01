/**
 * createOpenClawNode() — LangGraph.js node factory for OpenClaw agents.
 *
 * Wraps an executor function as a LangGraph.js node that:
 * - Reads the last message or task from state
 * - Injects it into a system prompt template
 * - Calls the executor (mock or real OpenClaw Gateway)
 * - Returns the result to a named state channel + tracks completion
 */

export interface OpenClawNodeConfig {
  /** Agent name (used for state tracking) */
  name: string;
  /** System prompt template; {input} is replaced with last message content */
  systemPrompt: string;
  /** Executor function — in production this calls OpenClaw Gateway */
  executor: (task: string) => Promise<string>;
  /** Output state field names (default: [name + "Result"]) */
  produces?: string[];
}

export interface AgentState {
  messages?: Array<{ content: string }>;
  task?: string;
  completedSteps?: string[];
  [key: string]: unknown;
}

export function createOpenClawNode(config: OpenClawNodeConfig) {
  const { name, systemPrompt, executor, produces } = config;
  const outputKey = (produces ?? [`${name}Result`])[0];

  return async (state: AgentState): Promise<Record<string, unknown>> => {
    const lastMessage = state.messages?.at(-1)?.content ?? state.task ?? "";
    const prompt = systemPrompt.replace(/{input}/g, lastMessage);
    const result = await executor(prompt);

    return {
      [outputKey]: result,
      completedSteps: name,
    };
  };
}
