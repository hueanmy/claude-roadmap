# Phase 3 — API Integration

> Cách gọi Anthropic API: SDK, streaming, vision, batches, error handling.

## Sub-topics

- [ ] **SDK (Python / JS)** — `anthropic` (Python), `@anthropic-ai/sdk` (TS). Auto retry, typed errors
- [ ] **Messages API** — `client.messages.create()` — endpoint duy nhất cho mọi text/vision/tool call
- [ ] **Streaming** — `client.messages.stream()` cho UX real-time. **Bắt buộc khi `max_tokens > ~16K`**
- [ ] **Batch API** — async, 50% giá. Cho job không cần realtime (label data, bulk classify...)
- [ ] **Vision / Multimodal** — Opus 4.7 hỗ trợ ảnh tới 2576px (high-res native)
- [ ] **PDF & documents** — gửi PDF base64 hoặc qua Files API
- [ ] **Rate limits** — RPM / TPM / TPD. SDK auto-retry 429 với exponential backoff
- [ ] **Error handling** — typed exceptions: `AuthenticationError`, `RateLimitError`, `BadRequestError`...

## Examples

- [01-streaming.py](./examples/01-streaming.py) — stream tokens real-time
- [02-vision.py](./examples/02-vision.py) — phân tích ảnh từ URL
- [03-error-handling.py](./examples/03-error-handling.py) — xử lý các loại error đúng cách

## Tài liệu chính chủ

- [Streaming](https://platform.claude.com/docs/en/build-with-claude/streaming)
- [Vision](https://platform.claude.com/docs/en/build-with-claude/vision)
- [Error codes](https://platform.claude.com/docs/en/api/errors)
- [Rate limits](https://platform.claude.com/docs/en/api/rate-limits)

## Notes của tôi

> ___
