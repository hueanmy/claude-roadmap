"""Tool calling — Claude decides to call our `get_weather` function.

The flow:
  1. We send tool definitions + user message.
  2. Claude responds with a `tool_use` block (it doesn't actually run the tool).
  3. We execute the tool ourselves and send the result back as a `tool_result`.
  4. Claude generates the final natural-language answer.

Run: uv run phase-4-tools-agents/examples/01-tool-calling.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _shared.client import client


def get_weather(location: str) -> str:
    """Pretend to call a weather API. In reality just return mock data."""
    return f"72°F and sunny in {location}"


tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a city. Use ONLY when user asks about weather.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name, e.g. 'San Francisco' or 'Hanoi'",
                }
            },
            "required": ["location"],
        },
    }
]

messages = [{"role": "user", "content": "What's the weather in Hanoi right now?"}]

# Round 1: Claude decides to call the tool.
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    tools=tools,
    messages=messages,
)

print(f"Round 1 stop_reason: {response.stop_reason}")  # "tool_use"

# Find the tool_use block, execute the tool, send the result back.
for block in response.content:
    if block.type == "tool_use":
        print(f"Claude wants to call: {block.name}({block.input})")
        result = get_weather(**block.input)

        # Round 2: append assistant turn + tool_result, ask Claude to wrap up.
        messages.append({"role": "assistant", "content": response.content})
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    }
                ],
            }
        )

final = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    tools=tools,
    messages=messages,
)

for block in final.content:
    if block.type == "text":
        print(f"\nFinal answer: {block.text}")
