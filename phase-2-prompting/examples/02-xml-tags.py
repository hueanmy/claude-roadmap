"""XML tags — structure complex prompts so Claude knows what's what.

Claude is trained to recognize XML-tagged sections. Use them when your prompt mixes
context, task, examples, and constraints.

Run: uv run phase-2-prompting/examples/02-xml-tags.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _shared.client import client

prompt = """\
<context>
You are reviewing customer support tickets for a SaaS product.
The product has 3 plans: Free, Pro ($29/mo), Enterprise (custom pricing).
</context>

<task>
Classify the ticket below into ONE of: bug, billing, feature_request, churn_risk.
Output JSON only, no preamble.
</task>

<examples>
<example>
<ticket>"App crashes when I upload a CSV over 5MB"</ticket>
<output>{"category": "bug", "confidence": "high"}</output>
</example>
<example>
<ticket>"Cancel my subscription, found a cheaper alternative"</ticket>
<output>{"category": "churn_risk", "confidence": "high"}</output>
</example>
</examples>

<ticket>
Hi, I've been a Pro user for 8 months. The new dashboard is confusing —
I can't find where to export reports. Considering switching to Notion.
</ticket>
"""

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=256,
    messages=[{"role": "user", "content": prompt}],
)

print(response.content[0].text)
