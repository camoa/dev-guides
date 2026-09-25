---
description: "Structure Playwright VR tests using fixtures, parallelism controls, and project metadata parameterization."
tldr: "Use `test.extend` fixtures for shared auth and page state instead of globals or `beforeEach` chains. Set `fullyParallel: true` globally. Run tests that share Drupal editorial state with one worker (a per-project `workers: 1`) or on per-test sites (Lullabot/playwright-drupal); `mode: 'serial'` does not stop other workers hitting the same database."
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
| Tests that share Drupal editorial state | Own project with `workers: 1`, or per-test sites (Lullabot/playwright-drupal) |
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

Fixtures are the idiomatic alternative to globals or chains of `beforeEach`.

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

`mode: 'serial'` does not protect Drupal editorial state. It keeps one describe block on one worker, but other workers still hit the same DDEV database. Give tests that share editorial state their own project with a per-project `workers: 1`, and make the other projects depend on it so nothing runs beside it:

```ts
projects: [
  { name: 'editorial', testMatch: /editorial\/.*\.spec\.ts/, workers: 1 },
  { name: 'visual', testIgnore: /editorial\//, dependencies: ['editorial'] },
]
```

A failing `editorial` test then skips the `visual` project, because Playwright skips a project whose dependency failed. For parallel runs of those tests, give each test its own site with Lullabot/playwright-drupal.

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

- **Globals for shared state** — fixtures are the proper alternative; avoid module-level state
- **Serial mode by default** — defeats Playwright's parallelism gains; only use for tests that genuinely depend on sequencing
- **`fullyParallel: true` on tests that share editorial state in Drupal** — they collide, because every worker uses the same DDEV database; a worker-scoped fixture does not isolate it. Run those tests with one worker, or give each test its own site with Lullabot/playwright-drupal

## See Also

- [Drupal & DDEV](pw-vr-drupal-ddev.md)
- [Config Walkthrough](pw-vr-config-walkthrough.md)
- Reference: [Playwright Fixtures](https://playwright.dev/docs/test-fixtures)
