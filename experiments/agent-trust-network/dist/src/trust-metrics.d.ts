/**
 * TrustMetrics - 信任网络指标计算
 *
 * 提供高级信任分析功能：
 * - Trust Velocity: 信任变化速度
 * - Trust Volatility: 信任波动性
 * - Reputation Score: 综合声誉评分
 * - Confidence Level: 信任置信度
 */
import { Agent } from './agent';
export interface TrustSnapshot {
    timestamp: Date;
    trustScore: number;
    interactions: number;
    successRate: number;
}
export interface AgentMetrics {
    agentId: string;
    trustVelocity: number;
    trustVolatility: number;
    reputationScore: number;
    confidenceLevel: number;
    trend: 'rising' | 'falling' | 'stable';
    reliability: 'high' | 'medium' | 'low';
}
export interface NetworkMetrics {
    totalAgents: number;
    averageTrust: number;
    averageReputation: number;
    networkHealth: number;
    trustDistribution: {
        high: number;
        medium: number;
        low: number;
    };
    volatilityIndex: number;
    confidenceIndex: number;
}
export declare class TrustMetrics {
    private trustHistory;
    private readonly historySize;
    constructor(historySize?: number);
    /**
     * 记录信任快照
     */
    recordSnapshot(agent: Agent): void;
    /**
     * 计算 Agent 的信任指标
     */
    calculateAgentMetrics(agent: Agent): AgentMetrics;
    /**
     * 计算网络整体指标
     */
    calculateNetworkMetrics(agents: Agent[]): NetworkMetrics;
    /**
     * 计算信任变化速度
     * 返回 -1 到 1 之间的值
     * 正值表示信任上升，负值表示信任下降
     */
    private calculateTrustVelocity;
    /**
     * 计算信任波动性
     * 返回 0 到 1 之间的值
     * 0 表示非常稳定，1 表示非常不稳定
     */
    private calculateTrustVolatility;
    /**
     * 计算综合声誉评分
     * 考虑：当前信任分数、成功率、稳定性、交互数量
     */
    private calculateReputationScore;
    /**
     * 计算信任置信度
     * 表示我们对信任分数的确信程度
     * 基于交互次数和稳定性
     */
    private calculateConfidenceLevel;
    /**
     * 确定信任趋势
     */
    private determineTrend;
    /**
     * 确定可靠性等级
     */
    private determineReliability;
    /**
     * 计算网络健康度
     */
    private calculateNetworkHealth;
    /**
     * 获取 Agent 的信任历史
     */
    getHistory(agentId: string): TrustSnapshot[];
    /**
     * 清除历史记录
     */
    clearHistory(): void;
    /**
     * 导出所有历史记录
     */
    exportHistory(): Record<string, TrustSnapshot[]>;
    /**
     * 导入历史记录
     */
    importHistory(data: Record<string, TrustSnapshot[]>): void;
}
//# sourceMappingURL=trust-metrics.d.ts.map