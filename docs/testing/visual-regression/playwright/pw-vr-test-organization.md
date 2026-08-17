---
description: Structure Playwright VR tests using fixtures, parallelism controls, and project metadata parameterization.
tldr: "Use `test.extend` fixtures for shared auth and page state instead of globals or `beforeEach` chains. Set `fullyParallel: true` globally but apply `mode: 'serial'` only to tests that share Drupal editorial state."
---

# Test Organization

## When to Use

> Use this when structuring tests for shared authentication, controlling parallelism, or parameterizing tests across viewports.

## Decision

| Need | Pattern |
|---|---|
| Shared auth / page state | `test.extend` fixture |
| Shared navigation | `test.beforeEach` |
| Tests that must run in sequence | `test.describe.configure({ mode: 'serial' })` |
| Max throughput | `fullyParallel: true` in config |
| Per-test metadata from project | `testInfo.project.metadata` |

## Pattern

### Fixtures (`test.extend`)

```ts
import { test as base, expect, type Page } from '@playwright/test';

type Fixtures = { authedPage: Page };

export const test = base.extend<Fixtures>({
  authedPage: async ({ page, context }, use) => {
    await context.addCookies([
      { name: 'SESS', value: '...', url: 'https://mysite.ddev.site' },
    ]);
    await use(page);
  },
});
```

### `beforeEach` for navigation

```ts
test.beforeEach(async ({ page }) => {
  await page.goto('/');
  await page.evaluate(() => document.fonts.ready);
});
```

### Parallelism

```ts
test.describe.configure({ mode: 'parallel' }); // tests in this block run in parallel
test.describe.configure({ mode: 'serial' });   // sequential, abort on first failure
```

At config level: `fullyParallel: true` makes everything parallel by default.

### Parameterized via project metadata

```ts
projects: [
  { name: 'desktop',
    use: { viewport: { width: 1440, height: 900 } },
    metadata: { device: 'desktop' } },
  { name: 'mobile',
    use: { viewport: { width: 375, height: 667 } },
    metadata: { device: 'mobile' } },
]
```

Read inside tests via `testInfo.project.metadata`.

## Common Mistakes

- **Wrong**: Module-level globals for shared state → **Right**: fixtures are the proper Playwright alternative
- **Wrong**: `serial` mode as the default → **Right**: defeats parallelism; use only when tests genuinely depend on ordering
- **Wrong**: `fullyParallel: true` on tests that share editorial state in Drupal → **Right**: isolate per-worker or use `serial`

## See Also

- [Drupal & DDEV](pw-vr-drupal-ddev.md)
- [Config Walkthrough](pw-vr-config-walkthrough.md)
- Reference: [Playwright Fixtures](https://playwright.dev/docs/test-fixtures)
