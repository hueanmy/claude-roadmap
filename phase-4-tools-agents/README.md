# Phase 4 — Tools & Agents

> Tool use là bước nhảy từ "chatbot" → "agent". Claude tự gọi function của bạn để truy cập DB, API, file system.

## Sub-topics

- [ ] **Tool / function calling** — Claude trả về `tool_use` block với input args
- [ ] **Tool schemas (JSON)** — `name`, `description`, `input_schema` (JSON Schema)
- [ ] **Multi-tool orchestration** — nhiều tool, Claude chọn cái nào (auto / any / specific)
- [ ] **Agentic loop** — Claude → tool_use → bạn run tool → tool_result → Claude → ... cho tới `end_turn`
- [ ] **Computer use** — Claude điều khiển màn hình (screenshot + mouse/keyboard)
- [ ] **Web search tool** — server-side, Anthropic chạy hộ
- [ ] **Human-in-the-loop** — chặn agent trước khi run tool, đợi user approve

## Examples

- [01-tool-calling.py](./examples/01-tool-calling.py) — single tool call, manual loop (1 round)
- [02-agentic-loop.py](./examples/02-agentic-loop.py) — full loop với 2 tools

## Tài liệu chính chủ

- [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- [Implementing tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use)
- [Computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use)

## Notes của tôi

> ___
