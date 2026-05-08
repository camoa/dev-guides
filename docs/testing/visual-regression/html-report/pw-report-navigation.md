---
description: How to navigate the Playwright HTML report home page to find tests to triage.
tldr: The report home page is a flat list filtered by status, project, and free-text search. Use status chip (Failed) → project filter → keyword search → click row as the standard triage flow. Tests are failed-first ordered; there is no manual sort.
---

# Report Navigation

## When to Use

> Use this when finding a specific test to triage in a long report, especially in multi-browser × multi-viewport runs.

## Decision

| Task | How |
|---|---|
| Narrow to failures | Click **Failed** status chip |
| Scope to one browser | Use project filter chip |
| Find by name or file | Free-text search box |
| Filter by tag | Click `@tag` chip or use `@tag` in search |

## Pattern

Standard triage flow:

```
1. Click Failed status chip          → narrow to failures
2. Filter by project                  → focus on one browser/viewport
3. Search for keyword                 → find the test
4. Click row                          → open per-test detail
```

Search prefixes:

| Prefix | Example | What it filters |
|---|---|---|
| `s:` | `s:failed` | Status |
| `p:` | `p:chromium` | Project |
| `@` | `@smoke` | Annotation tag |
| `file:` | `file:header` | File path |

## Common Mistakes

- **Wrong**: expecting a sort UI → **Right**: ordering is implicit (failed first, then by file); no manual sort
- **Wrong**: looking for `@tag` filter chips when tests have no annotations → **Right**: tags only appear if tests use `test.annotations` with tag syntax

## See Also

- [VR Diff Panel](pw-report-vr-diff-panel.md)
- [Per-Test Detail](pw-report-per-test-detail.md)
- [Multiple Projects](pw-report-multiple-projects.md)
