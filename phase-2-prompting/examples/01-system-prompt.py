"""System prompt — sets persona, constraints, and output style.

Compare what happens when you ask the same question with vs without a system prompt.

Run: uv run phase-2-prompting/examples/01-system-prompt.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _shared.client import client

QUESTION = "What's the best way to structure a Python project?"

# Without system prompt — Claude defaults to its general assistant persona.
plain = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=512,
    messages=[{"role": "user", "content": QUESTION}],
)

# With system prompt — narrower persona, terser style, opinionated answers.
opinionated = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=512,
    system=(
        "You are a senior Python engineer with 15 years of experience. "
        "Answer in 3 bullet points max. Be opinionated — recommend ONE approach, "
        "not a list of options. No preamble."
    ),
    messages=[{"role": "user", "content": QUESTION}],
)

print("=== WITHOUT system prompt ===")
print(plain.content[0].text)
print("\n=== WITH system prompt (senior engineer persona) ===")
print(opinionated.content[0].text)
