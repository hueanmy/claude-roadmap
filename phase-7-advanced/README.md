# Phase 7 — Production & Scale

> Build prototype dễ. Ship to prod khó. Phase này về evals, observability, cost, security, multi-agent — kỹ năng phân biệt "demo" và "production".

## Sub-topics

### - [ ] Agent Teams

Pattern: orchestrator agent điều phối nhiều specialist agents. Mỗi specialist có scope hẹp + tool surface riêng. Orchestrator handle: task decomposition, routing, result synthesis.

**Tại sao matter:** Single agent với 30 tools confuse — Claude khó pick tool đúng, system prompt phình to. Split: orchestrator chỉ biết về 5 specialists, mỗi specialist 5-7 tools. Total 30 tools nhưng Claude từng layer chỉ thấy 5-7.

**Học gì cụ thể:**
- Orchestrator pattern: planner agent quyết delegate → handler agent execute → reporter aggregate
- Tool surface design: mỗi specialist define hẹp ("billing agent" thấy stripe + invoice tools, không thấy code tools)
- Communication: shared state (DB, file system) hoặc message passing (orchestrator forward)
- Cost: mỗi agent là 1 API call → tăng cost. Trade-off vs improved quality
- Anthropic case study: Claude Code dùng pattern này (Explore subagent, routine-worker)

