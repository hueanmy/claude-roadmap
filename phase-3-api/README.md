# Phase 3 — API Integration

> Cách thực sự gọi Anthropic API: SDK, streaming, vision, batches, error handling. Phase này là kỹ năng plumbing — không sexy nhưng thiếu thì app crash trong prod.

## Sub-topics

### - [ ] SDK (Python / JS / Go / Java / Ruby / C# / PHP)

Anthropic ship SDK chính chủ cho 7 ngôn ngữ, generated từ OpenAPI spec → field names map 1:1. Python (`anthropic`) và TypeScript (`@anthropic-ai/sdk`) là 2 SDK đầy đủ feature nhất, support tool runner, MCP helpers, managed agents beta.

**Tại sao matter:** Đừng tự code raw HTTP nếu ngôn ngữ có SDK. SDK auto retry 429/5xx với exponential backoff, typed exceptions, streaming helpers. Tự viết = reinvent wheel + bugs.

**Học gì cụ thể:**
- Init: `client = Anthropic()` auto đọc `ANTHROPIC_API_KEY` từ env
- `client.messages.create(...)` cho non-stream, `client.messages.stream(...)` cho streaming
- `client.beta.*` namespace cho features beta (tool runner, managed agents, files API)
- Cấu hình retry: `Anthropic(max_retries=3, timeout=60.0)`
- Khi nào dùng raw HTTP: shell script, ngôn ngữ không có SDK (Rust, Swift, Elixir...)

