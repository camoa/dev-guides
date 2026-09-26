---
description: "What ATK ships in 2.1.0-beta5, when to choose it, and the production-only warning that governs every install."
tldr: "Use ATK for ready-made Drupal E2E tests (login, forms, CRUD, menus, search, caching, sitemaps) plus Cypress/Playwright helpers; never enable ATK or qa_accounts on production — it serves data/ files, including qaUsers.json, to anonymous users."
drupal_version: "11.x"
---

# ATK Overview

## When to Use

> Use ATK when you want **ready-made Drupal end-to-end tests** without writing them from scratch. It covers registration and login, contact forms, 403/404 pages, entity CRUD, menus, search, caching and sitemaps. You add project-specific tests on top.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Ready-made Drupal E2E tests + helpers | ATK | Ships tests for both Cypress and Playwright |
| Parallel Playwright tests on isolated SQLite sites | Lullabot/playwright-drupal | Test infrastructure, no test catalog |
| Tests that stay in PHP | Core's PHPUnit FunctionalJavascript | No JS runner needed |
| Visual regression | Playwright `toHaveScreenshot()` | ATK ships no VR code; see the VR guides |
| FedRAMP-oriented tests | ATK 2.1.0-beta | `atk_fedramp/` exists only on the 2.1 line |
| Drupal CMS 2.x | ATK 3.0.0-alpha | The 3.0 CHANGELOG targets Drupal CMS 2.x |

## Pattern

ATK spans **two drupal.org projects** and one submodule:

- `automated_testing_kit`: the module. It holds the tests (`playwright/e2e/`, `cypress/e2e/`), helpers (`playwright/support/`, `cypress/support/`), data fixtures (`data/`), Drush commands and the `module_support/atk_setup` script.
- `automated_testing_kit_demo_recipe`: a Drupal recipe that installs the modules and content the shipped tests expect.
- `automated_testing_kit_demo`: a submodule inside ATK. The recipe enables it, and it runs `atk_setup playwright` when the recipe is applied.

ATK does not bundle the runner. Its `atk_setup` script copies ATK's own `package.json` into your project, and you then run `npm install`.

## What Ships in the Box (2.1.0-beta5)

| Component | Where |
|---|---|
| 39 Playwright test declarations in 18 spec files (38 active, `ATK-PW-1011` skipped; 40 run — `1231` and `1234` each loop over two URLs), plus one setup test | `playwright/e2e/atk_*/` |
| 37 Cypress test declarations in 17 spec files (36 active, `ATK-CY-1011` skipped) | `cypress/e2e/atk_*/` |
| 27 Playwright helpers; 26 Cypress custom commands | `*/support/atk_commands.js` |
| Two preprocess hooks exposing entity IDs | `automated_testing_kit.module` |
| Pre-flight check, defined in YAML | `data/preflightTests.yml` |
| Drush commands `file:properties`, `file:create` | `src/Drush/Commands/AutomatedTestingKitDrushCommands.php` |
| Test account fixture (`qa_administrator`, `qa_authenticated`) | `data/qaUsers.json` |
| Email checks via Mailpit or testmail.app | `expectEmail()`; `email` block in `*.atk.config.js` |
| Playwright log-level reporter | `playwright/support/atk_reporter.js` |
| Setup script | `module_support/atk_setup` |

The test accounts come from the separate `qa_accounts` module, which the pre-flight requires.

Counts are test declarations, not runtime executions. Playwright declares 39 (38 active, `ATK-PW-1011` skipped); `1231` and `1234` each loop over two URLs, so 40 Playwright tests run. Cypress declares 37, including the skipped `ATK-CY-1011` (36 active).

> **Test sites only.** Never enable ATK or `qa_accounts` on a production site. ATK's route `/automated-testing-kit/test-data/{filename}` has `_access: 'TRUE'`. It serves every file in the module's `data/` directory to anonymous users, including `qaUsers.json` with its passwords. `qa_accounts` creates accounts whose password equals the username, and its own description says never to enable it in production.

## Common Mistakes

- **Treating ATK as a runner** — it is tests plus helpers; Cypress or Playwright still runs them
- **Confusing Lullabot/playwright-drupal with ATK** — different projects; ATK has the catalog, Lullabot's package has the isolation infrastructure
- **Expecting visual regression out of the box** — ATK has none; layer Playwright's own API on top
- **Expecting Testor inside ATK** — Testor is a separate tool
- **Enabling ATK or `qa_accounts` in production** — it exposes test data and creates accounts with known passwords

## See Also

- [Ecosystem & Alternatives](atk-ecosystem.md)
- [Cypress vs Playwright](atk-cypress-vs-playwright.md)
- [Testor Snapshots](atk-testor.md)
- [Visual Regression Layering](atk-visual-regression-layering.md)
- Reference: https://www.drupal.org/project/automated_testing_kit
