---
description: One-table lookup — which reading strategy to apply for a specific task
tldr: "Use when you need the one-line answer for a specific task without reading the full guidance."
---

# Quick Reference

## When to Use

> Use when you need the one-line answer for a specific task without reading the full guidance.

## Decision

| Task | Default strategy |
|------|------------------|
| Fix a known bug | Grep → Read with offset/limit (±50 lines) |
| Rename a symbol | Grep everywhere, Read each hit's context |
| Document a module / package | Glob inventory → Read all source + config in full |
| Security audit | Glob inventory → Read all source + config in full |
| Architecture review | Glob inventory → Read all source + config in full |
| Onboard to unfamiliar but bounded component | Read entry points + manifests in full, branch outward |
| Explore huge codebase (open-ended) | Dispatch Explore / general-purpose subagent |
| Check one constant / value | Grep → Read with offset/limit |
| "How does feature X work" (scoped) | Read the feature's files in full |
| "How does this whole system work" (open-ended) | Dispatch subagent |
| Harness warns about token usage | Check which wasteful pattern applied; Type B reads are not wasteful |

## Common Mistakes

- **Wrong**: Picking a strategy based on file size alone → **Right**: Pick based on task type (targeted vs comprehensive vs exploration)
- **Wrong**: Applying the same strategy to every task in a session → **Right**: Different tasks in one session can need different strategies

## See Also

- [Overview](overview.md) — the core principle
- [Type A — Targeted Edits](task-type-a-targeted-edits.md)
- [Type B — Comprehensive Understanding](task-type-b-comprehensive-understanding.md)
- [Type C — Large Exploration](task-type-c-large-exploration.md)
