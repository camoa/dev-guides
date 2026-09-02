---
description: "Use ATK's data-qa-id selector hooks and helper functions in plain Playwright tests without adopting ATK's full test catalog."
tldr: "Set testIdAttribute:'data-qa-id' in playwright.config.ts to get ATK's stable selector guarantees without writing your own preprocess hooks. Import only the ATK helper functions you need — drupalLogin, createNode — rather than adopting the full 36-test catalog."
---

# ATK Integration

## When to Use

> Using ATK's helpers and selector hooks in plain Playwright tests, without adopting ATK's full test catalog.

## Pattern: ATK's Selector Hooks

ATK ships preprocess hooks decorating Drupal markup with stable selectors via `data-qa-id`. To make these first-class in Playwright, set the test ID attribute:

```ts
// playwright.config.ts
use: { testIdAttribute: 'data-qa-id' }
```

Now `page.getByTestId('login-form')` matches `<form data-qa-id="login-form">` — you get ATK's stability guarantees without writing your own preprocess hooks.

## Pattern: Importing ATK Helpers Without the Catalog

ATK's Playwright package exports helper functions. Selectively import:

```ts
import { drupalLogin, drupalLogout, createNode } from 'automated-testing-kit/helpers';

test('my custom flow', async ({ page }) => {
  await drupalLogin(page, 'editor', 'editor');
  /* your bespoke test, not ATK's catalog */
});
```

The right model for projects with an existing test suite that want ATK's plumbing without its 36 canned tests.

## Pattern: Testor Snapshots in Fixtures

To get **per-worker DB state**, wrap a Testor restore in a worker-scoped fixture:

```ts
export const test = base.extend<{}, { dbReset: void }>({
  dbReset: [async ({}, use) => {
    execSync('ddev drush testor:restore qa-baseline', { stdio: 'inherit' });
    await use();
  }, { scope: 'worker', auto: true }],
});
```

Per-test (not per-worker) is much more expensive — only do it when tests must not see each other's DB writes. Per-worker reset + good test isolation (each test creates its own node with a unique title) usually suffices.

## Common Mistakes

- **Adopting ATK's full test catalog** when you only want the helpers — copy what you need
- **Per-test DB reset** without measuring cost — usually unnecessary
- **Setting `testIdAttribute` to `data-qa-id` without enabling ATK module** — selectors don't exist

## See Also

- [Automated Testing Kit (ATK)](../atk/index.md) — full ATK guide
- [Fixtures](pw-e2e-fixtures.md) — worker-scoped fixture patterns
- [Drupal & DDEV Patterns](pw-e2e-drupal-patterns.md) — Drush setup from tests
