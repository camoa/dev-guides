---
description: Running VR against a Drupal site under DDEV — authentication, HTTPS, cache, masking, and directory layout.
tldr: Use storage-state authentication (global.setup.ts writes .auth/admin.json, gitignored). Set baseURL to DDEV_PRIMARY_URL with ignoreHTTPSErrors and run inside ddev exec. Clear Drupal cache once before the suite in global.setup.ts, never between individual tests. Mask time, counters, contextual links, and Big Pipe placeholders.
---

# Drupal & DDEV Procedure

## When to Use

> Use this guide when running VR against a Drupal site under DDEV.

## Decision

| Question | Answer |
|----------|--------|
| Clear Drupal cache between tests? | Almost never — clears take 5–30 s and torpedo suite runtime |
| When to clear cache? | Once in `global.setup.ts` before the whole suite (after `drush updb`); or when the test exercises a cache-rebuild path specifically |
| When to clear before re-running? | After Twig/CSS changes: `ddev drush cr` once, then re-run — not between tests |

## Pattern

Storage-state authentication:

1. `auth.setup.ts` logs in via `/user/login` and writes `playwright/.auth/admin.json` via `context.storageState()`
2. Authenticated projects declare `use: { storageState: 'playwright/.auth/admin.json' }`
3. Anonymous projects omit `storageState`
4. `.auth/` is gitignored — files contain session cookies

DDEV URL + self-signed certs:

```ts
// playwright.config.ts
use: {
  baseURL: process.env.DDEV_PRIMARY_URL ?? 'https://my-site.ddev.site',
  ignoreHTTPSErrors: true,
}
```

Run inside the DDEV web container:

```bash
ddev exec npx playwright test
```

Common Drupal elements to mask:

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

Olivero/Claro peculiarities:
- **Admin toolbar** — wait for `'.toolbar-loading'` to disappear or hide via `stylePath`
- **CKEditor 5 iframe** — `mask` doesn't pierce iframes; `stylePath` does (`iframe { visibility: hidden; }`)
- **Big Pipe placeholders** — always `await page.waitForLoadState('networkidle')` after `goto`

Directory layout:

```
<repo>/
├── composer.json
├── web/
└── tests/playwright/
    ├── playwright.config.ts
    ├── screenshot.css
    ├── auth.setup.ts
    ├── .auth/                         # gitignored
    ├── e2e/
    │   ├── homepage.spec.ts
    │   └── homepage.spec.ts-snapshots/ # committed baselines
    └── playwright-report/             # gitignored
```

## Common Mistakes

- **Wrong**: capturing on the host → **Right**: works locally, fails in CI; capture inside the Docker image always
- **Wrong**: running `drush cr` between every test → **Right**: kills suite time
- **Wrong**: forgetting `ignoreHTTPSErrors` → **Right**: every navigation fails on DDEV TLS
- **Wrong**: committing `.auth/` files → **Right**: leaks session cookies

## See Also

- [Stability Checklist](vr-stability-checklist.md)
- [Authoring Patterns](vr-authoring-patterns.md)
- [Baseline Management](vr-baseline-management.md)
