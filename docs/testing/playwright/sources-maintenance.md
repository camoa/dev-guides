---
description: "Source references and maintenance manifest for the playwright guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Web Sources
| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Playwright Locators | https://playwright.dev/docs/locators | 2, 14 | 2026-05-08 |
| Playwright Best Practices | https://playwright.dev/docs/best-practices | 14 | 2026-05-08 |
| Playwright Authentication | https://playwright.dev/docs/auth | 5, 14 | 2026-05-08 |
| Playwright Network | https://playwright.dev/docs/network | 6, 14 | 2026-05-08 |
| Playwright API Testing | https://playwright.dev/docs/api-testing | 7, 14 | 2026-05-08 |
| Lullabot/playwright-drupal | https://github.com/Lullabot/playwright-drupal | 11, 12 | 2026-09-25 |
| Playwright Parallelism (workers, test locks, worker index) | https://playwright.dev/docs/test-parallel | 12 | 2026-09-25 |
| Playwright Fixtures (worker scope) | https://playwright.dev/docs/test-fixtures | 11, 12 | 2026-09-25 |
| Playwright Global Setup (project dependencies) | https://playwright.dev/docs/test-global-setup-teardown | 12 | 2026-09-25 |
| Playwright 1.63 release notes (test locks) | https://playwright.dev/docs/release-notes | 12 | 2026-09-25 |

## Code Sources
The code shown in this guide is example code (TypeScript test snippets, fixtures, and CLI commands) written directly in the guide body. There is no installed module or package on disk backing it — no Research Install path applies. Version of `@playwright/test` targeted: not verified in this pass.

Section 12's database decision was checked against: Lullabot/playwright-drupal 1.11.0 `src/testcase/test.ts` (per-test `context` fixture, `SIMPLETEST_USER_AGENT` cookie), `settings/settings.playwright.php` and `tasks/playwright.yml` (`playwright:prepare` copies the base SQLite database per test ID); Drupal core 11.4.6 `core/includes/bootstrap.inc` (`drupal_valid_test_ua()` reads the cookie or User-Agent, HMAC, 600-second window) and `core/tests/Drupal/TestSite/Commands/TestSiteInstallCommand.php` (installs a profile, prints `db_prefix` and `user_agent`); `playwright` 1.63.0 `types/test.d.ts`, which `@playwright/test` re-exports (`lock?: string | string[]`, `TestProject.workers`, `test.setTimeout()`), and `lib/program.js` (`--no-deps`); Automated Testing Kit 2.1.0-beta5 `module_support/playwright.config.js` (`setup` project with `testMatch: /.*\.setup\.js/`, `chromium` depends on it, CI `retries: 2` and `workers: 1`); playwright-drupal 1.11.0 `src/testcase/test.ts` also shows the cookie goes only on `context`, only when `DDEV_HOSTNAME` is set, and not at all under `PLAYWRIGHT_NO_TEST_ISOLATION`.

## Version History
| Date | Change |
|------|--------|
| 2026-05-08 | Manifest reconstructed from the guide's own citations and the installed source. |
| 2026-09-25 | Section 12: replaced the worker-scoped Testor restore fixture, which isolated nothing against one shared DDEV database, with a database-state decision (one worker, unique data, or Lullabot/playwright-drupal). Section 11: `beforeAll`/worker fixtures repeat site-wide setup per worker; playwright-drupal isolates per test, not per worker. |
