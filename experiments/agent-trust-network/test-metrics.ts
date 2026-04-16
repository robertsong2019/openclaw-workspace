/**
 * Test - Trust Metrics 测试套件
 */

import { Agent } from './src/agent';
import { TrustMetrics, AgentMetrics, NetworkMetrics } from './src/trust-metrics';

let passed = 0;
let failed = 0;

function test(name: string, fn: () => boolean) {
  try {
    if (fn()) {
      passed++;
      console.log(`  ✅ ${name}`);
    } else {
      failed++;
      console.log(`  ❌ ${name} - assertion failed`);
    }
  } catch (error) {
    failed++;
    console.log(`  ❌ ${name} - ${error}`);
  }
}

console.log('╔════════════════════════════════════════════════════════════╗');
console.log('║           📊 Trust Metrics Tests                           ║');
console.log('╚════════════════════════════════════════════════════════════╝');
console.log('');

// Basic Functionality Tests
console.log('🔧 Basic Functionality Tests:');
console.log('');

test('TrustMetrics: Creates instance with default history size', () => {
  const metrics = new TrustMetrics();
  return metrics instanceof TrustMetrics;
});

test('TrustMetrics: Records snapshot for agent', () => {
  const metrics = new TrustMetrics();
  const agent = new Agent({ id: 'test-1', name: 'Test', behavior: 'cooperative' });
  
  agent.recordInteraction(true);
  metrics.recordSnapshot(agent);
  
  const history = metrics.getHistory('test-1');
  return history.length === 1 && history[0].trustScore === 0.5;
});

test('TrustMetrics: Limits history size', () => {
  const metrics = new TrustMetrics(5);
  const agent = new Agent({ id: 'test-2', name: 'Test', behavior: 'cooperative' });
  
  // Record 10 snapshots
  for (let i = 0; i < 10; i++) {
    agent.recordInteraction(true);
    metrics.recordSnapshot(agent);
  }
  
  const history = metrics.getHistory('test-2');
  return history.length === 5;
});

// Trust Velocity Tests
console.log('');
console.log('📈 Trust Velocity Tests:');
console.log('');

test('Trust Velocity: Returns 0 for single snapshot', () => {
  const metrics = new TrustMetrics();
  const agent = new Agent({ id: 'vel-1', name: 'Test', behavior: 'cooperative' });
  
  metrics.recordSnapshot(agent);
  const agentMetrics = metrics.calculateAgentMetrics(agent);
  
  return agentMetrics.trustVelocity === 0;
});

test('Trust Velocity: Detects rising trend', () => {
  const metrics = new TrustMetrics();
  const agent = new Agent({ id: 'vel-2', name: 'Test', behavior: 'cooperative' });
  
  // Simulate rising trust by manually setting trust scores
  for (let i = 0; i < 10; i++) {
    agent.trustScore = 0.3 + (i * 0.05); // Rising from 0.3 to 0.75
    agent.recordInteraction(true);
    metrics.recordSnapshot(agent);
  }
  
  const agentMetrics = metrics.calculateAgentMetrics(agent);
  return agentMetrics.trustVelocity > 0 && agentMetrics.trend === 'rising';
});

test('Trust Velocity: Detects falling trend', () => {
  const metrics = new TrustMetrics();
  const agent = new Agent({ id: 'vel-3', name: 'Test', behavior: 'cooperative' });
  
  // Simulate falling trust
  for (let i = 0; i < 10; i++) {
    agent.trustScore = 0.8 - (i * 0.05); // Falling from 0.8 to 0.35
    agent.recordInteraction(false);
    metrics.recordSnapshot(agent);
  }
  
  const agentMetrics = metrics.calculateAgentMetrics(agent);
  return agentMetrics.trustVelocity < 0 && agentMetrics.trend === 'falling';
});

test('Trust Velocity: Detects stable trend', () => {
  const metrics = new TrustMetrics();
  const agent = new Agent({ id: 'vel-4', name: 'Test', behavior: 'cooperative' });
  
  // Simulate stable trust
  for (let i = 0; i < 10; i++) {
    agent.recordInteraction(true);
    agent.recordInteraction(true);
    agent.recordInteraction(false); // Keep around 0.67
    metrics.recordSnapshot(agent);
  }
  
  const agentMetrics = metrics.calculateAgentMetrics(agent);
  return agentMetrics.trend === 'stable';
});

