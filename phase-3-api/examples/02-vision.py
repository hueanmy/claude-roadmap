"""Vision — describe an image. Opus 4.7 supports up to 2576px on the long edge.

Two ways to send images:
1. URL (shown here) — Anthropic fetches the image
2. Base64 — embed bytes inline. Use when the image isn't publicly reachable.

Run: uv run phase-3-api/examples/02-vision.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from _shared.client import client

# A public image of the Anthropic logo (or any image URL you want).
IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/280px-PNG_transparency_demonstration_1.png"

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=512,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"type": "url", "url": IMAGE_URL},
                },
                {"type": "text", "text": "Describe this image in 2 sentences."},
            ],
        }
    ],
)

print(response.content[0].text)
