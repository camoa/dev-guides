---
description: Run Playwright VR tests against a Drupal site under DDEV — config, auth setup, directory layout, and common masks.
tldr: Set `baseURL` to `DDEV_PRIMARY_URL`, `ignoreHTTPSErrors: true`, and run via `ddev exec npx playwright test`. Use storage-state auth with a setup project; gitignore `.auth/`. Mask `[data-contextual-id]`, timestamps, and user fields.
---

# Drupal & DDEV

## When to Use

> Use this when running Playwright VR tests against a Drupal site served by DDEV.

## Pattern

### Config for DDEV

```ts
use: {
  baseURL: process.env.DDEV_PRIMARY_URL ?? 'https://my-site.ddev.site',
  ignoreHTTPSErrors: true,
}
```

Run inside DDEV so `.ddev.site` hostnames resolve:

```bash
ddev exec npx playwright test
```

### Storage-state authentication

```ts
// auth.setup.ts
import { test as setup } from '@playwright/test';

setup('authenticate as admin', async ({ page }) => {
  await page.goto('/user/login');
  await page.fill('#edit-name', 'admin');
  await page.fill('#edit-pass', 'admin');
  await page.click('#edit-submit');
  await page.context().storageState({ path: '.auth/admin.json' });
});
```

```ts
// playwright.config.ts
projects: [
  { name: 'setup', testMatch: /auth\.setup\.ts/ },
  {
    name: 'chromium-admin',
    dependencies: ['setup'],
    use: {
      ...devices['Desktop Chrome'],
      storageState: '.auth/admin.json',
    },
  },
]
```

`.auth/` must be in `.gitignore` — contains session cookies.

### Directory layout

```
<repo>/
├── composer.json
├── web/
└── tests/playwright/
    ├── package.json
    ├── playwright.config.ts
    ├── screenshot.css
    ├── auth.setup.ts
    ├── .auth/                            # gitignored
    ├── e2e/
    │   ├── homepage.spec.ts
    │   └── homepage.spec.ts-snapshots/   # committed baselines
    │       ├── homepage-1-chromium-1440-linux.png
    │       └── homepage-1-chromium-375-linux.png
    └── playwright-report/                # gitignored
```

### Common Drupal masks

```ts
const dynamic = [
  page.locator('time[datetime]'),
  page.locator('.views-row .submitted'),
  page.locator('.user--name'),
  page.locator('.toolbar-tray .messages'),
  page.locator('[data-contextual-id]'),
];
await expect(page).toHaveScreenshot({ mask: dynamic });
```

## Common Mistakes

- **Wrong**: Running on host without DDEV's hostname resolution → **Right**: use `ddev exec`; the `.ddev.site` domain only resolves inside DDEV
- **Wrong**: Forgetting `ignoreHTTPSErrors: true` → **Right**: every navigation TLS-errors on DDEV's self-signed cert
- **Wrong**: Committing `.auth/admin.json` → **Right**: it contains the session cookie; gitignore `.auth/`

## See Also

- [Setup](pw-vr-setup.md)
- [Stability Controls](pw-vr-stability-controls.md)
- [Determinism](pw-vr-determinism.md)
- Reference: [Playwright Visual Comparisons](https://playwright.dev/docs/test-snapshots)
- Reference: [Playwright Docker](https://playwright.dev/docs/docker)
