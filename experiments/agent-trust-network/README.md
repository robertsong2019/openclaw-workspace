# Agent Trust Network

🤖 **多 Agent 信任网络模拟器** - 使用 PageRank 式算法的去中心化信任评估系统

## 项目简介

这是一个实验性的多 Agent 信任网络模拟器，探索去中心化系统中的信任传播机制。通过 PageRank 式的算法，Agent 可以根据彼此的交互历史建立信任关系，并自动识别恶意 Agent。

### 核心特性

- ✅ **PageRank 式信任传播** - 基于图论的信任分数计算
- ✅ **多种 Agent 行为类型** - 合作型、中立型、恶意型、对抗型
- ✅ **信任衰减机制** - 时间因素影响信任度
- ✅ **恶意 Agent 检测** - 自动识别低信任节点
- ✅ **交互模拟** - 模拟 Agent 之间的协作
- ✅ **网络可视化** - ASCII 艺术风格的网络拓扑图
- ✅ **状态持久化** - 导出/导入网络状态

## 技术架构

### Agent 类

```typescript
interface AgentConfig {
  id: string;
  name: string;
  behavior: 'cooperative' | 'neutral' | 'malicious' | 'adversarial';
  initialTrust?: number;      // 0-1, 默认 0.5
  expertise?: string[];        // 专业领域
  reliability?: number;        // 行为一致性 (0-1)
}
```

**行为类型**：
- 🟢 **cooperative** - 总是愿意合作，高成功率 (85%)
- 🟡 **neutral** - 有条件合作，中等成功率 (65%)
- 🔴 **malicious** - 不可预测，低成功率 (40%)
- ⚫ **adversarial** - 故意破坏，极低成功率 (10%)

### TrustNetwork 类

**核心算法**：

```
TrustScore(Agent) = (1 - d) / N + d × Σ(TrustScore(Incoming) × Weight / OutgoingWeight)
```

其中：
- `d` = 阻尼因子 (默认 0.85)
- `N` = 网络中的 Agent 总数

**信任衰减**：

```
Trust(t) = Trust(0) × (1 - decayRate)^hours
```

默认衰减率：0.001/小时

## 快速开始

### 安装依赖

```bash
cd experiments/agent-trust-network
npm install
```

### 运行演示

```bash
npm run demo
```

### 运行测试

```bash
npm test
```

## 使用示例

### 创建信任网络

```typescript
import { Agent } from './src/agent';
import { TrustNetwork } from './src/trust-network';

// 创建网络
const network = new TrustNetwork({
  dampingFactor: 0.85,
  trustDecayRate: 0.001
});

// 添加 Agent
const alice = new Agent({
  id: 'alice',
  name: 'Alice',
  behavior: 'cooperative',
  reliability: 0.95
});

const bob = new Agent({
  id: 'bob',
  name: 'Bob',
  behavior: 'neutral',
  reliability: 0.75
});

network.addAgent(alice);
network.addAgent(bob);

// 建立信任关系
network.setTrustRelation('alice', 'bob', 0.8);

// 计算信任分数
network.calculateTrustScores();

console.log(`Alice's trust: ${alice.trustScore}`);
console.log(`Bob's trust: ${bob.trustScore}`);
```

### 模拟交互

```typescript
// 模拟 Alice 请求 Bob 的服务
const result = network.simulateInteraction('alice', 'bob', 0.5);

console.log(`Success: ${result.success}`);
console.log(`Trust change: ${result.trustChange}`);
```

### 识别恶意 Agent

```typescript
// 获取低信任 Agent
const malicious = network.identifyMaliciousAgents(0.3);
console.log('Malicious agents:', malicious);

// 获取可信 Agent
const trusted = network.getTrustedAgents(0.7);
console.log('Trusted agents:', trusted.map(a => a.name));
```

### 应用信任衰减

```typescript
// 模拟 24 小时后的信任衰减
network.applyTrustDecay(24);
network.calculateTrustScores();
```

### 导出/导入网络

```typescript
// 导出
const data = network.export();
const json = JSON.stringify(data);

// 导入
const imported = TrustNetwork.import(JSON.parse(json));
```

## 可视化

### 网络拓扑图

```typescript
import { Visualizer } from './src/visualizer';

console.log(Visualizer.renderNetworkGraph(network));
```

输出示例：

```
╔════════════════════════════════════════════════════════════╗
║           🤖 Agent Trust Network Visualization             ║
╚════════════════════════════════════════════════════════════╝

