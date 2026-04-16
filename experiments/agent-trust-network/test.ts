/**
 * Test - 信任网络测试套件
 */

import { Agent, AgentBehavior } from './src/agent';
import { TrustNetwork } from './src/trust-network';

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
console.log('║              🧪 Agent Trust Network Tests                  ║');
console.log('╚════════════════════════════════════════════════════════════╝');
console.log('');

// Agent Tests
console.log('📦 Agent Tests:');
console.log('');

test('Agent creation with default values', () => {
  const agent = new Agent({ id: 'test-1', name: 'Test', behavior: 'neutral' });
  return agent.id === 'test-1' && 
         agent.name === 'Test' && 
         agent.behavior === 'neutral' &&
         agent.trustScore === 0.5;
});

test('Agent creation with custom trust score', () => {
  const agent = new Agent({ 
    id: 'test-2', 
    name: 'Test', 
    behavior: 'cooperative',
    initialTrust: 0.8 
  });
  return agent.trustScore === 0.8;
});

test('Agent trust score bounds (0-1)', () => {
  const agent = new Agent({ id: 'test-3', name: 'Test', behavior: 'neutral' });
  agent.trustScore = 1.5;
  if (agent.trustScore !== 1) return false;
  agent.trustScore = -0.5;
  return agent.trustScore === 0;
});

test('Agent interaction recording', () => {
  const agent = new Agent({ id: 'test-4', name: 'Test', behavior: 'cooperative' });
  agent.recordInteraction(true);
  agent.recordInteraction(true);
  agent.recordInteraction(false);
  return agent.interactions === 3 && 
         Math.abs(agent.successRate - 0.6666) < 0.01;
});

test('Agent cooperation decision', () => {
  const cooperative = new Agent({ id: 'test-5', name: 'Coop', behavior: 'cooperative' });
  const adversarial = new Agent({ id: 'test-6', name: 'Adv', behavior: 'adversarial' });
  const other = new Agent({ id: 'test-7', name: 'Other', behavior: 'neutral' });
  
  return cooperative.shouldCooperate(other) === true &&
         adversarial.shouldCooperate(other) === false;
});

test('Agent task performance varies by behavior', () => {
  const cooperative = new Agent({ 
    id: 'test-8', 
    name: 'Coop', 
    behavior: 'cooperative',
    reliability: 1.0 
  });
  const adversarial = new Agent({ 
    id: 'test-9', 
    name: 'Adv', 
    behavior: 'adversarial',
    reliability: 1.0 
  });
  
  // 运行多次测试
  let coopSuccess = 0;
  let advSuccess = 0;
  const trials = 100;
  
  for (let i = 0; i < trials; i++) {
    if (cooperative.performTask(0)) coopSuccess++;
    if (adversarial.performTask(0)) advSuccess++;
  }
  
  // 合作型应该有更高的成功率
  return coopSuccess > advSuccess;
});

test('Agent JSON export', () => {
  const agent = new Agent({ 
    id: 'test-10', 
    name: 'Test', 
    behavior: 'neutral',
    expertise: ['testing', 'validation']
  });
  const json = agent.toJSON() as any;
  return json.id === 'test-10' &&
         json.name === 'Test' &&
         json.expertise.length === 2;
});

console.log('');

// TrustNetwork Tests
console.log('🌐 TrustNetwork Tests:');
console.log('');

test('Network creation', () => {
  const network = new TrustNetwork();
  const stats = network.getStats();
  return stats.totalAgents === 0 && stats.totalRelations === 0;
});

test('Add agents to network', () => {
  const network = new TrustNetwork();
  const agent = new Agent({ id: 'net-1', name: 'Agent 1', behavior: 'neutral' });
  network.addAgent(agent);
  const stats = network.getStats();
  return stats.totalAgents === 1;
});

test('Remove agents from network', () => {
  const network = new TrustNetwork();
  const agent = new Agent({ id: 'net-2', name: 'Agent 2', behavior: 'neutral' });
  network.addAgent(agent);
  network.removeAgent('net-2');
  const stats = network.getStats();
  return stats.totalAgents === 0;
});

test('Set trust relation', () => {
  const network = new TrustNetwork();
  const agent1 = new Agent({ id: 'net-3', name: 'Agent 3', behavior: 'neutral' });
  const agent2 = new Agent({ id: 'net-4', name: 'Agent 4', behavior: 'neutral' });
  network.addAgent(agent1);
  network.addAgent(agent2);
  network.setTrustRelation('net-3', 'net-4', 0.8);
  return network.getTrustWeight('net-3', 'net-4') === 0.8;
});

