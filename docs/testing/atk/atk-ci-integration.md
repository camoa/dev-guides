---
description: "Running ATK in CI — a DDEV/GitHub Actions sketch, Tugboat and Pantheon Drush routing, with no ddev-atk addon and no preflight command."
tldr: "ATK ships no GitHub Actions workflow and no ddev-atk addon — build your own against ddev/github-action-setup-ddev, or route Drush through the tugboat or pantheon config block. Never add a drush atk:preflight CI step; the pre-flight runs inside npx playwright test itself."
drupal_version: "11.x"
---

# ATK CI Integration

## When to Use

> Running ATK in continuous integration.

## Pattern: GitHub Actions + DDEV

ATK ships no GitHub Actions workflow for DDEV. This sketch runs Playwright on the runner host against DDEV, as the demo subscriber configures it (`drushCmd: 'ddev drush'`).

```yaml
# .github/workflows/atk.yml
name: ATK E2E
on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: ddev/github-action-setup-ddev@v1   # autostart defaults to true

      - name: Build the site
        run: |
          ddev composer install
          ddev drush site:install -y
          ddev drush recipe ../recipes/automated_testing_kit_demo_recipe

      - name: Install Playwright
        run: |
          npm install
          npx playwright install --with-deps

      - name: Run ATK tests (pre-flight runs in the setup project)
        run: npx playwright test --grep @smoke

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

`package.json` and `playwright.config.js` sit at `ATK_HOME`, usually the project root. `baseURL` must match the DDEV URL; ATK reads no environment variable for it.

## Pattern: there is no `ddev-atk` addon

ATK ships no DDEV addon. Install it with Composer like any module. For Playwright inside DDEV, **`Lullabot/ddev-playwright`** is a separate addon.

## Pattern: Tugboat (2.1)

ATK routes Drush to a Tugboat preview when `tugboat.isTarget` is `true`. It runs `tugboat shell <service> command="vendor/drush/drush/drush …"`, so the runner needs the Tugboat CLI.

Testor can create the preview and point ATK at it:

```bash
testor preview:create --set       # new preview; rewrites baseURL and the tugboat block
testor preview:set <preview-id>   # point ATK at an existing preview
```

ATK's own `.github/workflows/test-tugboat-preview-gha-pw.yml` creates a preview on `workflow_dispatch`. Its Playwright step is commented out.

## Pattern: Pantheon

```js
// playwright.atk.config.js
pantheon: {
  isTarget: true,
  site: 'mysite',
  environment: 'test',
},
```

```js
// playwright.config.js
use: { baseURL: 'https://test-mysite.pantheonsite.io/' },
```

ATK then runs Drush as `terminus remote:drush mysite.test -- <cmd>`. The runner needs Terminus and its login.

## Decision

| Environment | CI strategy |
|---|---|
| Local dev | DDEV; run Playwright on the host with `drushCmd: 'ddev drush'` |
| Per-PR (GitHub) | setup-ddev + `--grep @smoke` |
| Nightly (GitHub) | setup-ddev + full catalog + project tests |
| Preview env (Tugboat) | `tugboat` block; Testor `preview:create --set` |
| Pantheon test env | `pantheon` block; Terminus on the runner |

## Common Mistakes

- **Adding a `drush atk:preflight` step** — the command does not exist; the pre-flight runs inside `npx playwright test`
- **Using `--no-deps` in CI** — it skips the pre-flight
- **Forgetting `--with-deps`** on `playwright install` — system libraries are missing
- **Not uploading the report on failure** — use `if: always()`

## See Also

- [Runner Configuration](atk-runner-config.md)
- [Testor Snapshots](atk-testor.md)
- [Pre-flight Checks](atk-preflight.md)
- Reference: https://github.com/ddev/github-action-setup-ddev
