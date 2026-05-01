/**
 * Preset supervisor routers for common workflow patterns.
 */

import { END } from "@langchain/langgraph";

export interface RouterState {
  completedSteps?: string[];
  [key: string]: unknown;
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
