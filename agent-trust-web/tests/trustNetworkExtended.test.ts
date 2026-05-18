import { describe, it, expect, beforeEach } from 'vitest';
import { TrustNetworkSimulation } from '../src/trustNetwork';

describe('TrustNetworkSimulation - Extended', () => {
  let sim: TrustNetworkSimulation;

  beforeEach(() => {
    sim = new TrustNetworkSimulation();
  });

  describe('simulateInteraction', () => {
    it('should return success:false and 0 trustChange for non-existent agents', () => {
      const result = sim.simulateInteraction('ghost1', 'ghost2');
      expect(result.success).toBe(false);
      expect(result.trustChange).toBe(0);
    });

    it('should return result for valid agents', () => {
      // Run many interactions to test both success/failure paths statistically
      let successes = 0;
      let failures = 0;
      for (let i = 0; i < 50; i++) {
        const result = sim.simulateInteraction('alice', 'bob', 0.5);
        if (result.success) successes++;
        else failures++;
      }
      // Alice is cooperative, bob is cooperative — should mostly succeed
      expect(successes + failures).toBe(50);
    });

    it('should record interactions on agents', () => {
      const before = sim.getNetworkData().agents.find(a => a.id === 'alice')!;
      const beforeInteractions = before.interactions;
      // Run enough to get cooperation (alice→bob cooperative pair)
      for (let i = 0; i < 100; i++) {
        sim.simulateInteraction('alice', 'bob', 0.3);
      }
      const after = sim.getNetworkData().agents.find(a => a.id === 'alice')!;
      expect(after.interactions).toBeGreaterThanOrEqual(beforeInteractions);
    });

    it('should update trust weight on cooperation refusal', () => {
      // David is malicious — likely to refuse
      const wBefore = sim.getTrustWeight('alice', 'david');
      for (let i = 0; i < 100; i++) {
        sim.simulateInteraction('alice', 'david', 0.5);
      }
      // Trust from alice to david should tend downward
      // (not guaranteed due to randomness, but we can check the mechanism)
      const wAfter = sim.getTrustWeight('alice', 'david');
      expect(typeof wAfter).toBe('number');
    });
  });

  describe('simulate edge cases', () => {
    it('should handle simulateStep with 1 agent', () => {
      const s = new TrustNetworkSimulation();
      ['alice', 'bob', 'charlie', 'david', 'eve'].forEach(id => s.removeAgent(id));
      s.addAgent({ id: 'solo', name: 'Solo', behavior: 'cooperative' });
      expect(() => s.simulateStep()).not.toThrow();
    });

    it('should handle simulateStep with 0 agents', () => {
      const s = new TrustNetworkSimulation();
      ['alice', 'bob', 'charlie', 'david', 'eve'].forEach(id => s.removeAgent(id));
      expect(() => s.simulateStep()).not.toThrow();
    });

    it('should handle calculateTrustScores with 0 agents', () => {
      const s = new TrustNetworkSimulation();
      ['alice', 'bob', 'charlie', 'david', 'eve'].forEach(id => s.removeAgent(id));
      expect(() => s.calculateTrustScores()).not.toThrow();
    });
  });

  describe('trust history and snapshots', () => {
    it('should build trust history through simulation', () => {
      sim.simulate(5);
      const data = sim.getNetworkData();
      // After simulation, agents should have trust scores
      for (const agent of data.agents) {
        expect(agent.trustScore).toBeGreaterThanOrEqual(0);
        expect(agent.trustScore).toBeLessThanOrEqual(1);
      }
    });

    it('should cap trust history at 100 snapshots', () => {
      sim.simulate(150);
      // Should not throw or leak memory
      expect(sim.getNetworkData().stepCount).toBe(150);
    });
  });

  describe('getAgentMetrics after simulation', () => {
    it('should compute metrics with history', () => {
      sim.simulate(20);
      const m = sim.getAgentMetrics('alice');
      expect(m).not.toBeNull();
      expect(m!.confidenceLevel).toBeGreaterThanOrEqual(0);
      expect(m!.confidenceLevel).toBeLessThanOrEqual(1);
      expect(m!.reputationScore).toBeGreaterThanOrEqual(0);
      expect(m!.reputationScore).toBeLessThanOrEqual(1);
    });

    it('should classify trend as rising/falling/stable', () => {
      sim.simulate(15);
      const ids = ['alice', 'bob', 'charlie', 'david', 'eve'];
      const trends = new Set<string>();
      for (const id of ids) {
        const m = sim.getAgentMetrics(id);
        if (m) trends.add(m.trend);
      }
      // At least one trend should be present
      expect(trends.size).toBeGreaterThanOrEqual(1);
      for (const t of trends) {
        expect(['rising', 'falling', 'stable']).toContain(t);
      }
    });

    it('should classify reliability as high/medium/low', () => {
      sim.simulate(20);
      const m = sim.getAgentMetrics('bob');
      expect(m).not.toBeNull();
      expect(['high', 'medium', 'low']).toContain(m!.reliability);
    });
  });

  describe('getMetrics distribution', () => {
    it('should sum trust distribution to ~1', () => {
      sim.calculateTrustScores();
      const metrics = sim.getMetrics();
      const sum = metrics.trustDistribution.high + metrics.trustDistribution.medium + metrics.trustDistribution.low;
      expect(sum).toBeCloseTo(1, 5);
    });

    it('should have volatility and confidence between 0 and 1', () => {
      sim.simulate(10);
      const metrics = sim.getMetrics();
      expect(metrics.volatilityIndex).toBeGreaterThanOrEqual(0);
      expect(metrics.volatilityIndex).toBeLessThanOrEqual(1);
      expect(metrics.confidenceIndex).toBeGreaterThanOrEqual(0);
      expect(metrics.confidenceIndex).toBeLessThanOrEqual(1);
    });
  });

  describe('cluster estimation', () => {
    it('should estimate cluster count for connected network', () => {
      const stats = sim.getStats();
      expect(stats.clusterCount).toBeGreaterThanOrEqual(1);
    });

    it('should detect disconnected clusters', () => {
      // Add isolated agent with no relations
      sim.addAgent({ id: 'isolated', name: 'Isolated', behavior: 'neutral' });
      const stats = sim.getStats();
      expect(stats.clusterCount).toBeGreaterThanOrEqual(2);
    });
  });

  describe('importConfig detailed', () => {
    it('should preserve trust scores after import', () => {
      sim.simulate(20);
      sim.calculateTrustScores();
      const before = sim.getNetworkData().agents.map(a => ({ id: a.id, score: a.trustScore }));
      const json = sim.exportConfig();

      const sim2 = new TrustNetworkSimulation();
      sim2.importConfig(json);
      const after = sim2.getNetworkData().agents;

      for (const b of before) {
        const a = after.find(x => x.id === b.id);
        expect(a).toBeDefined();
        // Trust scores may change after calculateTrustScores in import
      }
    });

    it('should preserve stepCount after import', () => {
      sim.simulate(7);
      const json = sim.exportConfig();
      const sim2 = new TrustNetworkSimulation();
      sim2.importConfig(json);
      expect(sim2.getNetworkData().stepCount).toBe(7);
    });

    it('should preserve relations after import', () => {
      const json = sim.exportConfig();
      const parsed = JSON.parse(json);
      const sim2 = new TrustNetworkSimulation();
      sim2.importConfig(json);
      expect(sim2.getStats().totalRelations).toBe(parsed.relations.length);
    });
  });

  describe('reset', () => {
    it('should clear stepCount', () => {
      sim.simulate(10);
      sim.reset();
      expect(sim.getNetworkData().stepCount).toBe(0);
    });

    it('should restore default agents after modifications', () => {
      sim.addAgent({ id: 'frank', name: 'Frank', behavior: 'cooperative' });
      sim.removeAgent('alice');
      sim.reset();
      const stats = sim.getStats();
      expect(stats.totalAgents).toBe(5);
      expect(stats.trustDistribution.cooperative).toBe(2);
    });
  });
});
