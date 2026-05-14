/**
 * Composable middleware chain for LangGraph nodes.
 *
 * `withMiddleware(node, [mw1, mw2, mw3])` applies middleware in left-to-right
 * order: mw1 wraps mw2 wraps mw3 wraps node. Each middleware receives the
 * `next` function (the wrapped node or next middleware) and the current state,
 * and must return a partial/full state object.
 *
 * This provides a cleaner alternative to manually nesting withRetry, withTimeout,
 * withFallback, etc. Middleware can inspect/modify state before and after calling
 * `next(state)`, and can short-circuit by returning without calling next.
 */

export type NodeFn = (state: Record<string, unknown>) => Promise<Record<string, unknown>>;

export type Middleware = (
  next: NodeFn,
  state: Record<string, unknown>,
) => Promise<Record<string, unknown>>;

/**
 * Wrap a node function with an ordered chain of middleware.
 *
 * Middleware are applied left-to-right: `[mw1, mw2]` means mw1 is outermost.
 * Each middleware receives `(next, state)` and must return a state object.
 */
export function withMiddleware(
  node: NodeFn,
  middlewares: Middleware[],
): NodeFn {
  // Fold right: last middleware wraps the node directly
  const wrapped = middlewares.reduceRight(
    (inner, mw) => {
      return (state: Record<string, unknown>) => mw(inner, state);
    },
    node,
  );
  return wrapped;
}
