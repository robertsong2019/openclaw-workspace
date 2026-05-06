import { describe, it, expect, beforeEach } from 'vitest';
import { TrustNetworkSimulation } from '../src/trustNetwork';

describe('TrustNetworkSimulation', () => {
  let sim: TrustNetworkSimulation;

  beforeEach(() => {
    sim = new TrustNetworkSimulation();
  });

  describe('initialization', () => {
    it('should have 5 default agents', () => {
      const stats = sim.getStats();
      expect(stats.totalAgents).toBe(5);
    });

    it('should have initial trust relations', () => {
      const stats = sim.getStats();
      expect(stats.totalRelations).toBeGreaterThan(0);
    });

    it('should have behavior distribution', () => {
      const stats = sim.getStats();
      expect(stats.trustDistribution.cooperative).toBe(2);
      expect(stats.trustDistribution.neutral).toBe(2);
      expect(stats.trustDistribution.malicious).toBe(1);
      expect(stats.trustDistribution.adversarial).toBe(0);
    });
  });

  describe('addAgent / removeAgent', () => {
    it('should add a new agent', () => {
      sim.addAgent({ id: 'frank', name: 'Frank', behavior: 'cooperative' });
      expect(sim.getStats().totalAgents).toBe(6);
    });

    it('should remove an agent and its relations', () => {
      sim.removeAgent('alice');
      const stats = sim.getStats();
      expect(stats.totalAgents).toBe(4);
      // relations involving alice should be gone
      expect(stats.totalRelations).toBeLessThan(6);
    });

    it('should handle removing non-existent agent gracefully', () => {
      sim.removeAgent('nonexistent');
      expect(sim.getStats().totalAgents).toBe(5);
    });
  });

  describe('setTrustRelation / getTrustWeight', () => {
    it('should set and get trust weight', () => {
      sim.setTrustRelation('alice', 'bob', 0.9);
      expect(sim.getTrustWeight('alice', 'bob')).toBe(0.9);
    });

    it('should clamp weight to [0, 1]', () => {
      sim.setTrustRelation('alice', 'bob', 1.5);
      expect(sim.getTrustWeight('alice', 'bob')).toBe(1);
      sim.setTrustRelation('alice', 'bob', -0.5);
      expect(sim.getTrustWeight('alice', 'bob')).toBe(0);
    });

    it('should ignore relations with non-existent agents', () => {
      sim.setTrustRelation('alice', 'ghost', 0.5);
      expect(sim.getTrustWeight('alice', 'ghost')).toBe(0);
    });

    it('should update existing relation', () => {
      sim.setTrustRelation('alice', 'bob', 0.5);
      sim.setTrustRelation('alice', 'bob', 0.8);
      expect(sim.getTrustWeight('alice', 'bob')).toBe(0.8);
    });
  });

  describe('calculateTrustScores', () => {
    it('should produce scores between 0 and 1', () => {
      sim.calculateTrustScores();
      const data = sim.getNetworkData();
      for (const agent of data.agents) {
        expect(agent.trustScore).toBeGreaterThanOrEqual(0);
        expect(agent.trustScore).toBeLessThanOrEqual(1);
      }
    });

    it('should handle single agent', () => {
      const single = new TrustNetworkSimulation();
      single.addAgent({ id: 'solo', name: 'Solo', behavior: 'cooperative' });
      single.calculateTrustScores();
      const data = single.getNetworkData();
      expect(data.agents.length).toBe(6); // includes default agents
    });
  });

  describe('simulateStep / simulate', () => {
    it('should increment stepCount after simulateStep', () => {
      const before = sim.getNetworkData().stepCount;
      sim.simulateStep();
      expect(sim.getNetworkData().stepCount).toBe(before + 1);
    });

    it('should run multiple steps', () => {
      sim.simulate(5);
      expect(sim.getNetworkData().stepCount).toBe(5);
    });
  });

  describe('getMetrics', () => {
    it('should return valid metrics structure', () => {
      sim.calculateTrustScores();
      const metrics = sim.getMetrics();
      expect(metrics.totalAgents).toBe(5);
      expect(metrics.averageTrust).toBeGreaterThanOrEqual(0);
      expect(metrics.networkHealth).toBeGreaterThanOrEqual(0);
      expect(metrics.networkHealth).toBeLessThanOrEqual(1);
      expect(metrics.trustDistribution.high + metrics.trustDistribution.medium + metrics.trustDistribution.low).toBeCloseTo(1);
    });

    it('should handle empty network', () => {
      const empty = new TrustNetworkSimulation();
      // remove all agents
      ['alice', 'bob', 'charlie', 'david', 'eve'].forEach(id => empty.removeAgent(id));
      const metrics = empty.getMetrics();
      expect(metrics.totalAgents).toBe(0);
      expect(metrics.averageTrust).toBe(0);
      expect(metrics.networkHealth).toBe(0);
    });
  });

  describe('getAgentMetrics', () => {
    it('should return metrics for existing agent', () => {
      sim.calculateTrustScores();
      const m = sim.getAgentMetrics('alice');
      expect(m).not.toBeNull();
      expect(m!.agentId).toBe('alice');
      expect(['rising', 'falling', 'stable']).toContain(m!.trend);
      expect(['high', 'medium', 'low']).toContain(m!.reliability);
    });

    it('should return null for non-existent agent', () => {
      expect(sim.getAgentMetrics('ghost')).toBeNull();
    });
  });

  describe('exportConfig / importConfig', () => {
    it('should round-trip config', () => {
      sim.calculateTrustScores();
      const json = sim.exportConfig();
      const parsed = JSON.parse(json);
      expect(parsed.agents.length).toBe(5);

      const sim2 = new TrustNetworkSimulation();
      sim2.importConfig(json);
      const stats2 = sim2.getStats();
      expect(stats2.totalAgents).toBe(5);
    });

    it('should handle invalid JSON gracefully', () => {
      // Should not throw
      expect(() => sim.importConfig('not json')).not.toThrow();
    });
  });

  describe('reset', () => {
    it('should reset to default state', () => {
      sim.simulate(10);
      sim.reset();
      const stats = sim.getStats();
      expect(stats.totalAgents).toBe(5);
    });
  });

  describe('getNetworkData', () => {
    it('should return complete network data', () => {
      const data = sim.getNetworkData();
      expect(data.agents.length).toBe(5);
      expect(data.relations.length).toBeGreaterThan(0);
      expect(data.stats).toBeDefined();
      expect(data.metrics).toBeDefined();
    });
  });
});
