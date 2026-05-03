# 01 — Stdio MCP server (hello world)

Một MCP server tối giản expose 1 tool `get_time`.

## Run

1. Cài dep nhóm `mcp`:
   ```bash
   uv sync --group mcp
   ```

2. Tạo file `.mcp.json` ở root repo này (hoặc bất kỳ project nào):
   ```json
   {
     "mcpServers": {
       "time-demo": {
         "command": "uv",
         "args": [
           "run",
           "--group", "mcp",
           "python",
           "phase-6-mcp/examples/01-stdio-mcp-server/server.py"
         ]
       }
     }
   }
   ```

3. Mở Claude Code ở root repo này → gõ `/mcp` → bạn thấy `time-demo` ở trạng thái connected.
4. Hỏi Claude: "What time is it in UTC?" → nó sẽ gọi tool `get_time`.

## Học gì từ example này

- **FastMCP decorator** (`@mcp.tool()`) auto generate JSON schema từ Python type hints
- **Stdio transport** — Claude Code spawn server thành subprocess, communicate qua stdin/stdout
- **Docstring = tool description** — quan trọng, Claude dùng để quyết định khi nào gọi tool

## Bước tiếp theo

- Thêm tool thứ 2 trả về timezone list
- Convert sang resource (data Claude đọc, không phải gọi)
- Add prompt template