**Refs:** [Python SDK](https://github.com/anthropics/anthropic-sdk-python) · [TypeScript SDK](https://github.com/anthropics/anthropic-sdk-typescript)

---

### - [ ] Messages API

Endpoint duy nhất cho mọi request: `POST /v1/messages`. Tools, vision, structured outputs, thinking, caching — tất cả là feature của endpoint này, không phải endpoint riêng.

**Tại sao matter:** Nhiều người mới tưởng có `chat`/`tools`/`vision` endpoint riêng (như OpenAI cũ). Hiểu Anthropic thiết kế đơn giản hơn: 1 endpoint, parameters làm phân biệt feature.

**Học gì cụ thể:**
- Required params: `model`, `max_tokens`, `messages`
- Optional: `system`, `tools`, `tool_choice`, `temperature` (legacy), `thinking`, `output_config`, `cache_control`
- Messages array shape: `[{"role": "user|assistant", "content": "..."}]`
- `content` có thể là string đơn (text only) hoặc array of blocks (multimodal, tool_use, tool_result)
- Stateless — gửi full history mỗi request, không có session ID

**Refs:** [Messages API reference](https://platform.claude.com/docs/en/api/messages)

---

### - [ ] Streaming

`client.messages.stream(...)` trả về Server-Sent Events thay vì wait full response. Token stream về như typing → UX real-time cho chat. **Bắt buộc khi `max_tokens > ~16K`** vì non-stream sẽ hit HTTP timeout.

**Tại sao matter:** Non-stream với `max_tokens=64000` sẽ timeout sau 600s — request tốn rồi nhưng user không nhận được gì. Stream xử lý case này tự nhiên: gửi token ngay khi sinh ra, không có "wait for completion".

**Học gì cụ thể:**
- Python: `with client.messages.stream(...) as stream:` (context manager auto-close)
- Iterate `stream.text_stream` cho text only, hoặc `stream` raw cho mọi event type
- Event types: `message_start`, `content_block_start/delta/stop`, `message_delta`, `message_stop`
- Always call `stream.get_final_message()` cuối để lấy stop_reason + usage
- TypeScript: `stream.on("text", cb)` + `stream.finalMessage()`, **đừng** wrap trong `new Promise()`

**Refs:** [Streaming](https://platform.claude.com/docs/en/build-with-claude/streaming) · example: [`examples/01-streaming.py`](./examples/01-streaming.py)

---

### - [ ] Batch API

`POST /v1/messages/batches` — async, **50% giá**, cho job không cần realtime. Up to 100K requests / 256MB per batch. Most batches done within 1h, max 24h. Results available 29 ngày.

**Tại sao matter:** Cho task như: label dataset 10K rows, extract data từ 5K PDFs, generate embeddings... batch tiết kiệm $$$. Đừng dùng streaming API cho batch processing — đắt 2x.

**Học gì cụ thể:**
- `client.messages.batches.create(requests=[...])` với mỗi request có `custom_id` để map result
- Poll status: `client.messages.batches.retrieve(batch_id)` cho tới `processing_status == "ended"`
- Stream results: `client.messages.batches.results(batch_id)` — yields `{custom_id, result}`
- Result types: `succeeded` / `errored` / `expired` / `canceled`
- Cancel mid-flight: `client.messages.batches.cancel(batch_id)`

**Refs:** [Batch API](https://platform.claude.com/docs/en/build-with-claude/batch-processing)

---

### - [ ] Vision / Multimodal

Claude xử lý ảnh native. **Opus 4.7** support **2576px** trên cạnh dài (high-res native, gấp ~1.6x Opus 4.6 max 1568px). Ảnh format: JPEG, PNG, GIF, WebP. Max 5 ảnh / request, max 100 pages PDF.

**Tại sao matter:** Vision use case mạnh: screenshot → code, sơ đồ → markdown, biên lai → JSON, document understanding, computer use agent. Opus 4.7 bounding box accuracy đủ để build computer use agent precision cao.

**Học gì cụ thể:**
- 2 cách gửi: URL (Anthropic fetch) hoặc base64 (`{"type": "base64", "media_type": "image/png", "data": "..."}`)
- Image cost: full-res Opus 4.7 ≈ 4784 token / image (gấp 3x Opus 4.6) — downsample nếu cần
- Coords trả về match 1:1 pixels, không cần scale math (4.7 only)
- Beta header KHÔNG cần — high-res automatic trên 4.7
- Token count khác PDF — PDF count theo page

**Refs:** [Vision](https://platform.claude.com/docs/en/build-with-claude/vision) · example: [`examples/02-vision.py`](./examples/02-vision.py)

---

### - [ ] PDF & documents

Claude xử lý PDF native qua content block `type: document`. Có thể gửi inline base64, URL, hoặc qua Files API (upload trước, reference bằng `file_id`). Limits: 100 pages, 32MB.

**Tại sao matter:** Skip OCR pipeline phức tạp — Claude đọc PDF như đọc ảnh + text mixed. Use case: contract analysis, research paper Q&A, invoice extraction, slide deck review.

**Học gì cụ thể:**
- Block format: `{"type": "document", "source": {"type": "base64|url|file", ...}}`
- Citations enabled: `"citations": {"enabled": true}` — Claude trả về reference với page number
- Files API recommend cho file dùng nhiều lần (avoid re-upload)
- Cache breakpoint trên document block → cache cả PDF, query nhiều lần rẻ hơn

**Refs:** [PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support) · [Files API](https://platform.claude.com/docs/en/build-with-claude/files)

---

### - [ ] Rate limits

Mỗi tier (1-4) có quota riêng cho **RPM** (requests/min), **ITPM** (input tokens/min), **OTPM** (output tokens/min), **TPD** (tokens/day). Anthropic auto-promote tier theo monthly spend.

**Tại sao matter:** Hit limit = 429 error → app crash nếu không có retry logic. Hiểu limit để: capacity plan, batch traffic, request tier upgrade khi cần.

**Học gì cụ thể:**
- Headers trả về: `x-ratelimit-limit-*`, `x-ratelimit-remaining-*`, `retry-after`
- SDK auto-retry 429 với exponential backoff (max_retries=2 default) — handle giùm bạn
- Per-model limits: Haiku có pool riêng, không share với Opus/Sonnet
- Tier upgrade: monthly spend $5 → Tier 1, $40 → Tier 2, $200 → Tier 3, $400 → Tier 4
- Workaround khi hit limit: dùng Batch API (separate quota), spread traffic, request limit increase ở Console

**Refs:** [Rate limits](https://platform.claude.com/docs/en/api/rate-limits)

---

### - [ ] Error handling

SDK throw typed exceptions theo HTTP status. **Đừng string-match error message** — fragile, breaks on SDK update.

| Status | Exception (Python) | Retryable | Cause thường gặp |
|---|---|---|---|
| 400 | `BadRequestError` | ❌ | Invalid params, max_tokens=0, schema sai |
| 401 | `AuthenticationError` | ❌ | API key sai/missing |
| 403 | `PermissionDeniedError` | ❌ | Không có access tới model/feature |
| 404 | `NotFoundError` | ❌ | Model ID typo (vd `claude-sonnet-4.6` thay vì `4-6`) |
| 413 | `request_too_large` | ❌ | Request > limit size |
| 429 | `RateLimitError` | ✅ (auto) | Hit quota |
| 500 | `InternalServerError` | ✅ (auto) | Anthropic-side bug |
| 529 | `OverloadedError` | ✅ (auto) | Service quá tải |

**Tại sao matter:** Production app fail gracefully khi 401 (alert dev), backoff khi 429 (đã handle), retry khi 500/529 (đã handle), surface message khi 400 (user input wrong).

**Học gì cụ thể:**
- Order except blocks từ specific → general (BadRequestError trước APIError)
- All extend `anthropic.APIError` với `.status_code`, `.message`, `.request_id`
- Log `request_id` khi report bug — Anthropic trace được end-to-end
- Stop reasons cũng cần handle: `end_turn`, `max_tokens`, `tool_use`, `pause_turn`, `refusal`, `stop_sequence`

**Refs:** [Error codes](https://platform.claude.com/docs/en/api/errors) · example: [`examples/03-error-handling.py`](./examples/03-error-handling.py)

---

## Examples

- [01-streaming.py](./examples/01-streaming.py) — stream tokens real-time với context manager
- [02-vision.py](./examples/02-vision.py) — phân tích ảnh từ URL
- [03-error-handling.py](./examples/03-error-handling.py) — xử lý các loại error đúng cách

## Notes của tôi

> ___
