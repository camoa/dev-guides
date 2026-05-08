---
description: Consolidated list of anti-patterns to avoid when working with the Playwright HTML report.
tldr: The twelve most common HTML report mistakes — from file:// access breaking traces to bulk --update-snapshots accepting regressions. Each has a direct Right answer. Use as a pre-review checklist.
---

# Anti-Patterns

## When to Use

> Use this as a checklist before committing a Playwright config or sharing a report.

## Wrong vs Right

| Wrong | Right |
|---|---|
| Opening `index.html` via `file://` | `show-report` or any HTTP server — `file://` breaks trace viewer |
| Committing `playwright-report/` to git | Add to `.gitignore`; it's regeneratable |
| Assuming reports auto-archive across runs | Every run overwrites; copy/zip if you want archives |
| `trace: 'on'` in CI | `'on-first-retry'` — keeps disk under control |
| Triaging from terminal output | Open the report; the slider is the triage tool |
| Bulk `--update-snapshots` after seeing red | Scoped `--update-snapshots --grep "<title>"` |
| `attachmentsBaseURL` without trailing slash | Trailing slash always — URL concatenation breaks |
| Extracting `trace.zip` before opening | Keep zip intact; viewer expects the archive |
| `host: 'localhost'` inside DDEV | `'0.0.0.0'` so the host can reach the container |
| Missing `if: always()` on artifact upload | Always upload — failures are the runs you most need to triage |
| Confusing `playwright-report/` with `test-results/` | Report = SPA + bundled attachments; test-results = raw per-test artifacts; report is what you ship |
| Using only `list` reporter and skipping `html` | Always include `html`; combine with others |

## See Also

- [Overview](pw-report-overview.md)
- [Viewing](pw-report-viewing.md)
- [Running Modes](pw-report-running-modes.md)
- [Baseline Updates](pw-report-baseline-updates.md)
- [Sharing](pw-report-sharing.md)
