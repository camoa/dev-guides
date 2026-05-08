---
description: Log in once with storageState and replay cookies/localStorage across tests — multi-role setup and session management.
tldr: Run a one-time setup project that logs in via API, saves storageState to a .auth/ file, then configure test projects to read that file via dependencies. Never commit .auth/ files — they contain live session cookies. Prefer programmatic API login over UI login for speed and stability.
---

# Authentication

## When to Use

> Use `storageState` to log in once per CI run per role and replay credentials across tests. Use programmatic API login (not UI login) when the API endpoint exists.

## Decision

| Approach | When |
|---|---|
| **Programmatic API token** (POST `/oauth/token`, `/user/login?_format=json`) | **Always preferred when the API exists** — faster, never breaks because of UI redesigns, isolates auth from feature tests |
| **UI login** | Only when verifying the actual login form, or when no API exists |
| **Mixed** | One UI login per worker into `storageState`, then every test reads the storage state |

## Pattern

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

### Multi-role

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
  { name: 'anonymous', testMatch: /anon\/.*\.spec\.ts/ },
],
```

### HTTP basic auth (staging environments)

```ts
use: {
  httpCredentials: {
    username: process.env.STAGING_USER!,
    password: process.env.STAGING_PASS!,
  },
}
```

## Common Mistakes

- **Wrong**: Committing `playwright/.auth/*.json` — leaks session cookies. **Right**: Add `.auth/` to `.gitignore`
- **Wrong**: UI login per test — slow. **Right**: Use `storageState` once per CI run
- **Wrong**: Hard-coded credentials in tests. **Right**: Use env vars or a secrets manager

## See Also

- [Fixtures](pw-e2e-fixtures.md) — wrapping auth reload detection in a fixture
- [Drupal & DDEV Patterns](pw-e2e-drupal-patterns.md) — Drupal session cookie specifics (`SESS…`/`SSESS…`)
- Reference: [Playwright Authentication](https://playwright.dev/docs/auth)
