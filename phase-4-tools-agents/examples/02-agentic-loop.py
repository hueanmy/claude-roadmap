"""Agentic loop — Claude can call tools multiple times until it decides to stop.

The pattern: keep calling the API in a `while True:` loop, executing tool_use blocks
and feeding tool_results back, until `stop_reason == "end_turn"`.

Run: uv run phase-4-tools-agents/examples/02-agentic-loop.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _shared.client import client


# Two trivial tools — pretend they hit a real DB / API.
def list_users() -> str:
    return json.dumps([{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}])


def get_user_orders(user_id: int) -> str:
    orders = {1: ["MacBook", "Mouse"], 2: ["Keyboard"]}
    return json.dumps(orders.get(user_id, []))


TOOLS = [
    {
        "name": "list_users",
        "description": "List all users in the system.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_user_orders",
        "description": "Get orders for a specific user by ID.",
        "input_schema": {
            "type": "object",
            "properties": {"user_id": {"type": "integer"}},
            "required": ["user_id"],
        },
    },
]


def run_tool(name: str, args: dict) -> str:
    if name == "list_users":
        return list_users()
    if name == "get_user_orders":
        return get_user_orders(**args)
    return f"Unknown tool: {name}"


messages = [
    {"role": "user", "content": "What did Alice buy? Use the tools to find out."}
]

# The loop: keep going until Claude says it's done.
for iteration in range(10):  # safety cap on iterations
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        tools=TOOLS,
        messages=messages,
    )

    print(f"\n--- Iteration {iteration + 1}, stop_reason: {response.stop_reason} ---")

    # Print any text blocks Claude produced (its reasoning between tool calls).
    for block in response.content:
        if block.type == "text":
            print(f"Claude: {block.text}")

    if response.stop_reason == "end_turn":
        break

    # Append the assistant turn (preserves tool_use blocks).
    messages.append({"role": "assistant", "content": response.content})

    # Execute every tool_use in this turn — there may be more than one.
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            print(f"  → calling {block.name}({block.input})")
            result = run_tool(block.name, block.input)
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                }
            )

    messages.append({"role": "user", "content": tool_results})
