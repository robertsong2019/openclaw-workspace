/**
 * pipeline() — Sequential node composition.
 *
 * Chains multiple node functions so each receives the state
 * accumulated by the previous one, enabling linear workflow graphs.
 */

import type { AgentState } from "./create-node.js";

export interface PipelineConfig {
  /** Pipeline name (for error messages and state tracking) */
  name: string;
  /** Ordered list of node functions to execute */
  nodes: Array<(state: AgentState) => Promise<Record<string, unknown>>>;
  /** If true, continue on individual node errors (default: false) */
  continueOnError?: boolean;
}

export interface PipelineResult {
  /** Merged state from all nodes */
  state: Record<string, unknown>;
  /** Names of successfully completed nodes */
  completedSteps: string[];
  /** Errors keyed by node index */
  errors: Map<number, Error>;
}

/**
 * Create a pipeline that runs nodes sequentially, merging state.
 */
export function pipeline(config: PipelineConfig) {
  const { name, nodes, continueOnError = false } = config;

  return async (state: AgentState): Promise<Record<string, unknown>> => {
    let current: Record<string, unknown> = { ...state };
    const completedSteps: string[] = [];
    const errors = new Map<number, Error>();

    for (let i = 0; i < nodes.length; i++) {
      try {
        const input: AgentState = { ...current } as AgentState;
        const output = await nodes[i](input);
        current = { ...current, ...output };
        // Track step name from completedSteps if node sets it
        if (output.completedSteps) {
          completedSteps.push(
            ...(Array.isArray(output.completedSteps)
              ? output.completedSteps
              : [output.completedSteps])
          );
        }
      } catch (err) {
        if (!continueOnError) {
          throw new Error(
            `Pipeline "${name}" failed at node ${i}: ${err instanceof Error ? err.message : String(err)}`
          );
        }
        errors.set(i, err instanceof Error ? err : new Error(String(err)));
      }
    }

    return {
      ...current,
      completedSteps,
      ...(errors.size > 0 ? { [`${name}Errors`]: Object.fromEntries(errors) } : {}),
    };
  };
}
