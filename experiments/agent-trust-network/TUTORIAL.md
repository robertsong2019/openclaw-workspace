# Tutorial - Agent Trust Network

> From zero to decentralized trust in 30 minutes

## Table of Contents

- [Introduction](#introduction)
- [Part 1: Understanding Trust Networks](#part-1-understanding-trust-networks)
- [Part 2: Your First Trust Network](#part-2-your-first-trust-network)
- [Part 3: Agent Behaviors](#part-3-agent-behaviors)
- [Part 4: Trust Propagation](#part-4-trust-propagation)
- [Part 5: Real-World Applications](#part-5-real-world-applications)
- [Part 6: Advanced Topics](#part-6-advanced-topics)

---

## Introduction

### What is a Trust Network?

A **trust network** is a system where entities (agents) build trust through interactions, without needing a central authority. Think of it like reputation in a community - you trust someone because others you trust vouch for them.

**Real-world examples:**

- **Social networks**: You trust a friend's recommendation
- **P2P networks**: Nodes trust each other based on file sharing history
- **Supply chains**: Companies trust suppliers based on past deliveries
- **Online markets**: Buyers/sellers build reputation through transactions

### Why Decentralized Trust?

Traditional systems use a **central authority**:

```
┌─────────┐
│ Central │ ←── Everyone trusts this
│Authority│
└─────────┘
     ↑
   ┌─┴─┐
   │   │
  👤  👤
```

**Problems:**

- Single point of failure
- Requires trust in authority
- Doesn't scale well
- Can be manipulated

**Decentralized trust**:

```
  👤 ←→ 👤
  ↑     ↑
  │     │
  └──→ 👤 ←── Trust flows through the network
```

**Advantages:**

- No single point of failure
- Trust emerges from interactions
- Scales naturally
- Resistant to manipulation

### What You'll Learn

By the end of this tutorial, you'll understand:

1. How trust networks work
2. How to build agents with different behaviors
3. How trust propagates through a network
4. How to detect malicious agents
5. Real-world applications and patterns

---

## Part 1: Understanding Trust Networks

### The PageRank Connection

This project uses a modified **PageRank algorithm** (the same one Google uses for search rankings).

**PageRank for web pages:**

```
Page A is important if:
  1. Many pages link to it
  2. Important pages link to it
```

**PageRank for trust:**

```
Agent A is trusted if:
  1. Many agents trust A
  2. Trusted agents trust A
```

### How Trust Scores Work

Each agent has a **trust score** between 0 and 1:

- **0.0**: Completely untrusted
- **0.5**: Neutral (starting point)
- **1.0**: Fully trusted

**Trust is dynamic:**

- Increases with successful interactions
- Decreases with failed interactions
- Decays over time (if no interactions)

### Trust Propagation Example

Imagine this network:

```
Alice (0.9) → Bob (0.8) → Charlie (0.7)
     ↓           ↓
  David      Eve (0.6)
```

**How trust flows:**

1. Alice is trusted by many → High score
2. Bob is trusted by Alice → Medium-high score
3. Charlie is trusted by Bob → Medium score
4. Eve is trusted by Bob → Medium score
5. David is only trusted by Alice → Lower score

---

## Part 2: Your First Trust Network

### Step 1: Install and Setup

```bash
# Clone or navigate to the project
cd experiments/agent-trust-network

# Install dependencies
npm install

# Run the demo
npm run demo
```

### Step 2: Create Agents

```typescript
import { Agent } from './src/agent';
import { TrustNetwork } from './src/trust-network';

// Create different types of agents
const alice = new Agent({
  id: 'alice-001',
  name: 'Alice',
  behavior: 'cooperative',     // Always helpful
  reliability: 0.95            // Very consistent
});

const bob = new Agent({
  id: 'bob-001',
  name: 'Bob',
  behavior: 'neutral',         // Sometimes helpful
  reliability: 0.75
});

const mallory = new Agent({
  id: 'mallory-001',
  name: 'Mallory',
  behavior: 'malicious',       // Unpredictable
  reliability: 0.3
});
```

**What do these properties mean?**

- **behavior**: How the agent acts (see Part 3)
- **reliability**: How consistent the behavior is (0-1)
  - 0.95: Alice almost always acts cooperatively
  - 0.3: Mallory is very unpredictable

### Step 3: Create Network

```typescript
// Create the trust network
const network = new TrustNetwork({
  dampingFactor: 0.85,        // PageRank parameter
  trustDecayRate: 0.001       // Trust decay per hour
});

// Add agents to the network
network.addAgent(alice);
network.addAgent(bob);
network.addAgent(mallory);
```

### Step 4: Establish Trust Relationships

```typescript
// Alice trusts Bob
network.setTrustRelation('alice-001', 'bob-001', 0.8);

// Bob trusts Alice (mutual trust)
network.setTrustRelation('bob-001', 'alice-001', 0.7);

// Alice initially trusts Mallory (unknown behavior)
network.setTrustRelation('alice-001', 'mallory-001', 0.5);
```

### Step 5: Calculate Trust Scores

```typescript
// Run PageRank algorithm
network.calculateTrustScores();

// Check the scores
console.log('Initial trust scores:');
console.log(`  Alice: ${alice.trustScore.toFixed(3)}`);      // 0.723
console.log(`  Bob: ${bob.trustScore.toFixed(3)}`);          // 0.689
console.log(`  Mallory: ${mallory.trustScore.toFixed(3)}`);  // 0.500
```

### Step 6: Simulate Interactions

```typescript
// Simulate Alice interacting with Mallory
for (let i = 0; i < 10; i++) {
  const result = network.simulateInteraction(
    'alice-001',    // Requester
    'mallory-001',  // Provider
    0.5             // Task difficulty
  );
  
  console.log(`Interaction ${i + 1}: ${result.success ? '✓' : '✗'}`);
}

// Recalculate trust scores
network.calculateTrustScores();

console.log('\nAfter interactions with Mallory:');
console.log(`  Mallory: ${mallory.trustScore.toFixed(3)}`);  // Likely decreased!
```

**What happens:**

1. Alice requests Mallory's help
2. Mallory (malicious) often fails
3. Trust score decreases
4. Network recalculates

### Step 7: Detect Malicious Agents

```typescript
// Identify low-trust agents
const malicious = network.identifyMaliciousAgents(0.3);

console.log('\nMalicious agents detected:');
malicious.forEach(agent => {
  console.log(`  - ${agent.name}: ${agent.trustScore.toFixed(3)}`);
});

// Get trusted agents
const trusted = network.getTrustedAgents(0.7);

console.log('\nTrusted agents:');
trusted.forEach(agent => {
  console.log(`  - ${agent.name}: ${agent.trustScore.toFixed(3)}`);
});
```

---

## Part 3: Agent Behaviors

### The Four Behavior Types

#### 1. Cooperative 🟢

**Strategy:** Always willing to collaborate, high success rate.

```typescript
const cooperative = new Agent({
  id: 'coop-001',
  name: 'Helpful Agent',
  behavior: 'cooperative',
  reliability: 0.95
});
```

**Characteristics:**

- Success rate: ~85%
- Builds trust quickly
- Ideal for long-term collaboration
- **Best strategy** in repeated interactions

**When to use:**

- Team members
- Reliable services
- Long-term partners

#### 2. Neutral 🟡

**Strategy:** Conditional collaboration, medium success rate.

```typescript
const neutral = new Agent({
  id: 'neutral-001',
  name: 'Cautious Agent',
  behavior: 'neutral',
  reliability: 0.75
});
```

**Characteristics:**

- Success rate: ~65%
- Trust builds slowly
- Risk-averse
- Pragmatic approach

**When to use:**

- New relationships
- Uncertain environments
- Cost-benefit analysis

#### 3. Malicious 🔴

**Strategy:** Unpredictable behavior, low success rate.

```typescript
const malicious = new Agent({
  id: 'malicious-001',
  name: 'Unreliable Agent',
  behavior: 'malicious',
  reliability: 0.4
});
```

**Characteristics:**

- Success rate: ~40%
- Trust decreases over time
- Detected by network
- Isolated eventually

**Why include in network?**

- Test network resilience
- Model real-world bad actors
- Demonstrate detection

#### 4. Adversarial ⚫

**Strategy:** Intentionally disruptive, very low success rate.

```typescript
const adversarial = new Agent({
  id: 'adversarial-001',
  name: 'Hostile Agent',
  behavior: 'adversarial',
  reliability: 0.1
});
```

**Characteristics:**

- Success rate: ~10%
- Quickly isolated
- Network self-protects
- Extreme case

### Behavior Comparison Table

| Behavior | Success Rate | Trust Build | Detection Time | Use Case |
|----------|-------------|-------------|----------------|----------|
| Cooperative | 85% | Fast | Never (trusted) | Ideal team member |
| Neutral | 65% | Medium | Rare | Cautious partner |
| Malicious | 40% | Negative | 10-20 interactions | Bad actor |
| Adversarial | 10% | Very negative | 5-10 interactions | Hostile actor |

### Experiment: Behavior Impact

```typescript
// Create 4 agents, one of each type
const agents = [
  new Agent({ id: 'coop', name: 'Cooperative', behavior: 'cooperative' }),
  new Agent({ id: 'neutral', name: 'Neutral', behavior: 'neutral' }),
  new Agent({ id: 'malicious', name: 'Malicious', behavior: 'malicious' }),
  new Agent({ id: 'adversarial', name: 'Adversarial', behavior: 'adversarial' })
];

// Add to network
agents.forEach(agent => network.addAgent(agent));

// Simulate 50 interactions for each
agents.forEach(agent => {
  for (let i = 0; i < 50; i++) {
    network.simulateInteraction('test-requester', agent.id, 0.5);
  }
});

// Calculate and compare
network.calculateTrustScores();

agents.sort((a, b) => b.trustScore - a.trustScore);

console.log('Trust ranking after 50 interactions:');
agents.forEach((agent, rank) => {
  console.log(`${rank + 1}. ${agent.name}: ${agent.trustScore.toFixed(3)}`);
});
```

**Expected output:**

```
1. Cooperative: 0.892
2. Neutral: 0.654
3. Malicious: 0.285
4. Adversarial: 0.053
```

---

## Part 4: Trust Propagation

### How Trust Spreads

Trust doesn't just come from direct interactions. It **propagates** through the network.

**Example:**

```
Alice → Bob → Charlie

If Alice trusts Bob, and Bob trusts Charlie,
then Alice indirectly trusts Charlie.
```

### The PageRank Formula

```typescript
TrustScore(Agent) = (1 - d) / N + d × Σ(TrustScore(Incoming) × Weight / OutgoingWeight)
```

**Breaking it down:**

1. **Base trust**: `(1 - d) / N`
   - Everyone gets minimum trust
   - `d` = damping factor (default 0.85)
   - `N` = number of agents

2. **Incoming trust**: `d × Σ(...)`
   - Sum of trust from all incoming links
   - Weighted by relationship strength
   - Divided by total outgoing weight

### Step-by-Step Calculation

**Network:**

```
Alice (trusts Bob: 0.8)
Bob (trusts Charlie: 0.9)
Charlie
```

**Iteration 1:**

```typescript
// Initialize all agents with 1/3 = 0.333
Alice.trustScore = 0.333
Bob.trustScore = 0.333
Charlie.trustScore = 0.333
```

**Iteration 2:**

```typescript
// Alice has no incoming links
Alice.trustScore = (1 - 0.85) / 3 + 0 = 0.05

// Bob is trusted by Alice (0.333 × 0.8)
Bob.trustScore = (1 - 0.85) / 3 + 0.85 × (0.333 × 0.8) = 0.276

// Charlie is trusted by Bob (0.333 × 0.9)
Charlie.trustScore = (1 - 0.85) / 3 + 0.85 × (0.333 × 0.9) = 0.304
```

**After 10 iterations (convergence):**

```typescript
Alice.trustScore = 0.089
Bob.trustScore = 0.312
Charlie.trustScore = 0.598
```

**Interpretation:**

- Alice has lowest score (no one trusts her)
- Bob has medium score (trusted by Alice)
- Charlie has highest score (trusted by Bob, who is trusted by Alice)

### Experiment: Network Topology

```typescript
// Create different network topologies
const star = new TrustNetwork();    // One central node
const chain = new TrustNetwork();   // Linear chain
const mesh = new TrustNetwork();    // Fully connected

// Star topology: Center agent is trusted by all
const center = new Agent({ id: 'center', name: 'Hub', behavior: 'cooperative' });
star.addAgent(center);

for (let i = 0; i < 5; i++) {
  const agent = new Agent({ 
    id: `star-${i}`, 
    name: `Agent ${i}`,
    behavior: 'cooperative'
  });
  star.addAgent(agent);
  star.setTrustRelation(`star-${i}`, 'center', 0.9);
}

star.calculateTrustScores();
console.log('Star network - Hub trust:', center.trustScore.toFixed(3));  // Very high
```

---

## Part 5: Real-World Applications

### Application 1: Multi-Agent System Coordination

**Scenario:** AI agents collaborating on a project.

```typescript
// Create specialized agents
const planner = new Agent({
  id: 'planner',
  name: 'Planner',
  behavior: 'cooperative',
  expertise: ['planning', 'coordination']
});

const coder = new Agent({
  id: 'coder',
  name: 'Coder',
  behavior: 'cooperative',
  expertise: ['coding', 'testing']
});

const reviewer = new Agent({
  id: 'reviewer',
  name: 'Reviewer',
  behavior: 'neutral',
  expertise: ['review', 'quality']
});

const network = new TrustNetwork();
network.addAgent(planner);
network.addAgent(coder);
network.addAgent(reviewer);

// Establish trust
network.setTrustRelation('planner', 'coder', 0.8);
network.setTrustRelation('coder', 'reviewer', 0.7);
network.setTrustRelation('reviewer', 'planner', 0.9);

// Simulate collaboration
for (let sprint = 0; sprint < 5; sprint++) {
  // Planner delegates to Coder
  network.simulateInteraction('planner', 'coder', 0.6);
  
  // Coder submits to Reviewer
  network.simulateInteraction('coder', 'reviewer', 0.7);
  
  // Reviewer gives feedback to Planner
  network.simulateInteraction('reviewer', 'planner', 0.5);
  
  network.calculateTrustScores();
  
  console.log(`\nSprint ${sprint + 1} trust scores:`);
  console.log(`  Planner: ${planner.trustScore.toFixed(3)}`);
  console.log(`  Coder: ${coder.trustScore.toFixed(3)}`);
  console.log(`  Reviewer: ${reviewer.trustScore.toFixed(3)}`);
}
```

### Application 2: P2P Network Reputation

**Scenario:** File sharing network with reputation.

```typescript
// Create peer nodes
const peers = [];
for (let i = 0; i < 20; i++) {
  const behavior = Math.random() > 0.8 ? 'malicious' : 'cooperative';
  const peer = new Agent({
    id: `peer-${i}`,
    name: `Peer ${i}`,
    behavior: behavior,
    expertise: ['file-sharing']
  });
  peers.push(peer);
  network.addAgent(peer);
}

// Simulate file sharing
for (let exchange = 0; exchange < 100; exchange++) {
  const requester = peers[Math.floor(Math.random() * peers.length)];
  const provider = peers[Math.floor(Math.random() * peers.length)];
  
  if (requester.id !== provider.id) {
    network.simulateInteraction(requester.id, provider.id, 0.5);
  }
}

// Identify good peers
network.calculateTrustScores();
const trustedPeers = network.getTrustedAgents(0.7);

console.log(`Trusted peers: ${trustedPeers.length} / ${peers.length}`);

// Identify malicious peers
const maliciousPeers = network.identifyMaliciousAgents(0.3);

console.log(`Malicious peers detected: ${maliciousPeers.length}`);
console.log('Malicious peer IDs:', maliciousPeers.map(p => p.id).join(', '));
```

### Application 3: Supply Chain Verification

**Scenario:** Supplier reputation in a supply chain.

```typescript
// Create supply chain nodes
const manufacturer = new Agent({
  id: 'manufacturer',
  name: 'ACME Corp',
  behavior: 'cooperative',
  expertise: ['manufacturing']
});

const supplier1 = new Agent({
  id: 'supplier-1',
  name: 'Quality Parts Inc',
  behavior: 'cooperative',
  expertise: ['components']
});

const supplier2 = new Agent({
  id: 'supplier-2',
  name: 'Cheap Parts Ltd',
  behavior: 'malicious',
  expertise: ['components']
});

const logistics = new Agent({
  id: 'logistics',
  name: 'FastShip Co',
  behavior: 'neutral',
  expertise: ['shipping']
});

const supplyChain = new TrustNetwork();
supplyChain.addAgent(manufacturer);
supplyChain.addAgent(supplier1);
supplyChain.addAgent(supplier2);
supplyChain.addAgent(logistics);

// Establish relationships
supplyChain.setTrustRelation('manufacturer', 'supplier-1', 0.8);
supplyChain.setTrustRelation('manufacturer', 'supplier-2', 0.6);
supplyChain.setTrustRelation('manufacturer', 'logistics', 0.7);

// Simulate deliveries
for (let order = 0; order < 20; order++) {
  // Alternate between suppliers
  const supplierId = order % 2 === 0 ? 'supplier-1' : 'supplier-2';
  
  const result = supplyChain.simulateInteraction(
    'manufacturer',
    supplierId,
    0.6
  );
  
  console.log(`Order ${order + 1} (${supplierId}): ${result.success ? '✓' : '✗'}`);
}

// Evaluate suppliers
supplyChain.calculateTrustScores();

console.log('\nSupplier evaluation:');
console.log(`  ${supplier1.name}: ${supplier1.trustScore.toFixed(3)}`);
console.log(`  ${supplier2.name}: ${supplier2.trustScore.toFixed(3)}`);

// Make decision
if (supplier1.trustScore > supplier2.trustScore) {
  console.log('\n✓ Decision: Use Quality Parts Inc for future orders');
}
```

### Application 4: Online Marketplace

**Scenario:** Buyer and seller reputation system.

```typescript
// Create marketplace participants
const buyers = [];
const sellers = [];

for (let i = 0; i < 10; i++) {
  buyers.push(new Agent({
    id: `buyer-${i}`,
    name: `Buyer ${i}`,
    behavior: Math.random() > 0.7 ? 'neutral' : 'cooperative'
  }));
  
  sellers.push(new Agent({
    id: `seller-${i}`,
    name: `Seller ${i}`,
    behavior: Math.random() > 0.8 ? 'malicious' : 'cooperative'
  }));
}

const marketplace = new TrustNetwork();
[...buyers, ...sellers].forEach(agent => marketplace.addAgent(agent));

// Simulate transactions
for (let transaction = 0; transaction < 100; transaction++) {
  const buyer = buyers[Math.floor(Math.random() * buyers.length)];
  const seller = sellers[Math.floor(Math.random() * sellers.length)];
  
  // Buyer rates seller
  const result = marketplace.simulateInteraction(buyer.id, seller.id, 0.5);
  
  // Seller rates buyer (reciprocal)
  marketplace.simulateInteraction(seller.id, buyer.id, 0.3);
}

// Identify top sellers
marketplace.calculateTrustScores();
const topSellers = marketplace.getTrustedAgents(0.75)
  .filter(a => a.id.startsWith('seller-'))
  .sort((a, b) => b.trustScore - a.trustScore);

console.log('Top sellers:');
topSellers.slice(0, 5).forEach((seller, rank) => {
  console.log(`${rank + 1}. ${seller.name}: ${seller.trustScore.toFixed(3)}`);
});

// Identify bad sellers
const badSellers = marketplace.identifyMaliciousAgents(0.3)
  .filter(a => a.id.startsWith('seller-'));

console.log('\n⚠️ Avoid these sellers:');
badSellers.forEach(seller => {
  console.log(`  - ${seller.name}: ${seller.trustScore.toFixed(3)}`);
});
```

---

## Part 6: Advanced Topics

### Topic 1: Trust Decay Over Time

```typescript
// Trust decays if no interactions occur
const network = new TrustNetwork({
  trustDecayRate: 0.001  // 0.1% per hour
});

// Add an agent
const agent = new Agent({
  id: 'agent-1',
  name: 'Test Agent',
  behavior: 'cooperative'
});
network.addAgent(agent);

// Initial trust
network.calculateTrustScores();
console.log('Initial trust:', agent.trustScore.toFixed(3));

// Simulate 30 days passing (720 hours)
network.applyTrustDecay(720);
network.calculateTrustScores();

console.log('After 30 days:', agent.trustScore.toFixed(3));

// Re-establish trust
network.simulateInteraction('other', 'agent-1', 0.5);
network.calculateTrustScores();

console.log('After interaction:', agent.trustScore.toFixed(3));
```

### Topic 2: Network Visualization

```typescript
import { Visualizer } from './src/visualizer';

// Create and populate network
const network = new TrustNetwork();
// ... add agents and relationships ...

// Render ASCII visualization
console.log(Visualizer.renderNetworkGraph(network));

// Visualize trust propagation
console.log(Visualizer.renderTrustPropagation(network, 10));
```

### Topic 3: Export and Persistence

```typescript
import * as fs from 'fs';

// Export network state
const data = network.export();
const json = JSON.stringify(data, null, 2);

// Save to file
fs.writeFileSync('trust-network-backup.json', json);

// Later, restore
const loaded = JSON.parse(fs.readFileSync('trust-network-backup.json', 'utf-8'));
const restored = TrustNetwork.import(loaded);

console.log('Restored agents:', restored.getAllAgents().length);
```

### Topic 4: Dynamic Networks

```typescript
// Agents can join and leave
const network = new TrustNetwork();

// Initial agents
for (let i = 0; i < 10; i++) {
  const agent = new Agent({
    id: `agent-${i}`,
    name: `Agent ${i}`,
    behavior: 'cooperative'
  });
  network.addAgent(agent);
}

// Simulate churn (agents leaving/joining)
for (let round = 0; round < 10; round++) {
  // Remove a random agent
  const agents = network.getAllAgents();
  const toRemove = agents[Math.floor(Math.random() * agents.length)];
  network.removeAgent(toRemove.id);
  
  // Add a new agent
  const newAgent = new Agent({
    id: `agent-new-${round}`,
    name: `New Agent ${round}`,
    behavior: Math.random() > 0.7 ? 'malicious' : 'cooperative'
  });
  network.addAgent(newAgent);
  
  // Recalculate
  network.calculateTrustScores();
  
  console.log(`Round ${round + 1}: ${network.getAllAgents().length} agents`);
}
```

### Topic 5: Custom Behaviors

```typescript
// Create a custom behavior
class TitForTatAgent extends Agent {
  private partnerHistory: Map<string, boolean> = new Map();
  
  performTask(difficulty: number, partnerId?: string): InteractionResult {
    // If we've interacted before, mirror their behavior
    if (partnerId && this.partnerHistory.has(partnerId)) {
      const lastSuccess = this.partnerHistory.get(partnerId);
      return {
        success: lastSuccess!,
        quality: lastSuccess ? 0.8 : 0.2,
        duration: 100,
        agentId: this.id,
        timestamp: new Date()
      };
    }
    
    // Otherwise, start cooperatively
    return super.performTask(difficulty);
  }
  
  recordInteraction(interaction: Interaction): void {
    this.partnerHistory.set(interaction.partnerId, interaction.success);
    super.recordInteraction(interaction);
  }
}

// Use custom agent
const titForTat = new TitForTatAgent({
  id: 'tft-001',
  name: 'Tit-for-Tat Agent',
  behavior: 'neutral'
});
```

---

## Summary

You've learned:

✅ What trust networks are and why they matter  
✅ How to create agents with different behaviors  
✅ How trust propagates through a network  
✅ How to detect malicious agents  
✅ Real-world applications (AI agents, P2P, supply chain, marketplaces)  
✅ Advanced topics (decay, visualization, persistence, custom behaviors)  

**Next Steps:**

- [ ] Run the demo: `npm run demo`
- [ ] Experiment with different network topologies
- [ ] Implement custom behaviors
- [ ] Visualize trust propagation
- [ ] Apply to your own use case

---

## Additional Resources

- [API Reference](API.md) - Complete API documentation
- [README](README.md) - Project overview
- [PageRank Paper](https://ilpubs.stanford.edu:8090/422/) - Original algorithm
- [Trust Networks Book](https://www.springer.com/gp/book/9781848004340) - Academic reference

---

**Questions? Feedback?**

Open an issue or reach out! This is an educational project, and your feedback helps improve it.

---

*Last updated: 2026-03-22*  
*Tutorial version: 1.0*
