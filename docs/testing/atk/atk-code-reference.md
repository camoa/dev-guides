---
description: ATK code reference — project URLs, key module files, Drush commands, and adjacent projects.
tldr: Canonical source is git.drupalcode.org/project/automated_testing_kit (not GitHub). Key files are automated_testing_kit.module (selector hooks), atk_prerequisites.yml (preflight), js-helpers/ (test helpers), and src/Commands/TestorCommands.php (snapshot Drush). Verify Drush command names with drush list on your install.
drupal_version: "11.x"
---

# ATK Code Reference

## When to Use

> Use this guide when you need to find services, module files, Drush commands, or adjacent project URLs.

## Pattern

### Project URLs

| Resource | URL |
|---|---|
| Drupal.org project | https://www.drupal.org/project/automated_testing_kit |
| Releases | https://www.drupal.org/project/automated_testing_kit/releases |
| Canonical repo | https://git.drupalcode.org/project/automated_testing_kit |
| Demo recipe | https://www.drupal.org/project/automated_testing_kit_demo_recipe |
| qa_accounts | https://www.drupal.org/project/qa_accounts |
| Vendor docs | https://performantlabs.com/automated-testing-kit/ |

### Key files in the module

| Path | Purpose |
|---|---|
| `automated_testing_kit.module` | Selector hook preprocess implementations |
| `atk_prerequisites.yml` | Pre-flight check definitions |
| `tests/cypress/` | Cypress test catalog |
| `tests/playwright/` | Playwright test catalog |
| `js-helpers/cypress/` | Cypress helper functions |
| `js-helpers/playwright/` | Playwright helper functions |
| `src/Commands/TestorCommands.php` | Drush snapshot commands |
| `composer.json` | Composer metadata + Drupal core constraints |

### Drush commands

| Command | Purpose |
|---|---|
| `drush atk:preflight` | Run pre-flight checks |
| `drush testor:list` | List available snapshots |
| `drush testor:pull <category>` | Pull a snapshot |
| `drush testor:push <category>` | Push current DB as a snapshot |
| `drush testor:snapshot --sanitize` | Create a sanitized snapshot |

Verify exact spelling against `drush list | grep -i atk` — names evolve between releases.

### Adjacent projects

| Project | URL | Relationship |
|---|---|---|
| `Lullabot/playwright-drupal` | https://github.com/Lullabot/playwright-drupal | Alternative Playwright integration; complementary |
| `Lullabot/ddev-playwright` | https://github.com/Lullabot/ddev-playwright | DDEV addon for Playwright in container |
| `ddev/github-action-setup-ddev` | https://github.com/ddev/github-action-setup-ddev | Standard CI pattern for DDEV |
| Drupal core #3467492 | https://www.drupal.org/project/drupal/issues/3467492 | "Replace Nightwatch with Playwright" — ecosystem direction |

## See Also

- [ATK Overview](atk-overview.md)
- [Playwright for Visual Regression](../visual-regression/playwright/index.md)
- [Visual Regression Workflow](../visual-regression/workflow/index.md)
- [Pixelmatch](../visual-regression/pixelmatch/index.md)
- [Playwright HTML Report](../visual-regression/html-report/index.md)
