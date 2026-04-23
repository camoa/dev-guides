---
description: Subagent delegation strategy for open-ended exploration across large or unfamiliar codebases
tldr: "Use when the task is open-ended, you don't know the structure yet, or a full Type B read would exceed ~30% of remaining context. Use [Type B](task-type-b-comprehensive-understanding.md) when the unit is bounded enough for main context."
---

# Task Type C — Large Exploration

## When to Use

> Use when the task is open-ended, you don't know the structure yet, or a full Type B read would exceed ~30% of remaining context. Use [Type B](task-type-b-comprehensive-understanding.md) when the unit is bounded enough for main context.

## Decision

| Signal | Action |
|--------|--------|
| Open-ended "how does X work" across many files | Dispatch Explore subagent |
| You don't know the structure or entry points yet | Dispatch Explore subagent |
| Full read would exceed ~30% of your remaining context | Dispatch subagent (Explore, general-purpose, or specialized) |
| Research question spans multiple repos or unfamiliar domains | Dispatch subagent |

## Pattern

```
1. Frame the research question for the subagent
   - What are you trying to understand?
   - What structured output do you want back?
     (e.g., "list of classes with their methods and relationships")

2. Dispatch to Explore or general-purpose subagent
   - The subagent burns ITS context doing full reads
   - It returns a structured summary to yours

3. Use the summary to decide what to Read targeted in your main context
   - Usually only 2-3 files from the original N
```

**The subagent trades its context for yours.** It can do 20+ full reads and return a 2-page summary, preserving your main conversation for actual authoring or implementation.

## Common Mistakes

- **Wrong**: Reading 20 files in main context to "get a feel" for the codebase → **Right**: Delegate to Explore; it does the full reads and returns a structured index
- **Wrong**: Asking the subagent "summarize" without specifying what fields you need → **Right**: Ask for specific structured output (class names, method signatures, inheritance chains, config keys)
- **Wrong**: Re-dispatching to the subagent for every follow-up → **Right**: Do targeted Reads in main context for specific files the summary flagged as important

## See Also

- [Type B — Comprehensive Understanding](task-type-b-comprehensive-understanding.md) — when the unit is bounded enough for main context
- [Pre-Completion Checklist](pre-completion-checklist.md) — still applies even when a subagent did the initial reads
- Reference: https://www.damiangalarza.com/posts/2025-12-08-understanding-claude-code-context-window/
