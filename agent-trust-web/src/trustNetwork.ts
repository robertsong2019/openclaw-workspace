import type { Agent, AgentBehavior, TrustRelation, NetworkStats, NetworkMetrics, TrustSnapshot, AgentMetrics, NetworkData } from './types';

// Simplified Agent class for in-browser simulation
class BrowserAgent {
  id: string;
  name: string;
  behavior: AgentBehavior;
  trustScore: number;
  interactions: number;
  successRate: number;
  expertise: number;
  reliability: number;

  constructor(config: {
    id: string;
    name: string;
    behavior: AgentBehavior;
    initialTrust?: number;
    expertise?: number;
    reliability?: number;
  }) {
    this.id = config.id;
    this.name = config.name;
    this.behavior = config.behavior;
    this.trustScore = config.initialTrust ?? 0.5;
    this.interactions = 0;
    this.successRate = 0.5;
    this.expertise = config.expertise ?? 0.5;
    this.reliability = config.reliability ?? 0.5;
  }

  shouldCooperate(requester: BrowserAgent): boolean {
    // Malicious agents rarely cooperate
    if (this.behavior === 'malicious') {
      return Math.random() < 0.2;
    }

    // Adversarial agents actively harm
    if (this.behavior === 'adversarial') {
      return Math.random() < 0.1;
    }

    // Neutral agents cooperate based on trust
    if (this.behavior === 'neutral') {
      return Math.random() < (0.5 + requester.trustScore * 0.3);
    }

    // Cooperative agents always try to help
    if (this.behavior === 'cooperative') {
      return Math.random() < 0.9;
    }

    return Math.random() < 0.5;
  }

  performTask(complexity: number): boolean {
    // Success depends on behavior, expertise, and complexity
    const baseSuccess = this.behavior === 'cooperative' ? 0.9 :
                       this.behavior === 'neutral' ? 0.7 :
                       this.behavior === 'malicious' ? 0.4 : 0.2;

    const expertiseBonus = this.expertise * 0.2;
    const complexityPenalty = complexity * 0.3;

    const successProbability = Math.max(0.1, Math.min(0.95,
      baseSuccess + expertiseBonus - complexityPenalty
    ));

    return Math.random() < successProbability;
  }

  recordInteraction(success: boolean): void {
    this.interactions++;
    const newSuccessRate = success ? 1 : 0;
    this.successRate = this.successRate * 0.9 + newSuccessRate * 0.1;
  }

  toJSON(): Agent {
    return {
      id: this.id,
      name: this.name,
      behavior: this.behavior,
      trustScore: this.trustScore,
      interactions: this.interactions,
      successRate: this.successRate,
      expertise: this.expertise,
      reliability: this.reliability,
    };
  }
}

// Browser-based Trust Network Simulation
export class TrustNetworkSimulation {
  private agents: Map<string, BrowserAgent> = new Map();
  private relations: TrustRelation[] = [];
  private trustMatrix: Map<string, Map<string, number>> = new Map();
  private trustHistory: Map<string, TrustSnapshot[]> = new Map();
  private stepCount: number = 0;

  private readonly dampingFactor: number = 0.85;
  private readonly convergenceThreshold: number = 0.0001;
  private readonly maxIterations: number = 100;

  constructor() {
    // Initialize with some default agents
    this.initializeDefaultAgents();
  }

  private initializeDefaultAgents(): void {
    const defaultAgents = [
      { id: 'alice', name: 'Alice', behavior: 'cooperative' as AgentBehavior, expertise: 0.8 },
      { id: 'bob', name: 'Bob', behavior: 'cooperative' as AgentBehavior, expertise: 0.7 },
      { id: 'charlie', name: 'Charlie', behavior: 'neutral' as AgentBehavior, expertise: 0.6 },
      { id: 'david', name: 'David', behavior: 'malicious' as AgentBehavior, expertise: 0.4 },
      { id: 'eve', name: 'Eve', behavior: 'neutral' as AgentBehavior, expertise: 0.5 },
    ];

    defaultAgents.forEach(config => {
      this.addAgent(config);
    });

    // Create some initial trust relations
    this.setTrustRelation('alice', 'bob', 0.8);
    this.setTrustRelation('bob', 'alice', 0.7);
    this.setTrustRelation('alice', 'charlie', 0.6);
    this.setTrustRelation('charlie', 'david', 0.4);
    this.setTrustRelation('david', 'eve', 0.3);
    this.setTrustRelation('eve', 'charlie', 0.5);
  }

  addAgent(config: {
    id: string;
    name: string;
    behavior: AgentBehavior;
    expertise?: number;
    reliability?: number;
  }): void {
    const agent = new BrowserAgent(config);
    this.agents.set(config.id, agent);
    this.trustMatrix.set(config.id, new Map());
  }

