/**
 * Test - 高级策略测试套件
 */

import { Agent } from './src/agent';
import { AdvancedAgent, AdvancedStrategy } from './src/advanced-agent';

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
console.log('║         🧠 Advanced Agent Strategy Tests                   ║');
console.log('╚════════════════════════════════════════════════════════════╝');
console.log('');

// Tit-for-Tat Tests
console.log('🎯 Tit-for-Tat Strategy Tests:');
console.log('');

test('Tit-for-Tat: Initial cooperation', () => {
  const agent1 = new AdvancedAgent({ 
    id: 'tft-1', 
    name: 'TFT Agent', 
    behavior: 'cooperative',
    strategy: 'tit-for-tat',
    initialCooperation: true
  });
  const agent2 = new Agent({ id: 'partner', name: 'Partner', behavior: 'neutral' });
  
  return agent1.shouldCooperateWith(agent2) === true;
});

test('Tit-for-Tat: Cooperates after partner cooperates', () => {
  const tft = new AdvancedAgent({ 
    id: 'tft-2', 
    name: 'TFT', 
    behavior: 'cooperative',
    strategy: 'tit-for-tat'
  });
  const partner = new Agent({ id: 'partner-2', name: 'Partner', behavior: 'cooperative' });
  
  // 记录对方合作
  tft.recordStrategicInteraction('partner-2', true);
  
  return tft.shouldCooperateWith(partner) === true;
});

test('Tit-for-Tat: Defects after partner defects', () => {
  const tft = new AdvancedAgent({ 
    id: 'tft-3', 
    name: 'TFT', 
    behavior: 'cooperative',
    strategy: 'tit-for-tat'
  });
  const partner = new Agent({ id: 'partner-3', name: 'Partner', behavior: 'adversarial' });
  
  // 记录对方背叛
  tft.recordStrategicInteraction('partner-3', false);
  
  return tft.shouldCooperateWith(partner) === false;
});

test('Tit-for-Tat: Forgives after partner returns to cooperation', () => {
  const tft = new AdvancedAgent({ 
    id: 'tft-4', 
    name: 'TFT', 
    behavior: 'cooperative',
    strategy: 'tit-for-tat'
  });
  const partner = new Agent({ id: 'partner-4', name: 'Partner', behavior: 'neutral' });
  
  // 背叛 -> 合作
  tft.recordStrategicInteraction('partner-4', false);
  tft.recordStrategicInteraction('partner-4', true);
  
  return tft.shouldCooperateWith(partner) === true;
});

// Grim Trigger Tests
console.log('');
console.log('💀 Grim Trigger Strategy Tests:');
console.log('');

test('Grim Trigger: Initial cooperation', () => {
  const grim = new AdvancedAgent({ 
    id: 'grim-1', 
    name: 'Grim', 
    behavior: 'cooperative',
    strategy: 'grim-trigger'
  });
  const partner = new Agent({ id: 'partner-5', name: 'Partner', behavior: 'neutral' });
  
  return grim.shouldCooperateWith(partner) === true;
});

test('Grim Trigger: Never forgives after defection', () => {
  const grim = new AdvancedAgent({ 
    id: 'grim-2', 
    name: 'Grim', 
    behavior: 'cooperative',
    strategy: 'grim-trigger'
  });
  const partner = new Agent({ id: 'partner-6', name: 'Partner', behavior: 'neutral' });
  
  // 对方背叛
  grim.recordStrategicInteraction('partner-6', false);
  
  // 即使对方后来合作，仍然不原谅
  grim.recordStrategicInteraction('partner-6', true);
  grim.recordStrategicInteraction('partner-6', true);
  
  return grim.shouldCooperateWith(partner) === false;
});

