/**
 * State validation utilities for OpenClaw LangGraph nodes.
 *
 * validateState() checks required fields exist and optionally match a type,
 * returning structured error info instead of throwing deep inside executor calls.
 */

export interface FieldRule {
  /** State field name */
  field: string;
  /** Expected JS type (typeof result). Skip check if omitted. */
  type?: string;
  /** Custom validation function */
  validate?: (value: unknown) => boolean;
}

export interface ValidationResult {
  valid: boolean;
  errors: string[];
}

/**
 * Validate that required fields exist (and optionally match type/predicate)
 * on a state object. Returns a structured result — never throws.
 */
export function validateState(
  state: Record<string, unknown>,
  rules: FieldRule[]
): ValidationResult {
  const errors: string[] = [];

  for (const rule of rules) {
    const value = state[rule.field];
    if (value === undefined || value === null) {
      errors.push(`Missing required field: "${rule.field}"`);
      continue;
    }
    if (rule.type && typeof value !== rule.type) {
      errors.push(
        `Field "${rule.field}" expected type "${rule.type}", got "${typeof value}"`
      );
    }
    if (rule.validate && !rule.validate(value)) {
      errors.push(`Field "${rule.field}" failed custom validation`);
    }
  }

  return { valid: errors.length === 0, errors };
}

/**
 * Create a node wrapper that validates state before calling the real node.
 * If validation fails, returns {validationError} instead of calling the node.
 */
export function withValidation(
  node: (state: Record<string, unknown>) => Promise<Record<string, unknown>>,
  rules: FieldRule[]
): (state: Record<string, unknown>) => Promise<Record<string, unknown>> {
  return async (state) => {
    const result = validateState(state, rules);
    if (!result.valid) {
      return { validationError: result.errors.join("; ") };
    }
    return node(state);
  };
}