📊 Network Statistics:
   Total Agents: 8
   Total Relations: 14
   Average Trust: 52.3%
   Clusters: 1

🤖 Agents (sorted by trust score):
┌────────────────────┬──────────┬─────────┬──────────┐
│ Name               │ Behavior │ Trust   │ Success  │
├────────────────────┼──────────┼─────────┼──────────┤
│ Alice              │ 🟢 coop  │ 89.2%   │ 100.0%   │ 🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜
│ Bob                │ 🟢 coop  │ 85.7%   │ 87.5%    │ 🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜
│ Charlie            │ 🟢 coop  │ 82.1%   │ 85.0%    │ 🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜
│ David              │ 🟡 neut  │ 65.4%   │ 60.0%    │ 🟨🟨🟨🟨🟨🟨🟨⬜⬜⬜
│ Eve                │ 🟡 neut  │ 58.2%   │ 40.0%    │ 🟨🟨🟨🟨🟨🟨⬜⬜⬜⬜
│ Mallory            │ 🔴 mali  │ 28.5%   │ 16.7%    │ 🟥🟥🟥⬜⬜⬜⬜⬜⬜⬜
│ Trudy              │ 🔴 mali  │ 22.1%   │ 0.0%     │ 🟥🟥⬜⬜⬜⬜⬜⬜⬜⬜
│ Adversary          │ ⚫ advers│ 5.3%    │ 0.0%     │ ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
└────────────────────┴──────────┴─────────┴──────────┘
```

### 交互历史

```typescript
console.log(Visualizer.renderInteractionHistory(history));
```

### 信任传播动画

```typescript
console.log(Visualizer.renderTrustPropagation(network, 10));
```

## 教育价值

### 1. 去中心化信任机制

演示了如何在没有中央权威的情况下建立信任：
- 每个 Agent 独立评估其他 Agent
- 信任通过交互历史积累
- 网络效应增强信任准确性

### 2. PageRank 算法应用

展示了 PageRank 在社交网络中的应用：
- 信任分数从高信任节点流向低信任节点
- 入链质量比数量更重要
- 迭代收敛到稳定状态

### 3. 恶意行为检测

演示了如何自动识别不良行为者：
- 低成功率导致信任下降
- 信任传播隔离恶意节点
- 时间衰减清理不活跃节点

### 4. 博弈论概念

展示了不同的策略：
- 合作型策略（长期收益最高）
- 短视策略（短期收益，长期损失）
- 对抗策略（总是失败）

## 实际应用场景

### 1. 多 Agent 系统

在 AI Agent 协作中：
- Agent 可以根据信任分数选择合作伙伴
- 自动隔离不可靠的 Agent
- 优化任务分配策略

### 2. P2P 网络

在点对点系统中：
- 评估节点的可靠性
- 防止恶意节点污染网络
- 优化路由选择

### 3. 供应链管理

在多方协作中：
- 评估供应商的可靠性
- 追踪历史表现
- 风险评估和预警

### 4. 在线市场

在电子商务中：
- 买家/卖家信誉系统
- 欺诈检测
- 推荐系统

## 未来增强

### 短期（1-2 周）

- [ ] Web UI 可视化（D3.js/Cytoscape.js）
- [ ] 更多行为策略（Tit-for-Tat、Grim Trigger）
- [ ] 信任网络图谱导出（GraphML/JSON）

### 中期（1-2 月）

- [ ] 机器学习预测 Agent 行为
- [ ] 动态网络拓扑（节点加入/离开）
- [ ] 多层信任网络（不同领域的信任）

### 长期（3-6 月）

- [ ] 区块链集成（不可篡改的信任记录）
- [ ] 联邦学习（跨网络信任共享）
- [ ] 实时可视化仪表板

## 技术栈

- **语言**: TypeScript
- **运行时**: Node.js
- **算法**: PageRank、图论
- **可视化**: ASCII 艺术（未来：D3.js）

## 参考文献

1. **PageRank**: Page, L., Brin, S., Motwani, R., & Winograd, T. (1999). The PageRank citation ranking: Bringing order to the web.
2. **Trust Networks**: Golbeck, J. (2009). Computing with social trust.
3. **Multi-Agent Systems**: Wooldridge, M. (2009). An introduction to multiagent systems.

## 许可证

MIT License

## 作者

Robert Song - [GitHub](https://github.com/robertsong2019)

## 致谢

本项目是代码实验室的实验性项目，旨在探索多 Agent 系统中的信任机制。感谢 OpenClaw 平台提供的开发环境。

---

**🌟 如果你觉得这个项目有趣，请给一个 Star！**
