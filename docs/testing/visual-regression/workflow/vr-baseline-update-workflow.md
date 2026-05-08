---
description: How to update baselines after an intentional UI change — scoped updates, code review models, and the atomic baseline rule.
tldr: Always scope baseline updates with --grep to affected tests. Pair every baseline update with the UI change in the same commit or PR. Never do a bulk --update-snapshots as a default response to red CI — that accepts regressions. Review diffs using the Playwright HTML report, not just GitHub's PNG diff.
---

# Baseline Update Workflow

## When to Use

> Use this guide after an *intentional* UI change that's expected to produce diffs. Bulk updates and baseline-only commits are the primary ways VR programs fail.

## Decision

| Model | When |
|-------|------|
| **Inline** — UI change + baseline updates in the same PR | Small, targeted changes (≤5 baseline files) |
| **Distinct VR-baseline commits** — UI change in commit A; `chore(vr): update baselines for button restyle` in commit B | Larger refactors; easier revert |

## Pattern

Scoped local update:

```bash
# Always scope with --grep to the affected tests
npx playwright test --update-snapshots --grep "button"
```

Review checklist using the HTML report:

```bash
npx playwright show-report
```

For each failed assertion, check:
1. Scrub the slider — is the diff in the region the PR claims to change?
2. Are there incidental diffs in *other* regions? If yes — investigate; this is the regression-finding moment
3. Are diffs cross-viewport consistent? A change affecting only desktop but not mobile suggests a media-query bug

The atomic baseline-update rule:

> **Never update a baseline without a code change in the same commit explaining why.**

A baseline-only commit (`update baselines`) with no corresponding source change is, definitionally, accepting a regression you don't understand.

## Common Mistakes

- **Wrong**: bulk `--update-snapshots` as the default response to red CI → **Right**: accepts regressions
- **Wrong**: updating baselines in CI on a separate "fix" commit with no explanation → **Right**: same problem, scaled
- **Wrong**: reviewing PNG diffs only in GitHub's UI without scrubbing the Playwright report → **Right**: misses sub-pixel shifts

## See Also

- [Baseline Management](vr-baseline-management.md)
- [Triaging False Positives](vr-triaging-false-positives.md)
- [VR Debt & Hygiene](vr-debt-and-hygiene.md)
