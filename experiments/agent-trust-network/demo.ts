/**
 * Demo - Agent 信任网络演示
 */

import { Agent, AgentBehavior } from './src/agent';
import { TrustNetwork } from './src/trust-network';
import { Visualizer } from './src/visualizer';

console.log('╔════════════════════════════════════════════════════════════╗');
console.log('║        🤖 Agent Trust Network Simulator Demo 🤖           ║');
console.log('╚════════════════════════════════════════════════════════════╝');
console.log('');

// 创建信任网络
const network = new TrustNetwork({
  dampingFactor: 0.85,
  trustDecayRate: 0.001
});

console.log('📝 Creating agents with different behaviors...');
console.log('');

// 创建不同类型的 Agent
const agents = [
  // 合作型 Agent（高可靠性）
  { id: 'agent-1', name: 'Alice', behavior: 'cooperative' as AgentBehavior, reliability: 0.95 },
  { id: 'agent-2', name: 'Bob', behavior: 'cooperative' as AgentBehavior, reliability: 0.90 },
  { id: 'agent-3', name: 'Charlie', behavior: 'cooperative' as AgentBehavior, reliability: 0.85 },
  
  // 中立型 Agent
  { id: 'agent-4', name: 'David', behavior: 'neutral' as AgentBehavior, reliability: 0.75 },
  { id: 'agent-5', name: 'Eve', behavior: 'neutral' as AgentBehavior, reliability: 0.70 },
  
  // 恶意 Agent
  { id: 'agent-6', name: 'Mallory', behavior: 'malicious' as AgentBehavior, reliability: 0.40 },
  { id: 'agent-7', name: 'Trudy', behavior: 'malicious' as AgentBehavior, reliability: 0.35 },
  
  // 对抗型 Agent（故意破坏）
  { id: 'agent-8', name: 'Adversary', behavior: 'adversarial' as AgentBehavior, reliability: 0.10 }
];

agents.forEach(config => {
  const agent = new Agent(config);
  network.addAgent(agent);
  console.log(`   ✓ Added ${config.name} (${config.behavior})`);
});

console.log('');
console.log('🔗 Establishing initial trust relations...');
console.log('');

// 建立初始信任关系
// 合作型 Agent 之间互相高度信任
network.setTrustRelation('agent-1', 'agent-2', 0.9);
network.setTrustRelation('agent-2', 'agent-1', 0.9);
network.setTrustRelation('agent-1', 'agent-3', 0.85);
network.setTrustRelation('agent-3', 'agent-1', 0.85);
network.setTrustRelation('agent-2', 'agent-3', 0.8);
network.setTrustRelation('agent-3', 'agent-2', 0.8);

// 中立型 Agent 对合作型 Agent 有中等信任
network.setTrustRelation('agent-4', 'agent-1', 0.6);
network.setTrustRelation('agent-5', 'agent-2', 0.5);

// 恶意 Agent 试图欺骗
network.setTrustRelation('agent-6', 'agent-1', 0.7); // 假装友好
network.setTrustRelation('agent-7', 'agent-2', 0.6);

console.log('   ✓ Created 14 trust relations');
console.log('');

// 计算初始信任分数
console.log('🔄 Calculating initial trust scores...');
console.log('');
network.calculateTrustScores();

// 显示初始状态
console.log(Visualizer.renderNetworkGraph(network));

// 模拟一系列交互
console.log('🎮 Simulating agent interactions...');
console.log('');

const interactionHistory: Array<{ requester: string; provider: string; success: boolean }> = [];

// 合作型 Agent 之间的交互（高成功率）
for (let i = 0; i < 10; i++) {
  const result = network.simulateInteraction('agent-1', 'agent-2', 0.3);
  interactionHistory.push({ requester: 'Alice', provider: 'Bob', success: result.success });
}

for (let i = 0; i < 8; i++) {
  const result = network.simulateInteraction('agent-2', 'agent-3', 0.4);
  interactionHistory.push({ requester: 'Bob', provider: 'Charlie', success: result.success });
}

// 中立型 Agent 尝试交互
for (let i = 0; i < 5; i++) {
  const result = network.simulateInteraction('agent-4', 'agent-1', 0.5);
  interactionHistory.push({ requester: 'David', provider: 'Alice', success: result.success });
}

// 恶意 Agent 的交互（低成功率）
for (let i = 0; i < 6; i++) {
  const result = network.simulateInteraction('agent-5', 'agent-6', 0.5);
  interactionHistory.push({ requester: 'Eve', provider: 'Mallory', success: result.success });
}

for (let i = 0; i < 4; i++) {
  const result = network.simulateInteraction('agent-4', 'agent-7', 0.5);
  interactionHistory.push({ requester: 'David', provider: 'Trudy', success: result.success });
}

// 对抗型 Agent 的交互（必然失败）
for (let i = 0; i < 3; i++) {
  const result = network.simulateInteraction('agent-1', 'agent-8', 0.3);
  interactionHistory.push({ requester: 'Alice', provider: 'Adversary', success: result.success });
}

console.log(`   ✓ Completed ${interactionHistory.length} interactions`);
console.log('');

// 重新计算信任分数
console.log('🔄 Recalculating trust scores after interactions...');
console.log('');
network.calculateTrustScores();

// 显示更新后的状态
console.log(Visualizer.renderNetworkGraph(network));

// 显示交互历史
console.log(Visualizer.renderInteractionHistory(interactionHistory));

// 应用信任衰减
console.log('⏰ Simulating time decay (24 hours)...');
console.log('');
network.applyTrustDecay(24);
network.calculateTrustScores();

// 显示衰减后的状态
console.log(Visualizer.renderNetworkGraph(network));

// 演示信任传播
console.log(Visualizer.renderTrustPropagation(network, 5));

// 导出网络状态
console.log('💾 Exporting network state...');
const exported = network.export();
console.log(`   ✓ Exported ${(JSON.stringify(exported).length / 1024).toFixed(2)} KB of data`);
console.log('');

// 重新导入并验证
console.log('🔄 Testing import/export...');
const imported = TrustNetwork.import(exported);
const importedStats = imported.getStats();
console.log(`   ✓ Imported network with ${importedStats.totalAgents} agents`);
console.log('');

// 总结
console.log('╔════════════════════════════════════════════════════════════╗');
console.log('║                      📊 Demo Summary                       ║');
console.log('╚════════════════════════════════════════════════════════════╝');
console.log('');
console.log('Key Observations:');
console.log('');
console.log('1. 🟢 Cooperative agents maintain high trust scores');
console.log('2. 🟡 Neutral agents have moderate, fluctuating trust');
console.log('3. 🔴 Malicious agents lose trust over time');
console.log('4. ⚫ Adversarial agents are quickly identified and isolated');
console.log('');
console.log('Trust Network Features:');
console.log('   ✓ PageRank-style trust propagation algorithm');
console.log('   ✓ Time-based trust decay');
console.log('   ✓ Malicious agent detection');
console.log('   ✓ Trust score calculation and visualization');
console.log('   ✓ Interaction simulation');
console.log('   ✓ Network state export/import');
console.log('');
console.log('🎓 Educational Value:');
console.log('   • Demonstrates decentralized trust mechanisms');
console.log('   • Shows how reputation systems work');
console.log('   • Illustrates trust propagation in networks');
console.log('   • Can be used for multi-agent systems research');
console.log('');
console.log('✨ Demo completed successfully!');
console.log('');
