"""Basic evals — score Claude's output against a golden dataset using an LLM judge.

The pattern:
  1. Define test cases (input + expected criteria — NOT exact match).
  2. Run model under test on each input.
  3. Use a stronger model to judge whether the output meets criteria.
  4. Aggregate pass rate.

This is the simplest eval loop — production setups add: caching, parallelism, regression
diff vs previous run, cost tracking, human review queue for low-confidence judgments.

Run: uv run phase-7-advanced/examples/01-evals-basic.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _shared.client import client

MODEL_UNDER_TEST = "claude-haiku-4-5"  # cheap model — what we're evaluating
JUDGE_MODEL = "claude-opus-4-7"  # smart model — grades the cheap one's output

# Golden dataset — input + criteria (not exact expected output).
TEST_CASES = [
    {
        "input": "What's 17 * 23?",
        "criteria": "Answer must include the number 391. Other commentary OK.",
    },
    {
        "input": "Translate 'good morning' to Vietnamese.",
        "criteria": "Must include 'chào buổi sáng'. Capitalization OK either way.",
    },
    {
        "input": "Write a python function to reverse a string in 1 line.",
        "criteria": "Must contain valid Python code that reverses a string. Slice [::-1] is the canonical answer.",
    },
]


def get_model_output(prompt: str) -> str:
    response = client.messages.create(
        model=MODEL_UNDER_TEST,
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def judge(prompt: str, output: str, criteria: str) -> tuple[bool, str]:
    """Use the judge model to grade the output. Returns (passed, reasoning)."""
    judge_prompt = f"""\
You are grading a model's output against criteria. Be strict but fair.

<input>
{prompt}
</input>

<output>
{output}
</output>

<criteria>
{criteria}
</criteria>

Respond with EXACTLY this JSON, no preamble:
{{"passed": true|false, "reasoning": "<one sentence>"}}
"""
    response = client.messages.create(
        model=JUDGE_MODEL,
        max_tokens=256,
        messages=[{"role": "user", "content": judge_prompt}],
    )
    import json

    parsed = json.loads(response.content[0].text)
    return parsed["passed"], parsed["reasoning"]


passes = 0
for i, case in enumerate(TEST_CASES, 1):
    output = get_model_output(case["input"])
    ok, reason = judge(case["input"], output, case["criteria"])
    status = "✓" if ok else "✗"
    print(f"[{status}] Test {i}: {case['input'][:50]}")
    print(f"    output: {output[:80]}")
    print(f"    judge:  {reason}")
    if ok:
        passes += 1

print(f"\n=== {passes}/{len(TEST_CASES)} passed ===")
