---
description: Automated Testing Kit (ATK) — decision guides for installing, configuring, and extending this Drupal-aware E2E test catalog for Cypress and Playwright.
tracks:
  - project: automated_testing_kit
    channel: alpha
    reason: guides follow the 2.1 line, which is beta-only; 2.0.0 is the latest stable
    declared: "2.1.0-beta5"
    verified: 2026-09-24
guide-meta:
  concepts:
    - automated_testing_kit
    - ATK
    - Drupal E2E testing
    - qa_accounts
    - automated_testing_kit_demo_recipe
    - automated_testing_kit_demo
    - selector hooks
    - data-media-id
    - node-nid
    - preflightTests.yml
    - pre-flight checks
    - Testor snapshots
    - testor snapshot:create
    - testor snapshot:restore
    - atk_commands.js
    - atk_utilities.js
    - execDrush
    - getUserPage
    - qaUsers.json
    - FedRAMP tests
    - atk_fedramp
    - ATK-PW-
    - ATK-CY-
    - Drupal functional tests
    - E2E test catalog
    - test helpers
    - PerformantLabs
    - atk_setup
    - Tugboat
    - Pantheon
  not:
    - Playwright VR baselines (see testing/visual-regression/playwright)
    - toHaveScreenshot (see testing/visual-regression/playwright)
    - pixelmatch (see testing/visual-regression/pixelmatch)
    - PHPUnit (see drupal/tdd)
    - Drupal kernel tests (see drupal/tdd)
    - data-qa-id (ATK never added this attribute, in any release)
    - drush atk:preflight (no such command; pre-flight runs inside the test run)
    - drush testor:* (Testor is its own CLI binary, not a Drush command set)
  requires: []
  complements:
    - testing/visual-regression/playwright
    - testing/visual-regression/workflow
    - drupal/tdd
  category: testing
---

