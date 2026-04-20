# 12-Factor Agents Explorer

A TypeScript framework for building AI agents with **multimodal understanding**, **adaptive learning**, and **collaborative creation** capabilities. Built around the [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) methodology.

## Architecture

```
┌─────────────────────────────────────────────┐
│           AgentFramework (entry)             │
├─────────────────────────────────────────────┤
│                  BaseAgent                   │
│  ┌──────────┬──────────┬──────────────────┐  │
│  │Multimodal│ Adaptive │  Collaborative   │  │
│  │  Agent   │  Agent   │  Creation Agent  │  │
│  └──────────┴──────────┴──────────────────┘  │
└─────────────────────────────────────────────┘
```

## Agent Types

### BaseAgent
Abstract foundation. Provides:
- Event-driven architecture (`EventEmitter`)
- Message history and context storage (`AgentMemory`)
- Lifecycle management (`start`/`stop`)
- Rapid prototyping mode

### MultimodalAgent
Processes input across text, image, and audio modalities:
- **Intent classification** — question, command, creation, analysis
- **Entity extraction** — keywords, objects, scenes, emotions
- **Multimodal fusion** — combines insights from multiple input types
- **Confidence thresholding** — configurable minimum confidence (default 0.7)

### AdaptiveAgent
Learns from experience and improves over time:
- **Pattern recognition** — identifies successful response patterns
- **Knowledge management** — stores, consolidates, and applies knowledge items
- **Forgetting mechanism** — decays unused knowledge over 7 days
- **Transfer learning** — applies knowledge across different task domains
- **Feedback loop** — `provideFeedback(0-1)` to rate responses

### CollaborativeCreationAgent
Orchestrates multiple agents on creative tasks:
- **Task delegation** — parses input into `CreativeTask`, assigns to suitable agents
- **Quality control** — coherence, completeness, and creativity checks
- **Conflict resolution** — voting, mediation, or escalation strategies
- **Innovation prompts** — injects creative challenges to boost novelty

## Quick Start

```bash
# Install dependencies
npm install

# Development
npm run dev

# Build
npm run build

# Run tests
npm test

# Run comprehensive demo
npm run examples
```

## Usage

```typescript
import {
  MultimodalAgent,
  AdaptiveAgent,
  CollaborativeCreationAgent
} from './src';

// 1. Multimodal understanding
const agent = new MultimodalAgent({
  name: 'my-agent',
  capabilities: ['text', 'image'],
  enableVision: true,
  confidenceThreshold: 0.8
});

const response = await agent.process('What is in this image?');

// 2. Adaptive learning
const learner = new AdaptiveAgent({
  name: 'learner',
  capabilities: ['pattern_learning'],
  learningRate: 0.1,
  maxMemorySize: 500
});

await learner.process('Help me with task A');
await learner.provideFeedback(0.9); // Rate the response

// 3. Collaborative creation
const team = new CollaborativeCreationAgent({
  name: 'team-lead',
  capabilities: ['coordination'],
  maxAgents: 5,
  enableQualityControl: true
});

const result = await team.process('Write a creative story about AI');
```

## API Reference

### BaseAgent
| Method | Description |
|--------|-------------|
| `process(input: string)` | Process input (abstract, implemented by subclasses) |
| `think(task: string)` | Reasoning step (abstract) |
| `act(action: string)` | Execute action (abstract) |
| `start()` / `stop()` | Lifecycle control |
| `addMessage(role, content)` | Add to conversation history |
| `getContext(key)` / `setContext(key, value)` | Key-value context store |
| `clearMemory()` | Reset messages and context |
| `getState()` | Get current agent state |
| `getCapabilities()` | List configured capabilities |

### AdaptiveAgent (extends BaseAgent)
| Method | Description |
|--------|-------------|
| `provideFeedback(score: 0-1)` | Rate the last response for learning |
| `getPerformanceMetrics()` | Get success rate, avg response time, learning efficiency |
| `getKnowledgeSummary()` | Top 20 knowledge items by confidence |
| `clearAllIntervals()` | Stop background learning processes |

### CollaborativeCreationAgent (extends BaseAgent)
| Method | Description |
|--------|-------------|
| `getCollaborationStatus()` | Active tasks, available agents, completed outputs |
| `requestInnovation()` | Generate an innovation challenge prompt |
| `clearAllIntervals()` | Stop background coordination processes |

## Configuration

All agents share `AgentConfig`:
```typescript
interface AgentConfig {
  name: string;
  model?: string;
  capabilities: string[];
  memorySize?: number;
  enableRapidProto?: boolean;
}
```

Agent-specific configs: `MultimodalAgentConfig`, `AdaptiveConfig`, `CollaborativeConfig`.

## Events

All agents emit events via `EventEmitter`:
- `initialized` — agent setup complete
- `started` / `stopped` — lifecycle changes
- `messageAdded` — new message in history
- `contextUpdated` — context key updated
- `memoryCleared` — memory reset
- `rapidProtoEnabled` — rapid prototyping mode activated

## Project Structure

```
src/
├── index.ts              # Entry point, AgentFramework class
├── agents/
│   ├── BaseAgent.ts            # Abstract base (119 lines)
│   ├── MultimodalAgent.ts      # Multimodal processing (340 lines)
│   ├── AdaptiveAgent.ts        # Learning & adaptation (463 lines)
│   └── CollaborativeCreationAgent.ts  # Multi-agent coordination (537 lines)
examples/
└── comprehensive-demo.ts       # Full framework demo
tests/                          # Jest test suite
```

## License

MIT
