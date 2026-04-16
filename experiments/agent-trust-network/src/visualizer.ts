/**
 * Visualizer - 信任网络可视化工具
 * 
 * 生成 ASCII 艺术和简单的可视化输出
 */

import { Agent } from './agent';
import { TrustNetwork } from './trust-network';

export class Visualizer {
  /**
   * 生成网络拓扑图（ASCII 艺术）
   */
  static renderNetworkGraph(network: TrustNetwork): string {
    const stats = network.getStats();
    const lines: string[] = [];
    
    lines.push('╔════════════════════════════════════════════════════════════╗');
    lines.push('║           🤖 Agent Trust Network Visualization             ║');
    lines.push('╚════════════════════════════════════════════════════════════╝');
    lines.push('');
    
    // 网络统计
    lines.push('📊 Network Statistics:');
    lines.push(`   Total Agents: ${stats.totalAgents}`);
    lines.push(`   Total Relations: ${stats.totalRelations}`);
    lines.push(`   Average Trust: ${(stats.averageTrust * 100).toFixed(1)}%`);
    lines.push(`   Clusters: ${stats.clusterCount}`);
    lines.push('');
    
    // Agent 列表（按信任分数排序）
    lines.push('🤖 Agents (sorted by trust score):');
    lines.push('┌────────────────────┬──────────┬─────────┬──────────┐');
    lines.push('│ Name               │ Behavior │ Trust   │ Success  │');
    lines.push('├────────────────────┼──────────┼─────────┼──────────┤');
    
    const agents = this.getSortedAgents(network);
    agents.forEach(agent => {
      const name = agent.name.padEnd(18).substring(0, 18);
      const behavior = this.getBehaviorEmoji(agent.behavior).padEnd(8);
      const trust = `${(agent.trustScore * 100).toFixed(1)}%`.padEnd(7);
      const success = `${(agent.successRate * 100).toFixed(1)}%`.padEnd(8);
      const bar = this.getTrustBar(agent.trustScore);
      
      lines.push(`│ ${name} │ ${behavior} │ ${trust} │ ${success} │ ${bar}`);
    });
    
    lines.push('└────────────────────┴──────────┴─────────┴──────────┘');
    lines.push('');
    
    // 信任分布
    lines.push('📈 Trust Distribution:');
    Object.entries(stats.trustDistribution).forEach(([behavior, count]) => {
      const emoji = this.getBehaviorEmoji(behavior as any);
      const bar = '█'.repeat(count);
      lines.push(`   ${emoji} ${behavior.padEnd(12)}: ${bar} (${count})`);
    });
    lines.push('');
    
    // 恶意 Agent 警告
    const malicious = network.identifyMaliciousAgents(0.3);
    if (malicious.length > 0) {
      lines.push('⚠️  Low Trust Agents:');
      malicious.forEach(id => {
        const agent = network['agents'].get(id);
        if (agent) {
          lines.push(`   - ${agent.name} (${(agent.trustScore * 100).toFixed(1)}%)`);
        }
      });
      lines.push('');
    }
    
    // 可信 Agent
    const trusted = network.getTrustedAgents(0.7);
    if (trusted.length > 0) {
      lines.push('✅ Highly Trusted Agents:');
      trusted.slice(0, 5).forEach(agent => {
        lines.push(`   - ${agent.name} (${(agent.trustScore * 100).toFixed(1)}%)`);
      });
      lines.push('');
    }
    
    return lines.join('\n');
  }

  /**
   * 生成交互历史图
   */
  static renderInteractionHistory(
    history: Array<{ requester: string; provider: string; success: boolean }>
  ): string {
    const lines: string[] = [];
    
    lines.push('📜 Interaction History:');
    lines.push('┌────────────────────┬────────────────────┬─────────┐');
    lines.push('│ Requester          │ Provider           │ Result  │');
    lines.push('├────────────────────┼────────────────────┼─────────┤');
    
    history.slice(-20).forEach(interaction => {
      const requester = interaction.requester.padEnd(18).substring(0, 18);
      const provider = interaction.provider.padEnd(18).substring(0, 18);
      const result = interaction.success ? '✅ Success' : '❌ Failed';
      
      lines.push(`│ ${requester} │ ${provider} │ ${result} │`);
    });
    
    lines.push('└────────────────────┴────────────────────┴─────────┘');
    
    return lines.join('\n');
  }

  /**
   * 生成信任传播动画（ASCII）
   */
  static renderTrustPropagation(
    network: TrustNetwork,
    iterations: number
  ): string {
    const lines: string[] = [];
    
    lines.push('🔄 Trust Propagation Simulation:');
    lines.push('');
    
    for (let i = 0; i < iterations; i++) {
      network.calculateTrustScores();
      const stats = network.getStats();
      
      const iteration = `Iteration ${i + 1}`.padEnd(15);
      const avgTrust = `Avg: ${(stats.averageTrust * 100).toFixed(1)}%`;
      const bar = this.getProgressBar(stats.averageTrust, 30);
      
      lines.push(`${iteration} ${avgTrust} ${bar}`);
    }
    
    lines.push('');
    lines.push('✨ Trust scores converged!');
    
    return lines.join('\n');
  }

  /**
   * 辅助方法：获取排序后的 Agent
   */
  private static getSortedAgents(network: TrustNetwork): Agent[] {
    const agents: Agent[] = [];
    network['agents'].forEach(agent => agents.push(agent));
    return agents.sort((a, b) => b.trustScore - a.trustScore);
  }

  /**
   * 辅助方法：获取行为表情
   */
  private static getBehaviorEmoji(behavior: string): string {
    const emojis: Record<string, string> = {
      cooperative: '🟢',
      neutral: '🟡',
      malicious: '🔴',
      adversarial: '⚫'
    };
    return emojis[behavior] || '⚪';
  }

  /**
   * 辅助方法：获取信任度进度条
   */
  private static getTrustBar(trust: number, length: number = 10): string {
    const filled = Math.round(trust * length);
    const empty = length - filled;
    
    const color = trust > 0.7 ? '🟩' : trust > 0.3 ? '🟨' : '🟥';
    
    return color.repeat(filled) + '⬜'.repeat(empty);
  }

  /**
   * 辅助方法：获取进度条
   */
  private static getProgressBar(value: number, length: number = 20): string {
    const filled = Math.round(value * length);
    const empty = length - filled;
    return '█'.repeat(filled) + '░'.repeat(empty);
  }
}
