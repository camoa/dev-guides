---
description: How to read Playwright HTML reports from multi-browser or multi-viewport project matrices.
tldr: Each browser/viewport project appears as a separate row with a color-coded project tag. Filter by project chip to scope to one browser; search by test title without project filter to see all browser variants side by side. The report has no cross-browser diff view — inspect one project at a time.
---

# Multiple Projects

## When to Use

> Use this when reading reports from a multi-browser × multi-viewport matrix and you need to find, filter, or compare results across projects.

## Decision

| Task | How |
|---|---|
| Scope list to one browser | Use project filter chip at the top |
| See all browsers for the same test | Search by test title, remove project filter |
| Merge reports from sharded CI runs | Use blob reporter per shard, then `merge-reports` |

## Pattern

Sharded run merge:

```bash
npx playwright merge-reports --reporter=html ./all-blobs
```

Produces one unified HTML report from N parallel shards.

## How Projects Appear

- Same `test()` runs once per project → **separate rows with a color-coded project chip**
- VR baselines are per-project per-platform by default — a regression in Firefox doesn't contaminate Chromium
- Report has **no side-by-side cross-browser diff** — inspect each project individually

## Common Mistakes

- **Wrong**: expecting a cross-browser slider comparison → **Right**: not supported; inspect each project row individually
- **Wrong**: hiding project chips and getting confused by duplicate test titles → **Right**: the project tag distinguishes them; keep chips visible

## See Also

- [Navigation](pw-report-navigation.md)
- [Generation](pw-report-generation.md)
- Reference: [Playwright Projects](https://playwright.dev/docs/test-projects)
