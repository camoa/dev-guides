---
description: Grep-first strategy for bug fixes and bounded edits where you already know the symbol
tldr: "Use when you already know what symbol you're changing and the scope is bounded to one or two files. Bug fix, rename, small feature edit."
---

# Task Type A — Targeted Edits

## When to Use

> Use when you already know what symbol you're changing and the scope is bounded to one or two files. Bug fix, rename, small feature edit. Use [Type B](task-type-b-comprehensive-understanding.md) when you don't know what you're looking for yet.

## Decision

| Signal | Action |
|--------|--------|
| You know the function/class name | Grep to locate the hit |
| You know the file but not the exact line | Grep within that file |
| You need context around the match | Read with `offset`/`limit` around the hit (±50 lines), not just the hit line |
| The "why" isn't on the match line | Expand the read window — rationale often lives 20-50 lines above |

## Pattern

```
1. Grep to locate the symbol
2. Read with offset/limit around the hit (±50 lines)
3. Edit
```

The ±50 line window (not the exact line) matters — context around the match often carries the "why" that determines whether your edit is correct.

## Common Mistakes

- **Wrong**: Reading a 2000-line file in full to change one constant → **Right**: Grep + Read with offset/limit on the hit
- **Wrong**: Reading only the single matched line → **Right**: Expand ±50 lines; the reason for the code lives around it, not on it
- **Wrong**: Using grep-first when you don't know the symbol name → **Right**: You're in Type B or C, not Type A — switch strategy

## See Also

- [Type B — Comprehensive Understanding](task-type-b-comprehensive-understanding.md) — when you don't know what you're looking for yet
- [Token Warning Interpretation](token-warning-interpretation.md)
- Reference: https://code.claude.com/docs/en/best-practices
