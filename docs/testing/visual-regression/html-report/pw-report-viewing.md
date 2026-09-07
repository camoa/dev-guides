---
description: "How to open and view a generated Playwright HTML report locally, in DDEV, or in CI."
tldr: "Use `npx playwright show-report` to open reports — never open index.html via file:// as it breaks the trace viewer. The command starts a static HTTP server at localhost:9323. On failure, the report auto-opens locally; in CI (CI=true) it never auto-opens."
---

# Viewing Reports

## When to Use

> Opening a generated report to triage failures.

## Pattern: Open Latest Report

```bash
npx playwright show-report
```

Defaults to `http://localhost:9323`.

## Pattern: Open Specific Report

```bash
npx playwright show-report ./playwright-report
npx playwright show-report ./reports/run-2026-05-08
```

## Pattern: Change Port / Host

```bash
npx playwright show-report --port 8080
npx playwright show-report --host 0.0.0.0     # bind on all interfaces (LAN sharing)
```

## Why a Real HTTP Server?

`show-report` starts a small static server. This is required because traces and some XHR-loaded attachments need correct MIME types and same-origin fetches. **Opening `index.html` via `file://` breaks** the trace viewer iframe.

## Auto-Open Behavior

| Context | Default |
|---|---|
| Local, run failed | Auto-opens browser to the report |
| Local, run passed | Doesn't open |
| CI (`CI=true`) | Doesn't open |

## Environment Variables (override config without editing)

| Var | Purpose |
|---|---|
| `PLAYWRIGHT_HTML_REPORT` | Override `outputFolder` |
| `PLAYWRIGHT_HTML_OPEN` | `always` \| `never` \| `on-failure` |
| `PLAYWRIGHT_HTML_HOST` | Bind host |
| `PLAYWRIGHT_HTML_PORT` | Bind port |

## Common Mistakes

- **Opening `index.html` via `file://`** — trace viewer breaks; always use `show-report` or another HTTP server
- **Port `9323` collision** — error message is explicit; use `--port` or `PLAYWRIGHT_HTML_PORT`
- **`show-report` from wrong cwd** — opens an old report from elsewhere; always pass an explicit path

## See Also

- [Generation](pw-report-generation.md)
- [Running Modes](pw-report-running-modes.md)
- [Sharing](pw-report-sharing.md)
