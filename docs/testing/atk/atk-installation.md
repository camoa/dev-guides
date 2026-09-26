---
description: "Installing ATK 2.1.0-beta5 with the demo recipe or on an existing site, and the resulting Playwright/Cypress layout."
tldr: "Install with the demo recipe on a fresh site (needs minimum-stability dev for performant-labs/qa_accounts:dev-main), or install drupal/qa_accounts:^1.1 yourself on an existing site, then run module_support/atk_setup playwright and npm install. Test sites only."
drupal_version: "11.x"
---

# ATK Installation

## When to Use

> Initial install of ATK on a Drupal 11 site.

## Pattern: install with the demo recipe (fresh site)

> **Test sites only.** Never enable ATK or `qa_accounts` on a production site. See [ATK Overview](atk-overview.md) for why.

The recipe requires `performant-labs/qa_accounts: dev-main`. Packagist serves it, from `github.com/Performant-Labs/qa_accounts`. A `dev-main` requirement needs `minimum-stability dev` (or `@dev`) in your root `composer.json`.

```bash
composer config minimum-stability dev
composer require 'drupal/automated_testing_kit:2.1.0-beta5' 'drupal/automated_testing_kit_demo_recipe:^2.1@beta'
drush recipe ../recipes/automated_testing_kit_demo_recipe
```

The `drush recipe` path is the vendor docs' form. The recipe is `type: drupal-recipe`, so Composer installs it under `recipes/`, not `modules/contrib/`. The 2.1 recipe:

- Installs ATK, `automated_testing_kit_demo`, `qa_accounts`, `webform`, `xmlsitemap`, `feeds`, `pathauto`, `redirect`, `token`, `admin_toolbar`, `autologout`, `session_management`, `login_security` and `contact_block`
- Imports demo nodes, a `contact` webform and a `private_file_test` content type
- Sets 403/404 pages to `/403-error-page` and `/404-error-page`, and lets visitors register

On `RecipeAppliedEvent`, the demo submodule then:

- Runs `atk_setup playwright` with `ATK_HOME=..`
- Sets `drushCmd` to `ddev drush` and `baseURL` to the current host
- Creates `../private` and points `file_private_path` at it
- Rebuilds caches and runs cron

It assumes DDEV and Playwright (`RecipeEventSubscriber.php`).

## Pattern: install on an existing site

ATK's `composer.json` requires only PHP, so require `qa_accounts` yourself. The drupal.org package `drupal/qa_accounts` 8.x-1.1 (2026-01-26) supports core `^9.5 || ^10 || ^11`. It creates one `qa_<role>` account per role, with the password equal to the username. That matches `qaUsers.json`.

```bash
composer require 'drupal/automated_testing_kit:2.1.0-beta5' 'drupal/qa_accounts:^1.1'
drush en automated_testing_kit qa_accounts
web/modules/contrib/automated_testing_kit/module_support/atk_setup playwright   # or: cypress
npm install
npx playwright install
```

Run `atk_setup` from the project root. Its second argument is `link` to symlink instead of copy, or `back` to copy tests back into the module. `ATK_HOME` sets the target directory (default `.`).

## Resulting Layout (Playwright)

```
<ATK_HOME>/
├── package.json               # from module_support/development/playwright.package.json
├── playwright.config.js       # testDir './tests', setup project, atk_reporter
├── playwright.atk.config.js   # drushCmd, routes, email, pantheon, targetSite, tugboat
└── tests/
    ├── atk_*/                 # the catalog
    ├── data/                  # qaUsers.json, preflightTests.yml, fixtures
    └── support/               # atk_commands.js, atk_utilities.js, atk_reporter.js
```

For Cypress, the tests go to `cypress/e2e/`, data to `cypress/data/` and support to `cypress/support/`. The config files still land at `ATK_HOME`.

Individual tests need more modules; enable only those for the suites you run (see [Test Catalog](atk-test-catalog.md)).

## Common Mistakes

- **Running `drush recipe modules/contrib/...`** — the recipe lives in `recipes/`
- **Leaving `minimum-stability` at `stable` for the recipe** — Composer rejects `performant-labs/qa_accounts: dev-main`
- **Installing both `drupal/qa_accounts` and `performant-labs/qa_accounts`** — they share the module machine name `qa_accounts`; pick one
- **Installing on production** — never; see [ATK Overview](atk-overview.md)
- **Skipping the target URL** — `baseURL` in `playwright.config.js` is hardcoded to ATK's own dev host until you change it
- **Assuming host-only runs** — the README supports native, host-against-container and in-container runs

## See Also

- [Versions & Compatibility](atk-versions.md)
- [Runner Configuration](atk-runner-config.md)
- [Playwright for Visual Regression — Setup](../visual-regression/playwright/pw-vr-setup.md)
- Reference: https://www.drupal.org/project/automated_testing_kit_demo_recipe