// Trust Volatility Tests
console.log('');
console.log('📊 Trust Volatility Tests:');
console.log('');

test('Trust Volatility: Returns 0 for single snapshot', () => {
  const metrics = new TrustMetrics();
  const agent = new Agent({ id: 'vol-1', name: 'Test', behavior: 'cooperative' });
  
  metrics.recordSnapshot(agent);
  const agentMetrics = metrics.calculateAgentMetrics(agent);
  
  return agentMetrics.trustVolatility === 0;
});

test('Trust Volatility: Low volatility for stable agent', () => {
  const metrics = new TrustMetrics();
  const agent = new Agent({ id: 'vol-2', name: 'Test', behavior: 'cooperative' });
  
  // Consistent behavior
  for (let i = 0; i < 20; i++) {
    agent.recordInteraction(true);
    metrics.recordSnapshot(agent);
  }
  
  const agentMetrics = metrics.calculateAgentMetrics(agent);
  return agentMetrics.trustVolatility < 0.3;
});

test('Trust Volatility: High volatility for unstable agent', () => {
  const metrics = new TrustMetrics();
  const agent = new Agent({ id: 'vol-3', name: 'Test', behavior: 'neutral' });
  
  // Erratic trust changes
  for (let i = 0; i < 20; i++) {
    // Alternate between high and low trust
    agent.trustScore = i % 2 === 0 ? 0.8 : 0.2;
    agent.recordInteraction(i % 2 === 0);
    metrics.recordSnapshot(agent);
  }
  
  const agentMetrics = metrics.calculateAgentMetrics(agent);
  return agentMetrics.trustVolatility > 0.3;
});

// Reputation Score Tests
console.log('');
console.log('⭐ Reputation Score Tests:');
console.log('');

test('Reputation Score: In range [0, 1]', () => {
  const metrics = new TrustMetrics();
  const agent = new Agent({ id: 'rep-1', name: 'Test', behavior: 'cooperative' });
  
  for (let i = 0; i < 10; i++) {
    agent.recordInteraction(true);
    metrics.recordSnapshot(agent);
  }
  
  const agentMetrics = metrics.calculateAgentMetrics(agent);
  return agentMetrics.reputationScore >= 0 && agentMetrics.reputationScore <= 1;
});

test('Reputation Score: Higher for cooperative agent', () => {
  const metrics1 = new TrustMetrics();
  const metrics2 = new TrustMetrics();
  
  const coopAgent = new Agent({ id: 'coop', name: 'Cooperative', behavior: 'cooperative' });
  const advAgent = new Agent({ id: 'adv', name: 'Adversarial', behavior: 'adversarial' });
  
  for (let i = 0; i < 20; i++) {
    coopAgent.recordInteraction(true);
    advAgent.recordInteraction(false);
    metrics1.recordSnapshot(coopAgent);
    metrics2.recordSnapshot(advAgent);
  }
  
  const coopMetrics = metrics1.calculateAgentMetrics(coopAgent);
  const advMetrics = metrics2.calculateAgentMetrics(advAgent);
  
  return coopMetrics.reputationScore > advMetrics.reputationScore;
});

test('Reputation Score: Increases with experience', () => {
  const metrics1 = new TrustMetrics();
  const metrics2 = new TrustMetrics();
  
  const newAgent = new Agent({ id: 'new', name: 'New', behavior: 'cooperative' });
  const expAgent = new Agent({ id: 'exp', name: 'Experienced', behavior: 'cooperative' });
  
  // New agent: few interactions
  for (let i = 0; i < 5; i++) {
    newAgent.recordInteraction(true);
    metrics1.recordSnapshot(newAgent);
  }
  
  // Experienced agent: many interactions
  for (let i = 0; i < 100; i++) {
    expAgent.recordInteraction(true);
    if (i % 10 === 0) {
      metrics2.recordSnapshot(expAgent);
    }
  }
  
  const newMetrics = metrics1.calculateAgentMetrics(newAgent);
  const expMetrics = metrics2.calculateAgentMetrics(expAgent);
  
  return expMetrics.reputationScore > newMetrics.reputationScore;
});

