/**
 * Preset supervisor routers for common workflow patterns.
 */

import { END } from "@langchain/langgraph";

export interface RouterState {
  completedSteps?: string[];
  [key: string]: unknown;
}

/**
 * Merge results from parallel nodes into a single field.
 *
 * Usage: After fan-out (multiple edges from one node),
 * route all branches into a merge node that uses this function
 * to combine outputs into a structured summary.
 */
export function mergeResults(
  state: RouterState,
  sourceFields: string[],
  targetField: string = "mergedResult"
): Record<string, unknown> {
  const merged: Record<string, string> = {};
  for (const field of sourceFields) {
    const value = state[field];
    if (typeof value === "string") {
      merged[field] = value;
    }
  }
  return {
    [targetField]: JSON.stringify(merged),
  };
}

/**
 * Create a sequential router that visits steps in order,
 * skipping already-completed ones.
 */
export function sequentialRouter(steps: string[]) {
  return (state: RouterState): string => {
    const completed = new Set(state.completedSteps ?? []);
    for (const step of steps) {
      if (!completed.has(step)) return step;
    }
    return END;
  };
}

/**
 * Create a conditional router that checks a state field
 * to decide which branch to enter.
 */
export function conditionalRouter(
  field: string,
  mapping: Record<string, string>,
  fallback: string = END
) {
  return (state: RouterState): string => {
    const value = state[field];
    if (typeof value === "string" && mapping[value]) return mapping[value];
    return fallback;
  };
}
