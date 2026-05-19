/**
 * race() — Returns the result of whichever node finishes first.
 *
 * Runs multiple nodes concurrently; the first to resolve wins.
 * Losers are ignored. Useful for "fastest responder" patterns.
 */

import type { AgentState } from "./create-node.js";

export interface RaceConfig {
  /** Race name (for state metadata) */
  name: string;
  /** Named nodes to race against each other */
  nodes: Record<string, (state: AgentState) => Promise<Record<string, unknown>>>;
  /** If all nodes fail, return this instead of throwing (optional) */
  fallback?: Record<string, unknown>;
}

/**
 * Run named nodes concurrently, return result of first to finish.
 * Adds `_raceWinner` field to indicate which node won.
 */
export function race(config: RaceConfig) {
  const { name, nodes, fallback } = config;

  return async (state: AgentState): Promise<Record<string, unknown>> => {
    const entries = Object.entries(nodes);
    if (entries.length === 0) {
      return fallback ?? {};
    }

    const wrapped = entries.map(
      ([key, node]) =>
        node({ ...state } as AgentState).then((result) => ({ key, result })),
    );

    try {
      const winner = await Promise.any(wrapped);
      return {
        ...winner.result,
        _raceWinner: winner.key,
      };
    } catch {
      // All rejected (AggregateError)
      if (fallback) return fallback;
      throw new Error(`Race "${name}": all nodes failed`);
    }
  };
}
