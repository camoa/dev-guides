---
description: "Build custom Playwright fixtures with test.extend — scoped state sharing that's typed, composable, and guaranteed to tear down."
tldr: "Replace beforeEach with test.extend fixtures — they're typed, compose across files, and scope setup to only the tests that need it. Use worker scope for expensive shared resources (OAuth token, DB pool); use test scope (default) for anything tests must not share."
---

# Fixtures

## When to Use

> Sharing state across tests cleanly. Fixtures are Playwright's idiomatic alternative to `beforeEach`/globals.

## Why Fixtures Beat `beforeEach`

- Only set up what a test asks for (no wasted login on tests that don't need login)
- Typed
- Compose (one fixture can depend on another)
- Explicit scopes (per-test or per-worker)
- Guaranteed teardown in reverse-of-setup order, even on failure

## Built-In Fixtures

| Fixture | Scope | What it is |
|---|---|---|
| `page` | test | Fresh `Page` in a fresh `BrowserContext` — most common dependency |
| `context` | test | The `BrowserContext` for `page` — use when you need multiple pages |
| `request` | test | An `APIRequestContext` honoring `baseURL`, `extraHTTPHeaders`, sharing cookies with browser context |
| `browser` | worker | Shared `Browser` instance for the worker |
| `browserName` | worker | `'chromium' \| 'firefox' \| 'webkit'` |
| `baseURL`, `viewport`, `storageState`, `httpCredentials`, … | options | Read from `use:` config |

## Pattern: Custom Fixtures

```ts
// fixtures.ts
import { test as base, expect } from '@playwright/test';

type MyFixtures = {
  authedPage: Page;          // test-scoped
  todoPage: TodoPage;        // test-scoped page object
};

type MyWorkerFixtures = {
  apiToken: string;          // worker-scoped — fetched once per worker
};

export const test = base.extend<MyFixtures, MyWorkerFixtures>({
  // Worker-scoped: one HTTP login per worker, reuse across tests
  apiToken: [async ({}, use) => {
    const res = await fetch('https://example.com/oauth/token', { /* ... */ });
    const { access_token } = await res.json();
    await use(access_token);
  }, { scope: 'worker' }],

  // Test-scoped: fresh page that already has the token in localStorage
  authedPage: async ({ page, apiToken }, use) => {
    await page.addInitScript(token => {
      window.localStorage.setItem('token', token);
    }, apiToken);
    await page.goto('/dashboard');
    await use(page);
  },

  todoPage: async ({ authedPage }, use) => {
    const todoPage = new TodoPage(authedPage);
    await use(todoPage);
  },
});

export { expect };
```

Then every spec file imports from `./fixtures.ts`:

```ts
import { test, expect } from './fixtures';

test('user creates a todo', async ({ todoPage }) => {
  await todoPage.add('Buy milk');
  await expect(todoPage.items).toHaveCount(1);
});
```

## Decision: Worker Scope vs Test Scope

| Use worker scope (`{ scope: 'worker' }`) when | Use test scope (default) when |
|---|---|
| Setup is **expensive** and **shared safely** between tests | Tests must not see each other's state |
| OAuth token, DB connection pool, external service handshake | Fresh page, page object, freshly seeded DB row |
| Setup runs once per worker process | Setup runs once per test |

A worker-scoped fixture **cannot** depend on a test-scoped one (the framework rejects it).

## Pattern: Auto Fixtures

Run even if no test asks for them — useful for cross-cutting concerns:

```ts
export const test = base.extend<{ logger: void }>({
  logger: [async ({}, use, testInfo) => {
    console.log(`>>> ${testInfo.title}`);
    await use();
    console.log(`<<< ${testInfo.title} (${testInfo.status})`);
  }, { auto: true }],
});
```

Common auto-fixtures: console error capture (fail test if `console.error` fired), unhandled promise rejection guard, per-test timing instrumentation.

## Pattern: Overriding Built-In Fixtures

```ts
// Override the page fixture for boilerplate every test needs
export const test = base.extend({
  page: async ({ page }, use) => {
    await page.goto('/');
    await page.route('**/api/analytics/**', r => r.abort()); // kill analytics
    await use(page);
  },
});
```

## Real Use Cases

- **Shared auth state per role** — see Section 5
- **Database seeding per test** — fixture POSTs a node via JSON:API, yields the ID, deletes on teardown
- **Mocked APIs** — fixture installs `page.route(...)` handlers on setup, removes on teardown
- **Page objects** — each spec asks for the high-level POs it needs
- **Per-test screenshot attachments** — auto fixture calls `testInfo.attach()` after each test

## Common Mistakes

- **Using `beforeEach` for state that produces a value** — fixtures are typed and compose; hooks aren't
- **Worker fixture trying to depend on test fixture** — framework error
- **Auto fixture for everything** — adds overhead even to tests that don't need it

## See Also

- [Authentication](pw-e2e-authentication.md) — shared auth state per role using fixtures
- [Test Organization](pw-e2e-test-organization.md) — hooks vs fixtures for cross-cutting setup
- Reference: [Playwright Fixtures](https://playwright.dev/docs/test-fixtures)
