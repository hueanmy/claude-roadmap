"""Minimal MCP server — exposes one tool: `get_time`.

This is the "hello world" of MCP. Run it as a subprocess of any MCP client
(Claude Code, Claude Desktop, etc.).

Wire it up in Claude Code by adding to your project's `.mcp.json`:

  {
    "mcpServers": {
      "time-demo": {
        "command": "uv",
        "args": ["run", "python", "phase-6-mcp/examples/01-stdio-mcp-server/server.py"]
      }
    }
  }

Then: claude → /mcp → see `time-demo` connected → ask "what time is it?"

Run standalone (it'll wait on stdin for JSON-RPC, that's normal):
  uv run --group mcp python phase-6-mcp/examples/01-stdio-mcp-server/server.py
"""
from datetime import datetime

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("time-demo")


@mcp.tool()
def get_time(timezone: str = "UTC") -> str:
    """Return the current time. Pass an IANA timezone like 'Asia/Ho_Chi_Minh'."""
    # Real impl would respect the timezone arg via zoneinfo. Keep it simple here.
    return f"Current time ({timezone}): {datetime.utcnow().isoformat()}Z"


if __name__ == "__main__":
    # FastMCP defaults to stdio transport — perfect for local subprocess use.
    mcp.run()