test('Trust relation bounds (0-1)', () => {
  const network = new TrustNetwork();
  const agent1 = new Agent({ id: 'net-5', name: 'Agent 5', behavior: 'neutral' });
  const agent2 = new Agent({ id: 'net-6', name: 'Agent 6', behavior: 'neutral' });
  network.addAgent(agent1);
  network.addAgent(agent2);
  
  network.setTrustRelation('net-5', 'net-6', 1.5);
  if (network.getTrustWeight('net-5', 'net-6') !== 1) return false;
  
  network.setTrustRelation('net-5', 'net-6', -0.5);
  return network.getTrustWeight('net-5', 'net-6') === 0;
});

test('Trust score calculation', () => {
  const network = new TrustNetwork();
  
  // 创建 3 个 agent
  for (let i = 1; i <= 3; i++) {
    const agent = new Agent({ 
      id: `agent-${i}`, 
      name: `Agent ${i}`, 
      behavior: 'cooperative' 
    });
    network.addAgent(agent);
  }
  
  // 建立信任关系
  network.setTrustRelation('agent-1', 'agent-2', 0.9);
  network.setTrustRelation('agent-2', 'agent-3', 0.8);
  network.setTrustRelation('agent-3', 'agent-1', 0.7);
  
  // 计算信任分数
  const scores = network.calculateTrustScores();
  
  return scores.size === 3;
});

test('Malicious agent detection', () => {
  const network = new TrustNetwork();
  
  const goodAgent = new Agent({ 
    id: 'good', 
    name: 'Good', 
    behavior: 'cooperative',
    initialTrust: 0.9 
  });
  const badAgent = new Agent({ 
    id: 'bad', 
    name: 'Bad', 
    behavior: 'malicious',
    initialTrust: 0.2 
  });
  
  network.addAgent(goodAgent);
  network.addAgent(badAgent);
  
  const malicious = network.identifyMaliciousAgents(0.3);
  return malicious.includes('bad') && !malicious.includes('good');
});

test('Trusted agent retrieval', () => {
  const network = new TrustNetwork();
  
  const trusted = new Agent({ 
    id: 'trusted', 
    name: 'Trusted', 
    behavior: 'cooperative',
    initialTrust: 0.9 
  });
  const untrusted = new Agent({ 
    id: 'untrusted', 
    name: 'Untrusted', 
    behavior: 'neutral',
    initialTrust: 0.5 
  });
  
  network.addAgent(trusted);
  network.addAgent(untrusted);
  
  const trustedAgents = network.getTrustedAgents(0.8);
  return trustedAgents.length === 1 && trustedAgents[0].id === 'trusted';
});

test('Interaction simulation', () => {
  const network = new TrustNetwork();
  
  const agent1 = new Agent({ 
    id: 'sim-1', 
    name: 'Agent 1', 
    behavior: 'cooperative',
    reliability: 1.0
  });
  const agent2 = new Agent({ 
    id: 'sim-2', 
    name: 'Agent 2', 
    behavior: 'cooperative',
    reliability: 1.0
  });
  
  network.addAgent(agent1);
  network.addAgent(agent2);
  
  const result = network.simulateInteraction('sim-1', 'sim-2', 0);
  
  return result.success === true && result.trustChange > 0;
});

test('Trust decay', () => {
  const network = new TrustNetwork();
  
  const agent = new Agent({ 
    id: 'decay', 
    name: 'Decay', 
    behavior: 'neutral',
    initialTrust: 1.0 
  });
  
  network.addAgent(agent);
  network.applyTrustDecay(100); // 100 小时
  
  return agent.trustScore < 1.0 && agent.trustScore > 0;
});

test('Export and import', () => {
  const network = new TrustNetwork();
  
  const agent = new Agent({ 
    id: 'export', 
    name: 'Export', 
    behavior: 'cooperative',
    initialTrust: 0.8 
  });
  
  network.addAgent(agent);
  network.setTrustRelation('export', 'export', 0.5);
  
  const exported = network.export();
  const imported = TrustNetwork.import(exported);
  
  return imported.getStats().totalAgents === 1;
});

console.log('');

// Summary
console.log('╔════════════════════════════════════════════════════════════╗');
console.log('║                      📊 Test Summary                       ║');
console.log('╚════════════════════════════════════════════════════════════╝');
console.log('');
console.log(`  Total:  ${passed + failed}`);
console.log(`  Passed: ${passed} ✅`);
console.log(`  Failed: ${failed} ${failed > 0 ? '❌' : ''}`);
console.log('');

if (failed === 0) {
  console.log('  🎉 All tests passed!');
} else {
  console.log('  ⚠️  Some tests failed. Please review.');
}

console.log('');

process.exit(failed > 0 ? 1 : 0);
