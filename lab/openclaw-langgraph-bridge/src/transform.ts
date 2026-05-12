/**
 * transform() — Composable state transformation utilities.
 *
 * Pure functions that map input state to output state,
 * useful for data reshaping between nodes.
 */

import type { AgentState } from "./create-node.js";

export type TransformFn = (state: AgentState) => Record<string, unknown>;

/**
 * Create a node that picks specific fields from state.
 */
export function pick(...fields: string[]): TransformFn {
  return (state) => {
    const out: Record<string, unknown> = {};
    for (const f of fields) {
      if (f in state) out[f] = state[f];
    }
    return out;
  };
}

/**
 * Create a node that omits specific fields from state.
 */
export function omit(...fields: string[]): TransformFn {
  const exclude = new Set(fields);
  return (state) => {
    const out: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(state)) {
      if (!exclude.has(k)) out[k] = v;
    }
    return out;
  };
}

/**
 * Create a node that renames fields.
 */
export function rename(mapping: Record<string, string>): TransformFn {
  return (state) => {
    const out: Record<string, unknown> = { ...state };
    for (const [from, to] of Object.entries(mapping)) {
      if (from in out) {
        out[to] = out[from];
        delete out[from];
      }
    }
    return out;
  };
}

/**
 * Create a node that applies defaults for missing fields.
 */
export function defaults(values: Record<string, unknown>): TransformFn {
  return (state) => {
    const out = { ...state };
    for (const [k, v] of Object.entries(values)) {
      if (!(k in out) || out[k] === undefined) out[k] = v;
    }
    return out;
  };
}

/**
 * Compose multiple transforms into one (left to right).
 */
export function compose(...fns: TransformFn[]): TransformFn {
  return (state) => {
    let current: Record<string, unknown> = { ...state };
    for (const fn of fns) {
      current = fn(current as AgentState);
    }
    return current;
  };
}
