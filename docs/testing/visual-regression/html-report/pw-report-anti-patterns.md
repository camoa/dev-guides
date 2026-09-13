---
description: "Consolidated list of anti-patterns to avoid when working with the Playwright HTML report."
tldr: "The twelve most common HTML report mistakes — from file:// access breaking traces to bulk --update-snapshots accepting regressions. Each has a direct Right answer. Use as a pre-review checklist."
---

# Anti-Patterns

## When to Use

> As a checklist before committing a Playwright config or sharing a report.

## Wrong vs Right

- **Wrong**: opening `index.html` via `file://` → **Right**: `show-report` or any HTTP server
- **Wrong**: committing `playwright-report/` to git → **Right**: `.gitignore` it
- **Wrong**: assuming reports auto-archive across runs → **Right**: every run overwrites; copy/zip if you want archives
- **Wrong**: `trace: 'on'` in CI → **Right**: `'on-first-retry'` keeps disk under control
- **Wrong**: triage from terminal output → **Right**: open the report; the slider is the triage tool
- **Wrong**: bulk `--update-snapshots` after seeing red → **Right**: scoped `--update-snapshots --grep "<title>"`
- **Wrong**: `attachmentsBaseURL: 'https://cdn.example.com/runs/123'` (no trailing slash) → **Right**: trailing slash always
- **Wrong**: extracting `trace.zip` before opening → **Right**: keep zip intact; viewer expects archive
- **Wrong**: `host: 'localhost'` inside DDEV → **Right**: `0.0.0.0` so the host can reach
- **Wrong**: missing `if: always()` on artifact upload → **Right**: always upload; failures are the runs you most need to triage
- **Wrong**: `playwright-report/` and `test-results/` confusion → **Right**: report has the SPA + bundled attachments; test-results has raw per-test artifacts; report is what you ship
- **Wrong**: using only `list` reporter and skipping `html` → **Right**: always include `html`; combine with others

## See Also

- [Overview](pw-report-overview.md)
- [Viewing](pw-report-viewing.md)
- [Running Modes](pw-report-running-modes.md)
- [Baseline Updates](pw-report-baseline-updates.md)
- [Sharing](pw-report-sharing.md)