test('Grim Trigger: Cooperates with different partners independently', () => {
  const grim = new AdvancedAgent({ 
    id: 'grim-3', 
    name: 'Grim', 
    behavior: 'cooperative',
    strategy: 'grim-trigger'
  });
  const partner1 = new Agent({ id: 'partner-7', name: 'Partner 1', behavior: 'neutral' });
  const partner2 = new Agent({ id: 'partner-8', name: 'Partner 2', behavior: 'neutral' });
  
  // Partner 1 背叛
  grim.recordStrategicInteraction('partner-7', false);
  
  // Partner 2 仍然可以合作
  return grim.shouldCooperateWith(partner1) === false && 
         grim.shouldCooperateWith(partner2) === true;
});

// Pavlov Strategy Tests
console.log('');
console.log('🐕 Pavlov Strategy Tests:');
console.log('');

test('Pavlov: Initial cooperation', () => {
  const pavlov = new AdvancedAgent({ 
    id: 'pavlov-1', 
    name: 'Pavlov', 
    behavior: 'cooperative',
    strategy: 'pavlov',
    initialCooperation: true
  });
  const partner = new Agent({ id: 'partner-9', name: 'Partner', behavior: 'neutral' });
  
  return pavlov.shouldCooperateWith(partner) === true;
});

test('Pavlov: Keeps strategy when both cooperate', () => {
  const pavlov = new AdvancedAgent({ 
    id: 'pavlov-2', 
    name: 'Pavlov', 
    behavior: 'cooperative',
    strategy: 'pavlov',
    initialCooperation: true
  });
  const partner = new Agent({ id: 'partner-10', name: 'Partner', behavior: 'cooperative' });
  
  // 双方合作（赢了）
  pavlov.recordStrategicInteraction('partner-10', true);
  
  // 保持合作
  return pavlov.shouldCooperateWith(partner) === true;
});

test('Pavlov: Changes strategy when exploited', () => {
  const pavlov = new AdvancedAgent({ 
    id: 'pavlov-3', 
    name: 'Pavlov', 
    behavior: 'cooperative',
    strategy: 'pavlov',
    initialCooperation: true
  });
  const partner = new Agent({ id: 'partner-11', name: 'Partner', behavior: 'adversarial' });
  
  // 我合作，对方背叛（输了）
  pavlov.recordStrategicInteraction('partner-11', false);
  
  // 改变策略：背叛
  return pavlov.shouldCooperateWith(partner) === false;
});

// Random Strategy Tests
console.log('');
console.log('🎲 Random Strategy Tests:');
console.log('');

test('Random: Returns boolean', () => {
  const random = new AdvancedAgent({ 
    id: 'random-1', 
    name: 'Random', 
    behavior: 'neutral',
    strategy: 'random'
  });
  const partner = new Agent({ id: 'partner-12', name: 'Partner', behavior: 'neutral' });
  
  const result = random.shouldCooperateWith(partner);
  return typeof result === 'boolean';
});

test('Random: Shows variation over multiple calls', () => {
  const random = new AdvancedAgent({ 
    id: 'random-2', 
    name: 'Random', 
    behavior: 'neutral',
    strategy: 'random'
  });
  const partner = new Agent({ id: 'partner-13', name: 'Partner', behavior: 'neutral' });
  
  const results = new Set();
  for (let i = 0; i < 20; i++) {
    results.add(random.shouldCooperateWith(partner));
  }
  
  // 应该有 True 和 False 两种结果
  return results.size === 2;
});

// Adaptive Strategy Tests
console.log('');
console.log('🧩 Adaptive Strategy Tests:');
console.log('');

test('Adaptive: Cooperates with high cooperation rate', () => {
  const adaptive = new AdvancedAgent({ 
    id: 'adaptive-1', 
    name: 'Adaptive', 
    behavior: 'neutral',
    strategy: 'adaptive'
  });
  const partner = new Agent({ id: 'partner-14', name: 'Partner', behavior: 'cooperative' });
  
  // 对方多次合作
  for (let i = 0; i < 10; i++) {
    adaptive.recordStrategicInteraction('partner-14', true);
  }
  
  return adaptive.shouldCooperateWith(partner) === true;
});

