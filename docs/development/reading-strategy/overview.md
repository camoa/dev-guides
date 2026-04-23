---
description: Match your file-reading strategy to task type — targeted edits, comprehensive understanding, or large exploration
tldr: "Use this guide before any code-reading task — before the first Read or Grep call — to pick the strategy that matches the task type instead of applying a blanket \"save tokens\" rule."
---

# Reading Strategy Overview

## When to Use

> Use this guide before any code-reading task — before the first Read or Grep call — to pick the strategy that matches the task type instead of applying a blanket "save tokens" rule.

## Decision

| Task type | Default strategy | Why |
|-----------|------------------|-----|
| Targeted edit / fix | Grep-first | You know the symbol; partial reads are sufficient |
| Comprehensive understanding (doc, audit, review) | Read every source + config file in full | Partial reads miss methods, hooks, annotations, inheritance |
| Large open-ended exploration | Dispatch a subagent | Protects main context; subagent returns a summary |

## Pattern

**Core principle — match strategy to task type, not blanket rules.**

The "use offset/limit, avoid re-reading entire files" advice optimizes for *targeted work*. It is the wrong default for *comprehensive understanding*, where partial reads cause missed methods, classes, hooks, config, and cross-references.

**Grep is a cross-reference tool, not a discovery tool.** Use it to answer *"who calls this?"* — not *"what exists?"*

## Common Mistakes

- **Wrong**: Defaulting to grep for every task to save tokens → **Right**: Check which of the 3 task types applies first; grep is correct for Type A but wrong for Type B
- **Wrong**: Re-reading the same file multiple times in a session → **Right**: Trust prior reads; use targeted re-reads only for specific sections you need to re-verify
- **Wrong**: Treating the harness "save tokens" warning as a universal rule → **Right**: It flags wasteful patterns; thorough reads for documentation work are the correct cost

## See Also

- [Type A — Targeted Edits](task-type-a-targeted-edits.md)
- [Type B — Comprehensive Understanding](task-type-b-comprehensive-understanding.md)
- [Type C — Large Exploration](task-type-c-large-exploration.md)
- Reference: https://grantslatton.com/claude-code
