/**
 * AdvancedAgent - 支持高级博弈论策略的 Agent
 *
 * 实现了经典的博弈论策略：
 * - Tit-for-Tat (以牙还牙)
 * - Grim Trigger (冷酷触发)
 * - Pavlov (赢留输变)
 * - Random (随机)
 * - Adaptive (自适应)
 */
import { Agent, AgentConfig } from './agent';
export type AdvancedStrategy = 'tit-for-tat' | 'grim-trigger' | 'pavlov' | 'random' | 'adaptive';
export interface AdvancedAgentConfig extends AgentConfig {
    strategy?: AdvancedStrategy;
    memoryLength?: number;
    initialCooperation?: boolean;
}
interface InteractionHistory {
    partnerId: string;
    cooperated: boolean;
    timestamp: Date;
}
export declare class AdvancedAgent extends Agent {
    readonly strategy: AdvancedStrategy;
    readonly memoryLength: number;
    private interactionHistory;
    private grimTriggered;
    private lastMove;
    private initialCooperation;
    constructor(config: AdvancedAgentConfig);
    /**
     * 决定是否与另一个 Agent 合作（基于策略）
     */
    shouldCooperateWith(otherAgent: Agent): boolean;
    /**
     * 记录交互历史
     */
    recordStrategicInteraction(partnerId: string, partnerCooperated: boolean): void;
    /**
     * Tit-for-Tat 策略：以牙还牙
     * - 第一次合作
     * - 之后复制对方上一次的行为
     */
    private titForTat;
    /**
     * Grim Trigger 策略：冷酷触发
     * - 初始合作
     * - 一旦被背叛，永远不合作
     */
    private grimTrigger;
    /**
     * Pavlov 策略：赢留输变
     * - 如果上一次结果好（双方合作或双方背叛），保持当前策略
     * - 如果上一次结果不好，改变策略
     */
    private pavlov;
    /**
     * Random 策略：完全随机
     */
    private randomStrategy;
    /**
     * Adaptive 策略：自适应策略
     * - 根据对方的历史合作率决定是否合作
     * - 合作率 > 0.6：合作
     * - 合作率 < 0.4：不合作
     * - 0.4-0.6：根据信任分数决定
     */
    private adaptiveStrategy;
    /**
     * 获取与特定 agent 的交互历史
     */
    getInteractionHistory(partnerId: string): InteractionHistory[];
    /**
     * 获取合作率统计
     */
    getCooperationStats(): {
        totalPartners: number;
        averageCooperationRate: number;
        strategyEffectiveness: number;
    };
    /**
     * 重置策略状态（用于新的博弈）
     */
    resetStrategy(): void;
    /**
     * 导出状态（包含策略信息）
     */
    toJSON(): object;
}
export {};
//# sourceMappingURL=advanced-agent.d.ts.map