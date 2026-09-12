---
description: "How to navigate the Playwright HTML report home page to find tests to triage."
tldr: "The report home page is a flat list filtered by status, project, and free-text search. Use status chip (Failed) → project filter → keyword search → click row as the standard triage flow. Tests are failed-first ordered; there is no manual sort."
---

# Report Navigation

## When to Use

> Finding the test you want to triage in a long report.

## Home Page Layout

A flat list of all executed tests. Per-test row: title, file path, project (browser), duration, status pill (`passed` / `failed` / `flaky` / `skipped` / `timed out`).

## Top-of-Page Controls

- **Status filter chips** — All / Passed / Failed / Flaky / Skipped
- **Project filter** — appears when `projects` config has multiple entries
- **Free-text search** — matches title and file path; supports prefixes:
  - `s:failed` — status filter
  - `p:chromium` — project filter
  - `@tag` — annotation tag
  - `file:` — file filter
- **Tags** — `@smoke`, `@vr` etc. become clickable filter chips

## Pattern: Triage Flow

```
1. Click Failed status chip          → narrow to failures
2. Filter by project                  → focus on one browser/viewport
3. Search for keyword                 → find the test
4. Click row                          → open per-test detail
```

## Common Mistakes

- **Sorting expectations** — sorting is implicit (failed first, then by file); no manual sort UI
- **Looking for tag UI without tagging tests** — `@smoke` etc. only appear if tests carry annotations

## See Also

- [VR Diff Panel](pw-report-vr-diff-panel.md)
- [Per-Test Detail](pw-report-per-test-detail.md)
- [Multiple Projects](pw-report-multiple-projects.md)
