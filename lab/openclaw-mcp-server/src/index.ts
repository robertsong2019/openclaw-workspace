import { randomUUID } from "node:crypto";
import { createServer } from "node:http";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";

const server = new McpServer({
  name: "openclaw-mcp-server",
  version: "0.1.0",
});

// Tool 1: query_memory
server.registerTool(
  "query_memory",
  {
    description:
      "Search Catalyst's memory for relevant context about past work and decisions.",
    inputSchema: {
      query: z.string().describe("Search query"),
      limit: z.number().optional().default(5).describe("Max results"),
    },
  },
  async ({ query, limit }) => {
    // MVP: mock results. Production: call memory_search API
    const results = [
      { score: 0.95, text: `Memory match for "${query}": AMS v1.0-dev has 640/640 tests passing.` },
      { score: 0.82, text: `Related: agent-task-cli at 380/380 tests, zero rollback rate maintained.` },
    ].slice(0, limit);
    return {
      content: results.map((r) => ({ type: "text" as const, text: `[${r.score}] ${r.text}` })),
    };
  }
);

// Tool 2: web_search
server.registerTool(
  "web_search",
  {
    description: "Search the web for latest information on a topic.",
    inputSchema: {
      query: z.string().describe("Search query"),
      count: z.number().optional().default(5).describe("Number of results"),
    },
  },
  async ({ query, count }) => {
    // MVP: mock. Production: call tavily_search
    return {
      content: [
        {
          type: "text" as const,
          text: `Web search results for "${query}" (top ${count}):\n1. Example result from tavily...\n2. Another result...`,
        },
      ],
    };
  }
);

// Tool 3: get_status
server.registerTool(
  "get_status",
  {
    description: "Get current system status including active projects and test coverage.",
    inputSchema: {},
  },
  async () => {
    const status = {
      projects: {
        ams: { tests: "640/640", phase: "v1.0-dev" },
        "agent-task-cli": { tests: "380/380" },
        "prompt-router": { tests: "34/34" },
      },
      autoresearch: { rollbackRate: "0%", streakDays: 30 },
      timestamp: new Date().toISOString(),
    };
    return {
      content: [{ type: "text" as const, text: JSON.stringify(status, null, 2) }],
    };
  }
);

// Streamable HTTP transport (stateful mode)
const transport = new StreamableHTTPServerTransport({
  sessionIdGenerator: () => randomUUID(),
});

await server.connect(transport);

const httpServer = createServer(async (req, res) => {
  // Collect request body
  const chunks: Buffer[] = [];
  for await (const chunk of req) chunks.push(chunk);
  const body = Buffer.concat(chunks).toString("utf-8");
  let parsed;
  try {
    parsed = JSON.parse(body);
  } catch {
    parsed = undefined;
  }
  await transport.handleRequest(req, res, parsed);
});

const PORT = process.env.PORT ? parseInt(process.env.PORT) : 3001;
httpServer.listen(PORT, () => {
  console.log(`🧪 OpenClaw MCP Server running on http://localhost:${PORT}/mcp`);
  console.log(`   Transport: Streamable HTTP (stateful)`);
  console.log(`   Tools: query_memory, web_search, get_status`);
});
