/**
 * subgraph() — Encapsulate a set of nodes as a composable sub-graph.
 *
 * Maps outer state into inner state, runs nodes sequentially,
 * maps inner state back to outer, with its own error boundary.
 */

import type { AgentState } from "./create-node.js";

export interface SubgraphConfig {
  /** Subgraph name */
  name: string;
  /** Ordered node functions that operate on inner state */
  nodes: Array<(state: AgentState) => Promise<Record<string, unknown>>>;
  /** Map outer state → inner state before execution */
  inputMapping?: (state: AgentState) => AgentState;
  /** Map inner state → outer state patches after execution */
  outputMapping?: (state: Record<string, unknown>) => Record<string, unknown>;
  /** If true, isolate errors within the subgraph (don't throw) */
  isolateErrors?: boolean;
}

/**
 * Create a subgraph node: maps state in → runs nodes → maps state out.
 */
export function subgraph(config: SubgraphConfig) {
  const { name, nodes, inputMapping, outputMapping, isolateErrors = false } = config;

  return async (state: AgentState): Promise<Record<string, unknown>> => {
    // Map outer → inner
    let inner: Record<string, unknown> = {
      ...(inputMapping ? inputMapping(state) : state),
    };

    const errors: Array<{ step: number; message: string }> = [];

    for (let i = 0; i < nodes.length; i++) {
      try {
        const output = await nodes[i](inner as AgentState);
        inner = { ...inner, ...output };
      } catch (err) {
        const message = err instanceof Error ? err.message : String(err);
        if (isolateErrors) {
          errors.push({ step: i, message });
        } else {
          throw new Error(
            `Subgraph "${name}" failed at node ${i}: ${message}`
          );
        }
      }
    }

    // Map inner → outer
    const mapped = outputMapping ? outputMapping(inner) : inner;

    return {
      ...mapped,
      ...(errors.length > 0 ? { [`${name}Errors`]: errors } : {}),
    };
  };
}
