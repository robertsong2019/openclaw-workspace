# 12-Factor Agents Explorer — Tutorial

This tutorial walks you through building with each agent type, from basic to advanced.

## Prerequisites

- Node.js 18+
- TypeScript knowledge
- `npm install` completed

## Step 1: Hello Agent

Create a file `examples/my-first-agent.ts`:

```typescript
import { MultimodalAgent } from '../src';

async function main() {
  const agent = new MultimodalAgent({
    name: 'hello-agent',
    capabilities: ['text'],
    enableText: true,
    confidenceThreshold: 0.5  // Lower threshold for testing
  });

  // Listen to events
  agent.on('initialized', (data) => console.log('Agent ready:', data.name));
  agent.on('messageAdded', (msg) => console.log(`[${msg.role}] ${msg.content}`));

  await agent.start();

  const response = await agent.process('Hello! Can you help me?');
  console.log('Response:', response);

  await agent.stop();
}

main().catch(console.error);
```

Run it:
```bash
npx ts-node examples/my-first-agent.ts
```

**What's happening:**
1. `MultimodalAgent` extends `BaseAgent`, which sets up event emitters and memory
2. `process()` classifies your input as an intent (question, command, etc.)
3. The agent generates a response based on the classified intent
4. Events fire at each lifecycle stage

## Step 2: Adaptive Learning

The `AdaptiveAgent` learns from feedback. Each interaction is stored as a `LearningExperience`.

```typescript
import { AdaptiveAgent } from '../src';

async function main() {
  const agent = new AdaptiveAgent({
    name: 'learning-agent',
    capabilities: ['pattern_learning'],
    learningRate: 0.15,        // How aggressively to update (0-1)
    forgettingRate: 0.05,      // How fast unused knowledge decays
    maxMemorySize: 100,        // Max experiences to retain
    enableTransferLearning: true
  });

  await agent.start();

  // Teach it something
  let response = await agent.process('How do I deploy a Node.js app?');
  console.log('First response:', response);

  // Give positive feedback (0 = bad, 1 = great)
  await agent.provideFeedback(0.9);

  // Ask something similar — it will use the learned pattern
  response = await agent.process('How do I deploy an Express server?');
  console.log('Learned response:', response);

  // Check how it's doing
  const metrics = agent.getPerformanceMetrics();
  console.log('Performance:', metrics);
  // { totalTasks: 2, successfulTasks: 2, learningEfficiency: 1.0 }

  // See what it has learned
  const knowledge = agent.getKnowledgeSummary();
  console.log(`Knowledge base: ${knowledge.length} items`);

  // Clean up background intervals when done
  agent.clearAllIntervals();
  await agent.stop();
}

main().catch(console.error);
```

**Key concepts:**
- **Experiences** — every input/output pair is recorded
- **Knowledge items** — patterns extracted from successful experiences, with confidence scores
- **Forgetting** — knowledge not used for 7 days decays and is eventually removed
- **Transfer learning** — knowledge from one domain is adapted to related tasks

## Step 3: Multimodal Processing

The `MultimodalAgent` can process text, image, and audio inputs (placeholder implementations included):

```typescript
import { MultimodalAgent, MultimodalInput } from '../src';

async function main() {
  const agent = new MultimodalAgent({
    name: 'multimodal',
    capabilities: ['text', 'image', 'audio'],
    enableVision: true,
    enableAudio: true,
    confidenceThreshold: 0.7
  });

  await agent.start();

  // Process multiple inputs at once
  const inputs: MultimodalInput[] = [
    {
      type: 'text',
      content: 'Analyze this image and audio',
      metadata: { timestamp: new Date() }
    },
    {
      type: 'image',
      content: Buffer.from('...'), // Image data
      metadata: { timestamp: new Date() }
    }
  ];

  const response = await agent.processMultimodal(inputs);
  console.log('Multimodal response:', response);

  // Check intent history
  const history = agent.getIntentHistory();
  console.log(`Processed ${history.length} intents`);

  await agent.stop();
}

main().catch(console.error);
```

**How fusion works:**
1. Each modality is processed independently → separate `Intent` objects
2. `fusePrimaryIntents()` picks the dominant intent
3. `calculateConfidence()` averages and boosts multimodal confidence
4. `fuseEntities()` and `fuseContext()` merge cross-modal data

