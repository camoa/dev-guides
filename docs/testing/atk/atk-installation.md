---
description: Installing ATK — the Drupal module, the demo recipe, the JS runner, and copying the test catalog into your project.
tldr: Install the module and qa_accounts companion, apply the demo recipe so shipped tests have the expected content and users, then install Cypress or Playwright separately in a sandboxed subdirectory. ATK does not bundle the runner.
drupal_version: "11.x"
---

# ATK Installation

## When to Use

> Use this guide for the initial install of ATK on a Drupal site.

## Decision

| Step | Required | Why |
|---|---|---|
| `automated_testing_kit` module + `qa_accounts` | Yes | Core module + test user seed |
| Demo recipe | Strongly recommended | Ships tests fail without expected content/users |
| Runner (Cypress or Playwright) | Yes | ATK doesn't bundle a runner |
| Copy test catalog to project | Yes | Tests live in the module; copy or symlink to runner project |

## Pattern

### Install the module

```bash
composer require 'drupal/automated_testing_kit:^2.0'
drush en automated_testing_kit qa_accounts
```

`qa_accounts` pre-seeds test users so ATK's login tests have predictable accounts.

### Apply the demo recipe (optional but recommended)

```bash
composer require 'drupal/automated_testing_kit_demo_recipe:^2.0'
drush recipe modules/contrib/automated_testing_kit_demo_recipe
drush cache:rebuild
```

The recipe creates sample content types, example nodes, QA test accounts in expected roles, and pre-configured permissions. For a fresh site, this makes the shipped tests run green out of the box.

### Install the runner

ATK does not bundle the JS test runner. Install separately in a sandboxed sub-tree:

```
<repo>/
├── composer.json
├── web/
└── tests/playwright/
    ├── package.json
    ├── playwright.config.js
    └── e2e/
```

```bash
cd tests/playwright
npm init -y
npm install -D @playwright/test
npx playwright install --with-deps
```

For Cypress:

```bash
cd tests/cypress
npm install -D cypress
```

### Copy the test catalog

```bash
# Tests
cp -R web/modules/contrib/automated_testing_kit/tests/playwright/* tests/playwright/e2e/atk/

# Helpers
cp -R web/modules/contrib/automated_testing_kit/js-helpers/playwright/* tests/playwright/helpers/
```

Some teams import directly via path aliases instead of copying — either pattern works.

### Compatibility

| Aspect | Value |
|---|---|
| Drupal core | `^11.0 \|\| <12` for ATK 2.x |
| PHP | 8.3+ |
| Drush | 12.x+ |
| Node.js | 20.x LTS+ |

## Common Mistakes

- **Wrong**: Installing only the module without the runner → **Right**: the module's tests don't run themselves
- **Wrong**: Skipping the demo recipe → **Right**: shipped tests fail because the site has no users/content matching the test fixtures
- **Wrong**: Running tests inside the Drupal container → **Right**: ATK's pattern is host-side runner targeting container-side site

## See Also

- [Versions & Compatibility](atk-versions.md)
- [Runner Configuration](atk-runner-config.md)
- [Playwright for Visual Regression — Setup](../visual-regression/playwright/pw-vr-setup.md)
- Reference: https://www.drupal.org/project/automated_testing_kit_demo_recipe
