---
description: "How to read Playwright HTML reports from multi-browser or multi-viewport project matrices."
tldr: "Each browser/viewport project appears as a separate row with a color-coded project tag. Filter by project chip to scope to one browser; search by test title without project filter to see all browser variants side by side. The report has no cross-browser diff view — inspect one project at a time."
---

# Multiple Projects

## When to Use

> Reading reports from a multi-browser × multi-viewport matrix.

## How Projects Appear

Same `test()` runs once per project. The HTML report shows them as **separate rows with a project tag** (color-coded chip).

- Filter chips at the top scope the list to one or more projects
- For VR tests, baselines are **per-project per-platform** by default — a regression in Firefox doesn't contaminate Chromium

## Comparing Across Browsers

To compare the same test across browsers:

1. Search by test title
2. Remove the project filter — all browser variants of that test appear
3. Inspect each row individually

The report does **not** currently render a side-by-side cross-browser diff. You inspect one project at a time.

## Sharded Runs

For runs split across multiple machines, use **blob reporter** on each shard, then merge:

```bash
npx playwright merge-reports --reporter=html ./all-blobs
```

Produces one unified HTML report from N parallel shards.

## Common Mistakes

- **Expecting cross-browser slider comparison** — not supported; inspect each project individually
- **Filtering away the project chips and getting confused by duplicate test titles** — the project tag distinguishes them; show project chips

## See Also

- [Navigation](pw-report-navigation.md)
- [Generation](pw-report-generation.md)
- Reference: [Playwright Projects](https://playwright.dev/docs/test-projects)
