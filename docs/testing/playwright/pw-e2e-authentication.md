---
description: "Log in once with storageState and replay cookies/localStorage across tests — multi-role setup and session management."
tldr: "Run a one-time setup project that logs in via API, saves storageState to a .auth/ file, then configure test projects to read that file via dependencies. Never commit .auth/ files — they contain live session cookies. Prefer programmatic API login over UI login for speed and stability."
---

# Authentication

## When to Use

> Logging in once and replaying cookies/localStorage to keep tests fast.

## Pattern: One-Time Login → Save State → Reuse

```ts
// tests/auth.setup.ts
import { test as setup, expect } from '@playwright/test';
import path from 'path';

const userFile = path.join(__dirname, '../playwright/.auth/user.json');

setup('authenticate as user', async ({ page }) => {
  await page.goto('/user/login');
  await page.getByLabel('Username').fill(process.env.TEST_USER!);
  await page.getByLabel('Password').fill(process.env.TEST_PASS!);
  await page.getByRole('button', { name: 'Log in' }).click();
  await expect(page.getByRole('navigation')).toContainText('Log out');
  await page.context().storageState({ path: userFile });
});
```

```ts
// playwright.config.ts
export default defineConfig({
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], storageState: 'playwright/.auth/user.json' },
      dependencies: ['setup'],
    },
  ],
});
```

`dependencies: ['setup']` guarantees setup runs (and succeeds) before any test in `chromium`. `.gitignore` the `.auth/` folder — files contain real session cookies.

## Pattern: Multi-Role

```ts
// auth.setup.ts — one setup test per role
setup('admin', async ({ page }) => { /* login as admin */ });
setup('editor', async ({ page }) => { /* login as editor */ });
// anonymous needs no setup; just don't pass storageState
```

```ts
// playwright.config.ts
projects: [
  { name: 'setup', testMatch: /.*\.setup\.ts/ },
  {
    name: 'admin',
    testMatch: /admin\/.*\.spec\.ts/,
    use: { storageState: 'playwright/.auth/admin.json' },
    dependencies: ['setup'],
  },
  {
    name: 'editor',
    testMatch: /editor\/.*\.spec\.ts/,
    use: { storageState: 'playwright/.auth/editor.json' },
    dependencies: ['setup'],
  },
  {
    name: 'anonymous',
    testMatch: /anon\/.*\.spec\.ts/,
    // no storageState, no dependency
  },
],
```

Put role-specific tests in role-specific folders so `testMatch` picks them up.

## Decision: UI Login vs Programmatic API Login

| Approach | When |
|---|---|
| **Programmatic API token** (POST `/oauth/token`, `/user/login?_format=json`) | **Always preferred when the API exists** — faster, never breaks because of UI redesigns, isolates auth from feature tests |
| **UI login** (the example above) | Only when verifying the actual login form, or when no API exists |
| **Mixed** | One UI login per worker into `storageState`, then every test reads the storage state |

If your only reason for UI login is "we don't know the API endpoint" — find the endpoint.

## Pattern: Session Expiry

`storageState` doesn't auto-refresh. Two strategies:

1. **Re-run setup before every CI run** (default — setup project runs each invocation)
2. **Detect expiry inside a fixture and re-login** — `authedPage` fixture navigates to a known URL; if it sees the login form, re-runs auth

For long suites that hit token expiry mid-run, prefer (1) plus increasing worker count so individual workers complete inside the token TTL.

## Pattern: HTTP Basic Auth

```ts
use: {
  httpCredentials: {
    username: process.env.STAGING_USER!,
    password: process.env.STAGING_PASS!,
  },
}
```

Common for protected staging environments. Scope to a single project or test via `test.use({ httpCredentials: ... })`.

## Common Mistakes

- **Committing `playwright/.auth/*.json`** — leaks session cookies; gitignore
- **UI login per test** — slow; use `storageState` once
- **Hard-coded credentials in tests** — use env vars or a secrets manager

## See Also

- [Fixtures](pw-e2e-fixtures.md) — wrapping auth reload detection in a fixture
- [Drupal & DDEV Patterns](pw-e2e-drupal-patterns.md) — Drupal session cookie specifics (`SESS…`/`SSESS…`)
- Reference: [Playwright Authentication](https://playwright.dev/docs/auth)
