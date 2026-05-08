---
description: Use ATK's data-qa-id selector hooks and helper functions in plain Playwright tests without adopting ATK's full test catalog.
tldr: Set testIdAttribute:'data-qa-id' in playwright.config.ts to get ATK's stable selector guarantees without writing your own preprocess hooks. Import only the ATK helper functions you need — drupalLogin, createNode — rather than adopting the full 36-test catalog.
---

# ATK Integration

## When to Use

> Use ATK integration when your project already has an existing Playwright test suite and you want ATK's Drupal-aware plumbing (stable selectors, login helpers, DB reset) without adopting ATK's full canned test catalog.

## Decision

| Need | Approach |
|---|---|
| Stable Drupal element selectors | Set `testIdAttribute: 'data-qa-id'` — uses ATK's preprocess hooks |
| Drupal login/logout/content helpers | Import selectively from `automated-testing-kit/helpers` |
| Per-worker DB reset | Wrap `ddev drush testor:restore` in a worker-scoped auto fixture |
| Full ATK test catalog (36 canned tests) | See [ATK guide](../atk/index.md) |

## Pattern

### ATK selector hooks

```ts
// playwright.config.ts
use: { testIdAttribute: 'data-qa-id' }
```

Now `page.getByTestId('login-form')` matches `<form data-qa-id="login-form">` — ATK's preprocess hooks add these attributes to Drupal markup automatically.

### Importing ATK helpers without the catalog

```ts
import { drupalLogin, drupalLogout, createNode } from 'automated-testing-kit/helpers';

test('my custom flow', async ({ page }) => {
  await drupalLogin(page, 'editor', 'editor');
  /* your bespoke test, not ATK's catalog */
});
```

### Testor snapshots in fixtures

```ts
export const test = base.extend<{}, { dbReset: void }>({
  dbReset: [async ({}, use) => {
    execSync('ddev drush testor:restore qa-baseline', { stdio: 'inherit' });
    await use();
  }, { scope: 'worker', auto: true }],
});
```

Per-worker reset (not per-test) is the right default — per-test DB reset is expensive. Worker scope + good test isolation (each test creates its own content with a unique title) usually suffices.

## Common Mistakes

- **Wrong**: Adopting ATK's full test catalog when you only want the helpers — import what you need
- **Wrong**: Per-test DB reset without measuring cost — usually unnecessary; per-worker is sufficient
- **Wrong**: Setting `testIdAttribute: 'data-qa-id'` without enabling the ATK module — selectors don't exist in the markup

## See Also

- [Automated Testing Kit (ATK)](../atk/index.md) — full ATK guide
- [Fixtures](pw-e2e-fixtures.md) — worker-scoped fixture patterns
- [Drupal & DDEV Patterns](pw-e2e-drupal-patterns.md) — Drush setup from tests
