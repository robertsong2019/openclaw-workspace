export class PolicyEngine {
    rules = new Map();
    addPolicy(category, rule) {
        const list = this.rules.get(category) ?? [];
        list.push(rule);
        this.rules.set(category, list);
    }
    removePolicy(category, ruleName) {
        const list = this.rules.get(category);
        if (!list)
            return false;
        const before = list.length;
        const filtered = list.filter(r => r.name !== ruleName);
        this.rules.set(category, filtered);
        return filtered.length < before;
    }
    evaluate(category, input) {
        const rules = this.rules.get(category) ?? [];
        const violations = [];
        for (const rule of rules) {
            if (!this.isRuleEnabled(category, rule.name))
                continue;
            const result = rule.evaluate(input);
            if (!result.allow) {
                violations.push({ rule: rule.name, reason: result.reason ?? 'Denied by policy' });
            }
        }
        return { allowed: violations.length === 0, violations };
    }
    loadFromJSON(data) {
        this._jsonDefs = data;
        for (const def of data) {
            const rule = this.buildRule(def);
            if (rule)
                this.addPolicy(def.category, rule);
        }
    }
    _jsonDefs = [];
    listCategories() {
        return [...this.rules.keys()];
    }
    ruleCount(category) {
        return this.rules.get(category)?.length ?? 0;
    }
    exportJSON() {
        return [...this._jsonDefs];
    }
    disabledRules = new Set();
    enableRule(category, ruleName) {
        this.disabledRules.delete(`${category}::${ruleName}`);
    }
    disableRule(category, ruleName) {
        this.disabledRules.add(`${category}::${ruleName}`);
    }
    isRuleEnabled(category, ruleName) {
        return !this.disabledRules.has(`${category}::${ruleName}`);
    }
    evaluateAll(input) {
        const results = {};
        for (const category of this.rules.keys()) {
            results[category] = this.evaluate(category, input);
        }
        return results;
    }
    /** Return all rule names across all categories */
    ruleNames() {
        const names = [];
        for (const rules of this.rules.values()) {
            for (const r of rules) {
                names.push(r.name);
            }
        }
        return names;
    }
    addPolicies(category, rules) {
        const list = this.rules.get(category) ?? [];
        list.push(...rules);
        this.rules.set(category, list);
    }
    batchEvaluate(inputs) {
        const results = {};
        for (const [category, input] of Object.entries(inputs)) {
            results[category] = this.evaluate(category, input);
        }
        return results;
    }
    getRule(category, ruleName) {
        return this.rules.get(category)?.find(r => r.name === ruleName);
    }
    hasCategory(category) {
        return this.rules.has(category) && (this.rules.get(category)?.length ?? 0) > 0;
    }
    /** Total rule count across all categories */
    countAll() {
        let total = 0;
        for (const rules of this.rules.values())
            total += rules.length;
        return total;
    }
    /** Import rules from JSON array, replacing existing rules */
    importRules(data) {
        this.rules.clear();
        this.disabledRules.clear();
        this._jsonDefs = [];
        let count = 0;
        for (const def of data) {
            const rule = this.buildRule(def);
            if (rule) {
                this.addPolicy(def.category, rule);
                this._jsonDefs.push(def);
                count++;
            }
        }
        return count;
    }
    /** Return all rules for a given category */
    getRulesByCategory(category) {
        return [...(this.rules.get(category) ?? [])];
    }
    /** Serialize all rules to JSON */
    toJSON() {
        const data = {};
        for (const [cat, rules] of this.rules) {
            data[cat] = rules.map(r => ({
                name: r.name,
                description: r.description,
                enabled: this.isRuleEnabled(cat, r.name),
            }));
        }
        return data;
    }
    /** Import rules from toJSON output (note: evaluate fns are lost, only metadata) */
    static fromJSON(data) {
        const engine = new PolicyEngine();
        for (const [cat, rules] of Object.entries(data)) {
            for (const r of rules) {
                engine.addPolicy(cat, {
                    name: r.name,
                    description: r.description,
                    category: cat,
                    evaluate: () => ({ allow: true }),
                });
            }
        }
        return engine;
    }
    clearCategory(category) {
        return this.rules.delete(category);
    }
    buildRule(def) {
        const helpers = {
            blockDestructiveOps: blockDestructiveOps,
            costLimit: costLimit,
            rateLimit: rateLimit,
            piiFilter: piiFilter,
        };
        const builder = helpers[def.type];
        return builder ? builder(def.config ?? {}) : null;
    }
}
// --- Built-in rule helpers ---
const DESTRUCTIVE_PATTERNS = ['rm ', 'drop ', 'delete ', 'truncate ', 'DROP ', 'DELETE ', 'TRUNCATE '];
export function blockDestructiveOps(_cfg = {}) {
    return {
        name: 'block_destructive_ops',
        description: 'Blocks commands that look destructive',
        category: 'tool_execution',
        evaluate: (input) => {
            const cmd = String(input.command ?? input.input ?? '');
            const blocked = DESTRUCTIVE_PATTERNS.some(p => cmd.includes(p));
            return blocked ? { allow: false, reason: `Destructive operation detected: ${cmd.slice(0, 50)}` } : { allow: true };
        },
    };
}
export function costLimit(cfg = {}) {
    const maxCost = Number(cfg.maxCost ?? 1.0);
    return {
        name: 'cost_limit',
        description: `Enforce max cost of $${maxCost}`,
        category: 'cost_control',
        evaluate: (input) => {
            const cost = Number(input.cost ?? input.estimatedCost ?? 0);
            return cost > maxCost
                ? { allow: false, reason: `Cost $${cost} exceeds limit $${maxCost}` }
                : { allow: true };
        },
    };
}
export function rateLimit(cfg = {}) {
    const maxCalls = Number(cfg.maxCalls ?? 10);
    const windowMs = Number(cfg.windowMs ?? 60_000);
    const timestamps = [];
    return {
        name: 'rate_limit',
        description: `Max ${maxCalls} calls per ${windowMs}ms`,
        category: 'rate_control',
        evaluate: (input) => {
            const now = Number(input.timestamp ?? Date.now());
            timestamps.push(now);
            const cutoff = now - windowMs;
            const recent = timestamps.filter(t => t >= cutoff);
            if (recent.length > maxCalls) {
                return { allow: false, reason: `Rate limit: ${recent.length} calls in window` };
            }
            return { allow: true };
        },
    };
}
const PII_PATTERNS = [/\b\d{3}[-.]?\d{2}[-.]?\d{4}\b/, /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/];
export function piiFilter(_cfg = {}) {
    return {
        name: 'pii_filter',
        description: 'Blocks input containing PII (SSN-like, email)',
        category: 'data_privacy',
        evaluate: (input) => {
            const text = String(input.text ?? input.content ?? input.input ?? '');
            const matched = PII_PATTERNS.find(p => p.test(text));
            return matched
                ? { allow: false, reason: 'PII detected in input' }
                : { allow: true };
        },
    };
}
