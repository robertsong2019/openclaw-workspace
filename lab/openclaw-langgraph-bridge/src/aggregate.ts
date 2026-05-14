/**
 * aggregate() — Reduce multiple node results into a single state.
 *
 * Takes a reducer function that combines an array of partial states
 * into a single result. Useful after batch() or parallel fan-out.
 */

export interface AggregateConfig {
  /** Aggregate name (for error messages) */
  name?: string;
}

/**
 * Aggregate an array of partial states using a reducer function.
 *
 * The reducer receives the accumulated result and each partial state.
 * Initial value is an empty object.
 */
export function aggregate(
  reducer: (
    acc: Record<string, unknown>,
    partial: Record<string, unknown>,
    index: number
  ) => Record<string, unknown>,
  config: AggregateConfig = {}
): (partials: Record<string, unknown>[]) => Record<string, unknown> {
  const name = config.name ?? "aggregate";

  return (partials) => {
    if (!Array.isArray(partials)) {
      throw new TypeError(`${name}: expected array of partial states`);
    }
    return partials.reduce(reducer, {});
  };
}

/**
 * Built-in: merge all partials, last-write-wins.
 */
export function mergeAll(
  config?: AggregateConfig
): (partials: Record<string, unknown>[]) => Record<string, unknown> {
  return aggregate(
    (acc, partial) => ({ ...acc, ...partial }),
    { name: config?.name ?? "mergeAll" }
  );
}

/**
 * Built-in: collect values for each key into arrays.
 * { a: 1 }, { a: 2, b: 3 } → { a: [1, 2], b: [undefined, 3] }
 */
export function collectAll(
  config?: AggregateConfig
): (partials: Record<string, unknown>[]) => Record<string, unknown> {
  const name = config?.name ?? "collectAll";

  return (partials) => {
    if (!Array.isArray(partials)) {
      throw new TypeError(`${name}: expected array of partial states`);
    }
    // Collect all keys
    const allKeys = new Set<string>();
    for (const p of partials) {
      for (const k of Object.keys(p)) allKeys.add(k);
    }

    const result: Record<string, unknown[]> = {};
    for (const key of allKeys) {
      result[key] = partials.map((p) => p[key]);
    }
    return result;
  };
}