// Confidence Level Tests
console.log('');
console.log('🎯 Confidence Level Tests:');
console.log('');

test('Confidence Level: Low for new agent', () => {
  const metrics = new TrustMetrics();
  const agent = new Agent({ id: 'conf-1', name: 'New', behavior: 'cooperative' });
  
  agent.recordInteraction(true);
  metrics.recordSnapshot(agent);
  
  const agentMetrics = metrics.calculateAgentMetrics(agent);
  return agentMetrics.confidenceLevel < 0.5;
});

test('Confidence Level: High for experienced stable agent', () => {
  const metrics = new TrustMetrics();
  const agent = new Agent({ id: 'conf-2', name: 'Experienced', behavior: 'cooperative' });
  
  // Many consistent interactions
  for (let i = 0; i < 50; i++) {
    agent.recordInteraction(true);
    metrics.recordSnapshot(agent);
  }
  
  const agentMetrics = metrics.calculateAgentMetrics(agent);
  return agentMetrics.confidenceLevel > 0.6;
});

test('Confidence Level: Reduced by volatility', () => {
  const metrics1 = new TrustMetrics();
  const metrics2 = new TrustMetrics();
  
  const stableAgent = new Agent({ id: 'stable', name: 'Stable', behavior: 'cooperative' });
  const volatileAgent = new Agent({ id: 'volatile', name: 'Volatile', behavior: 'neutral' });
  
  // Stable interactions - consistent trust
  for (let i = 0; i < 30; i++) {
    stableAgent.trustScore = 0.7; // Constant
    stableAgent.recordInteraction(true);
    metrics1.recordSnapshot(stableAgent);
  }
  
  // Volatile interactions - fluctuating trust
  for (let i = 0; i < 30; i++) {
    volatileAgent.trustScore = i % 2 === 0 ? 0.8 : 0.2;
    volatileAgent.recordInteraction(i % 2 === 0);
    metrics2.recordSnapshot(volatileAgent);
  }
  
  const stableMetrics = metrics1.calculateAgentMetrics(stableAgent);
  const volatileMetrics = metrics2.calculateAgentMetrics(volatileAgent);
  
  return stableMetrics.confidenceLevel > volatileMetrics.confidenceLevel;
});

// Reliability Tests
console.log('');
console.log('🔒 Reliability Tests:');
console.log('');

test('Reliability: High for high confidence + low volatility', () => {
  const metrics = new TrustMetrics();
  const agent = new Agent({ id: 'rel-1', name: 'Reliable', behavior: 'cooperative' });
  
  for (let i = 0; i < 50; i++) {
    agent.recordInteraction(true);
    metrics.recordSnapshot(agent);
  }
  
  const agentMetrics = metrics.calculateAgentMetrics(agent);
  return agentMetrics.reliability === 'high';
});

test('Reliability: Low for low confidence or high volatility', () => {
  const metrics = new TrustMetrics();
  const agent = new Agent({ id: 'rel-2', name: 'Unreliable', behavior: 'neutral' });
  
  // Few interactions, very volatile
  for (let i = 0; i < 10; i++) {
    agent.trustScore = Math.random(); // Random trust
    agent.recordInteraction(Math.random() > 0.5);
    metrics.recordSnapshot(agent);
  }
  
  const agentMetrics = metrics.calculateAgentMetrics(agent);
  return agentMetrics.reliability === 'low' || agentMetrics.reliability === 'medium';
});

// Network Metrics Tests
console.log('');
console.log('🌐 Network Metrics Tests:');
console.log('');

test('Network Metrics: Handles empty network', () => {
  const metrics = new TrustMetrics();
  const networkMetrics = metrics.calculateNetworkMetrics([]);
  
  return networkMetrics.totalAgents === 0 && networkMetrics.networkHealth === 0;
});

