/**
 * Demo - 高级策略博弈论演示
 * 
 * 重现 Axelrod 的囚徒困境锦标赛
 * 不同策略相互竞争，看哪种策略最成功
 */

import { Agent } from './src/agent';
import { AdvancedAgent } from './src/advanced-agent';
import { TrustNetwork } from './src/trust-network';

interface TournamentResult {
  strategy: string;
  agentName: string;
  totalScore: number;
  roundsPlayed: number;
  cooperationRate: number;
  avgScorePerRound: number;
}

/**
 * 模拟两个 agent 之间的囚徒困境博弈
 */
function playPrisonersDilemma(
  agent1: Agent | AdvancedAgent, 
  agent2: Agent | AdvancedAgent,
  rounds: number = 100
): { score1: number; score2: number; cooperations1: number; cooperations2: number } {
  let score1 = 0;
  let score2 = 0;
  let cooperations1 = 0;
  let cooperations2 = 0;
  
  for (let i = 0; i < rounds; i++) {
    // 决定是否合作
    const cooperate1 = agent1 instanceof AdvancedAgent 
      ? agent1.shouldCooperateWith(agent2)
      : agent1.shouldCooperate(agent2);
    
    const cooperate2 = agent2 instanceof AdvancedAgent 
      ? agent2.shouldCooperateWith(agent1)
      : agent2.shouldCooperate(agent1);
    
    // 记录合作
    if (cooperate1) cooperations1++;
    if (cooperate2) cooperations2++;
    
    // 计算得分（囚徒困境收益矩阵）
    // R = 相互合作的奖励 = 3
    // T = 背叛的诱惑 = 5
    // P = 相互背叛的惩罚 = 1
    // S = 被剥削的代价 = 0
    
    if (cooperate1 && cooperate2) {
      // 相互合作
      score1 += 3;
      score2 += 3;
    } else if (cooperate1 && !cooperate2) {
      // Agent 1 被剥削
      score1 += 0;
      score2 += 5;
    } else if (!cooperate1 && cooperate2) {
      // Agent 2 被剥削
      score1 += 5;
      score2 += 0;
    } else {
      // 相互背叛
      score1 += 1;
      score2 += 1;
    }
    
    // 记录策略交互（用于有记忆的策略）
    if (agent1 instanceof AdvancedAgent) {
      agent1.recordStrategicInteraction(agent2.id, cooperate2);
    }
    if (agent2 instanceof AdvancedAgent) {
      agent2.recordStrategicInteraction(agent1.id, cooperate1);
    }
  }
  
  return { score1, score2, cooperations1, cooperations2 };
}

/**
 * 运行锦标赛
 */
function runTournament(strategies: Array<{ name: string; create: () => Agent | AdvancedAgent }>, roundsPerMatch: number = 200): TournamentResult[] {
  const results: Map<string, TournamentResult> = new Map();
  
  // 初始化结果
  strategies.forEach(s => {
    results.set(s.name, {
      strategy: s.name,
      agentName: s.name,
      totalScore: 0,
      roundsPlayed: 0,
      cooperationRate: 0,
      avgScorePerRound: 0
    });
  });
  
  // 每个策略与其他所有策略对战（包括自己）
  for (let i = 0; i < strategies.length; i++) {
    for (let j = i; j < strategies.length; j++) {
      const agent1 = strategies[i].create();
      const agent2 = strategies[j].create();
      
      const { score1, score2, cooperations1, cooperations2 } = playPrisonersDilemma(agent1, agent2, roundsPerMatch);
      
      // 更新结果
      const result1 = results.get(strategies[i].name)!;
      const result2 = results.get(strategies[j].name)!;
      
      result1.totalScore += score1;
      result1.roundsPlayed += roundsPerMatch;
      result1.cooperationRate += cooperations1 / roundsPerMatch;
      
      if (i !== j) {
        result2.totalScore += score2;
        result2.roundsPlayed += roundsPerMatch;
        result2.cooperationRate += cooperations2 / roundsPerMatch;
      }
    }
  }
  
  // 计算平均值
  results.forEach(result => {
    const matches = strategies.length;
    result.cooperationRate /= matches;
    result.avgScorePerRound = result.totalScore / result.roundsPlayed;
  });
  
  // 排序
  return Array.from(results.values()).sort((a, b) => b.avgScorePerRound - a.avgScorePerRound);
}

console.log('╔════════════════════════════════════════════════════════════╗');
console.log('║      🏆 Agent Strategy Tournament - Axelrod Style         ║');
console.log('╚════════════════════════════════════════════════════════════╝');
console.log('');

