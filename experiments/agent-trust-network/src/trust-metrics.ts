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
  trustVelocity: number;       // 信任变化速度（-1 到 1）
  trustVolatility: number;     // 信任波动性（0 到 1）
  reputationScore: number;     // 综合声誉评分（0 到 1）
  confidenceLevel: number;     // 信任置信度（0 到 1）
  trend: 'rising' | 'falling' | 'stable';
  reliability: 'high' | 'medium' | 'low';
}

export interface NetworkMetrics {
  totalAgents: number;
  averageTrust: number;
  averageReputation: number;
  networkHealth: number;       // 0 到 1
  trustDistribution: {
    high: number;              // trust > 0.7
    medium: number;            // 0.3 <= trust <= 0.7
    low: number;               // trust < 0.3
  };
  volatilityIndex: number;     // 网络整体波动性
  confidenceIndex: number;     // 网络整体置信度
}

export class TrustMetrics {
  private trustHistory: Map<string, TrustSnapshot[]> = new Map();
  private readonly historySize: number;
  
  constructor(historySize: number = 100) {
    this.historySize = historySize;
  }
  
  /**
   * 记录信任快照
   */
  recordSnapshot(agent: Agent): void {
    const snapshot: TrustSnapshot = {
      timestamp: new Date(),
      trustScore: agent.trustScore,
      interactions: agent.interactions,
      successRate: agent.successRate
    };
    
    if (!this.trustHistory.has(agent.id)) {
      this.trustHistory.set(agent.id, []);
    }
    
    const history = this.trustHistory.get(agent.id)!;
    history.push(snapshot);
    
    // 保持历史记录大小
    if (history.length > this.historySize) {
      history.shift();
    }
  }
  
  /**
   * 计算 Agent 的信任指标
   */
  calculateAgentMetrics(agent: Agent): AgentMetrics {
    const history = this.trustHistory.get(agent.id) || [];
    
    const trustVelocity = this.calculateTrustVelocity(history);
    const trustVolatility = this.calculateTrustVolatility(history);
    const reputationScore = this.calculateReputationScore(agent, history);
    const confidenceLevel = this.calculateConfidenceLevel(agent, history);
    
    return {
      agentId: agent.id,
      trustVelocity,
      trustVolatility,
      reputationScore,
      confidenceLevel,
      trend: this.determineTrend(trustVelocity),
      reliability: this.determineReliability(confidenceLevel, trustVolatility)
    };
  }
  
  /**
   * 计算网络整体指标
   */
  calculateNetworkMetrics(agents: Agent[]): NetworkMetrics {
    if (agents.length === 0) {
      return {
        totalAgents: 0,
        averageTrust: 0,
        averageReputation: 0,
        networkHealth: 0,
        trustDistribution: { high: 0, medium: 0, low: 0 },
        volatilityIndex: 0,
        confidenceIndex: 0
      };
    }
    
    const agentMetrics = agents.map(a => this.calculateAgentMetrics(a));
    
    // 计算平均值
    const averageTrust = agents.reduce((sum, a) => sum + a.trustScore, 0) / agents.length;
    const averageReputation = agentMetrics.reduce((sum, m) => sum + m.reputationScore, 0) / agents.length;
    
    // 信任分布
    const trustDistribution = {
      high: agents.filter(a => a.trustScore > 0.7).length / agents.length,
      medium: agents.filter(a => a.trustScore >= 0.3 && a.trustScore <= 0.7).length / agents.length,
      low: agents.filter(a => a.trustScore < 0.3).length / agents.length
    };
    
    // 网络健康度：综合信任分数和分布
    const networkHealth = this.calculateNetworkHealth(averageTrust, trustDistribution, agentMetrics);
    
    // 波动性指数和置信度指数
    const volatilityIndex = agentMetrics.reduce((sum, m) => sum + m.trustVolatility, 0) / agents.length;
    const confidenceIndex = agentMetrics.reduce((sum, m) => sum + m.confidenceLevel, 0) / agents.length;
    
    return {
      totalAgents: agents.length,
      averageTrust,
      averageReputation,
      networkHealth,
      trustDistribution,
      volatilityIndex,
      confidenceIndex
    };
  }
  
  /**
   * 计算信任变化速度
   * 返回 -1 到 1 之间的值
   * 正值表示信任上升，负值表示信任下降
   */
  private calculateTrustVelocity(history: TrustSnapshot[]): number {
    if (history.length < 2) {
      return 0;
    }
    
    // 使用线性回归计算趋势
    const recentHistory = history.slice(-Math.min(10, history.length));
    const n = recentHistory.length;
    
    let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;
    
    recentHistory.forEach((snapshot, i) => {
      sumX += i;
      sumY += snapshot.trustScore;
      sumXY += i * snapshot.trustScore;
      sumX2 += i * i;
    });
    
    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    
    // 归一化到 -1 到 1
    return Math.max(-1, Math.min(1, slope * 10));
  }
  
