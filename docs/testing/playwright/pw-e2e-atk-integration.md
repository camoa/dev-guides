---
description: "Use ATK's body-class and data-media-id selector hooks and helper functions in plain Playwright tests without adopting ATK's full test catalog, and keep one shared DDEV database consistent across Playwright workers."
tldr: "Scope locators from ATK's body classes and data-media-id, and import atkCommands helpers without the full catalog. Against one DDEV database, restore it once per run and use one worker — a worker-scoped restore fixture isolates nothing."
---

# ATK Integration

## When to Use

> Using ATK's helpers and selector hooks in plain Playwright tests, without adopting ATK's full test catalog.

## Pattern: ATK's Selector Hooks

ATK's preprocess hooks add body classes (`node-type-*`, `node-nid-*`, `term-vid-*`, `term-tid-*`) and a `data-media-id` attribute on media images. It adds no test-id attribute, so keep Playwright's default `data-testid`. Scope locators from the body class. ATK's helpers read the two IDs: `atkCommands.getNid(page)` reads the node ID from the body class, and `atkCommands.getMid(locator)` reads a media ID from an image's `data-media-id` attribute:

```ts
await page.locator('body.node-nid-42').getByRole('heading').click();
```

## Pattern: Importing ATK Helpers Without the Catalog

ATK's Playwright support file exports helper functions. `atk_setup` copies it into your project; import it directly:

```ts
// tests/custom/my-flow.spec.ts
import { test } from '@playwright/test';
import * as atkCommands from '../support/atk_commands';
import qaUserAccounts from '../data/qaUsers.json';

test('my custom flow', async ({ page, context }) => {
  await atkCommands.logInViaForm(page, context, qaUserAccounts.admin);
  /* your bespoke test, not ATK's catalog */
});
```

The right model for projects with an existing test suite that want ATK's plumbing without its full catalog.

## Decision: Database State Across Parallel Workers

Every Playwright worker drives the same DDEV site, so every worker reads and writes the same database. A worker-scoped fixture runs once per worker process, not once per database. A Testor restore inside one isolates nothing: each worker restores the shared database as it starts, and can wipe content that another worker's test just created.

| Option | What is isolated | Use when |
|---|---|---|
| **Restore once per run, one worker** (default) | Nothing; tests run one at a time | ATK-style suites on one DDEV site, and any suite where tests change site-wide state |
| **Restore once per run, parallel workers, unique data per test** | Nothing; tests avoid each other's records | Every test creates and reads only its own content, and no test changes site-wide state |
| **Lullabot/playwright-drupal** | A SQLite copy of the site for each test | You need parallel runs and tests that change site-wide state, and the site can install or import into SQLite |

The default: restore the baseline once in a `restore` project, then run one worker. ATK's `playwright.config.js` already has a `setup` project (`testMatch: /.*\.setup\.js/`) that `chromium` depends on. Put the restore in front of it: give `setup` `dependencies: ['restore']`, and name the restore file so that only the `restore` project matches it. A `restore.setup.js` would also match ATK's `setup` pattern.

```ts
// playwright.config.ts (ATK ships playwright.config.js; the keys are the same)
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  workers: 1, // all workers would share the one DDEV database
  projects: [
    { name: 'restore', testMatch: /restore\.db\.ts/ },
    { name: 'setup', testMatch: /.*\.setup\.js/, dependencies: ['restore'] },
    { name: 'chromium', use: { ...devices['Desktop Chrome'] }, dependencies: ['setup'] },
  ],
});
```

```ts
// tests/restore.db.ts
import { test as setup } from '@playwright/test';
import { execSync } from 'child_process';

setup('restore the QA baseline', () => {
  setup.setTimeout(10 * 60_000); // a snapshot download and import outlasts ATK's 3-minute test timeout
  // Requires a stored qa snapshot, a configured .testor.yml, and storage
  // credentials in .testor_secret.yml or the environment variables it reads.
  execSync('ddev exec testor snapshot:restore --name=qa', { stdio: 'inherit' });
});
```

