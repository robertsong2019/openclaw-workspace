/**
 * Fallback and state mapping utilities for resilient workflows.
 *
 * withFallback() wraps a node to catch errors and return a default result.
 * mapState() transforms state fields between nodes (rename, pick, reshape).
 */

/**
 * Wrap a node so that on failure it returns `fallbackValue` instead of throwing.
 * Optionally logs the error via `onError` callback.
 */
export function withFallback(
  node: (state: Record<string, unknown>) => Promise<Record<string, unknown>>,
  fallbackValue: Record<string, unknown>,
  onError?: (error: unknown, state: Record<string, unknown>) => void
): (state: Record<string, unknown>) => Promise<Record<string, unknown>> {
  return async (state) => {
    try {
      return await node(state);
    } catch (err) {
      onError?.(err, state);
      return fallbackValue;
    }
  };
}

/**
 * Create a state transformer that maps fields from input to output.
 *
 * Useful when a downstream node expects different field names
 * than the upstream produces, or when you need to reshape state
 * at a branch point.
 *
 * @param mapping - { inputField: outputField } pairs
 * @param passthrough - if true, include all original fields (default: false)
 */
export function mapState(
  mapping: Record<string, string>,
  passthrough: boolean = false
): (state: Record<string, unknown>) => Record<string, unknown> {
  return (state) => {
    const result: Record<string, unknown> = passthrough ? { ...state } : {};
    for (const [from, to] of Object.entries(mapping)) {
      if (from in state) {
        result[to] = state[from];
      }
    }
    return result;
  };
}
