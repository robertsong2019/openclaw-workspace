/**
 * Tap into a node pipeline for side effects without modifying state.
 *
 * tap() calls a callback with the current state but always returns
 * the original state unchanged. Useful for logging, metrics, debugging,
 * or triggering notifications.
 */

export interface TapConfig {
  /** Side-effect callback. If it throws, the error is swallowed (or passed to onError). */
  onState: (state: Record<string, unknown>) => void | Promise<void>;
  /** Optional error handler for when onState throws. */
  onError?: (error: unknown, state: Record<string, unknown>) => void;
}

/**
 * Create a tap node: calls `onState` for side effects, always returns original state.
 */
export function tap(config: TapConfig): (state: Record<string, unknown>) => Promise<Record<string, unknown>> {
  return async (state) => {
    try {
      await config.onState(state);
    } catch (err) {
      if (config.onError) {
        config.onError(err, state);
      }
      // Swallow error — tap must never break the pipeline
    }
    return state;
  };
}

/**
 * Wrap an existing node, adding a tap before it executes.
 */
export function tapBefore(
  node: (state: Record<string, unknown>) => Promise<Record<string, unknown>>,
  onState: (state: Record<string, unknown>) => void | Promise<void>
): (state: Record<string, unknown>) => Promise<Record<string, unknown>> {
  return async (state) => {
    try { await onState(state); } catch { /* swallow */ }
    return node(state);
  };
}

/**
 * Wrap an existing node, adding a tap after it executes (sees the output state).
 */
export function tapAfter(
  node: (state: Record<string, unknown>) => Promise<Record<string, unknown>>,
  onState: (state: Record<string, unknown>) => void | Promise<void>
): (state: Record<string, unknown>) => Promise<Record<string, unknown>> {
  return async (state) => {
    const result = await node(state);
    try { await onState(result); } catch { /* swallow */ }
    return result;
  };
}