# Automated Testing Kit (ATK)

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what ATK is and when to use it | [Overview](atk-overview.md) | Use ATK for ready-made Drupal E2E tests (login, forms, CRUD, menus, search, caching, sitemaps) plus Cypress/Playwright helpers; never enable ATK or qa_accounts on production — it serves data/ files, including qaUsers.json, to anonymous users. |
| Decide between ATK, Lullabot's playwright-drupal, or core's test tools | [Ecosystem & Alternatives](atk-ecosystem.md) | Choose ATK for a Drupal-aware Cypress/Playwright test catalog, Lullabot/playwright-drupal for isolated parallel test sites, or core PHPUnit to stay in PHP. Nightwatch is not deprecated — core accepted a policy to replace it with Playwright, but nothing has landed yet. |
| Pick Cypress or Playwright as the runner | [Cypress vs Playwright](atk-cypress-vs-playwright.md) | Pick Playwright for new ATK projects — the larger 2.1 catalog (6 FedRAMP spec files against 4) and core's accepted policy both point that way. Keep Cypress only for an existing suite; ATK ships both catalogs but atk_setup writes package.json per runner, so running both overwrites the first. |
| Pick the right ATK release, or run on 2.0.0 stable | [Versions & Compatibility](atk-versions.md) | This guide targets 2.1.0-beta5 (2026-02-04); latest stable is 2.0.0 (2025-05-15). Use 2.1.0-beta for FedRAMP tests, Feeds, or Tugboat; on a 2.0.0 site the pre-flight filename, setup project and file:create don't exist, so 2.1 instructions break there. |
| Install ATK on a Drupal site | [Installation](atk-installation.md) | Install with the demo recipe on a fresh site (needs minimum-stability dev for performant-labs/qa_accounts:dev-main), or install drupal/qa_accounts:^1.1 yourself on an existing site, then run module_support/atk_setup playwright and npm install. Test sites only. |
| Configure the target site and Drush access | [Runner Configuration](atk-runner-config.md) | *.atk.config.js sets drushCmd, *Url routes, email and the pantheon/targetSite/tugboat blocks; execDrush() tries Pantheon, then SSH targetSite, then Tugboat, then drushCmd, in that order. baseURL lives in the runner's own config, not *.atk.config.js. |
| Run and extend the pre-flight check | [Pre-flight Checks](atk-preflight.md) | The pre-flight runs inside the test run, not via a Drush command — Playwright's setup project calls preflightTest() before chromium; Cypress checks in a global before(). Only eq conditions are implemented; there is no drush atk:preflight command in any release. |
| Use ATK's preprocess hooks to find IDs in markup | [Selector Hooks](atk-selector-hooks.md) | ATK adds no generic test attribute — only two preprocess hooks: body classes like node-nid-42 on node/term routes, and data-media-id on images tied to a media entity. Read them with atkCommands.getNid()/getMid() or cy.getNid()/getMid(); ATK never added data-qa-id. |
| Find the test that fits my use case | [Test Catalog](atk-test-catalog.md) | 39 Playwright test declarations (38 active, 18 spec files) and 37 Cypress declarations (36 active, 17 files) cover register/login, contact, error pages, sitemap, caching, entity CRUD, menu, search and feeds — no logout, role-access, admin, forms, navigation, revision or scheduling suite exists. Tags are uneven upstream. |
| Use the helper functions | [Helper Functions](atk-helper-functions.md) | Playwright ships 27 helpers in atk_commands.js (login, execDrush, config, users, nodes/media, assertions, preflightTest, skipIfLocal) plus 4 in atk_utilities.js. Never call Drush with execSync or cy.exec — it bypasses the Pantheon, SSH and Tugboat routing; read credentials from data/qaUsers.json, never hardcode them. |
| Write custom Drupal-aware tests | [Custom Tests](atk-custom-tests.md) | Keep custom tests in directories without the atk_ prefix — atk_setup … back copies all of tests/atk*/, tests/support/* and tests/data/* back into the module, so project helpers and data belong outside those two directories, for example tests/project-support/. |
| Snapshot databases with Testor | [Testor Snapshots](atk-testor.md) | Testor is a separate Robo CLI (performantlabs/testor), not an ATK or Drush command — install with composer require performantlabs/testor, then testor snapshot:create/list/get/restore/delete. The default snapshot:create --env=@self runs drush sql:sanitize on your LOCAL database before dumping it; run it on a throwaway copy. |
| Run ATK in CI | [CI Integration](atk-ci-integration.md) | ATK ships no GitHub Actions workflow and no ddev-atk addon — build your own against ddev/github-action-setup-ddev, or route Drush through the tugboat or pantheon config block. Never add a drush atk:preflight CI step; the pre-flight runs inside npx playwright test itself. |
| Use the FedRAMP tests and other 2.1 features | [FedRAMP & 2.1 Features](atk-fedramp.md) | 2.1.0-beta adds FedRAMP-oriented tests (rapid login, CORS/CSRF, session termination, unauthorized access, HTTPS redirect, security headers), Feeds tests and Tugboat routing — Playwright ships 6 FedRAMP spec files, Cypress 4. A green run covers some control areas; it is not an audit, and 2.1 has had betas only since 2025-08-05. |
| Migrate from Cypress to Playwright | [Cypress → Playwright Migration](atk-cypress-to-playwright-migration.md) | Preprocess hooks, drushCmd/pantheon/targetSite/tugboat config, preflightTests.yml, qaUsers.json and Testor snapshots carry over unchanged — only test bodies need translation. Playwright's execDrush() returns stdout directly instead of chaining like a Cypress command. |
| Add visual regression on top of ATK | [Visual Regression Layering](atk-visual-regression-layering.md) | ATK ships no visual-regression layer — no test takes a screenshot baseline. Layer native Playwright toHaveScreenshot(), Lullabot's VisualDiffTestCases, or a custom pixelmatch script on top; ATK's getUserPage() handles the login, Playwright's API does the VR. |
| Avoid common mistakes | [Anti-Patterns](atk-anti-patterns.md) | The most repeated ATK mistakes: following dead PerformantLabs GitHub URLs, running drush atk:preflight or drush testor:*, selecting [data-qa-id], enabling ATK or qa_accounts on production, and treating a green FedRAMP run as compliance certification. |
| Find module files, commands and URLs | [Code Reference](atk-code-reference.md) | Canonical source is git.drupalcode.org/project/automated_testing_kit, not GitHub — PerformantLabs' own atk-cypress/atk-playwright repos 404. ATK defines exactly two Drush commands, file:properties and file:create; check drush list --filter=file to confirm on your install. |
