---
description: How to interpret harness token-usage warnings without incorrectly switching away from full reads
tldr: "Use when the harness emits a warning like *\"Read results using 881.4k tokens (88%) → save ~264.4k\"* and you're unsure whether to change your reading strategy."
---

# Token Warning Interpretation

## When to Use

> Use when the harness emits a warning like *"Read results using 881.4k tokens (88%) → save ~264.4k"* and you're unsure whether to change your reading strategy.

## Decision

| The warning means | The warning does NOT mean |
|-------------------|---------------------------|
| Don't re-read the same file repeatedly | Always prefer grep |
| Don't read a 2000-line file to check one constant | Never do full reads |
| Don't read generated code, lockfiles, or vendor code that grep could answer | Documentation/audit tasks are wasteful |
| Don't read a file whole when you only need one section AND know the structure | Full reads are always avoidable |

## Pattern

The warning flags **wasteful patterns**:

1. Re-reading the same file multiple times in a session → trust prior reads + targeted re-reads
2. Reading a huge file to check one constant → use `offset`/`limit`
3. Reading generated/vendor/lockfile code → use `Grep` for the one symbol you need
4. Reading whole when you already know the structure and need one section → use `offset`/`limit`

**It does NOT flag**: a thorough read of 15 small source files to document a module. That is the correct cost for Type B, not waste.

## Common Mistakes

- **Wrong**: Switching a Type B task to grep-first because the harness warned about token usage → **Right**: Verify you weren't doing one of the 4 wasteful patterns; if not, the warning doesn't apply to your strategy
- **Wrong**: Treating "88% context used" as a hard stop mid-audit → **Right**: If remaining work would push over budget, dispatch remaining exploration to a subagent
- **Wrong**: Using the warning to justify skipping parent class reads → **Right**: Missing parent class content causes audit/doc failures that cost more than tokens

## See Also

- [Task Type A — Targeted Edits](task-type-a-targeted-edits.md) — where token warnings usually apply
- [Type C — Large Exploration](task-type-c-large-exploration.md) — when real budget constraint needs delegation
- Reference: https://code.claude.com/docs/en/best-practices