  /**
   * 计算信任波动性
   * 返回 0 到 1 之间的值
   * 0 表示非常稳定，1 表示非常不稳定
   */
  private calculateTrustVolatility(history: TrustSnapshot[]): number {
    if (history.length < 2) {
      return 0;
    }
    
    const recentHistory = history.slice(-Math.min(20, history.length));
    
    // 计算标准差
    const mean = recentHistory.reduce((sum, s) => sum + s.trustScore, 0) / recentHistory.length;
    const variance = recentHistory.reduce((sum, s) => sum + Math.pow(s.trustScore - mean, 2), 0) / recentHistory.length;
    const stdDev = Math.sqrt(variance);
    
    // 归一化到 0 到 1（假设标准差最大为 0.5）
    return Math.min(1, stdDev * 2);
  }
  
  /**
   * 计算综合声誉评分
   * 考虑：当前信任分数、成功率、稳定性、交互数量
   */
  private calculateReputationScore(agent: Agent, history: TrustSnapshot[]): number {
    const weights = {
      trustScore: 0.4,
      successRate: 0.3,
      stability: 0.2,
      experience: 0.1
    };
    
    // 信任分数贡献
    const trustContribution = agent.trustScore;
    
    // 成功率贡献
    const successContribution = agent.successRate;
    
    // 稳定性贡献（波动性越低，贡献越高）
    const volatility = this.calculateTrustVolatility(history);
    const stabilityContribution = 1 - volatility;
    
    // 经验贡献（交互次数越多，贡献越高，但有上限）
    const experienceContribution = Math.min(1, agent.interactions / 100);
    
    return (
      weights.trustScore * trustContribution +
      weights.successRate * successContribution +
      weights.stability * stabilityContribution +
      weights.experience * experienceContribution
    );
  }
  
  /**
   * 计算信任置信度
   * 表示我们对信任分数的确信程度
   * 基于交互次数和稳定性
   */
  private calculateConfidenceLevel(agent: Agent, history: TrustSnapshot[]): number {
    // 最少需要 5 次交互才能有较高置信度
    const interactionConfidence = Math.min(1, agent.interactions / 20);
    
    // 稳定性贡献
    const volatility = this.calculateTrustVolatility(history);
    const stabilityConfidence = 1 - volatility;
    
    // 历史长度贡献
    const historyConfidence = Math.min(1, history.length / 50);
    
    // 综合置信度
    return (
      0.4 * interactionConfidence +
      0.4 * stabilityConfidence +
      0.2 * historyConfidence
    );
  }
  
  /**
   * 确定信任趋势
   */
  private determineTrend(velocity: number): 'rising' | 'falling' | 'stable' {
    if (velocity > 0.1) return 'rising';
    if (velocity < -0.1) return 'falling';
    return 'stable';
  }
  
  /**
   * 确定可靠性等级
   */
  private determineReliability(
    confidence: number, 
    volatility: number
  ): 'high' | 'medium' | 'low' {
    // 高置信度 + 低波动性 = 高可靠性
    if (confidence > 0.7 && volatility < 0.3) {
      return 'high';
    }
    // 低置信度或高波动性 = 低可靠性
    if (confidence < 0.4 || volatility > 0.6) {
      return 'low';
    }
    return 'medium';
  }
  
  /**
   * 计算网络健康度
   */
  private calculateNetworkHealth(
    averageTrust: number,
    distribution: { high: number; medium: number; low: number },
    agentMetrics: AgentMetrics[]
  ): number {
    // 平均信任贡献（40%）
    const trustContribution = averageTrust;
    
    // 分布健康度贡献（30%）
    // 理想分布：高信任多，低信任少
    const distributionHealth = distribution.high * 1.0 + distribution.medium * 0.6 + distribution.low * 0.2;
    
    // 整体可靠性贡献（30%）
    const reliabilityHealth = agentMetrics.filter(m => m.reliability === 'high').length / Math.max(1, agentMetrics.length);
    
    return (
      0.4 * trustContribution +
      0.3 * distributionHealth +
      0.3 * reliabilityHealth
    );
  }
  
  /**
   * 获取 Agent 的信任历史
   */
  getHistory(agentId: string): TrustSnapshot[] {
    return this.trustHistory.get(agentId) || [];
  }
  
  /**
   * 清除历史记录
   */
  clearHistory(): void {
    this.trustHistory.clear();
  }
  
  /**
   * 导出所有历史记录
   */
  exportHistory(): Record<string, TrustSnapshot[]> {
    const result: Record<string, TrustSnapshot[]> = {};
    this.trustHistory.forEach((history, agentId) => {
      result[agentId] = history;
    });
    return result;
  }
  
  /**
   * 导入历史记录
   */
  importHistory(data: Record<string, TrustSnapshot[]>): void {
    Object.entries(data).forEach(([agentId, history]) => {
      this.trustHistory.set(agentId, history);
    });
  }
}
