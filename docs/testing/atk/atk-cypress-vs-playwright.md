---
description: "Cypress vs Playwright as the ATK runner — what's shared, what differs, and why Playwright leads for new projects."
tldr: "Pick Playwright for new ATK projects — the larger 2.1 catalog (6 FedRAMP spec files against 4) and core's accepted policy both point that way. Keep Cypress only for an existing suite; ATK ships both catalogs but atk_setup writes package.json per runner, so running both overwrites the first."
drupal_version: "11.x"
---

# Cypress vs Playwright (ATK Runner)

## When to Use

> Picking the runner ATK will drive.

## Decision

| If you... | Pick |
|---|---|
| Have an existing Cypress suite | Cypress (ATK still ships the Cypress catalog) |
| Are starting fresh | Playwright: it has the larger 2.1 catalog, and core's accepted policy picks Playwright. See [Playwright for Visual Regression](../visual-regression/playwright/index.md) for runner setup |
| Want the full FedRAMP set | Playwright (6 FedRAMP spec files against 4 for Cypress) |
| Already use Playwright for visual regression | Playwright (one runner, one set of fixtures) |

## What's the Same Across Runners

| Convention | Cypress | Playwright |
|---|---|---|
| File suffix | `*.cy.js` | `*.spec.js` |
| Test ID | `ATK-CY-NNNN` | `ATK-PW-NNNN` |
| ATK config file | `cypress.atk.config.js` | `playwright.atk.config.js` |
| Drush routing | `drushCmd`, `pantheon`, `targetSite`, `tugboat` keys | Same keys |
| Pre-flight | `preflightTests.yml` | Same file |
| Test accounts | `data/qaUsers.json` | Same file |

## What Differs

| Concern | Cypress | Playwright |
|---|---|---|
| Helper style | Custom commands: `cy.execDrush(...)` | ES module: `atkCommands.execDrush(...)` |
| Helper location after setup | `cypress/support/` | `tests/support/` |
| Pre-flight trigger | `before()` in `cypress/support/e2e.js` | `preflightTest()` in the `setup` project |
| Login reuse | `cy.session()` inside `cy.logInViaForm()` | `getUserPage()` caches `storageState` files |
| Tag filtering | `@cypress/grep`: `--env grepTags=@smoke` | Built in: `--grep @smoke` |
| Logging | `cypress-log-to-term`, `env.atkLogLevel` | `atk_reporter.js` with a `level` option |
| Pinned runner | `cypress: ^13` | `@playwright/test: ^1.48` |

Both pins come from `module_support/development/*.package.json`, which `atk_setup` copies to your `package.json`.

## Common Mistakes

- **Declaring one runner "better"** — ATK supports both; pick what your team runs
- **Running both runners in one project** — `atk_setup` writes `package.json` at the project root for each, so the second run overwrites the first
- **Assuming tests are 1:1 portable** — helper names mostly match, but signatures and test bodies differ

## See Also

- [Cypress → Playwright Migration](atk-cypress-to-playwright-migration.md)
- [Runner Configuration](atk-runner-config.md)
- [Playwright for Visual Regression](../visual-regression/playwright/index.md)
