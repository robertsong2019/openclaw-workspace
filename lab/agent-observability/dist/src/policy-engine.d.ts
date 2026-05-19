export interface PolicyRule {
    name: string;
    description: string;
    category: string;
    evaluate: (input: Record<string, unknown>) => {
        allow: boolean;
        reason?: string;
    };
}
export interface EvalResult {
    allowed: boolean;
    violations: Array<{
        rule: string;
        reason: string;
    }>;
}
export declare class PolicyEngine {
    private rules;
    addPolicy(category: string, rule: PolicyRule): void;
    removePolicy(category: string, ruleName: string): boolean;
    evaluate(category: string, input: Record<string, unknown>): EvalResult;
    loadFromJSON(data: Array<{
        name: string;
        description: string;
        category: string;
        type: string;
        config?: Record<string, unknown>;
    }>): void;
    private _jsonDefs;
    listCategories(): string[];
    ruleCount(category: string): number;
    exportJSON(): Array<{
        name: string;
        description: string;
        category: string;
        type: string;
        config?: Record<string, unknown>;
    }>;
    private disabledRules;
    enableRule(category: string, ruleName: string): void;
    disableRule(category: string, ruleName: string): void;
    isRuleEnabled(category: string, ruleName: string): boolean;
    evaluateAll(input: Record<string, unknown>): Record<string, EvalResult>;
    /** Return all rule names across all categories */
    ruleNames(): string[];
    addPolicies(category: string, rules: PolicyRule[]): void;
    batchEvaluate(inputs: Record<string, Record<string, unknown>>): Record<string, EvalResult>;
    getRule(category: string, ruleName: string): PolicyRule | undefined;
    hasCategory(category: string): boolean;
    /** Total rule count across all categories */
    countAll(): number;
    /** Import rules from JSON array, replacing existing rules */
    importRules(data: Array<{
        name: string;
        description: string;
        category: string;
        type: string;
        config?: Record<string, unknown>;
    }>): number;
    /** Return all rules for a given category */
    getRulesByCategory(category: string): PolicyRule[];
    /** Serialize all rules to JSON */
    toJSON(): object;
    /** Import rules from toJSON output (note: evaluate fns are lost, only metadata) */
    static fromJSON(data: Record<string, Array<{
        name: string;
        description: string;
    }>>): PolicyEngine;
    clearCategory(category: string): boolean;
    private buildRule;
}
export declare function blockDestructiveOps(_cfg?: Record<string, unknown>): PolicyRule;
export declare function costLimit(cfg?: Record<string, unknown>): PolicyRule;
export declare function rateLimit(cfg?: Record<string, unknown>): PolicyRule;
export declare function piiFilter(_cfg?: Record<string, unknown>): PolicyRule;