The sample assumes Playwright runs on the host, where `ddev exec` reaches the web container. If Playwright runs inside the web container, as the [VR guide's DDEV setup](../visual-regression/playwright/pw-vr-drupal-ddev.md) and playwright-drupal do, call `testor snapshot:restore --name=qa` directly. Without Testor, run `ddev snapshot restore <name>` from the host.

> **Warning: the restore overwrites your local database.** Playwright runs project dependencies on every CLI invocation, including a single spec file. Each run replaces the developer's DDEV database with the baseline. `--no-deps` skips every dependency, ATK's `setup` (its preflight check and QA-user logins) included. UI mode runs a dependency only when its project is ticked in the Projects filter, and ignores `--no-deps`.

ATK's own `playwright.config.js` also sets `workers: 1` on CI. This is not the anti-pattern **Disabling `fullyParallel` to "stabilize"** in [Anti-Patterns](pw-e2e-anti-patterns.md): the shared state is the database, and no Playwright setting isolates it.

**Parallel workers with unique data.** Keep the one restore, raise `workers`, and name everything a test creates from `${testInfo.testId}-${testInfo.retry}`, so no two tests touch the same node. The retry number matters: `testId` stays the same across retries, and ATK retries twice on CI. A test that changes site-wide state, such as enabling a module or saving a settings form, still reaches every test running beside it. A test `lock` (Playwright 1.63+) keeps tests that share the lock name apart, but tests without the lock still run alongside them. Keep site-wide changes in the one-worker suite.

**Lullabot/playwright-drupal.** Its `test` fixture copies a base SQLite database for each test and sets a `SIMPLETEST_USER_AGENT` cookie in the browser context. Core's `drupal_valid_test_ua()` reads that cookie and checks its HMAC. The package's `settings.playwright.php` then points the request at that test's database. The isolation is per test, not per worker. It covers only the browser `context`: the `request` fixture and a plain `ddev drush` call from a test hit the main database; use the package's `execDrushInTestSite()` for Drush. It sets the cookie only when `DDEV_HOSTNAME` is defined, and `PLAYWRIGHT_NO_TEST_ISOLATION` turns the isolation off. It needs the ddev-playwright add-on, a Taskfile and a `settings.php` include, and the site must install into SQLite or convert from MySQL. The ATK guide's ecosystem section covers running ATK tests on it.

Core's `core/scripts/test-site.php install` uses the same user-agent mechanism, but installs an install profile rather than your site. Core accepts the user agent it returns for 600 seconds.

## Common Mistakes

- **Adopting ATK's full test catalog** when you only want the helpers — copy what you need
- **Restoring the database in a worker-scoped fixture** — every worker shares the one DDEV database, so each restore resets the others' state mid-test. Restore once per run in a setup project
- **Parallel workers against one DDEV site while tests change site-wide state** — run one worker, or give each test its own site with Lullabot/playwright-drupal
- **Assuming `data-qa-id` is ATK's selector convention** — ATK uses body classes and `data-media-id`, not a generic test attribute

## See Also

- [Automated Testing Kit (ATK)](../atk/index.md) — full ATK guide
- [ATK Ecosystem & Alternatives](../atk/atk-ecosystem.md) — ATK tests on Lullabot/playwright-drupal infrastructure
- [ATK Testor](../atk/atk-testor.md) — creating and restoring Testor snapshots
- [Fixtures](pw-e2e-fixtures.md) — worker-scoped fixtures
- [Drupal & DDEV Patterns](pw-e2e-drupal-patterns.md) — Drush setup from tests
- [Lullabot/playwright-drupal documentation](https://lullabot.github.io/playwright-drupal/latest/) — installation and per-test SQLite sites
- Reference: [Playwright Parallelism](https://playwright.dev/docs/test-parallel) — workers, test locks, isolating test data
