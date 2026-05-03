"""Prompt caching — cache a long prefix once, query it many times at ~10% cost.

Cache hits are visible in `usage.cache_read_input_tokens`. The first request writes
the cache (~1.25x cost), subsequent requests within 5 minutes read it (~0.1x cost).

Run twice in quick succession:
  uv run phase-2-prompting/examples/03-prompt-caching.py

Run #1: cache_creation_input_tokens > 0, cache_read_input_tokens = 0
Run #2: cache_creation_input_tokens = 0, cache_read_input_tokens > 0
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _shared.client import client

# Imagine this is a long doc — API reference, codebase, contract, whatever.
# The minimum cacheable prefix on Sonnet 4.6 is 2048 tokens, so we pad to be safe.
LONG_DOC = (
    "ANTHROPIC API CHEAT SHEET\n"
    "=========================\n\n"
    "Endpoint: POST /v1/messages\n"
    "Required fields: model, max_tokens, messages\n"
    "...\n"
    + "Filler line to push past the 2048-token cache minimum. " * 200
)

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=256,
    system=[
        {
            "type": "text",
            "text": LONG_DOC,
            # cache_control marks this block as a cache breakpoint.
            # Everything before (none here) and including it gets cached.
            "cache_control": {"type": "ephemeral"},
        }
    ],
    messages=[
        {"role": "user", "content": "What's the endpoint? Answer in 5 words or less."}
    ],
)

print(response.content[0].text)
print(
    f"\n--- usage:"
    f"\n  input_tokens (uncached):       {response.usage.input_tokens}"
    f"\n  cache_creation_input_tokens:   {response.usage.cache_creation_input_tokens}"
    f"\n  cache_read_input_tokens:       {response.usage.cache_read_input_tokens}"
)
