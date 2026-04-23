---
description: Context-Efficient Reading Strategy — decide between grep-first, full-read, and subagent delegation based on task type
guide-meta:
  concepts:
    - reading strategy
    - context window
    - grep vs read
    - token usage
    - full file read
    - offset limit
    - subagent delegation
    - code exploration
    - Type A Type B Type C
    - pre-completion checklist
    - token warning
    - audit reading
    - documentation reading
  not:
    - file search patterns
    - code search syntax
    - ripgrep flags
  requires: []
  complements:
    - development/solid-principles
    - development/tdd-spec-driven
  specializes: ""
  category: dev-practices
---

# Context-Efficient Reading Strategy

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand the core principle before picking a strategy | [Overview](overview.md) | Use this guide before any code-reading task — before the first Read or Grep call — to pick the strategy that matches the task type instead of applying a blanket "save tokens" rule. |
| Fix a known bug or edit a known symbol | [Type A — Targeted Edits](task-type-a-targeted-edits.md) | Use when you already know what symbol you're changing and the scope is bounded to one or two files. Bug fix, rename, small feature edit. |
| Document, audit, or review a module/package | [Type B — Comprehensive Understanding](task-type-b-comprehensive-understanding.md) | Use when the task requires understanding a whole unit — a module, package, library, or feature area. Documentation authoring, security/code review, architecture analysis, onboarding, multi-file refactoring. |
| Explore a large unfamiliar codebase | [Type C — Large Exploration](task-type-c-large-exploration.md) | Use when the task is open-ended, you don't know the structure yet, or a full Type B read would exceed ~30% of remaining context. Use [Type B](task-type-b-comprehensive-understanding.md) when the unit is bounded enough for main context. |
| Know what full reads catch that grep misses | [What Grep Misses](what-grep-misses.md) | Use when you're tempted to grep-first for a Type B task "to save tokens." This list explains what you'll miss and why that's fatal to documentation or audit accuracy. |
| Interpret a harness token-usage warning | [Token Warning Interpretation](token-warning-interpretation.md) | Use when the harness emits a warning like *"Read results using 881.4k tokens (88%) → save ~264.4k"* and you're unsure whether to change your reading strategy. |
| Verify a Type B task is actually complete | [Pre-Completion Checklist](pre-completion-checklist.md) | Use before declaring a Type B task complete — documentation finished, audit signed off, review approved. If any item was skipped because of context-saving instincts, the work is incomplete. |
| Look up the right strategy for a specific task quickly | [Quick Reference](quick-reference.md) | Use when you need the one-line answer for a specific task without reading the full guidance. |
