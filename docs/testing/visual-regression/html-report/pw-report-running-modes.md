---
description: How to run and view Playwright HTML reports in local, DDEV, and CI environments.
tldr: Local runs auto-open the report on failure. In DDEV, run show-report on the host (not in the container) since playwright-report/ is on the bind-mounted volume. In CI, upload as an artifact with if:always() and set open:'never'.
---

# Running Modes

## When to Use

> Use this when you need environment-specific configuration for viewing reports — local machine, DDEV container, or CI pipeline.

## Decision

| Environment | Approach |
|---|---|
| Local | `npx playwright test` — report auto-opens on failure at `localhost:9323` |
| DDEV | Run `show-report` on the host, not inside the container |
| CI | Upload artifact with `if: always()`; set `open: 'never'` |

## Pattern

Local:

```bash
npx playwright test     # report auto-opens on failure
```

DDEV — run on host (simplest):

```bash
cd $PROJECT_DIR
npx playwright show-report
```

The host needs `@playwright/test` installed but no browsers.

DDEV — run inside container with port exposure (`.ddev/config.yaml`):

```yaml
web_extra_exposed_ports:
  - name: playwright-report
    container_port: 9323
    http_port: 9323
```

Then inside container: `npx playwright show-report --host 0.0.0.0`

CI (GitHub Actions):

```yaml
- name: Run Playwright
  run: npx playwright test
- name: Upload report
  uses: actions/upload-artifact@v4
  if: always()
  with:
    name: playwright-report
    path: playwright-report/
    retention-days: 30
```

Set `open: 'never'` or rely on `CI=true` auto-detection. Use `trace: 'on-first-retry'` to limit trace size.

## Common Mistakes

- **Wrong**: binding `localhost` inside DDEV and trying to access from host → **Right**: host can't reach container's localhost; use `0.0.0.0`
- **Wrong**: missing `if: always()` on artifact upload → **Right**: failed runs don't upload; you can't triage
- **Wrong**: `open: 'always'` in CI → **Right**: wastes a browser launch; use `'never'`

## See Also

- [Viewing](pw-report-viewing.md)
- [Sharing](pw-report-sharing.md)
- [Configuration Reference](pw-report-configuration.md)
