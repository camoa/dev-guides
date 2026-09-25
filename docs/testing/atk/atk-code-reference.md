---
description: "ATK 2.1.0-beta5 file reference — project URLs, key module files, the only two Drush commands, and adjacent projects."
tldr: "Canonical source is git.drupalcode.org/project/automated_testing_kit, not GitHub — PerformantLabs' own atk-cypress/atk-playwright repos 404. ATK defines exactly two Drush commands, file:properties and file:create; check drush list --filter=file to confirm on your install."
drupal_version: "11.x"
---

# ATK Code Reference

## When to Use

> Finding module files, Drush commands or adjacent project URLs.

## Project URLs

| Resource | URL |
|---|---|
| Drupal.org project | https://www.drupal.org/project/automated_testing_kit |
| Releases | https://www.drupal.org/project/automated_testing_kit/releases |
| Canonical repo | https://git.drupalcode.org/project/automated_testing_kit |
| Demo recipe | https://www.drupal.org/project/automated_testing_kit_demo_recipe |
| qa_accounts (drupal.org) | https://www.drupal.org/project/qa_accounts |
| qa_accounts (used by the demo recipe) | https://github.com/Performant-Labs/qa_accounts |
| Testor | https://github.com/Performant-Labs/testor |
| Vendor docs | https://performantlabs.com/automated-testing-kit/ |

## Key Files in the Module (2.1.0-beta5)

| Path | Purpose |
|---|---|
| `automated_testing_kit.module` | `preprocess_html` (body classes) and `preprocess_image` (`data-media-id`) |
| `automated_testing_kit.info.yml` | `core_version_requirement: ">=11.0 <12"` |
| `composer.json` | `php: >=8.3` |
| `src/Drush/Commands/AutomatedTestingKitDrushCommands.php` | `file:properties`, `file:create` |
| `src/Controller/TestDataController.php` + `automated_testing_kit.routing.yml` | Serves `data/` files at `/automated-testing-kit/test-data/{filename}` with `_access: 'TRUE'`, so anonymous users can read them, `qaUsers.json` included. Test sites only |
| `data/preflightTests.yml` | Pre-flight entries |
| `data/qaUsers.json` | Test accounts |
| `playwright/e2e/atk_*/`, `playwright/e2e/atk_setup/` | Playwright catalog and setup project |
| `cypress/e2e/atk_*/` | Cypress catalog |
| `playwright/support/atk_commands.js`, `atk_utilities.js`, `atk_reporter.js` | Playwright helpers and reporter |
| `cypress/support/atk_commands.js`, `atk_utilities.js`, `e2e.js` | Cypress commands, utilities, pre-flight hook |
| `module_support/atk_setup` | Copies or links tests, data, support and config into the project |
| `module_support/playwright.config.js`, `playwright.atk.config.js` | Playwright config templates |
| `module_support/cypress.config.js`, `cypress.atk.config.js` | Cypress config templates |
| `module_support/development/*.package.json` | Runner dependency lists |
| `automated_testing_kit_demo/src/EventSubscriber/RecipeEventSubscriber.php` | Post-recipe setup |

## Drush Commands

| Command | Purpose |
|---|---|
| `drush file:properties <filepath>` (alias `fprop`) | File directory, name, size and timestamps |
| `drush file:create <filepath> [--size=30] [--permissions=0600]` | Creates a test file; used by FedRAMP access tests (2.1 only) |

These are the only Drush commands ATK defines. Check with `drush list --filter=file`.

## Adjacent Projects

| Project | URL | Relationship |
|---|---|---|
| `Lullabot/playwright-drupal` | https://github.com/Lullabot/playwright-drupal | Playwright infrastructure for Drupal; complementary |
| `Lullabot/ddev-playwright` | https://github.com/Lullabot/ddev-playwright | DDEV addon for Playwright in the container |
| `ddev/github-action-setup-ddev` | https://github.com/ddev/github-action-setup-ddev | DDEV in GitHub Actions |
| Drupal core #3467492 | https://www.drupal.org/project/drupal/issues/3467492 | Policy to replace Nightwatch with Playwright (accepted November 2025) |

## See Also

- [Playwright for Visual Regression](../visual-regression/playwright/index.md) — the runner ATK drives; setup, config, screenshot APIs, Drupal/DDEV
- [Visual Regression Workflow](../visual-regression/workflow/index.md) — procedure for layering VR on top of ATK
- [Pixelmatch Image Diff](../visual-regression/pixelmatch/index.md) — diff engine internals
- [Playwright HTML Report](../visual-regression/html-report/index.md) — triage UI for both VR diffs and functional test failures
