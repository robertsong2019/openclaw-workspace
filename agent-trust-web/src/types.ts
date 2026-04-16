export type AgentBehavior = 'cooperative' | 'neutral' | 'malicious' | 'adversarial';

export interface Agent {
  id: string;
  name: string;
  behavior: AgentBehavior;
  trustScore: number;
  interactions: number;
  successRate: number;
  expertise?: number;
  reliability?: number;
}

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

export interface NetworkData {
  agents: Agent[];
  relations: TrustRelation[];
  stats: NetworkStats;
  stepCount: number;
  metrics?: NetworkMetrics;
}

export interface GraphNode {
  id: string;
  name: string;
  behavior: AgentBehavior;
  trustScore: number;
  interactions: number;
  successRate: number;
  radius: number;
  x?: number;
  y?: number;
  vx?: number;
  vy?: number;
  fx?: number | null;
  fy?: number | null;
}

export interface GraphLink {
  source: string | GraphNode;
  target: string | GraphNode;
  weight: number;
}
