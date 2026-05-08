---
description: How to open and view a generated Playwright HTML report locally, in DDEV, or in CI.
tldr: Use `npx playwright show-report` to open reports — never open index.html via file:// as it breaks the trace viewer. The command starts a static HTTP server at localhost:9323. On failure, the report auto-opens locally; in CI (CI=true) it never auto-opens.
---

# Viewing Reports

## When to Use

> Use `npx playwright show-report` when opening a generated report to triage failures. Never open `index.html` directly via `file://`.

## Decision

| Context | Default behavior |
|---|---|
| Local, run failed | Auto-opens browser to the report |
| Local, run passed | Does not auto-open |
| CI (`CI=true`) | Does not auto-open |

## Pattern

Open latest report:

```bash
npx playwright show-report
```

Open specific report:

```bash
npx playwright show-report ./playwright-report
npx playwright show-report ./reports/run-2026-05-08
```

Change port or bind interface:

```bash
npx playwright show-report --port 8080
npx playwright show-report --host 0.0.0.0     # bind on all interfaces (LAN sharing)
```

## Environment Variables

| Var | Purpose |
|---|---|
| `PLAYWRIGHT_HTML_REPORT` | Override `outputFolder` |
| `PLAYWRIGHT_HTML_OPEN` | `always` \| `never` \| `on-failure` |
| `PLAYWRIGHT_HTML_HOST` | Bind host |
| `PLAYWRIGHT_HTML_PORT` | Bind port |

## Common Mistakes

- **Wrong**: opening `index.html` via `file://` → **Right**: trace viewer breaks; always use `show-report` or another HTTP server
- **Wrong**: port `9323` collision with no error handling → **Right**: use `--port` or `PLAYWRIGHT_HTML_PORT` to override
- **Wrong**: running `show-report` from the wrong cwd and getting an old report → **Right**: always pass an explicit path

## See Also

- [Generation](pw-report-generation.md)
- [Running Modes](pw-report-running-modes.md)
- [Sharing](pw-report-sharing.md)
