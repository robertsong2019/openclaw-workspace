# openclaw-langgraph-bridge

Bridge [OpenClaw](https://github.com/nicepkg/openclaw) agent execution to [LangGraph.js](https://github.com/langchain-ai/langgraphjs) workflow nodes.

## Install

```bash
npm install openclaw-langgraph-bridge @langchain/langgraph zod
```

## Usage

```ts
import { createOpenClawNode, sequentialRouter } from "openclaw-langgraph-bridge";
import { OpenClawClient } from "openclaw-langgraph-bridge";
import { StateGraph, StateSchema, ReducedValue, MessagesValue, START, END } from "@langchain/langgraph";
import { z } from "zod";

// 1. Define state
const State = new StateSchema({
  messages: MessagesValue,
  task: z.string(),
  researcherResult: z.string().optional(),
  analystResult: z.string().optional(),
  writerResult: z.string().optional(),
  completedSteps: new ReducedValue(
    z.array(z.string()).default(() => []),
    { inputSchema: z.string(), reducer: (c, n) => [...c, n] }
  ),
});

// 2. Create nodes
const researcher = createOpenClawNode({
  name: "researcher",
  systemPrompt: "Research: {input}",
  executor: async (task) => `Research results for: ${task}`,
});

const analyst = createOpenClawNode({
  name: "analyst",
  systemPrompt: "Analyze: {input}",
  executor: async (task) => `Analysis of: ${task}`,
});

// 3. Build workflow
const roles = ["researcher", "analyst", "writer"];
const router = sequentialRouter(roles);

const graph = new StateGraph(State)
  .addNode("researcher", researcher)
  .addNode("analyst", analyst)
  .addNode("writer", writer)
  .addConditionalEdges(START, router, [...roles, END])
  .addConditionalEdges("researcher", router, [...roles, END])
  .addConditionalEdges("analyst", router, [...roles, END])
  .addEdge("writer", END)
  .compile();

// 4. Run
const result = await graph.invoke(
  { messages: [{ role: "user", content: "AI trends 2026" }], task: "AI trends 2026" },
  { configurable: { thread_id: crypto.randomUUID() } }
);
```

## OpenClaw Gateway Integration

```ts
const client = new OpenClawClient({ baseUrl: "http://localhost:3000" });

const realResearcher = createOpenClawNode({
  name: "researcher",
  systemPrompt: "Research: {input}",
  executor: client.executor("You are a research assistant"),
});
```

## API

### `createOpenClawNode(config)`
Creates a LangGraph.js node function from an OpenClaw-style agent config.

### `OpenClawClient`
HTTP client for OpenClaw Gateway. Methods: `spawn()`, `executor()`.

### `sequentialRouter(steps)`
Returns a router function that visits steps in order, skipping completed ones.

### `conditionalRouter(field, mapping, fallback)`
Routes based on a state field value.

## License

MIT
