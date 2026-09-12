---
description: "How to run and view Playwright HTML reports in local, DDEV, and CI environments."
tldr: "Local runs auto-open the report on failure. In DDEV, run show-report on the host (not in the container) since playwright-report/ is on the bind-mounted volume. In CI, upload as an artifact with if:always() and set open:'never'."
---

# Running Modes

## When to Use

> Running reports in your specific environment.

## Local (Host Machine)

```bash
npx playwright test                    # report auto-opens on failure
```

Triage in browser at `http://localhost:9323`.

## DDEV (or Any Container)

Tests run inside the container; `playwright-report/` lives on the bind-mounted project volume, so the host's browser can serve it.

**Easiest path**: don't run `show-report` *in* the container. Just open the report from the host:

```bash
cd $PROJECT_DIR
npx playwright show-report
```

The host needs Playwright installed (`npm i -D @playwright/test` at minimum), but no browsers required.

**Alternative**: run `show-report` inside the container with `--host 0.0.0.0` and expose the port. In `.ddev/config.yaml`:

```yaml
web_extra_exposed_ports:
  - name: playwright-report
    container_port: 9323
    http_port: 9323
```

## CI (GitHub Actions, GitLab, etc.)

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

Triage flow: download artifact → unzip → `npx playwright show-report ./playwright-report`.

Set `open: 'never'` (or rely on `CI=true` auto-detection). Use `trace: 'on-first-retry'` to keep traces only when needed.

## Decision

| Environment | Approach |
|---|---|
| Local | `npx playwright test` — report auto-opens on failure at `localhost:9323` |
| DDEV | Run `show-report` on the host, not inside the container |
| CI | Upload artifact with `if: always()`; set `open: 'never'` |

## Common Mistakes

- **Trying to bind `localhost` inside DDEV and access from host** — host can't reach container's localhost; bind to `0.0.0.0`
- **Forgetting `if: always()` on artifact upload** — failed runs don't upload; you can't triage
- **Setting `open: 'always'` in CI** — wastes a browser launch; use `'never'`

## See Also

- [Viewing](pw-report-viewing.md)
- [Sharing](pw-report-sharing.md)
- [Configuration Reference](pw-report-configuration.md)
