/**
 * Agent - 网络中的代理节点
 */
export type AgentBehavior = 'cooperative' | 'neutral' | 'malicious' | 'adversarial';
export interface AgentConfig {
    id: string;
    name: string;
    behavior: AgentBehavior;
    initialTrust?: number;
    expertise?: string[];
    reliability?: number;
}
export declare class Agent {
    readonly id: string;
    readonly name: string;
    readonly behavior: AgentBehavior;
    readonly expertise: string[];
    readonly reliability: number;
    private _trustScore;
    private _interactions;
    private _successfulInteractions;
    private _lastActiveTime;
    constructor(config: AgentConfig);
    get trustScore(): number;
    set trustScore(value: number);
    get interactions(): number;
    get successRate(): number;
    get lastActiveTime(): Date;
    /**
     * 记录一次交互
     */
    recordInteraction(success: boolean): void;
    /**
     * 决定是否与另一个 Agent 合作
     */
    shouldCooperate(otherAgent: Agent): boolean;
    /**
     * 执行任务（根据行为类型返回结果）
     */
    performTask(taskComplexity?: number): boolean;
    private getBaseSuccessRate;
    /**
     * 导出状态
     */
    toJSON(): object;
}
//# sourceMappingURL=agent.d.ts.map