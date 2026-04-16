# API Reference - Agent Trust Network

> Complete API documentation for the multi-agent trust network simulator

## Table of Contents

- [Core Classes](#core-classes)
  - [Agent](#agent)
  - [TrustNetwork](#trustnetwork)
  - [Visualizer](#visualizer)
- [Interfaces](#interfaces)
- [Algorithms](#algorithms)
- [Examples](#examples)

---

## Core Classes

### Agent

Represents an individual agent in the trust network.

#### Constructor

```typescript
import { Agent } from './src/agent';

const agent = new Agent(config: AgentConfig);
```

**Parameters:**

```typescript
interface AgentConfig {
  id: string;                          // Unique identifier
  name: string;                        // Display name
  behavior: AgentBehavior;             // Behavior type
  initialTrust?: number;               // Initial trust score (0-1, default: 0.5)
  expertise?: string[];                // Areas of expertise
  reliability?: number;                // Behavior consistency (0-1)
}

type AgentBehavior = 
  | 'cooperative'   // Always willing to collaborate
  | 'neutral'       // Conditional collaboration
  | 'malicious'     // Unpredictable behavior
  | 'adversarial';  // Intentionally disruptive
```

**Example:**

```typescript
const alice = new Agent({
  id: 'alice-001',
  name: 'Alice',
  behavior: 'cooperative',
  initialTrust: 0.7,
  expertise: ['machine-learning', 'data-analysis'],
  reliability: 0.95
});
```

---

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | string | Unique identifier |
| `name` | string | Display name |
| `behavior` | AgentBehavior | Behavior type |
| `trustScore` | number | Current trust score (0-1) |
| `expertise` | string[] | Areas of expertise |
| `reliability` | number | Behavior consistency (0-1) |
| `interactions` | Interaction[] | History of interactions |
| `lastActiveTime` | Date | Last activity timestamp |

---

#### Methods

##### `performTask(difficulty: number): InteractionResult`

Perform a task with given difficulty.

```typescript
const result = alice.performTask(0.5);

console.log(result.success);      // true/false
console.log(result.quality);      // 0-1
console.log(result.duration);     // milliseconds
```

**Parameters:**

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| `difficulty` | number | 0-1 | Task difficulty (0=easy, 1=hard) |

**Returns:**

```typescript
interface InteractionResult {
  success: boolean;       // Whether task succeeded
  quality: number;        // Quality of output (0-1)
  duration: number;       // Time taken (ms)
  agentId: string;        // Agent ID
  timestamp: Date;        // When it occurred
}
```

**Behavior Success Rates:**

| Behavior | Base Success Rate |
|----------|-------------------|
| cooperative | 85% |
| neutral | 65% |
| malicious | 40% |
| adversarial | 10% |

---

##### `recordInteraction(interaction: Interaction): void`

Record an interaction with another agent.

```typescript
alice.recordInteraction({
  partnerId: 'bob-001',
  success: true,
  trustChange: 0.05,
  timestamp: new Date()
});
```

---

##### `updateTrustScore(delta: number): void`

Update trust score by a delta.

```typescript
// Increase trust
alice.updateTrustScore(0.05);

// Decrease trust
alice.updateTrustScore(-0.1);
```

**Note:** Trust score is clamped to [0, 1].

---

### TrustNetwork

The main network class that manages agents and trust relationships.

#### Constructor

```typescript
import { TrustNetwork } from './src/trust-network';

const network = new TrustNetwork(config?: NetworkConfig);
```

**Parameters:**

```typescript
interface NetworkConfig {
  dampingFactor?: number;      // PageRank damping (default: 0.85)
  trustDecayRate?: number;     // Trust decay per hour (default: 0.001)
  minTrustThreshold?: number;  // Min trust to be "trusted" (default: 0.3)
  maxTrustThreshold?: number;  // Max trust to be "trusted" (default: 0.7)
}
```

---

#### Methods

##### `addAgent(agent: Agent): void`

Add an agent to the network.

```typescript
network.addAgent(alice);
network.addAgent(bob);
```

---

##### `removeAgent(agentId: string): void`

Remove an agent from the network.

```typescript
network.removeAgent('mallory-001');
```

---

##### `setTrustRelation(sourceId: string, targetId: string, weight: number): void`

Set trust relationship between two agents.

```typescript
// Alice trusts Bob with weight 0.8
network.setTrustRelation('alice-001', 'bob-001', 0.8);

// Charlie trusts Alice with weight 0.9
network.setTrustRelation('charlie-001', 'alice-001', 0.9);
```

**Parameters:**

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| `sourceId` | string | - | Source agent ID |
| `targetId` | string | - | Target agent ID |
| `weight` | number | 0-1 | Trust weight |

---

##### `calculateTrustScores(): Map<string, number>`

Calculate trust scores using PageRank algorithm.

```typescript
const scores = network.calculateTrustScores();

console.log(scores.get('alice-001'));  // 0.892
console.log(scores.get('bob-001'));    // 0.857
```

**Algorithm:**

```
TrustScore(Agent) = (1 - d) / N + d × Σ(TrustScore(Incoming) × Weight / OutgoingWeight)
```

Where:
- `d` = damping factor (default 0.85)
- `N` = total number of agents

---

##### `simulateInteraction(requesterId: string, providerId: string, difficulty: number): InteractionResult`

Simulate an interaction between two agents.

```typescript
const result = network.simulateInteraction('alice-001', 'bob-001', 0.5);

if (result.success) {
  console.log('Interaction succeeded!');
  console.log(`Trust change: +${result.trustChange}`);
} else {
  console.log('Interaction failed!');
  console.log(`Trust change: ${result.trustChange}`);
}
```

**Returns:**

```typescript
interface InteractionResult {
  success: boolean;
  trustChange: number;       // Change in trust score
  requesterId: string;
  providerId: string;
  timestamp: Date;
}
```

**Trust Change Calculation:**

```typescript
if (success) {
  trustChange = 0.05 × (1 - currentTrust)  // Diminishing returns
} else {
  trustChange = -0.1 × currentTrust        // Proportional penalty
}
```

---

##### `identifyMaliciousAgents(threshold?: number): Agent[]`

Identify agents below trust threshold.

```typescript
const malicious = network.identifyMaliciousAgents(0.3);

console.log('Malicious agents:');
malicious.forEach(agent => {
  console.log(`  - ${agent.name}: ${agent.trustScore.toFixed(3)}`);
});
```

**Default threshold:** 0.3

---

##### `getTrustedAgents(threshold?: number): Agent[]`

Get agents above trust threshold.

```typescript
const trusted = network.getTrustedAgents(0.7);

console.log('Trusted agents:');
trusted.forEach(agent => {
  console.log(`  - ${agent.name}: ${agent.trustScore.toFixed(3)}`);
});
```

**Default threshold:** 0.7

---

##### `applyTrustDecay(hours: number): void`

Apply time-based trust decay.

```typescript
// Simulate 24 hours of decay
network.applyTrustDecay(24);
network.calculateTrustScores();
```

**Decay Formula:**

```
Trust(t) = Trust(0) × (1 - decayRate)^hours
```

**Default decay rate:** 0.001 per hour

---

##### `getAgentById(agentId: string): Agent | undefined`

Get agent by ID.

```typescript
const agent = network.getAgentById('alice-001');
if (agent) {
  console.log(`Found: ${agent.name}`);
}
```

---

##### `getAllAgents(): Agent[]`

Get all agents in the network.

```typescript
const agents = network.getAllAgents();
console.log(`Total agents: ${agents.length}`);
```

---

##### `export(): NetworkData`

Export network state for persistence.

```typescript
const data = network.export();
const json = JSON.stringify(data, null, 2);

// Save to file
fs.writeFileSync('network-state.json', json);
```

**Returns:**

```typescript
interface NetworkData {
  agents: AgentData[];
  relations: RelationData[];
  config: NetworkConfig;
  timestamp: string;
}

interface AgentData {
  id: string;
  name: string;
  behavior: AgentBehavior;
  trustScore: number;
  expertise: string[];
  reliability: number;
  interactions: Interaction[];
}

interface RelationData {
  sourceId: string;
  targetId: string;
  weight: number;
}
```

---

##### `static import(data: NetworkData): TrustNetwork`

Import network from saved state.

```typescript
// Load from file
const json = fs.readFileSync('network-state.json', 'utf-8');
const data = JSON.parse(json);

// Import
const network = TrustNetwork.import(data);
```

---

### Visualizer

Static class for network visualization.

#### Methods

##### `static renderNetworkGraph(network: TrustNetwork): string`

Render ASCII art network visualization.

```typescript
import { Visualizer } from './src/visualizer';

const output = Visualizer.renderNetworkGraph(network);
console.log(output);
```

**Output:**

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
│ Mallory            │ 🔴 mali  │ 28.5%   │ 16.7%    │ 🟥🟥🟥⬜⬜⬜⬜⬜⬜⬜
└────────────────────┴──────────┴─────────┴──────────┘
```

---

##### `static renderInteractionHistory(interactions: Interaction[]): string`

Render interaction history.

```typescript
const history = alice.interactions;
console.log(Visualizer.renderInteractionHistory(history));
```

---

##### `static renderTrustPropagation(network: TrustNetwork, iterations: number): string`

Animate trust propagation over iterations.

```typescript
console.log(Visualizer.renderTrustPropagation(network, 10));
```

---

## Interfaces

### Interaction

```typescript
interface Interaction {
  partnerId: string;        // Who the interaction was with
  success: boolean;         // Whether it succeeded
  trustChange: number;      // Change in trust
  timestamp: Date;          // When it occurred
  difficulty?: number;      // Task difficulty
}
```

### NetworkStats

```typescript
interface NetworkStats {
  totalAgents: number;
  totalRelations: number;
  averageTrust: number;
  clusters: number;
  density: number;
}
```

---

## Algorithms

### PageRank Trust Calculation

The trust network uses a modified PageRank algorithm:

```typescript
function calculatePageRank(
  agents: Agent[],
  relations: Map<string, Map<string, number>>,
  dampingFactor: number
): Map<string, number> {
  const N = agents.length;
  const scores = new Map<string, number>();
  
  // Initialize with uniform distribution
  agents.forEach(agent => {
    scores.set(agent.id, 1 / N);
  });
  
  // Iterate until convergence
  for (let i = 0; i < 100; i++) {
    const newScores = new Map<string, number>();
    
    agents.forEach(agent => {
      let sum = 0;
      
      // Sum contributions from incoming links
      agents.forEach(other => {
        const weight = relations.get(other.id)?.get(agent.id);
        if (weight) {
          const outgoingWeight = getTotalOutgoingWeight(other.id, relations);
          sum += (scores.get(other.id) || 0) * weight / outgoingWeight;
        }
      });
      
      // Apply PageRank formula
      const newScore = (1 - dampingFactor) / N + dampingFactor * sum;
      newScores.set(agent.id, newScore);
    });
    
    scores = newScores;
  }
  
  return scores;
}
```

### Trust Decay

```typescript
function applyDecay(
  trustScore: number,
  hours: number,
  decayRate: number
): number {
  return trustScore * Math.pow(1 - decayRate, hours);
}
```

### Malicious Agent Detection

```typescript
function detectMalicious(
  agents: Agent[],
  threshold: number = 0.3
): Agent[] {
  return agents.filter(agent => agent.trustScore < threshold);
}
```

---

## Examples

### Example 1: Basic Network

```typescript
import { Agent } from './src/agent';
import { TrustNetwork } from './src/trust-network';

// Create network
const network = new TrustNetwork({
  dampingFactor: 0.85,
  trustDecayRate: 0.001
});

// Add agents
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

// Establish trust
network.setTrustRelation('alice', 'bob', 0.8);
network.setTrustRelation('bob', 'alice', 0.7);

// Calculate scores
network.calculateTrustScores();

console.log(`Alice trust: ${alice.trustScore.toFixed(3)}`);
console.log(`Bob trust: ${bob.trustScore.toFixed(3)}`);
```

### Example 2: Detect Malicious Agents

```typescript
// Add some malicious agents
const mallory = new Agent({
  id: 'mallory',
  name: 'Mallory',
  behavior: 'malicious'
});

const trudy = new Agent({
  id: 'trudy',
  name: 'Trudy',
  behavior: 'adversarial'
});

network.addAgent(mallory);
network.addAgent(trudy);

// Simulate interactions
for (let i = 0; i < 10; i++) {
  network.simulateInteraction('alice', 'mallory', 0.5);
  network.simulateInteraction('alice', 'trudy', 0.5);
}

// Calculate and detect
network.calculateTrustScores();
const malicious = network.identifyMaliciousAgents(0.3);

console.log('Malicious agents detected:');
malicious.forEach(agent => {
  console.log(`  - ${agent.name}: ${agent.trustScore.toFixed(3)}`);
});
```

### Example 3: Time-Based Decay

```typescript
// Initial state
network.calculateTrustScores();
console.log('Initial trust:', alice.trustScore);

// Simulate 48 hours passing
network.applyTrustDecay(48);
network.calculateTrustScores();

console.log('After 48 hours:', alice.trustScore);

// Re-establish trust through successful interactions
network.simulateInteraction('bob', 'alice', 0.3);
network.calculateTrustScores();

console.log('After interaction:', alice.trustScore);
```

### Example 4: Export and Import

```typescript
// Export
const data = network.export();
const json = JSON.stringify(data, null, 2);
fs.writeFileSync('network-backup.json', json);

// Later, import
const loaded = JSON.parse(fs.readFileSync('network-backup.json', 'utf-8'));
const restored = TrustNetwork.import(loaded);

console.log('Restored agents:', restored.getAllAgents().length);
```

---

## Performance

### Complexity

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| `addAgent` | O(1) | O(1) |
| `setTrustRelation` | O(1) | O(1) |
| `calculateTrustScores` | O(N² × I) | O(N) |
| `simulateInteraction` | O(1) | O(1) |
| `identifyMaliciousAgents` | O(N) | O(N) |

Where:
- N = number of agents
- I = PageRank iterations (typically 10-100)

### Benchmarks

**Network Size: 100 agents**

- `calculateTrustScores`: ~50ms (10 iterations)
- `simulateInteraction`: ~0.1ms
- `identifyMaliciousAgents`: ~1ms

**Network Size: 1000 agents**

- `calculateTrustScores`: ~5s (10 iterations)
- `simulateInteraction`: ~0.1ms
- `identifyMaliciousAgents`: ~10ms

---

## Error Handling

```typescript
try {
  network.setTrustRelation('invalid-id', 'bob', 0.5);
} catch (error) {
  if (error instanceof AgentNotFoundError) {
    console.error('Agent not found:', error.agentId);
  }
}

try {
  network.calculateTrustScores();
} catch (error) {
  if (error instanceof NetworkEmptyError) {
    console.error('Network has no agents');
  }
}
```

---

## Version History

- **v1.0.0** (2026-03-20): Initial release
  - PageRank trust calculation
  - 4 behavior types
  - Trust decay
  - Visualization
  - Export/Import

---

**Next:** [TUTORIAL.md](TUTORIAL.md) - Step-by-step tutorial

**Questions?** Open an issue or check the [README](README.md)
