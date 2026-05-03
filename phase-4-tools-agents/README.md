# Phase 4 — Tools & Agents

> Tool use là bước nhảy từ "chatbot" → "agent". Claude tự gọi function của bạn để truy cập DB, API, file system, search web. Đây là phase quan trọng nhất nếu bạn muốn build product, không chỉ chat UI.

## Sub-topics

### - [ ] Tool / function calling

Bạn define một list tools (mỗi tool có `name` + `description` + `input_schema`), gửi cùng request. Claude trả về `tool_use` block với `input` args nếu nó muốn gọi tool. **Bạn execute tool**, gửi `tool_result` lại, Claude tiếp tục reasoning.

**Tại sao matter:** Đây là cách Claude tương tác với thế giới ngoài. Không có tool: Claude chỉ generate text. Có tool: Claude truy vấn DB, gọi API, đọc file, gửi email — bất cứ gì code của bạn handle được.

**Học gì cụ thể:**
- Tool definition: `name` (snake_case), `description` (clear, vì sao và khi nào dùng), `input_schema` (JSON Schema)
- Flow: Claude `stop_reason="tool_use"` → bạn run tool → append `tool_result` block → call API lại
- Tool result phải có `tool_use_id` match với block ban đầu
- Multiple tool_use trong 1 turn: handle hết rồi gửi all results trong 1 user message

**Refs:** [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) · example: [`examples/01-tool-calling.py`](./examples/01-tool-calling.py)

---

### - [ ] Tool schemas (JSON Schema)

Schema viết bằng JSON Schema, dùng để validate input Claude tạo. Quality của schema = quality của tool calls. Vague schema → Claude pass garbage args. Strict schema → Claude prompt user khi thiếu info.

**Tại sao matter:** Bug phổ biến nhất khi build agent: tool nhận args sai → app crash. Schema chặt loại bỏ class lỗi này ở API layer, không cần defensive code.

**Học gì cụ thể:**
- Required fields: liệt kê trong `required: [...]` array
- Enum cho fixed values: `{"type": "string", "enum": ["pending", "done"]}`
- Description per property — Claude đọc cả description, không chỉ field name
- `strict: true` (Strict tool use) — guarantee schema valid 100%, hơi tăng latency
- Limitations: không support recursive schema, no `minLength`/`maxLength`/`pattern`

**Refs:** [Implementing tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use)

---

### - [ ] Multi-tool orchestration

Define nhiều tools cùng lúc, Claude tự chọn cái nào (hoặc nhiều cái cùng lúc — parallel tool use). Control bằng `tool_choice`:

| `tool_choice` | Behavior |
|---|---|
| `{"type": "auto"}` | Default — Claude tự quyết định, có thể không dùng tool |
| `{"type": "any"}` | Bắt buộc dùng ít nhất 1 tool |
| `{"type": "tool", "name": "X"}` | Bắt buộc dùng tool X |
| `{"type": "none"}` | Cấm dùng tool |

**Tại sao matter:** Production agent thường có 5-30 tools. Hiểu Claude reason về tool choice để debug "why didn't it call X?" — usually description không clear.

**Học gì cụ thể:**
- `disable_parallel_tool_use: true` để force 1 tool / response (cho tool có side effect, vd send_email)
- Tool description là **chính** signal Claude dùng để pick — invest time vào description
- Khi nhiều tool có thể match: Claude pick theo description specificity, không phải order
- 4.6/4.7 tendency: dùng tool ít hơn 4.5 — nếu Claude không gọi tool đủ → tăng `effort` hoặc prompt explicit

**Refs:** [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)

---

### - [ ] Agentic loop

Loop: API call → Claude trả `tool_use` → execute tool → `tool_result` back → API call → ... cho tới `stop_reason == "end_turn"`. Đây là engine của mọi agent.

**Tại sao matter:** Hiểu loop = build được agent từ scratch. Tất cả frameworks (LangChain, LlamaIndex, etc.) chỉ là wrapper quanh loop này.

**Học gì cụ thể:**
- Manual loop: `while True: response = api.create(...); if stop_reason == "end_turn": break; ...`
- Tool runner (beta) — Python `@beta_tool` decorator + `client.beta.messages.toolRunner(...)` tự handle loop
- Safety cap: luôn có max iterations (10-20) để prevent infinite loop
- Cost optimize: cache prefix (system + tools list) — không thay đổi giữa iterations
- Manual loop control khi cần: human-in-the-loop approval, conditional tool exec, custom logging

**Refs:** [Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) · example: [`examples/02-agentic-loop.py`](./examples/02-agentic-loop.py)

---

### - [ ] Computer use

Claude điều khiển máy tính: chụp screenshot, click chuột, gõ phím. Có 2 mode: **Anthropic-hosted** (Claude run trong sandbox của Anthropic) hoặc **self-hosted** (bạn provide environment, Claude trả tool_use, bạn execute).

**Tại sao matter:** Tự động hóa task GUI mà API không tới được — fill form web cũ, navigate desktop app, scrape SPA phức tạp. Opus 4.7 cải thiện đáng kể coordinate precision.

**Học gì cụ thể:**
- Tool: `{"type": "computer_20250124", "name": "computer", "display_width_px": ..., "display_height_px": ...}`
- Self-hosted: bạn run Docker với VNC + agent loop của bạn, gửi screenshot mỗi step
- Cost: nhiều screenshots = nhiều image tokens = tốn $$$. Use case nên scope hẹp
- 4.7 best practice: 1080p screenshots cân bằng performance/cost
- Risk: prompt injection qua content trên screen — sandbox tốt

**Refs:** [Computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use)

---

### - [ ] Web search tool

Server-side tool, Anthropic chạy hộ — không cần bạn implement. Just declare `{"type": "web_search_20260209", "name": "web_search"}` trong tools array.

**Tại sao matter:** Không cần tích hợp Bing/Google API + parse SERP. Cho task cần info mới hơn training cutoff (Jan 2026 cho Opus 4.7), tool này là path đơn giản nhất.

**Học gì cụ thể:**
- Pair với `web_fetch_20260209` để Claude fetch full page content khi cần
- 2026-09-02 version có **dynamic filtering** — Claude write code filter results trước khi vào context (efficient hơn)
- Cost: search free, but tokens count vào input
- Limitations: không support paywall content, không work qua Bedrock/Vertex (1P only)

**Refs:** [Web search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)

---

### - [ ] Human-in-the-loop (HITL)

Pattern: trước khi execute tool có side effect (send email, charge card, delete record), agent pause, hỏi user confirm. Implement bằng cách: detect specific tool name → render confirm UI → wait approval → mới run tool.

**Tại sao matter:** Production agent KHÔNG được autonomous 100% cho destructive action. HITL = safety net + audit trail.

**Học gì cụ thể:**
- Manual loop pattern: check `block.name` trước khi execute, prompt user nếu trong allowlist
- Managed Agents có built-in: `permission_policy: "always_ask"` → session goes idle, user gửi `tool_confirmation` event
- UX consideration: có "always allow this tool" / "deny + provide reason" options
- Audit log: lưu mọi tool_use + decision để compliance
- Don't use HITL cho read-only tools — chỉ slow down user

**Refs:** [Permission policies (Managed Agents)](https://platform.claude.com/docs/en/managed-agents/permission-policies)

---

## Examples

- [01-tool-calling.py](./examples/01-tool-calling.py) — single tool call, 1 round trip
- [02-agentic-loop.py](./examples/02-agentic-loop.py) — full loop với 2 tools, multi-iteration

## Notes của tôi

> ___
