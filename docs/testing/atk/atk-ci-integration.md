---
description: Running ATK in CI — GitHub Actions + DDEV canonical pattern, Tugboat preview environments, and Pantheon SSH Drush invocation.
tldr: The canonical CI pattern is ddev/github-action-setup-ddev + composer install + demo recipe + preflight + playwright test. There is no ddev-atk addon. Always pass --with-deps to playwright install in CI and upload the report artifact with if: always().
drupal_version: "11.x"
---

# ATK CI Integration

## When to Use

> Use this guide when running ATK in continuous integration (GitHub Actions, Tugboat, Pantheon).

## Decision

| Environment | CI strategy |
|---|---|
| Local dev | DDEV + ATK + tests run via `ddev exec` (or host) |
| Per-PR (GitHub) | github-action-setup-ddev + smoke subset of tests |
| Nightly (GitHub) | github-action-setup-ddev + full ATK + project tests |
| Preview env (Tugboat) | Tugboat init runs ATK pre-flight; CI runs tests against Tugboat URL |
| Pantheon staging/test | SSH Drush invocation; tests run from CI runner |

## Pattern

### GitHub Actions + DDEV (canonical 2026 shape)

```yaml
# .github/workflows/atk.yml
name: ATK E2E

on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup DDEV
        uses: ddev/github-action-setup-ddev@v1
        with:
          autostart: false

      - name: Start DDEV
        run: ddev start

      - name: Install Drupal
        run: ddev composer install

      - name: Apply demo recipe
        run: ddev drush recipe modules/contrib/automated_testing_kit_demo_recipe

      - name: Pre-flight check
        run: ddev drush atk:preflight

      - name: Install Playwright
        working-directory: tests/playwright
        run: |
          npm ci
          npx playwright install --with-deps

      - name: Run ATK tests
        working-directory: tests/playwright
        env:
          DDEV_PRIMARY_URL: https://my-site.ddev.site
        run: npx playwright test

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: tests/playwright/playwright-report/
          retention-days: 30
```

There is no `ddev-atk` addon. Use `ddev/github-action-setup-ddev` + ATK module install. For Playwright in DDEV, `Lullabot/ddev-playwright` is a separate optional addon.

### Tugboat (preview environments, 2.1+)

```yaml
# .tugboat/config.yml
services:
  php:
    image: tugboatqa/php:8.3-apache
    default: true
    commands:
      init:
        - composer install
        - drush si --existing-config -y
        - drush recipe modules/contrib/automated_testing_kit_demo_recipe
        - drush testor:pull tugboat-base
      build:
        - drush atk:preflight
```

Then trigger an ATK run from your CI workflow against the Tugboat URL.

### Pantheon (SSH Drush)

```js
// atk.config.js
export default {
  baseUrl: 'https://test-mysite.pantheonsite.io',
  drushCmd: 'terminus drush mysite.test --',
};
```

## Common Mistakes

- **Wrong**: Looking for a `ddev-atk` addon → **Right**: doesn't exist; use the canonical pattern
- **Wrong**: Forgetting `--with-deps` on `playwright install` in CI → **Right**: fonts/system libs missing; tests fail
- **Wrong**: Not uploading the report on failure → **Right**: use `if: always()` + artifact upload; otherwise CI failures are unreviewable
- **Wrong**: Running pre-flight against production → **Right**: pre-flight is for test environments only

## See Also

- [Pre-flight Checks](atk-preflight.md)
- [Runner Configuration](atk-runner-config.md)
- [Testor Snapshots](atk-testor.md)
- Reference: https://github.com/ddev/github-action-setup-ddev