**Refs:** [Building effective agents](https://www.anthropic.com/research/building-effective-agents)

---

### - [ ] Multi-agent orchestration

Cách agents talk to each other:
- **Sequential** — A xong → B chạy với output A. Đơn giản, dễ debug, latency tăng
- **Parallel** — A, B, C chạy đồng thời, orchestrator wait all → synthesize. Faster, nhưng phải design tasks độc lập
- **Hierarchical** — root → branches → leaves. Cho task complex (research với 10+ subtopics)

**Tại sao matter:** Choice ảnh hưởng latency 10x và cost. Sequential 5 steps × 10s = 50s. Parallel 5 steps = 10s. Pick đúng pattern theo task structure.

**Học gì cụ thể:**
- Sequential pattern: chain of `messages.create()` calls, output→input
- Parallel: `asyncio.gather()` (Python) hoặc `Promise.all()` (TS) cho N agents song song
- Map-reduce: parallel "map" agents process chunks → 1 "reduce" agent merge
- Pitfall: parallel agents thấy state cũ (race condition) — cần version/lock nếu shared state
- Managed Agents (Anthropic) có sub-agent invocation built-in — composition layer

**Refs:** [Multi-agent](https://platform.claude.com/docs/en/managed-agents/multi-agent)

---

### - [ ] Evals & testing

Đánh giá output Claude tự động: golden dataset (input + expected criteria) + LLM judge (model mạnh hơn grade output). Critical cho regression test khi thay model/prompt.

**Tại sao matter:** "Trust me, it works" không scale. Khi bạn iterate prompt 10 lần, không có eval = không biết version nào tốt hơn. Anthropic prompt engineers chạy eval mỗi lần release.

**Học gì cụ thể:**
- Golden dataset: 50-200 cases, cover happy path + edge cases + adversarial input
- Criteria, không exact match: "must mention 391" thay vì "= '391'"
- Judge model phải mạnh hơn model under test (vd: judge bằng Opus 4.7, test Haiku 4.5)
- Metrics: accuracy, latency p50/p95, cost per request, refusal rate
- A/B testing: split traffic giữa prompt v1 vs v2, measure win rate
- Frameworks: PromptFoo, Anthropic's evaluator, custom Python script

**Refs:** [Building evals](https://docs.claude.com/en/docs/build-with-claude/develop-tests) · example: [`examples/01-evals-basic.py`](./examples/01-evals-basic.py)

---

### - [ ] Fine-tuning strategy

⚠️ **TL;DR: thường KHÔNG cần fine-tune.** Anthropic không offer fine-tuning trực tiếp (chỉ Bedrock có cho Claude). Prompt engineering + few-shot + RAG cover 95% use case.

**Tại sao matter:** Hiểu khi nào fine-tune đáng vs khi nào chỉ là cargo cult. Fine-tune đắt (compute), maintenance (re-tune mỗi model upgrade), data prep tốn (cần 1000+ labeled examples chất lượng cao).

**Học gì cụ thể:**
- Khi nào FT đáng:
  - Domain rất hẹp với jargon riêng (medical coding, legal citation)
  - Task style không control được bằng prompt (specific tone for brand)
  - Latency critical + có thể chấp nhận model nhỏ hơn
- Khi nào KHÔNG đáng:
  - Cải thiện accuracy chung — prompt engineering rẻ hơn 100x
  - Dataset < 1000 examples
  - Underlying model upgrade thường xuyên (FT model = lock vào version)
- Alternative: prompt caching (free perf), few-shot (cheap), RAG (scalable)

**Refs:** [Fine-tuning on Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-customization.html)

---

### - [ ] Cost optimization

5 lever chính, ranked theo impact:

1. **Prompt caching** — 90% rẻ hơn cho cached portion. Single biggest win.
2. **Model routing** — classify task complexity → route Haiku ($1/$5) cho simple, Opus ($5/$25) cho hard
3. **Batch API** — 50% off cho async workload (label, classify, extract)
4. **Effort tuning** — `effort: "low"` cho task đơn giản trên Opus
5. **Output minimization** — output token đắt 5x input → prompt "be concise", limit `max_tokens`

**Tại sao matter:** Production app với 100K req/ngày: tối ưu vs không = $15K/tháng vs $150K/tháng. Cost optimization không phải premature optimization — nó là survival skill.

**Học gì cụ thể:**
- Track cost per request: log `usage` object mỗi response, aggregate
- Build cost dashboard: cost per user, per feature, per session
- Set spend limits ở Console — alert khi vượt threshold
- Recompute cost mỗi khi thay model — Opus 4.7 token count khác 4.6 (cùng prompt, khác token count)

**Refs:** [Pricing](https://platform.claude.com/docs/en/pricing) · [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)

---

### - [ ] Security best practices

Vector tấn công thường gặp:

| Vector | Mô tả | Mitigation |
|---|---|---|
| **Prompt injection** | User input chứa instruction override system prompt | Don't trust user input as instruction; sanitize/sandbox |
| **Jailbreak** | Prompt compose để bypass safety guardrails | Anthropic safety filter + your own content moderation |
| **Tool exfiltration** | Claude bị trick gọi tool destructive | Strict permission, HITL cho destructive tools, sandboxing |
| **Data leak qua output** | Sensitive data trong prompt leak qua output | Don't put secrets in prompt; use vault for credentials |
| **Indirect injection** | Web content / file content chứa injection | Treat external content as untrusted; mark in prompt |

**Tại sao matter:** Một prompt injection có thể: leak system prompt, gọi tool xóa data, gen output giả mạo. Production app phải defense-in-depth.

**Học gì cụ thể:**
- Separation of trust: user content vs system content vs external data
- Tool permissions: read-only vs destructive — destructive luôn HITL
- Output validation: structured output + schema validation, never trust JSON to be valid
- Audit log: log mọi tool_use + input + result + timestamp
- Rate limit per user: prevent abuse
- Test với adversarial inputs: red team prompt injection cases

**Refs:** [Security best practices](https://platform.claude.com/docs/en/build-with-claude/best-practices) · [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

---

### - [ ] Observability & logging

Log mọi: request_id, model, input tokens, output tokens, cache_read_tokens, latency, stop_reason, tool_use, errors. Aggregate thành dashboards.

**Tại sao matter:** Khi prod fail (tăng latency, sai output, cost spike), bạn cần data để diagnose. "It worked yesterday" không debug được.

**Học gì cụ thể:**
- Mỗi response có `id` + `request_id` — log để Anthropic trace nếu support
- Track p50/p95/p99 latency theo: model, route, time of day
- Cost dashboard: $ per session, per user, per feature
- Tool use analytics: tool A được gọi mấy lần/ngày, fail rate, avg latency
- Distributed trace: nếu agent loop multi-step, trace request_id qua các step
- Tools: Datadog, Honeycomb, OpenTelemetry, hoặc tự build với Postgres + Grafana

**Refs:** [Observability for managed agents](https://platform.claude.com/docs/en/managed-agents/observability)

---

### - [ ] CI/CD integration

Claude trong pipeline: auto code review trên PR, auto fix CI failures, auto generate release notes, auto triage issues. Implement bằng `claude -p` headless mode + GitHub Actions / GitLab CI.

**Tại sao matter:** Move từ "Claude help me code" → "Claude help my team continuously". Claude Code thành component standard trong pipeline, không phải tool đặc biệt mỗi dev xài riêng.

**Học gì cụ thể:**
- GitHub Action: `anthropics/claude-code-action` — official action
- Trigger pattern: PR opened → Claude review → comment với findings
- CI fix pattern: tests fail → Claude analyze + propose fix → tạo PR
- Spend control: set MAX_COST env var, fail-safe nếu vượt
- Approve/permission: sandbox permission mode trong CI (đừng dùng `bypass-permissions` cho external repos)
- Examples: auto-update dependencies, auto-respond to issue, weekly digest

**Refs:** [Claude Code GitHub Action](https://github.com/anthropics/claude-code-action) · [CI integration](https://docs.claude.com/en/docs/claude-code/ci)

---

## Examples

- [01-evals-basic.py](./examples/01-evals-basic.py) — golden dataset + LLM judge cơ bản

## Tài liệu chính chủ

- [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
- [Effective context engineering](https://www.anthropic.com/news/contextual-retrieval)
- [Production best practices](https://platform.claude.com/docs/en/build-with-claude/best-practices)

## Notes của tôi

> ___
