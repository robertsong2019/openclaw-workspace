/**
 * switchRoute() — Multi-branch routing based on state field value.
 *
 * Like a switch/case for LangGraph edges: inspect a state field,
 * match against cases, and return the matching node name.
 * Supports default fallback, predicate functions, and priority ordering.
 */

import type { AgentState } from "./create-node.js";

export interface SwitchCase {
  /** Value to match (string) or a predicate function */
  match: string | ((value: unknown, state: AgentState) => boolean);
  /** Target node name to route to */
  route: string;
}

export interface SwitchRouteConfig {
  /** State field to inspect */
  field: string;
  /** Ordered list of cases — first match wins */
  cases: SwitchCase[];
  /** Default route if no case matches (default: "__end__") */
  default?: string;
}

/**
 * Create a switch-case router for LangGraph conditional edges.
 */
export function switchRoute(config: SwitchRouteConfig) {
  const { field, cases, default: defaultRoute = "__end__" } = config;

  return (state: AgentState): string => {
    const value = state[field];

    for (const c of cases) {
      if (typeof c.match === "function") {
        if (c.match(value, state)) return c.route;
      } else {
        if (value === c.match) return c.route;
      }
    }

    return defaultRoute;
  };
}
