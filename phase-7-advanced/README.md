# Phase 7 — Production & Scale

> Build prototype dễ. Ship to prod khó. Phase này về evals, observability, cost, và multi-agent patterns.

## Sub-topics

- [ ] **Agent Teams** — orchestrator + specialist agents, mỗi agent có scope riêng
- [ ] **Multi-agent orchestration** — parallel vs sequential, message passing
- [ ] **Evals & testing** — tự động đánh giá output (LLM-as-judge, golden dataset, regression test)
- [ ] **Fine-tuning strategy** — khi nào worth, khi nào prompt engineer là đủ (thường là đủ)
- [ ] **Cost optimization** — caching, model routing (Haiku for cheap tasks), batch API
- [ ] **Security best practices** — prompt injection, output validation, sandbox tool execution
- [ ] **Observability & logging** — log mọi request, track p50/p95 latency, cost per session
- [ ] **CI/CD integration** — Claude trong PR review, auto-fix, headless mode

## Examples

- [01-evals-basic.py](./examples/01-evals-basic.py) — golden dataset + LLM judge cơ bản

## Tài liệu chính chủ

- [Building agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Effective context engineering](https://www.anthropic.com/news/contextual-retrieval)

## Notes của tôi

> ___
