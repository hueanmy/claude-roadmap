"""Streaming — print tokens as they arrive instead of waiting for the full reply.

Required when max_tokens is large (anything > ~16K) to avoid HTTP timeouts.
Also better UX for chat — user sees response immediately.

Run: uv run phase-3-api/examples/01-streaming.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _shared.client import client

with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    messages=[
        {"role": "user", "content": "Write a haiku about prompt caching, then explain it."}
    ],
) as stream:
    # text_stream yields just the text deltas — simplest path.
    # For raw events (thinking, tool_use, etc.), iterate stream itself instead.
    for text in stream.text_stream:
        print(text, end="", flush=True)

    # Always grab the final message — has stop_reason + usage info.
    final = stream.get_final_message()

print(f"\n\n--- stop_reason: {final.stop_reason}")
print(f"--- usage: {final.usage.input_tokens} in / {final.usage.output_tokens} out")
