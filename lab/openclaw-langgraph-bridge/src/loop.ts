/**
 * loop() — Conditional loop that re-runs a node until a condition is met.
 *
 * A fundamental graph pattern: repeat a node with accumulated state
 * until a termination predicate returns true, with a max-iterations guard.
 */

import type { AgentState } from "./create-node.js";

export interface LoopConfig {
  /** Loop name (for error messages and state tracking) */
  name: string;
  /** The node function to repeat */
  node: (state: AgentState) => Promise<Record<string, unknown>>;
  /** Termination predicate — loop stops when this returns true */
  until: (state: Record<string, unknown>, iteration: number) => boolean;
  /** Max iterations before forcing stop (default: 10) */
  maxIterations?: number;
}

/**
 * Create a loop node that re-runs a node function until a condition is met.
 *
 * The node receives accumulated state each iteration. When `until` returns
 * true or maxIterations is reached, the final state is returned.
 */
export function loop(config: LoopConfig) {
  const { name, node, until, maxIterations = 10 } = config;

  return async (state: AgentState): Promise<Record<string, unknown>> => {
    let current: Record<string, unknown> = { ...state };
    let iteration = 0;

    while (iteration < maxIterations) {
      const input: AgentState = { ...current } as AgentState;
      const output = await node(input);
      current = { ...current, ...output };
      iteration++;

      if (until(current, iteration)) break;
    }

    return {
      ...current,
      [`${name}Iterations`]: iteration,
    };
  };
}
