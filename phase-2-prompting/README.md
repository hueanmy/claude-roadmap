# Phase 2 — Prompting

> Cùng 1 model, prompt khác nhau → output khác hẳn. Đây là kỹ năng đòn bẩy nhất khi làm việc với LLM.

## Sub-topics

- [ ] **System prompt** — khác user message ở chỗ nào, cách dùng để set persona/constraints
- [ ] **Role & persona** — "you are a senior engineer" có thật sự work không? khi nào?
- [ ] **Few-shot examples** — show, don't tell — đưa 2-3 ví dụ mẫu trong prompt
- [ ] **Chain of thought** — "think step by step" vs adaptive thinking (Opus 4.7)
- [ ] **XML tags** — Claude đặc biệt nhạy với `<context>`, `<task>`, `<example>` tags
- [ ] **Output format control** — JSON via `output_config.format`, structured outputs
- [ ] **Temperature & top_p** — ⚠️ **Opus 4.7 đã bỏ** sampling params; chỉ còn ở model cũ
- [ ] **Prompt caching** — cache prefix dài → 90% rẻ hơn, ~85% nhanh hơn

## Examples

- [01-system-prompt.py](./examples/01-system-prompt.py) — vai trò của system prompt
- [02-xml-tags.py](./examples/02-xml-tags.py) — structure prompt bằng XML tags
- [03-prompt-caching.py](./examples/03-prompt-caching.py) — cache 1 document dài, query nhiều lần

## Tài liệu chính chủ

- [Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
- [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

## Notes của tôi

> ___
