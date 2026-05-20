/**
 * Partition state into multiple branches based on predicates.
 *
 * partition() evaluates a set of named predicates against the current state
 * and returns only the matching branches' state transformations.
 * Useful for conditional fan-out where each branch gets different state slices.
 */

/**
 * A branch definition: a predicate function and an optional state transformer.
 */
export interface PartitionBranch {
  /** Return true to include this branch in the output. */
  when: (state: Record<string, unknown>) => boolean;
  /** Optional state transform applied to matching branches. */
  select?: (state: Record<string, unknown>) => Record<string, unknown>;
}

export interface PartitionConfig {
  /** Named branches to evaluate. */
  branches: Record<string, PartitionBranch>;
  /** If no branch matches, return this (default: empty object). */
  defaultResult?: Record<string, unknown>;
}

/**
 * Evaluate all branches against state, return object keyed by matching branch names.
 */
export function partition(
  config: PartitionConfig
): (state: Record<string, unknown>) => Record<string, Record<string, unknown>> {
  return (state) => {
    const result: Record<string, Record<string, unknown>> = {};
    let matched = false;
    for (const [name, branch] of Object.entries(config.branches)) {
      if (branch.when(state)) {
        matched = true;
        result[name] = branch.select ? branch.select(state) : { ...state };
      }
    }
    if (!matched && config.defaultResult) {
      result["_default"] = config.defaultResult;
    }
    return result;
  };
}

/**
 * A simpler variant: split an array field into groups by predicate.
 * Returns { match: T[], rest: T[] }.
 */
export function splitBy<T = unknown>(
  field: string,
  predicate: (item: T) => boolean
): (state: Record<string, unknown>) => { match: T[]; rest: T[] } {
  return (state) => {
    const arr = Array.isArray(state[field]) ? (state[field] as T[]) : [];
    const match: T[] = [];
    const rest: T[] = [];
    for (const item of arr) {
      if (predicate(item)) {
        match.push(item);
      } else {
        rest.push(item);
      }
    }
    return { match, rest };
  };
}
