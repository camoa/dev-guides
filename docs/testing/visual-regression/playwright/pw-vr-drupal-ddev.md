---
description: "Run Playwright VR tests against a Drupal site under DDEV — config, worker caps, auth setup, directory layout, and common masks."
tldr: "Set `baseURL` to `DDEV_PRIMARY_URL`, `ignoreHTTPSErrors: true`, cap `workers: 2` against DDEV's single web container, and run via `ddev exec npx playwright test`. Use storage-state auth with a setup project; gitignore `.auth/`."
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

### Cap workers against a single-container backend

Playwright's `workers` default is `"50%"` of the machine's logical CPU cores — four parallel workers on an eight-core laptop, each driving its own browser. Those workers scale the harness, not the site: a DDEV site is one web container with one PHP-FPM pool, so the workers queue against the same backend and slow each other down.

Measured on a real Drupal site, **36 of 72 captures failed** at the default worker count with no site change and no code change — purely the harness competing with itself. `workers: 2` fixed it completely and held across four further full runs.

It also disguises itself as a stability problem: contention lengthens response times, which makes a racing lazy-load or `networkidle` settle more likely to lose. Chasing that with longer waits is a dead end while the real cause is concurrency. Cap workers first, then tune stability.

```ts
// playwright.config.ts
workers: 2,   // one web container, one PHP-FPM pool — the 50%-of-cores default oversubscribes it
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

`.auth/` must be in `.gitignore` — files contain session cookies.

### Directory layout

```
<repo>/
├── composer.json
├── web/
└── tests/playwright/
    ├── package.json
    ├── playwright.config.ts
    ├── screenshot.css                    # global stabilizer
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
- **Wrong**: Leaving `workers` at the default → **Right**: the default is 50% of your logical cores; one web container cannot serve them, and captures fail in batches that look like flake
- **Wrong**: Forgetting `ignoreHTTPSErrors: true` → **Right**: every navigation TLS-errors on DDEV's self-signed cert
- **Wrong**: Committing `.auth/admin.json` → **Right**: it contains the session cookie; gitignore `.auth/`

## See Also

- [Setup](pw-vr-setup.md)
- [Config Walkthrough](pw-vr-config-walkthrough.md)
- [Stability Controls](pw-vr-stability-controls.md)
- [Determinism](pw-vr-determinism.md)
- Reference: [Playwright Visual Comparisons](https://playwright.dev/docs/test-snapshots)
- Reference: [Playwright Docker image](https://playwright.dev/docs/docker)