## Step 4: Collaborative Creation

The `CollaborativeCreationAgent` coordinates multiple agents:

```typescript
import { CollaborativeCreationAgent } from '../src';

async function main() {
  const team = new CollaborativeCreationAgent({
    name: 'creative-team',
    capabilities: ['coordination', 'creation'],
    maxAgents: 5,
    enableQualityControl: true,
    enableInnovationBoost: true,
    protocol: {
      communicationMethod: 'mediated',
      decisionMaking: 'consensus',
      qualityControl: 'hybrid',
      conflictResolution: 'mediation'
    }
  });

  await team.start();

  // The agent automatically:
  // 1. Parses input into a CreativeTask
  // 2. Finds suitable agents (multimodal-expert, adaptive-learner)
  // 3. Creates task segments for each agent
  // 4. Gathers and combines results
  // 5. Runs quality control checks

  const result = await team.process(
    'Write a creative story about AI agents learning to collaborate'
  );
  console.log('Team result:', result);

  // Check team status
  const status = await team.getCollaborationStatus();
  console.log('Available agents:', status.availableAgents);
  console.log('Completed outputs:', status.completedOutputs.length);

  // Spark innovation
  const innovation = await team.requestInnovation();
  console.log('Innovation challenge:', innovation);

  team.clearAllIntervals();
  await team.stop();
}

main().catch(console.error);
```

**Task types recognized:**
- `content_creation` — "write", "create", "generate"
- `code_generation` — "code", "program", "develop"
- `design` — "design", "visual", "creative"
- `research` — research tasks
- `problem_solving` — general problem solving

## Step 5: Custom Agent

Extend `BaseAgent` to create your own:

```typescript
import { BaseAgent, AgentConfig } from '../src';

class MyCustomAgent extends BaseAgent {
  constructor(config: AgentConfig) {
    super(config);
  }

  async process(input: string): Promise<string> {
    // Your logic here
    return `Processed: ${input}`;
  }

  async think(task: string): Promise<string> {
    // Reasoning step
    return `Thinking about: ${task}`;
  }

  async act(action: string): Promise<any> {
    // Execution step
    return { action, result: 'done' };
  }
}

// Use it
const agent = new MyCustomAgent({
  name: 'custom',
  capabilities: ['custom-processing'],
  enableRapidProto: true
});

agent.on('initialized', () => console.log('Custom agent ready!'));
await agent.start();
const result = await agent.process('Hello custom agent');
```

## Event-Driven Patterns

All agents support event-driven workflows:

```typescript
// Chain operations via events
agent.on('messageAdded', async (msg) => {
  if (msg.role === 'user') {
    // Auto-respond to user messages
    const response = await agent.process(msg.content);
    await agent.addMessage('assistant', response);
  }
});

// Monitor state changes
agent.on('contextUpdated', ({ key, value }) => {
  console.log(`Context updated: ${key} = ${value}`);
});
```

## Common Pitfalls

1. **Forgetting to `clearAllIntervals()`** — `AdaptiveAgent` and `CollaborativeCreationAgent` run background timers. Always call `clearAllIntervals()` before stopping, or your process won't exit cleanly.

2. **Low confidence responses** — If the agent returns "I'm not confident enough", lower `confidenceThreshold` or provide more specific input.

3. **AdaptiveAgent not learning** — You must call `provideFeedback()` after responses. Without feedback, all experiences default to score 0.5, and learning is very slow.

4. **CollaborativeCreationAgent no suitable agents** — The agent only has 2 built-in sub-agents. If your task description doesn't match their expertise keywords, no agent will be assigned.

## Extending the Framework

### Add a new modality to MultimodalAgent

Create a processor in `createXxxProcessor()` and add the type to `MultimodalInput.type`.

### Add domain knowledge to AdaptiveAgent

Pre-seed the knowledge base:
```typescript
const agent = new AdaptiveAgent(config);
// After construction, directly populate knowledge if needed
```

### Add specialized agents to CollaborativeCreationAgent

Register new agents in `createSpecializedAgents()` with matching expertise tags.

## Next Steps

- Run `npm run examples` to see the comprehensive demo
- Read the source code in `src/agents/` — it's well-documented and ~1500 lines total
- Check tests in `tests/` for more usage patterns
