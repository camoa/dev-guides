---
description: Full-read strategy for documentation, audits, and reviews where partial reads miss critical behavior
tldr: "Use when the task requires understanding a whole unit — a module, package, library, or feature area. Documentation authoring, security/code review, architecture analysis, onboarding, multi-file refactoring."
---

# Task Type B — Comprehensive Understanding

## When to Use

> Use when the task requires understanding a whole unit — a module, package, library, or feature area. Documentation authoring, security/code review, architecture analysis, onboarding, multi-file refactoring. Use [Type C](task-type-c-large-exploration.md) if the unit is too big for main context.

## Decision

| Signal | Action |
|--------|--------|
| Documenting a module, package, or library | Full reads of every source + config file |
| Security review or audit | Full reads — partial reads miss vulnerable methods |
| Architecture analysis | Full reads; grep only AFTER you have the full picture |
| First-time exploration of an unfamiliar but bounded component | Full reads of entry points + source + config |
| Refactoring spanning multiple files | Full reads of all affected files before proposing changes |

## Pattern

```
1. Glob the structural inventory
   - manifests (composer.json, package.json, *.info.yml)
   - entry points (*.module, index.js, main.py)
   - config (services.yml, routing.yml, *.config.ts)
   - source tree (src/, lib/, modules/)

2. Read every source file in full
   - classes/modules are contracts; partial reads miss methods,
     inherited behavior, annotations, and docblocks

3. Read every config/manifest file in full
   - they are small and every line matters

4. Grep AFTER you have the full picture
   - for cross-references: "who calls this?"
```

**The token cost of reading everything is the correct cost for this task type. Do not optimize it away.**

## Common Mistakes

- **Wrong**: Greping for method names before reading class files → **Right**: You can't grep for what you don't know exists; read the class fully first
- **Wrong**: Skipping config/manifest files because "they're small" → **Right**: Read them in full; every line matters and they're the wiring
- **Wrong**: Declaring a Type B task complete without following the inheritance chain → **Right**: Read parent classes, traits, interfaces — they carry contract-relevant behavior
- **Wrong**: Reading source but skipping docblocks → **Right**: Plugin metadata, ORM mappings, validation rules live in annotations that grep output truncates

## See Also

- [What Grep Misses](what-grep-misses.md) — why partial reads fail Type B tasks
- [Pre-Completion Checklist](pre-completion-checklist.md) — verify you finished
- [Type C — Large Exploration](task-type-c-large-exploration.md) — if the unit is too big for main context
- Reference: https://milvus.io/blog/why-im-against-claude-codes-grep-only-retrieval-it-just-burns-too-many-tokens.md
