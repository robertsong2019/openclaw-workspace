import type { Span } from './tracer.js';
export interface EvalCheckResult {
    dimension: string;
    score: number;
    reason: string;
}
export type EvalCheck = (spans: Span[]) => EvalCheckResult[];
export declare class Evaluator {
    private checks;
    private weights;
    addCheck(name: string, fn: EvalCheck, weight?: number): void;
    evaluate(spans: Span[], dimensions?: string[]): EvalCheckResult[];
    aggregateScore(results: EvalCheckResult[]): number;
    listChecks(): string[];
    removeCheck(name: string): boolean;
    setWeight(name: string, weight: number): boolean;
    resetChecks(): void;
    getCheck(name: string): {
        name: string;
        fn: EvalCheck;
        weight: number;
    } | undefined;
    /** Return dimension names from all registered checks */
    dimensionNames(): string[];
    /** Return overall pass rate (fraction of results with score >= 0.5) */
    overallPassRate(results: EvalCheckResult[]): number;
    /** Return dimensions with lowest scores from a set of results */
    topFailures(results: EvalCheckResult[], limit?: number): EvalCheckResult[];
    /** Run each check separately and return per-check results */
    evaluateEach(spans: Span[]): Array<{
        check: string;
        results: EvalCheckResult[];
    }>;
    /** Count how many results pass (score >= 0.5) */
    passCount(results: EvalCheckResult[]): number;
    /** Aggregate summary: total/pass/fail/avg/min/max by dimension */
    summary(results: EvalCheckResult[]): {
        total: number;
        passed: number;
        failed: number;
        avgScore: number;
        dimensions: number;
    };
    /** Filter results by dimension name */
    byDimension(results: EvalCheckResult[], dimension: string): EvalCheckResult[];
    /** Generate human-readable markdown report */
    toMarkdown(results: EvalCheckResult[]): string;
}
export declare function policyComplianceCheck(spans: Span[]): EvalCheckResult[];
export declare function latencyCheck(spans: Span[]): EvalCheckResult[];
export declare function reliabilityCheck(spans: Span[]): EvalCheckResult[];
export interface TraceComparison {
    dimension: string;
    baseline: number;
    current: number;
    delta: number;
    regression: boolean;
}
export declare function compareTraces(baselineSpans: Span[], currentSpans: Span[], checks?: EvalCheck[], threshold?: number): TraceComparison[];
export declare function costEfficiencyCheck(spans: Span[]): EvalCheckResult[];
