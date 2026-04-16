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

import { Agent, AgentBehavior, AgentConfig } from './agent';

export type AdvancedStrategy = 
  | 'tit-for-tat' 
  | 'grim-trigger' 
  | 'pavlov' 
  | 'random' 
  | 'adaptive';

export interface AdvancedAgentConfig extends AgentConfig {
  strategy?: AdvancedStrategy;
  memoryLength?: number; // 记忆长度（用于 Tit-for-Tat 等）
  initialCooperation?: boolean; // 初始是否合作
}

interface InteractionHistory {
  partnerId: string;
  cooperated: boolean; // 对方是否合作
  timestamp: Date;
}

export class AdvancedAgent extends Agent {
  public readonly strategy: AdvancedStrategy;
  public readonly memoryLength: number;
  
  private interactionHistory: Map<string, InteractionHistory[]> = new Map();
  private grimTriggered: Set<string> = new Set(); // 被 Grim Trigger 标记的 agents
  private lastMove: Map<string, boolean> = new Map(); // 上一次的决策（用于 Pavlov）
  private initialCooperation: boolean;
  
  constructor(config: AdvancedAgentConfig) {
    super(config);
    this.strategy = config.strategy || 'tit-for-tat';
    this.memoryLength = config.memoryLength || 10;
    this.initialCooperation = config.initialCooperation ?? true;
  }
  
  /**
   * 决定是否与另一个 Agent 合作（基于策略）
   */
  shouldCooperateWith(otherAgent: Agent): boolean {
    switch (this.strategy) {
      case 'tit-for-tat':
        return this.titForTat(otherAgent);
      case 'grim-trigger':
        return this.grimTrigger(otherAgent);
      case 'pavlov':
        return this.pavlov(otherAgent);
      case 'random':
        return this.randomStrategy();
      case 'adaptive':
        return this.adaptiveStrategy(otherAgent);
      default:
        return super.shouldCooperate(otherAgent);
    }
  }
  
  /**
   * 记录交互历史
   */
  recordStrategicInteraction(partnerId: string, partnerCooperated: boolean): void {
    if (!this.interactionHistory.has(partnerId)) {
      this.interactionHistory.set(partnerId, []);
    }
    
    const history = this.interactionHistory.get(partnerId)!;
    history.push({
      partnerId,
      cooperated: partnerCooperated,
      timestamp: new Date()
    });
    
    // 保持记忆长度
    if (history.length > this.memoryLength) {
      history.shift();
    }
    
    // 如果对方背叛，触发 Grim Trigger
    if (!partnerCooperated && this.strategy === 'grim-trigger') {
      this.grimTriggered.add(partnerId);
    }
  }
  
  /**
   * Tit-for-Tat 策略：以牙还牙
   * - 第一次合作
   * - 之后复制对方上一次的行为
   */
  private titForTat(otherAgent: Agent): boolean {
    const history = this.interactionHistory.get(otherAgent.id);
    
    // 第一次交互：合作
    if (!history || history.length === 0) {
      return this.initialCooperation;
    }
    
    // 复制对方上一次的行为
    return history[history.length - 1].cooperated;
  }
  
  /**
   * Grim Trigger 策略：冷酷触发
   * - 初始合作
   * - 一旦被背叛，永远不合作
   */
  private grimTrigger(otherAgent: Agent): boolean {
    // 如果已经被触发，永远不合作
    if (this.grimTriggered.has(otherAgent.id)) {
      return false;
    }
    
    // 初始合作
    return true;
  }
  
  /**
   * Pavlov 策略：赢留输变
   * - 如果上一次结果好（双方合作或双方背叛），保持当前策略
   * - 如果上一次结果不好，改变策略
   */
  private pavlov(otherAgent: Agent): boolean {
    const history = this.interactionHistory.get(otherAgent.id);
    
    // 第一次交互：合作
    if (!history || history.length === 0) {
      this.lastMove.set(otherAgent.id, this.initialCooperation);
      return this.initialCooperation;
    }
    
    const lastInteraction = history[history.length - 1];
    const myLastMove = this.lastMove.get(otherAgent.id) ?? true;
    
    // 赢了（双方都合作或双方都背叛）：保持策略
    // 输了（一方合作一方背叛）：改变策略
    const bothCooperated = myLastMove && lastInteraction.cooperated;
    const bothDefected = !myLastMove && !lastInteraction.cooperated;
    
    if (bothCooperated || bothDefected) {
      // 赢了，保持当前策略
      return myLastMove;
    } else {
      // 输了，改变策略
      const newMove = !myLastMove;
      this.lastMove.set(otherAgent.id, newMove);
      return newMove;
    }
  }
  
  /**
   * Random 策略：完全随机
   */
  private randomStrategy(): boolean {
    return Math.random() > 0.5;
  }
  
  /**
   * Adaptive 策略：自适应策略
   * - 根据对方的历史合作率决定是否合作
   * - 合作率 > 0.6：合作
   * - 合作率 < 0.4：不合作
   * - 0.4-0.6：根据信任分数决定
   */
  private adaptiveStrategy(otherAgent: Agent): boolean {
    const history = this.interactionHistory.get(otherAgent.id);
    
    // 没有历史：根据信任分数决定
    if (!history || history.length === 0) {
      return otherAgent.trustScore > 0.5;
    }
    
    // 计算对方的历史合作率
    const cooperationRate = history.filter(h => h.cooperated).length / history.length;
    
    if (cooperationRate > 0.6) {
      return true;
    } else if (cooperationRate < 0.4) {
      return false;
    } else {
      // 中间区域：根据信任分数决定
      return otherAgent.trustScore > 0.5;
    }
  }
  
  /**
   * 获取与特定 agent 的交互历史
   */
  getInteractionHistory(partnerId: string): InteractionHistory[] {
    return this.interactionHistory.get(partnerId) || [];
  }
  
  /**
   * 获取合作率统计
   */
  getCooperationStats(): {
    totalPartners: number;
    averageCooperationRate: number;
    strategyEffectiveness: number;
  } {
    let totalCooperation = 0;
    let totalInteractions = 0;
    
    this.interactionHistory.forEach((history) => {
      totalInteractions += history.length;
      totalCooperation += history.filter(h => h.cooperated).length;
    });
    
    const avgRate = totalInteractions > 0 ? totalCooperation / totalInteractions : 0;
    
    // 策略有效性：基于成功率
    const effectiveness = this.successRate;
    
    return {
      totalPartners: this.interactionHistory.size,
      averageCooperationRate: avgRate,
      strategyEffectiveness: effectiveness
    };
  }
  
  /**
   * 重置策略状态（用于新的博弈）
   */
  resetStrategy(): void {
    this.interactionHistory.clear();
    this.grimTriggered.clear();
    this.lastMove.clear();
  }
  
  /**
   * 导出状态（包含策略信息）
   */
  toJSON(): object {
    return {
      ...super.toJSON(),
      strategy: this.strategy,
      memoryLength: this.memoryLength,
      cooperationStats: this.getCooperationStats()
    };
  }
}
