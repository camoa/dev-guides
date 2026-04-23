---
description: Why grep-only reading fails documentation and audit tasks — a reference list of what grep cannot find
tldr: "Use when you're tempted to grep-first for a Type B task \"to save tokens.\" This list explains what you'll miss and why that's fatal to documentation or audit accuracy."
---

# What Grep Misses

## When to Use

> Use when you're tempted to grep-first for a Type B task "to save tokens." This list explains what you'll miss and why that's fatal to documentation or audit accuracy.

## Decision

| Missed by grep | Why it matters | What to do instead |
|----------------|----------------|--------------------|
| Inherited / trait / mixin behavior | Methods in parent classes don't show in child-file grep | Read parent classes and traits in full |
| Dynamic dispatch (magic methods, reflection) | `__call`, decorators, string-based lookup don't match literal grep | Read full class; check constructor wiring |
| Config-to-code wiring | Service containers reference classes not greppable from source | Read service/DI configs in full |
| Annotations / docblocks | Plugin metadata, ORM mappings, validation rules in comments — grep output truncates | Read classes in full; preserve docblock context |
| Constructor vs. factory wiring | Real dependencies span `__construct` and `create`/factory methods | Read both; don't stop at `__construct` |
| Entry-point callback files | Hooks, event listeners, lifecycle handlers live anywhere in the file | Read entry-point files fully |
| Implicit contracts (interfaces, abstracts) | Required methods defined elsewhere than the implementer | Follow the inheritance chain |
| "Why" context around a match | Rationale lives 20-50 lines above the hit | Use wide `offset`/`limit` windows, not single-line reads |

## Pattern

Grep finds *explicit textual matches*. Code behavior comes from *implicit contracts* (inheritance, dispatch, wiring, metadata). These are invisible to grep.

**Rule**: if documenting or auditing, assume grep-only will miss 20-40% of what matters. Read fully.

## Common Mistakes

- **Wrong**: "I grepped for all the public methods" → **Right**: Inherited methods don't appear; read parents
- **Wrong**: "The service is wired to class X" based on grepping the class → **Right**: Read the services.yml / container config to see the actual wiring
- **Wrong**: "No annotations found" based on grep → **Right**: Annotations in docblocks are often multi-line and grep-unfriendly; read the class

## See Also

- [Type B — Comprehensive Understanding](task-type-b-comprehensive-understanding.md)
- [Pre-Completion Checklist](pre-completion-checklist.md)
- Reference: https://github.com/anthropics/claude-code/issues/5256