  removeAgent(agentId: string): void {
    this.agents.delete(agentId);
    this.trustMatrix.delete(agentId);
    this.relations = this.relations.filter(r => r.from !== agentId && r.to !== agentId);
    this.trustMatrix.forEach(row => row.delete(agentId));
    this.trustHistory.delete(agentId);
  }

  setTrustRelation(fromId: string, toId: string, weight: number): void {
    if (!this.agents.has(fromId) || !this.agents.has(toId)) {
      return;
    }

    weight = Math.max(0, Math.min(1, weight));

    const existingIndex = this.relations.findIndex(r => r.from === fromId && r.to === toId);
    if (existingIndex >= 0) {
      this.relations[existingIndex].weight = weight;
      this.relations[existingIndex].timestamp = new Date();
    } else {
      this.relations.push({ from: fromId, to: toId, weight, timestamp: new Date() });
    }

    this.trustMatrix.get(fromId)!.set(toId, weight);
  }

  getTrustWeight(fromId: string, toId: string): number {
    return this.trustMatrix.get(fromId)?.get(toId) ?? 0;
  }

  private recordSnapshot(): void {
    this.agents.forEach(agent => {
      const snapshot: TrustSnapshot = {
        timestamp: new Date(),
        trustScore: agent.trustScore,
        interactions: agent.interactions,
        successRate: agent.successRate,
      };

      if (!this.trustHistory.has(agent.id)) {
        this.trustHistory.set(agent.id, []);
      }

      const history = this.trustHistory.get(agent.id)!;
      history.push(snapshot);

      if (history.length > 100) {
        history.shift();
      }
    });
  }

  calculateTrustScores(): void {
    const n = this.agents.size;
    if (n === 0) return;

    const scores = new Map<string, number>();
    const newScores = new Map<string, number>();

    this.agents.forEach((_, id) => {
      scores.set(id, 1 / n);
    });

    let iterations = 0;
    let converged = false;

    while (!converged && iterations < this.maxIterations) {
      this.agents.forEach((_, id) => {
        let incomingTrust = 0;

        this.relations
          .filter(r => r.to === id)
          .forEach(r => {
            const sourceScore = scores.get(r.from) || 0;
            const outgoingWeight = this.getOutgoingWeight(r.from);
            if (outgoingWeight > 0) {
              incomingTrust += (sourceScore * r.weight) / outgoingWeight;
            }
          });

        const newScore = (1 - this.dampingFactor) / n + this.dampingFactor * incomingTrust;
        newScores.set(id, newScore);
      });

      converged = this.checkConvergence(scores, newScores);

      newScores.forEach((value, key) => {
        scores.set(key, value);
      });

      iterations++;
    }

    const maxScore = Math.max(...Array.from(scores.values()), 0.001);
    const minScore = Math.min(...Array.from(scores.values()));
    const range = maxScore - minScore;

    if (range > 0) {
      scores.forEach((value, key) => {
        scores.set(key, (value - minScore) / range);
      });
    }

    scores.forEach((score, id) => {
      const agent = this.agents.get(id);
      if (agent) {
        agent.trustScore = score;
      }
    });
  }

  private getOutgoingWeight(agentId: string): number {
    let total = 0;
    this.trustMatrix.get(agentId)?.forEach(weight => {
      total += weight;
    });
    return total;
  }

  private checkConvergence(oldScores: Map<string, number>, newScores: Map<string, number>): boolean {
    for (const [id, oldScore] of oldScores) {
      const newScore = newScores.get(id);
      if (newScore === undefined || Math.abs(oldScore - newScore) > this.convergenceThreshold) {
        return false;
      }
    }
    return true;
  }

  simulateInteraction(requesterId: string, providerId: string, taskComplexity: number = 0.5): {
    success: boolean;
    trustChange: number;
  } {
    const requester = this.agents.get(requesterId);
    const provider = this.agents.get(providerId);

    if (!requester || !provider) {
      return { success: false, trustChange: 0 };
    }

    const willCooperate = provider.shouldCooperate(requester);

    if (!willCooperate) {
      const trustChange = -0.1;
      const currentWeight = this.getTrustWeight(requesterId, providerId);
      const newWeight = Math.max(0, currentWeight + trustChange);
      this.setTrustRelation(requesterId, providerId, newWeight);
      return { success: false, trustChange };
    }

    const success = provider.performTask(taskComplexity);

    provider.recordInteraction(success);
    requester.recordInteraction(success);

    const trustChange = success ? 0.05 : -0.1;
    const currentWeight = this.getTrustWeight(requesterId, providerId);
    const newWeight = Math.max(0, Math.min(1, currentWeight + trustChange));
    this.setTrustRelation(requesterId, providerId, newWeight);

    return { success, trustChange };
  }

