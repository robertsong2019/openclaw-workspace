/**
 * withRateLimit() — Rate limiting node wrapper.
 *
 * Ensures a node is not called more than N times within a time window.
 * Uses a sliding window counter.
 */

import type { AgentState } from "./create-node.js";

export interface RateLimitConfig {
  /** Max calls allowed in the window */
  maxCalls: number;
  /** Window duration in milliseconds */
  windowMs: number;
  /** Key function to partition rate limits by state (default: global) */
  keyFn?: (state: AgentState) => string;
  /** What to do when rate limited: "reject" throws, "return" returns fallback state */
  strategy?: "reject" | "return";
  /** Fallback state when rate limited (only for strategy "return") */
  fallbackState?: Record<string, unknown>;
}

interface WindowEntry {
  timestamps: number[];
}

/**
 * Wrap a node with rate limiting.
 */
export function withRateLimit(
  node: (state: AgentState) => Promise<Record<string, unknown>>,
  config: RateLimitConfig
) {
  const { maxCalls, windowMs, keyFn, strategy = "reject", fallbackState = {} } = config;
  const windows = new Map<string, WindowEntry>();

  function cleanup(key: string, now: number) {
    const entry = windows.get(key);
    if (!entry) return;
    entry.timestamps = entry.timestamps.filter((t) => now - t < windowMs);
    if (entry.timestamps.length === 0) windows.delete(key);
  }

  return async (state: AgentState): Promise<Record<string, unknown>> => {
    const now = Date.now();
    const key = keyFn ? keyFn(state) : "__global__";

    cleanup(key, now);

    const entry = windows.get(key) ?? { timestamps: [] };
    if (entry.timestamps.length >= maxCalls) {
      if (strategy === "reject") {
        throw new Error(
          `Rate limit exceeded for key "${key}": ${maxCalls} calls per ${windowMs}ms`
        );
      }
      return { ...fallbackState, rateLimited: true };
    }

    entry.timestamps.push(now);
    windows.set(key, entry);

    return node(state);
  };
}
