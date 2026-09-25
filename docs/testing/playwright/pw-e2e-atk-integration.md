---
description: "Use ATK's body-class and data-media-id selector hooks and helper functions in plain Playwright tests without adopting ATK's full test catalog."
tldr: "ATK's preprocess hooks add body classes and a data-media-id attribute on media images, not a generic test-id attribute — scope locators from the body class and import atkCommands helpers directly rather than adopting ATK's full test catalog."
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

## Pattern: Testor Snapshots in Fixtures

To get **per-worker DB state**, wrap a Testor restore in a worker-scoped fixture:

```ts
export const test = base.extend<{}, { dbReset: void }>({
  dbReset: [async ({}, use) => {
    execSync('ddev exec testor snapshot:restore --name=qa-baseline', { stdio: 'inherit' });
    await use();
  }, { scope: 'worker', auto: true }],
});
```

Per-test (not per-worker) is much more expensive — only do it when tests must not see each other's DB writes. Per-worker reset + good test isolation (each test creates its own node with a unique title) usually suffices.

## Common Mistakes

- **Adopting ATK's full test catalog** when you only want the helpers — copy what you need
- **Per-test DB reset** without measuring cost — usually unnecessary
- **Assuming `data-qa-id` is ATK's selector convention** — ATK uses body classes and `data-media-id`, not a generic test attribute

## See Also

- [Automated Testing Kit (ATK)](../atk/index.md) — full ATK guide
- [Fixtures](pw-e2e-fixtures.md) — worker-scoped fixture patterns
- [Drupal & DDEV Patterns](pw-e2e-drupal-patterns.md) — Drush setup from tests