  simulateStep(): void {
    this.recordSnapshot();

    // Simulate random interactions
    const agentIds = Array.from(this.agents.keys());
    if (agentIds.length < 2) return;

    const numInteractions = Math.floor(agentIds.length / 2) + 1;

    for (let i = 0; i < numInteractions; i++) {
      const fromIdx = Math.floor(Math.random() * agentIds.length);
      let toIdx = Math.floor(Math.random() * agentIds.length);
      while (toIdx === fromIdx) {
        toIdx = Math.floor(Math.random() * agentIds.length);
      }

      const fromId = agentIds[fromIdx];
      const toId = agentIds[toIdx];

      this.simulateInteraction(fromId, toId, 0.3 + Math.random() * 0.5);
    }

    this.calculateTrustScores();
    this.stepCount++;
  }

  simulate(steps: number): void {
    for (let i = 0; i < steps; i++) {
      this.simulateStep();
    }
  }

  reset(): void {
    this.agents.clear();
    this.relations = [];
    this.trustMatrix.clear();
    this.trustHistory.clear();
    this.stepCount = 0;
    this.initializeDefaultAgents();
    this.calculateTrustScores();
  }

  getStats(): NetworkStats {
    const behaviorCounts: Record<AgentBehavior, number> = {
      cooperative: 0,
      neutral: 0,
      malicious: 0,
      adversarial: 0,
    };

    let totalTrust = 0;

    this.agents.forEach(agent => {
      behaviorCounts[agent.behavior]++;
      totalTrust += agent.trustScore;
    });

    return {
      totalAgents: this.agents.size,
      totalRelations: this.relations.length,
      averageTrust: this.agents.size > 0 ? totalTrust / this.agents.size : 0,
      trustDistribution: behaviorCounts,
      clusterCount: this.estimateClusterCount(),
    };
  }

  private estimateClusterCount(): number {
    const visited = new Set<string>();
    let clusterCount = 0;

    const dfs = (agentId: string) => {
      if (visited.has(agentId)) return;
      visited.add(agentId);

      this.trustMatrix.get(agentId)?.forEach((_, neighborId) => {
        if (!visited.has(neighborId)) {
          dfs(neighborId);
        }
      });

      this.trustMatrix.forEach((row, fromId) => {
        if (row.get(agentId) && !visited.has(fromId)) {
          dfs(fromId);
        }
      });
    };

    this.agents.forEach((_, id) => {
      if (!visited.has(id)) {
        dfs(id);
        clusterCount++;
      }
    });

    return clusterCount;
  }

  private calculateTrustVelocity(history: TrustSnapshot[]): number {
    if (history.length < 2) return 0;

    const recentHistory = history.slice(-Math.min(10, history.length));
    const n = recentHistory.length;

    if (n < 2) return 0;

    let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;

    recentHistory.forEach((snapshot, i) => {
      sumX += i;
      sumY += snapshot.trustScore;
      sumXY += i * snapshot.trustScore;
      sumX2 += i * i;
    });

    const denominator = n * sumX2 - sumX * sumX;
    if (denominator === 0) return 0;

    const slope = (n * sumXY - sumX * sumY) / denominator;
    return Math.max(-1, Math.min(1, slope * 10));
  }

  private calculateTrustVolatility(history: TrustSnapshot[]): number {
    if (history.length < 2) return 0;

    const recentHistory = history.slice(-Math.min(20, history.length));

    const mean = recentHistory.reduce((sum, s) => sum + s.trustScore, 0) / recentHistory.length;
    const variance = recentHistory.reduce((sum, s) => sum + Math.pow(s.trustScore - mean, 2), 0) / recentHistory.length;
    const stdDev = Math.sqrt(variance);

    return Math.min(1, stdDev * 2);
  }

  private calculateReputationScore(agent: BrowserAgent, history: TrustSnapshot[]): number {
    const volatility = this.calculateTrustVolatility(history);
    const stabilityContribution = 1 - volatility;
    const experienceContribution = Math.min(1, agent.interactions / 100);

    return (
      0.4 * agent.trustScore +
      0.3 * agent.successRate +
      0.2 * stabilityContribution +
      0.1 * experienceContribution
    );
  }

