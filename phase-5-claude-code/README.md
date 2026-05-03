# Phase 5 — Claude Code

> Claude Code = Anthropic CLI chính chủ để code. Đây là productivity multiplier khác hẳn web Claude.ai — agentic, có quyền đọc/sửa file, chạy bash, gọi MCP servers.

## Sub-topics

### Commands
- [ ] `/help` — list lệnh
- [ ] `/plan` — vào plan mode (read-only, lập kế hoạch trước khi sửa)
- [ ] `/clear` — clear context window
- [ ] `/compact` — nén context khi gần đầy
- [ ] `/memory` — quản lý memory file
- [ ] `/cost` — xem chi phí session
- [ ] `/doctor` — chẩn đoán issues

### Concepts
- [ ] **CLAUDE.md** — file context auto-load mỗi session, định nghĩa convention dự án
- [ ] **Skills** — folder với `SKILL.md` description, load on-demand khi task match
- [ ] **Subagents** — spawn Claude khác (thường Haiku) cho subtask, save context chính
- [ ] **Hooks** — shell commands chạy tại lifecycle events (PreToolUse, PostToolUse, Stop...)
- [ ] **MCP integration** — kết nối tools bên ngoài qua Model Context Protocol
- [ ] **Slash commands** — custom command tự định nghĩa
- [ ] **Permission modes** — accept-edits, plan, bypass-permissions
- [ ] **Plan mode** — Claude lên kế hoạch trước, user duyệt rồi mới execute
- [ ] **Headless mode** — `claude -p "..."` chạy non-interactive cho automation
- [ ] **Git worktrees** — chạy nhiều Claude instances song song trên branches khác nhau

### Shortcuts
- `Ctrl+C` — cancel current operation
- `Ctrl+R` — reverse-search history
- `Shift+Tab` — toggle plan mode
- `Esc + Esc` — interrupt + clear input
- `@` — mention file (auto-include trong context)
- `\` (cuối dòng) — multiline input

## Examples

- [CLAUDE.md.example](./examples/CLAUDE.md.example) — template CLAUDE.md cho dự án Python
- [hooks-example/](./examples/hooks-example/) — hook chạy `ruff format` sau khi Claude edit Python file
- [skill-example/](./examples/skill-example/) — skill folder structure với SKILL.md

## Tài liệu chính chủ

- [Claude Code overview](https://docs.claude.com/en/docs/claude-code/overview)
- [CLAUDE.md memory](https://docs.claude.com/en/docs/claude-code/memory)
- [Hooks](https://docs.claude.com/en/docs/claude-code/hooks)

## Notes của tôi

> ___
