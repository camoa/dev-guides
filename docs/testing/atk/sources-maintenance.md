---
description: "Source references and maintenance manifest for the atk guides — web sources, code sources read at tag, and version history"
---

# Sources & Maintenance

## Web Sources
| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Drupal.org project page | https://www.drupal.org/project/automated_testing_kit | 1, 2, 18 | 2026-09-24 |
| Release feed (updates.drupal.org) | https://updates.drupal.org/release-history/automated_testing_kit/current | 2, 4, 14 | 2026-09-24 |
| Releases page | https://www.drupal.org/project/automated_testing_kit/releases | 4, 18 | 2026-09-24 |
| Demo recipe project page | https://www.drupal.org/project/automated_testing_kit_demo_recipe | 5, 18 | 2026-09-24 |
| qa_accounts project page and release feed (8.x-1.1) | https://www.drupal.org/project/qa_accounts | 5, 6, 18 | 2026-09-24 |
| Packagist `performant-labs/qa_accounts` | https://packagist.org/packages/performant-labs/qa_accounts | 5 | 2026-09-24 |
| Vendor docs (Performant Labs) | https://performantlabs.com/automated-testing-kit/ | 5, 18 | 2026-09-24 |
| Lullabot/playwright-drupal README and `src/testcase/visualdiff.ts` | https://github.com/Lullabot/playwright-drupal | 2, 16, 18 | 2026-09-24 |
| Lullabot/ddev-playwright | https://github.com/Lullabot/ddev-playwright | 13, 18 | 2026-09-24 |
| ddev/github-action-setup-ddev `action.yml` (`autostart` default `true`) | https://github.com/ddev/github-action-setup-ddev | 13, 18 | 2026-09-24 |
| Drupal core issue #3467492 (Replace Nightwatch with Playwright) | https://www.drupal.org/project/drupal/issues/3467492 | 2, 18 | 2026-09-01 |
| Drupal core issue #3553673 (Nightwatch to Playwright migration) | https://www.drupal.org/project/drupal/issues/3553673 | 2 | 2026-09-01 |

## Code Sources
Read from source at tags, not from an installed site.

| Repository | Ref | Files read | Guide Sections |
|--------|-----|------------|----------------|
| https://git.drupalcode.org/project/automated_testing_kit | tag `2.1.0-beta5` (f479758) | `automated_testing_kit.info.yml`, `.module`, `.routing.yml`, `.services.yml`, `composer.json`, `CHANGELOG.txt`, `README.md`; `src/Drush/Commands/AutomatedTestingKitDrushCommands.php`; `src/Controller/TestDataController.php`; `data/preflightTests.yml`, `data/qaUsers.json`; `module_support/atk_setup`, `playwright.config.js`, `playwright.atk.config.js`, `cypress.config.js`, `cypress.atk.config.js`, `development/*.package.json`; `playwright/support/*.js`; `cypress/support/*.js`; every `playwright/e2e/` and `cypress/e2e/` spec (titles, tags, setup comments); `automated_testing_kit_demo/`; `.tugboat/config.yml`; `.github/workflows/test-tugboat-preview-gha-pw.yml` | 1–18 |
| https://git.drupalcode.org/project/automated_testing_kit | tag `2.0.0` | Diffed against 2.1.0-beta5: `data/atk_prerequisites.yml`, `playwright/support/atk_commands.js`, `module_support/playwright.config.js`, `playwright.atk.config.js`, Drush commands, e2e directories | 4 |
| https://git.drupalcode.org/project/automated_testing_kit_demo_recipe | tags `2.1.0-beta4`, `2.0.0` | `composer.json`, `recipe.yml`, `README.md`, `config/` | 5, 14 |
| https://git.drupalcode.org/project/qa_accounts | tag `8.x-1.1` | `qa_accounts.info.yml`, `composer.json`, `src/QaAccountsCreateDelete.php` | 5, 6 |
| https://github.com/Performant-Labs/testor | `main` (2f532c3, CHANGELOG 1.11.3) | `README.md`, `src/Robo/Plugin/Commands/TestorCommands.php`, `src/Robo/Common/TestorConfig.php`, `src/Robo/Task/Testor/TestorConfigInit.php`, `TestorCustomCommand.php`, `TugboatPreviewSet.php`, `DbSanitize.php` | 12, 13 |

## Version History
| Date | Change |
|------|--------|
| 2026-05-08 | Manifest reconstructed from the guide's own citations. |
| 2026-09-24 | Rewritten against ATK 2.1.0-beta5 source. Removed invented identifiers (`drush atk:preflight`, `drush testor:*`, `data-qa-id`, `loginAsRole` and other helpers, `atk.config.js`, `js-helpers/`, `tests/playwright/`). Added the 2.0.0 differences table. Testor rewritten from its own repository. |
| 2026-09-24 | Review corrections: FedRAMP file count, test IDs and tags, `qa_accounts` install paths, production warning, Testor sanitise and restore behaviour, `atk_setup back` scope. |
| 2026-09-24 | Partitioned into the 18 atomic guides + index from the rewritten source (commit 41b0d68); all partition slugs unchanged. |
