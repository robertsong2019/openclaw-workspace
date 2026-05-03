# OpenClaw MCP Server

> Expose OpenClaw capabilities (memory, search, status) via the [Model Context Protocol](https://modelcontextprotocol.io/).

## Overview

An MCP Server implementation using **Streamable HTTP** transport, allowing any MCP-compatible client (Claude Desktop, Cursor, etc.) to interact with Catalyst's workspace.

```
MCP Client → Streamable HTTP → openclaw-mcp-server → OpenClaw APIs
```

## Tools Provided

| Tool | Description |
|------|-------------|
| `query_memory` | Search Catalyst's memory for past work and decisions |
| `web_search` | Search the web for latest information |
| `get_status` | Get system status: active projects, test coverage |

## Quick Start

```bash
# Install dependencies
npm install

# Development (with tsx)
npm run dev

# Production build + run
npm run build && npm start
```

Server starts at `http://localhost:3001/mcp` by default. Set `PORT` env var to change.

## Connecting a Client

Configure your MCP client to connect via Streamable HTTP:

```json
{
  "mcpServers": {
    "openclaw": {
      "url": "http://localhost:3001/mcp",
      "transport": "streamable-http"
    }
  }
}
```

## Architecture

- **Transport**: `@modelcontextprotocol/sdk` StreamableHTTPServerTransport (stateful sessions)
- **Schema**: Zod for input validation
- **Runtime**: Node.js 22+ with ESM

## Project Structure

```
src/
  index.ts    # Server entry, tool definitions, HTTP handler
dist/         # Compiled JS output
test/         # Test files
```

## Status

🚧 MVP — Tool handlers return mock data. Production integration with actual OpenClaw APIs is pending.

## License

MIT

---

*Part of the [OpenClaw workspace](https://github.com/robertsong2019)*
