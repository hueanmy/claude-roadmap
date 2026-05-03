---
name: pr-description-writer
description: Use when the user asks to write a PR description, draft PR body, or summarize a branch's changes for review. Generates a structured PR body with summary, test plan, and risk callouts.
---

# PR Description Writer

When invoked, follow this exact procedure:

## 1. Gather context

Run in parallel:
- `git status` — see uncommitted changes
- `git diff main...HEAD` — see all changes on this branch
- `git log main...HEAD --oneline` — see commit list

## 2. Draft the PR body

Use this template:

```markdown
## Summary

<2-3 sentence overview of what changed and why>

## Changes

- <bulleted list of meaningful changes — group by area, not by commit>

## Test plan

- [ ] <how reviewer can verify it works>
- [ ] <edge case to test>

## Risk

<one sentence: what could break, what to watch in prod after merge>
```

## 3. Rules

- Keep title under 70 chars.
- Body focuses on WHY, not WHAT (the diff shows what).
- Don't list trivial commits (typo fix, format).
- If risk is low, write "Low — isolated to <module>, no DB changes".
- Don't include the AI co-author line unless user asks.

## 4. Output

Print the title and body in fenced markdown blocks so the user can copy-paste into `gh pr create`.
