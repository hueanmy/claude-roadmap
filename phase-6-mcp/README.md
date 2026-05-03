# Phase 6 — Model Context Protocol (MCP)

> MCP = giao thức chuẩn để LLM (Claude, GPT...) kết nối với tools / data sources external. Anthropic mở source 2024-11.

## Sub-topics

- [ ] **MCP architecture** — client (Claude Code, Claude Desktop) ↔ server (database, API, file system...)
- [ ] **MCP servers** — process expose tools/resources/prompts qua JSON-RPC
- [ ] **MCP clients** — apps gọi server (Claude Code có MCP support built-in)
- [ ] **Build custom MCP** — viết server bằng Python (`mcp` package) hoặc TS
- [ ] **MCP + Claude Code** — `.mcp.json` config, `/mcp` slash command để debug
- [ ] **Stdio vs SSE transport** — stdio: server chạy local subprocess. SSE: server qua HTTP, remote
- [ ] **Auth & security** — OAuth cho remote servers, env var cho local

## Examples

- [01-stdio-mcp-server/](./examples/01-stdio-mcp-server/) — MCP server siêu nhỏ với 1 tool (`get_time`)

## Setup

```bash
# Install MCP deps (optional group)
uv sync --group mcp
```

## Tài liệu chính chủ

- [MCP introduction](https://modelcontextprotocol.io/introduction)
- [Build a server (Python)](https://modelcontextprotocol.io/quickstart/server)
- [MCP in Claude Code](https://docs.claude.com/en/docs/claude-code/mcp)

## Notes của tôi

> ___
