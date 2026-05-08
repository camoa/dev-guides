---
description: What ATK is, what ships in the box, and when to choose it over alternatives.
tldr: Use ATK when you need a curated catalog of ~36 Drupal-aware E2E tests plus helpers without writing them from scratch; it provides the test catalog and Drupal-side glue, while you supply the Cypress or Playwright runner. ATK does not include a visual regression layer.
drupal_version: "11.x"
---

# ATK Overview

## When to Use

> Use ATK when you need a curated catalog of Drupal-aware E2E tests (login, content CRUD, role access, page errors) without writing them all from scratch. Use Playwright/Cypress alone when you only need a runner with no pre-built catalog.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Curated Drupal-specific E2E tests + helpers | ATK | Largest catalog of Drupal-aware tests in the contrib ecosystem |
| Just a Playwright runner with parallel SQLite | Lullabot/playwright-drupal | Different philosophy — infrastructure-first, no test catalog |
| Functional tests inside Drupal core | Core's PHPUnit / FunctionalJavascript | Stays inside PHP land; no JS runner needed |
| Visual regression | Playwright (toHaveScreenshot) | ATK doesn't ship a VR layer; see VR guides |
| FedRAMP compliance test pack | ATK 2.1+ (beta) | Only contrib option that ships these specific tests |
| Drupal CMS 2.x support | ATK 3.0-alpha | The 3.0 track is Drupal-CMS-aware |

## Pattern

ATK ships as two coordinated projects on drupal.org:

- `automated_testing_kit` — the module (selector hooks, Drush commands, helper libraries, test catalog)
- `automated_testing_kit_demo_recipe` — a Drupal Recipe that installs sample content + content types + accounts

The runner (Cypress or Playwright) lives in your project's `package.json` — ATK does not bundle the runner.

### What Ships in the Box

| Component | Purpose |
|---|---|
| ~36 ready-to-use tests | Login, content CRUD, role access, page errors, navigation, search, menu, media, forms |
| ~24 helper functions | Login, snapshot management, form interactions, common assertions |
| Selector hooks | Drupal preprocess hooks adding stable test attributes to volatile DOM |
| Pre-flight check mechanism | YAML-defined site-readiness checks before tests run |
| Testor snapshot tool | Drush commands for sanitised DB snapshot storage on S3/SFTP |
| Mailtrap + Testmail helpers | Verify outbound email in tests |
| Custom log-level reporter | Structured log output for CI consumption |
| Companion `qa_accounts` module | Pre-seeds test users for predictable role-based testing |

## Common Mistakes

- **Wrong**: Treating ATK as a runner replacement → **Right**: ATK is a catalog + helpers; install Cypress or Playwright separately
- **Wrong**: Confusing Lullabot/playwright-drupal with ATK → **Right**: different projects, different philosophy; ATK has the curated test catalog, Lullabot's package has the parallel-SQLite infrastructure
- **Wrong**: Expecting visual regression to work out of the box → **Right**: ATK doesn't include a VR layer; layer Playwright's native VR API on top

## See Also

- [Ecosystem & Alternatives](atk-ecosystem.md)
- [Cypress vs Playwright](atk-cypress-vs-playwright.md)
- [Playwright for Visual Regression](../visual-regression/playwright/index.md)
- Reference: https://www.drupal.org/project/automated_testing_kit
