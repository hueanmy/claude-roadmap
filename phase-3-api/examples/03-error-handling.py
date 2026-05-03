"""Error handling — use typed exceptions, never string-match error messages.

The SDK retries 429 / 5xx automatically with exponential backoff (max_retries=2).
For custom retry logic, increase max_retries when constructing the client.

Run: uv run phase-3-api/examples/03-error-handling.py
"""
import sys
from pathlib import Path

import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _shared.client import client

try:
    response = client.messages.create(
        model="claude-opus-4-7",
        # Intentionally bad: max_tokens must be a positive int. This triggers a 400.
        max_tokens=0,
        messages=[{"role": "user", "content": "hello"}],
    )
    print(response.content[0].text)

# Order: most specific to least specific. All extend anthropic.APIError.
except anthropic.BadRequestError as e:
    print(f"Bad request (400): {e.message}")
except anthropic.AuthenticationError:
    print("Invalid API key — check your .env")
except anthropic.RateLimitError as e:
    print(f"Rate limited (429): retry after {e.response.headers.get('retry-after')}s")
except anthropic.APIError as e:
    # Catch-all for anything else (500, network errors, etc.)
    print(f"API error {e.status_code}: {e.message}")
