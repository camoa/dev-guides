---
description: Automated Testing Kit (ATK) — decision guides for installing, configuring, and extending this Drupal-aware E2E test catalog for Cypress and Playwright.
tracks:
  - project: automated_testing_kit
    channel: stable
    declared: "2.0.0"
    verified: 2026-05-08
guide-meta:
  concepts:
    - automated_testing_kit
    - ATK
    - Drupal E2E testing
    - qa_accounts
    - automated_testing_kit_demo_recipe
    - selector hooks
    - data-qa-id
    - atk_prerequisites.yml
    - pre-flight checks
    - Testor snapshots
    - testor:pull
    - testor:push
    - loginAsRole
    - runDrush
    - drushCmd
    - FedRAMP tests
    - Drupal functional tests
    - E2E test catalog
    - test helpers
    - PerformantLabs
  not:
    - Playwright VR baselines (see testing/visual-regression/playwright)
    - toHaveScreenshot (see testing/visual-regression/playwright)
    - pixelmatch (see testing/visual-regression/pixelmatch)
    - PHPUnit (see drupal/tdd)
    - Drupal kernel tests (see drupal/tdd)
  requires: []
  complements:
    - testing/visual-regression/playwright
    - testing/visual-regression/workflow
    - drupal/tdd
  specializes: ""
  category: testing
---

# Automated Testing Kit (ATK)

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what ATK is and when to choose it | [Overview](atk-overview.md) | Use ATK when you need a curated catalog of ~36 Drupal-aware E2E tests plus helpers without writing them from scratch; it provides the test catalog and Drupal-side glue, while you supply the Cypress or Playwright runner. ATK does not include a visual regression layer. |
| Choose between ATK, Lullabot/playwright-drupal, or PHPUnit | [Ecosystem & Alternatives](atk-ecosystem.md) | Use ATK for a curated Drupal-aware test catalog; use Lullabot/playwright-drupal for parallel SQLite infrastructure — they solve different problems and combining both is valid. Avoid starting new projects on Nightwatch, which is being replaced in Drupal core by Playwright. |
| Pick Cypress or Playwright as the runner | [Cypress vs Playwright](atk-cypress-vs-playwright.md) | Use Playwright for new projects in 2026 — cross-browser, built-in parallelism, web-first assertions, and the emerging community direction. Use Cypress only when an existing suite justifies staying. ATK ships both catalogs; pick one runner per project. |
| Pick the right ATK release track | [Versions & Compatibility](atk-versions.md) | Use ATK 2.0.0 stable for production Drupal 11 sites. Use 2.1-beta only if you need FedRAMP tests, Feeds, or Tugboat support. Use 3.0-alpha only for Drupal CMS 2.x. The canonical source is git.drupalcode.org — GitHub PerformantLabs repos 404. |
| Install ATK on a Drupal site | [Installation](atk-installation.md) | Install the module and qa_accounts companion, apply the demo recipe so shipped tests have the expected content and users, then install Cypress or Playwright separately in a sandboxed subdirectory. ATK does not bundle the runner. |
| Configure Cypress or Playwright for ATK | [Runner Configuration](atk-runner-config.md) | Set baseURL from DDEV_PRIMARY_URL, use ignoreHTTPSErrors for DDEV self-signed certs, and configure drushCmd to match your environment (local, container exec, or SSH). Wrong drushCmd is the most common ATK CI failure. |
| Run ATK's pre-flight checks | [Pre-flight Checks](atk-preflight.md) | Pre-flight runs before any test via atk_prerequisites.yml and aborts with a structured error if any check fails. Run it in CI always — that is exactly where misconfigured environments produce confusing test failures. Extend it only when your tests assume state that isn't enforced by Composer or config-import. |
| Target Drupal markup without volatile class names | [Selector Hooks](atk-selector-hooks.md) | ATK adds stable data-qa-id attributes to common Drupal markup via preprocess hooks, decoupling tests from volatile class names and Form API ID mangling. Extend the same convention in your module/theme preprocess hooks for custom markup. |
| Find the test that fits my use case | [Test Catalog](atk-test-catalog.md) | ATK ships ~36 tests organized by area (auth, content, page errors, forms, navigation, search, media, email, FedRAMP) with parallel Cypress and Playwright variants. Run only the auth + page-error suites for a first-day smoke check; never modify ATK's shipped test files in-place. |
| Use the helper utility functions | [Helper Functions](atk-helper-functions.md) | ATK ships ~24 helpers covering auth (loginAsRole), Drush invocation (runDrush), snapshot management (testorPull), form interactions, email verification, and cleanup. Use loginAsRole instead of hardcoded credentials; use runDrush instead of cy.exec — both handle environment-specific invocation automatically. |
| Write custom Drupal-aware tests | [Custom Tests](atk-custom-tests.md) | Put project-specific tests in e2e/content/ or e2e/workflows/ separate from ATK's copied catalog. Use ATK helpers (loginAsRole, runDrush) and selector hooks (data-qa-id) in your custom tests. Tag tests with @smoke and @auth for selective CI runs. |
| Snapshot databases with Testor | [Testor Snapshots](atk-testor.md) | Testor is ATK's Drush command set for pushing and pulling sanitised DB snapshots to S3-compatible or SFTP storage, categorised by audience (dev, qa, tugboat-base). Always use --sanitize when pushing; store access keys in env vars or CI secrets, never in YAML. |
| Run ATK in CI (GitHub Actions + DDEV) | [CI Integration](atk-ci-integration.md) | The canonical CI pattern is ddev/github-action-setup-ddev + composer install + demo recipe + preflight + playwright test. There is no ddev-atk addon. Always pass --with-deps to playwright install in CI and upload the report artifact with if: always(). |
| Use the FedRAMP compliance pack | [FedRAMP & 2.1 Features](atk-fedramp.md) | ATK 2.1-beta adds FedRAMP-aligned tests (login lockout, CORS headers, session timeout, 403 checks) plus Feeds, Tugboat Drush, and persistent sessions. These tests pass does not mean the site is FedRAMP-compliant — they are one verification mechanism. Stay on 2.0 stable if you don't need these features. |
| Migrate from Cypress to Playwright | [Cypress → Playwright Migration](atk-cypress-to-playwright-migration.md) | Selector hooks, Drush config, Testor snapshots, qa_accounts, and pre-flight checks are all reusable. Test logic needs translation — adopt Playwright's web-first assertions rather than translating literally. Never build a compatibility shim. |
| Add visual regression on top of ATK | [Visual Regression Layering](atk-visual-regression-layering.md) | ATK's test catalog is functional E2E only — no VR assertions. Layer visual regression using Playwright's native toHaveScreenshot() combined with ATK's loginAsRole() for auth setup. Keep VR in dedicated test files separate from functional tests. |
| Avoid common mistakes | [Anti-Patterns](atk-anti-patterns.md) | The most damaging ATK mistakes are following dead GitHub URLs, skipping the demo recipe, editing shipped tests in-place, hardcoding drushCmd or credentials, and treating FedRAMP test passes as compliance certification. |
| Find services, modules, files | [Code Reference](atk-code-reference.md) | Canonical source is git.drupalcode.org/project/automated_testing_kit (not GitHub). Key files are automated_testing_kit.module (selector hooks), atk_prerequisites.yml (preflight), js-helpers/ (test helpers), and src/Commands/TestorCommands.php (snapshot Drush). Verify Drush command names with drush list on your install. |
