"""Hello Claude — the smallest possible API call.

Run: uv run phase-1-foundation/examples/01-hello-claude.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _shared.client import client

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello! In one sentence, what is Claude?"},
    ],
)

# response.content is a list of content blocks. For plain text replies it's
# a single text block — but always iterate, never assume content[0].text.
for block in response.content:
    if block.type == "text":
        print(block.text)

# Inspect the usage object to learn what each call costs.
print(f"\n--- usage: {response.usage.input_tokens} in / {response.usage.output_tokens} out")