test('Adaptive: Defects against low cooperation rate', () => {
  const adaptive = new AdvancedAgent({ 
    id: 'adaptive-2', 
    name: 'Adaptive', 
    behavior: 'neutral',
    strategy: 'adaptive'
  });
  const partner = new Agent({ id: 'partner-15', name: 'Partner', behavior: 'adversarial' });
  
  // 对方多次背叛
  for (let i = 0; i < 10; i++) {
    adaptive.recordStrategicInteraction('partner-15', false);
  }
  
  return adaptive.shouldCooperateWith(partner) === false;
});

test('Adaptive: Uses trust score in uncertain cases', () => {
  const adaptive = new AdvancedAgent({ 
    id: 'adaptive-3', 
    name: 'Adaptive', 
    behavior: 'neutral',
    strategy: 'adaptive'
  });
  
  const highTrustPartner = new Agent({ 
    id: 'partner-16', 
    name: 'High Trust', 
    behavior: 'cooperative',
    initialTrust: 0.8
  });
  
  // 中等合作率（50%）
  for (let i = 0; i < 5; i++) {
    adaptive.recordStrategicInteraction('partner-16', true);
    adaptive.recordStrategicInteraction('partner-16', false);
  }
  
  // 应该根据信任分数决定
  return adaptive.shouldCooperateWith(highTrustPartner) === true;
});

// Integration Tests
console.log('');
console.log('🔬 Integration Tests:');
console.log('');

test('Strategy effectiveness tracking', () => {
  const tft = new AdvancedAgent({ 
    id: 'tft-int', 
    name: 'TFT', 
    behavior: 'cooperative',
    strategy: 'tit-for-tat'
  });
  
  // 模拟多次交互（包括策略交互和普通交互）
  tft.recordStrategicInteraction('partner-a', true);
  tft.recordStrategicInteraction('partner-a', true);
  tft.recordStrategicInteraction('partner-b', false);
  
  // 记录普通交互以更新成功率
  tft.recordInteraction(true);
  tft.recordInteraction(true);
  tft.recordInteraction(true);
  
  const stats = tft.getCooperationStats();
  
  return stats.totalPartners === 2 && 
         stats.averageCooperationRate === 2/3 && // 2 out of 3 cooperative
         typeof stats.strategyEffectiveness === 'number';
});

test('Reset strategy clears history', () => {
  const grim = new AdvancedAgent({ 
    id: 'grim-reset', 
    name: 'Grim', 
    behavior: 'cooperative',
    strategy: 'grim-trigger'
  });
  const partner = new Agent({ id: 'partner-reset', name: 'Partner', behavior: 'neutral' });
  
  // 背叛并触发
  grim.recordStrategicInteraction('partner-reset', false);
  
  // 重置
  grim.resetStrategy();
  
  // 应该重新合作
  return grim.shouldCooperateWith(partner) === true;
});

test('AdvancedAgent extends Agent correctly', () => {
  const advanced = new AdvancedAgent({ 
    id: 'extend-test', 
    name: 'Advanced', 
    behavior: 'cooperative',
    strategy: 'tit-for-tat'
  });
  
  // 继承的方法应该工作
  advanced.recordInteraction(true);
  
  return advanced.interactions === 1 && 
         advanced.trustScore === 0.5 &&
         advanced.strategy === 'tit-for-tat';
});

test('JSON export includes strategy info', () => {
  const advanced = new AdvancedAgent({ 
    id: 'json-test', 
    name: 'Advanced', 
    behavior: 'cooperative',
    strategy: 'pavlov'
  });
  
  advanced.recordStrategicInteraction('partner-json', true);
  
  const json = advanced.toJSON() as any;
  
  return json.strategy === 'pavlov' &&
         json.memoryLength === 10 &&
         typeof json.cooperationStats === 'object';
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