test('Network Metrics: Calculates average trust', () => {
  const metrics = new TrustMetrics();
  const agents = [
    new Agent({ id: 'n1', name: 'A1', behavior: 'cooperative' }),
    new Agent({ id: 'n2', name: 'A2', behavior: 'cooperative' })
  ];
  
  agents[0].recordInteraction(true);
  agents[0].recordInteraction(true);
  agents[1].recordInteraction(true);
  agents[1].recordInteraction(false);
  
  agents.forEach(a => metrics.recordSnapshot(a));
  
  const networkMetrics = metrics.calculateNetworkMetrics(agents);
  
  return networkMetrics.totalAgents === 2 && networkMetrics.averageTrust > 0;
});

test('Network Metrics: Calculates trust distribution', () => {
  const metrics = new TrustMetrics();
  const agents = [
    new Agent({ id: 'd1', name: 'High', behavior: 'cooperative' }),
    new Agent({ id: 'd2', name: 'Medium', behavior: 'neutral' }),
    new Agent({ id: 'd3', name: 'Low', behavior: 'adversarial' })
  ];
  
  // High trust
  for (let i = 0; i < 20; i++) agents[0].recordInteraction(true);
  // Medium trust
  for (let i = 0; i < 10; i++) {
    agents[1].recordInteraction(true);
    agents[1].recordInteraction(false);
  }
  // Low trust
  for (let i = 0; i < 20; i++) agents[2].recordInteraction(false);
  
  agents.forEach(a => metrics.recordSnapshot(a));
  
  const networkMetrics = metrics.calculateNetworkMetrics(agents);
  
  return networkMetrics.trustDistribution.high > 0 &&
         networkMetrics.trustDistribution.medium > 0 &&
         networkMetrics.trustDistribution.low > 0;
});

test('Network Metrics: Network health in range [0, 1]', () => {
  const metrics = new TrustMetrics();
  const agents = [];
  
  for (let i = 0; i < 10; i++) {
    const agent = new Agent({ 
      id: `health-${i}`, 
      name: `Agent ${i}`, 
      behavior: i % 2 === 0 ? 'cooperative' : 'neutral' 
    });
    
    for (let j = 0; j < 20; j++) {
      agent.recordInteraction(i % 2 === 0);
    }
    agents.push(agent);
    metrics.recordSnapshot(agent);
  }
  
  const networkMetrics = metrics.calculateNetworkMetrics(agents);
  
  return networkMetrics.networkHealth >= 0 && networkMetrics.networkHealth <= 1;
});

// Import/Export Tests
console.log('');
console.log('💾 Import/Export Tests:');
console.log('');

test('Export/Import: Preserves history', () => {
  const metrics1 = new TrustMetrics();
  const agent = new Agent({ id: 'export-1', name: 'Test', behavior: 'cooperative' });
  
  for (let i = 0; i < 5; i++) {
    agent.recordInteraction(true);
    metrics1.recordSnapshot(agent);
  }
  
  const exported = metrics1.exportHistory();
  const metrics2 = new TrustMetrics();
  metrics2.importHistory(exported);
  
  const history1 = metrics1.getHistory('export-1');
  const history2 = metrics2.getHistory('export-1');
  
  return history1.length === history2.length;
});

test('Clear History: Removes all data', () => {
  const metrics = new TrustMetrics();
  const agent = new Agent({ id: 'clear-1', name: 'Test', behavior: 'cooperative' });
  
  for (let i = 0; i < 5; i++) {
    agent.recordInteraction(true);
    metrics.recordSnapshot(agent);
  }
  
  metrics.clearHistory();
  const history = metrics.getHistory('clear-1');
  
  return history.length === 0;
});

// Summary
console.log('');
console.log('╔════════════════════════════════════════════════════════════╗');
console.log('║                      📊 Test Summary                       ║');
console.log('╚════════════════════════════════════════════════════════════╝');
console.log('');

const total = passed + failed;
console.log(`  Total:  ${total}`);
console.log(`  Passed: ${passed} ✅`);
console.log(`  Failed: ${failed}`);
console.log('');

if (failed === 0) {
  console.log('  🎉 All tests passed!');
} else {
  console.log(`  ⚠️  ${failed} test(s) failed`);
}

process.exit(failed === 0 ? 0 : 1);