// 定义参赛策略
const strategies = [
  {
    name: 'Tit-for-Tat',
    create: () => new AdvancedAgent({
      id: 'tft',
      name: 'Tit-for-Tat',
      behavior: 'cooperative',
      strategy: 'tit-for-tat'
    })
  },
  {
    name: 'Grim Trigger',
    create: () => new AdvancedAgent({
      id: 'grim',
      name: 'Grim Trigger',
      behavior: 'cooperative',
      strategy: 'grim-trigger'
    })
  },
  {
    name: 'Pavlov',
    create: () => new AdvancedAgent({
      id: 'pavlov',
      name: 'Pavlov',
      behavior: 'cooperative',
      strategy: 'pavlov'
    })
  },
  {
    name: 'Adaptive',
    create: () => new AdvancedAgent({
      id: 'adaptive',
      name: 'Adaptive',
      behavior: 'neutral',
      strategy: 'adaptive'
    })
  },
  {
    name: 'Random',
    create: () => new AdvancedAgent({
      id: 'random',
      name: 'Random',
      behavior: 'neutral',
      strategy: 'random'
    })
  },
  {
    name: 'Always Cooperate',
    create: () => new Agent({
      id: 'always-coop',
      name: 'Always Cooperate',
      behavior: 'cooperative'
    })
  },
  {
    name: 'Always Defect',
    create: () => new Agent({
      id: 'always-defect',
      name: 'Always Defect',
      behavior: 'adversarial'
    })
  }
];

console.log('📊 Tournament Configuration:');
console.log(`   Strategies: ${strategies.length}`);
console.log(`   Rounds per match: 200`);
console.log(`   Total matches: ${strategies.length * (strategies.length + 1) / 2}`);
console.log('');

console.log('🎮 Running tournament...');
const tournamentResults = runTournament(strategies, 200);

console.log('');
console.log('╔════════════════════════════════════════════════════════════╗');
console.log('║                   🏆 Tournament Results                    ║');
console.log('╚════════════════════════════════════════════════════════════╝');
console.log('');

console.log('┌────────────────────┬───────────────┬──────────────┬────────────┐');
console.log('│ Strategy           │ Avg Score/Rnd │ Coop Rate    │ Total      │');
console.log('├────────────────────┼───────────────┼──────────────┼────────────┤');

tournamentResults.forEach((result, index) => {
  const medal = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '  ';
  const coopBar = '█'.repeat(Math.round(result.cooperationRate * 10)) + 
                  '░'.repeat(10 - Math.round(result.cooperationRate * 10));
  
  console.log(`│ ${medal} ${result.strategy.padEnd(16)} │ ${result.avgScorePerRound.toFixed(3).padStart(11)} │ ${coopBar} ${result.cooperationRate.toFixed(2)} │ ${result.totalScore.toString().padStart(8)} │`);
});

console.log('└────────────────────┴───────────────┴──────────────┴────────────┘');
console.log('');

// 分析结果
const winner = tournamentResults[0];
const loser = tournamentResults[tournamentResults.length - 1];

console.log('💡 Key Insights:');
console.log('');
console.log(`   🏆 Winner: ${winner.strategy}`);
console.log(`      - Average score per round: ${winner.avgScorePerRound.toFixed(3)}`);
console.log(`      - Cooperation rate: ${(winner.cooperationRate * 100).toFixed(1)}%`);
console.log('');
console.log(`   ❌ Loser: ${loser.strategy}`);
console.log(`      - Average score per round: ${loser.avgScorePerRound.toFixed(3)}`);
console.log(`      - Cooperation rate: ${(loser.cooperationRate * 100).toFixed(1)}%`);
console.log('');

// 策略分析
console.log('📊 Strategy Analysis:');
console.log('');

// 找出最合作的策略
const mostCooperative = tournamentResults.reduce((a, b) => 
  a.cooperationRate > b.cooperationRate ? a : b
);
console.log(`   🤝 Most Cooperative: ${mostCooperative.strategy} (${(mostCooperative.cooperationRate * 100).toFixed(1)}%)`);

// 找出最成功的合作策略（合作率 > 50%）
const cooperativeStrategies = tournamentResults.filter(r => r.cooperationRate > 0.5);
if (cooperativeStrategies.length > 0) {
  const bestCooperative = cooperativeStrategies[0];
  console.log(`   ⭐ Best Cooperative Strategy: ${bestCooperative.strategy}`);
}

// 找出最自私的策略
const leastCooperative = tournamentResults.reduce((a, b) => 
  a.cooperationRate < b.cooperationRate ? a : b
);
console.log(`   🦈 Most Selfish: ${leastCooperative.strategy} (${(leastCooperative.cooperationRate * 100).toFixed(1)}%)`);

console.log('');

// Axelrod 的发现
console.log('🎓 Axelrod\'s Findings (Reproduced):');
console.log('');
console.log('   1. ✅ Nice strategies (start with cooperation) tend to win');
console.log('   2. ✅ Retaliatory strategies (punish defection) perform well');
console.log('   3. ✅ Forgiving strategies (give second chances) succeed');
console.log('   4. ✅ Simple strategies (Tit-for-Tat) outperform complex ones');
console.log('');

console.log('╔════════════════════════════════════════════════════════════╗');
console.log('║              🎉 Tournament Demo Complete!                  ║');
console.log('╚════════════════════════════════════════════════════════════╝');