  private calculateConfidenceLevel(agent: BrowserAgent, history: TrustSnapshot[]): number {
    const interactionConfidence = Math.min(1, agent.interactions / 20);
    const volatility = this.calculateTrustVolatility(history);
    const stabilityConfidence = 1 - volatility;
    const historyConfidence = Math.min(1, history.length / 50);

    return 0.4 * interactionConfidence + 0.4 * stabilityConfidence + 0.2 * historyConfidence;
  }

  getMetrics(): NetworkMetrics {
    const agents = Array.from(this.agents.values());
    if (agents.length === 0) {
      return {
        totalAgents: 0,
        averageTrust: 0,
        averageReputation: 0,
        networkHealth: 0,
        trustDistribution: { high: 0, medium: 0, low: 0 },
        volatilityIndex: 0,
        confidenceIndex: 0,
      };
    }

    let totalReputation = 0;
    let totalVolatility = 0;
    let totalConfidence = 0;

    agents.forEach(agent => {
      const history = this.trustHistory.get(agent.id) || [];
      const reputation = this.calculateReputationScore(agent, history);
      const volatility = this.calculateTrustVolatility(history);
      const confidence = this.calculateConfidenceLevel(agent, history);

      totalReputation += reputation;
      totalVolatility += volatility;
      totalConfidence += confidence;
    });

    const averageTrust = agents.reduce((sum, a) => sum + a.trustScore, 0) / agents.length;
    const averageReputation = totalReputation / agents.length;
    const volatilityIndex = totalVolatility / agents.length;
    const confidenceIndex = totalConfidence / agents.length;

    const trustDistribution = {
      high: agents.filter(a => a.trustScore > 0.7).length / agents.length,
      medium: agents.filter(a => a.trustScore >= 0.3 && a.trustScore <= 0.7).length / agents.length,
      low: agents.filter(a => a.trustScore < 0.3).length / agents.length,
    };

    const networkHealth = 0.4 * averageTrust + 0.3 * trustDistribution.high + 0.3 * confidenceIndex;

    return {
      totalAgents: agents.length,
      averageTrust,
      averageReputation,
      networkHealth,
      trustDistribution,
      volatilityIndex,
      confidenceIndex,
    };
  }

  getAgentMetrics(agentId: string): AgentMetrics | null {
    const agent = this.agents.get(agentId);
    if (!agent) return null;

    const history = this.trustHistory.get(agentId) || [];
    const trustVelocity = this.calculateTrustVelocity(history);
    const trustVolatility = this.calculateTrustVolatility(history);
    const reputationScore = this.calculateReputationScore(agent, history);
    const confidenceLevel = this.calculateConfidenceLevel(agent, history);

    let trend: 'rising' | 'falling' | 'stable' = 'stable';
    if (trustVelocity > 0.1) trend = 'rising';
    else if (trustVelocity < -0.1) trend = 'falling';

    let reliability: 'high' | 'medium' | 'low' = 'medium';
    if (confidenceLevel > 0.7 && trustVolatility < 0.3) reliability = 'high';
    else if (confidenceLevel < 0.4 || trustVolatility > 0.6) reliability = 'low';

    return {
      agentId,
      trustVelocity,
      trustVolatility,
      reputationScore,
      confidenceLevel,
      trend,
      reliability,
    };
  }

  exportConfig(): string {
    const data = {
      agents: Array.from(this.agents.values()).map(a => a.toJSON()),
      relations: this.relations,
      stepCount: this.stepCount,
    };
    return JSON.stringify(data, null, 2);
  }

  importConfig(jsonString: string): void {
    try {
      const data = JSON.parse(jsonString);

      this.agents.clear();
      this.relations = [];
      this.trustMatrix.clear();
      this.trustHistory.clear();

      data.agents.forEach((agentData: Agent) => {
        const agent = new BrowserAgent({
          id: agentData.id,
          name: agentData.name,
          behavior: agentData.behavior,
          expertise: agentData.expertise,
          reliability: agentData.reliability,
        });
        agent.trustScore = agentData.trustScore;
        agent.interactions = agentData.interactions;
        agent.successRate = agentData.successRate;
        this.agents.set(agentData.id, agent);
        this.trustMatrix.set(agentData.id, new Map());
      });

      data.relations.forEach((r: TrustRelation) => {
        this.setTrustRelation(r.from, r.to, r.weight);
      });

      this.stepCount = data.stepCount || 0;
      this.calculateTrustScores();
    } catch (e) {
      console.error('Failed to import config:', e);
    }
  }

  getNetworkData(): NetworkData {
    return {
      agents: Array.from(this.agents.values()).map(a => a.toJSON()),
      relations: this.relations,
      stats: this.getStats(),
      stepCount: this.stepCount,
      metrics: this.getMetrics(),
    };
  }
}

// Singleton instance
export const trustNetwork = new TrustNetworkSimulation();
