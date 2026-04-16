/**
 * TrustNetwork - 多 Agent 信任网络
 *
 * 使用 PageRank 式算法计算信任分数
 */
import { Agent, AgentBehavior } from './agent';
export interface TrustRelation {
    from: string;
    to: string;
    weight: number;
    timestamp: Date;
}
export interface NetworkStats {
    totalAgents: number;
    totalRelations: number;
    averageTrust: number;
    trustDistribution: Record<AgentBehavior, number>;
    clusterCount: number;
}
export declare class TrustNetwork {
    private agents;
    private relations;
    private trustMatrix;
    private readonly dampingFactor;
    private readonly convergenceThreshold;
    private readonly maxIterations;
    private readonly trustDecayRate;
    constructor(config?: {
        dampingFactor?: number;
        trustDecayRate?: number;
    });
    /**
     * 添加 Agent 到网络
     */
    addAgent(agent: Agent): void;
    /**
     * 移除 Agent
     */
    removeAgent(agentId: string): void;
    /**
     * 建立/更新信任关系
     */
    setTrustRelation(fromId: string, toId: string, weight: number): void;
    /**
     * 获取两个 Agent 之间的信任权重
     */
    getTrustWeight(fromId: string, toId: string): number;
    /**
     * 计算信任分数（PageRank 算法）
     */
    calculateTrustScores(): Map<string, number>;
    /**
     * 获取节点的出链总权重
     */
    private getOutgoingWeight;
    /**
     * 检查是否收敛
     */
    private checkConvergence;
    /**
     * 应用信任衰减
     */
    applyTrustDecay(hoursElapsed: number): void;
    /**
     * 模拟交互
     */
    simulateInteraction(requesterId: string, providerId: string, taskComplexity?: number): {
        success: boolean;
        trustChange: number;
    };
    /**
     * 识别恶意 Agent
     */
    identifyMaliciousAgents(threshold?: number): string[];
    /**
     * 获取可信 Agent
     */
    getTrustedAgents(threshold?: number): Agent[];
    /**
     * 获取网络统计
     */
    getStats(): NetworkStats;
    /**
     * 估算网络中的集群数量（简化算法）
     */
    private estimateClusterCount;
    /**
     * 导出网络状态
     */
    export(): object;
    /**
     * 导入网络状态
     */
    static import(data: any): TrustNetwork;
}
//# sourceMappingURL=trust-network.d.ts.map