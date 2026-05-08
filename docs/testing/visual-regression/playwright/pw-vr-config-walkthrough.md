---
description: Annotated playwright.config.ts with every key relevant to visual regression testing.
tldr: Set `reporter: 'html'`, `outputDir: 'test-results'`, `forbidOnly: !!process.env.CI`, and pin `colorScheme`, `locale`, `timezoneId` in `use`. Define the browser × viewport matrix under `projects`.
---

# Config Walkthrough

## When to Use

> Use this as a reference when configuring `playwright.config.ts` for a VR project.

## Pattern

### Annotated config

```ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: 'e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,           // fail CI if test.only committed
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',                        // required for VR diff viewer
  outputDir: 'test-results',              // diff PNGs on failure

  use: {
    baseURL: 'https://mysite.ddev.site',
    ignoreHTTPSErrors: true,              // for DDEV self-signed
    trace: 'on-first-retry',
    colorScheme: 'light',                 // pin to avoid OS dark mode
    locale: 'en-US',
    timezoneId: 'UTC',
  },

  expect: {
    timeout: 5000,
    toHaveScreenshot: {
      threshold: 0.15,
      maxDiffPixelRatio: 0.005,
      stylePath: './screenshot.css',
      animations: 'disabled',
      caret: 'hide',
    },
  },

  snapshotPathTemplate: '{testDir}/__screenshots__{/projectName}/{testFilePath}/{arg}{ext}',

  projects: [
    { name: 'chromium-1440',
      use: { ...devices['Desktop Chrome'], viewport: { width: 1440, height: 900 } } },
    { name: 'chromium-768',
      use: { ...devices['Desktop Chrome'], viewport: { width: 768, height: 1024 } } },
    { name: 'chromium-375',
      use: { ...devices['Desktop Chrome'], viewport: { width: 375, height: 667 } } },
  ],
});
```

## Key Reference (VR-relevant)

| Key | Purpose |
|---|---|
| `testDir` | Where tests live; relative to config file |
| `fullyParallel` | Parallelize all tests across files |
| `forbidOnly` | Fail CI if `test.only` is committed |
| `retries` | Per-test retry count |
| `workers` | Parallel worker count |
| `outputDir` | Where actual/diff PNGs land (default `test-results/`) |
| `reporter` | `'html'` required for the visual diff viewer |
| `use.baseURL` | Default URL for `page.goto('/')` |
| `use.ignoreHTTPSErrors` | Trust self-signed TLS (DDEV) |
| `use.colorScheme / locale / timezoneId` | Pin for reproducibility |
| `expect.timeout` | `expect()` web-first wait time |
| `expect.toHaveScreenshot` | Defaults for every screenshot assertion |
| `snapshotPathTemplate` | Where baselines are stored |
| `updateSnapshots` | Default `'missing'`; usually overridden via CLI |
| `ignoreSnapshots` | Skip snapshot assertions entirely |
| `projects[]` | Browser × viewport matrix |

## Common Mistakes

- **Wrong**: `reporter: 'list'` without `'html'` → **Right**: no visual diff viewer; triage becomes painful
- **Wrong**: `workers` unset in CI → **Right**: random parallelism; tests touching shared Drupal state collide
- **Wrong**: Missing `ignoreHTTPSErrors` → **Right**: DDEV TLS errors fail every navigation

## See Also

- [Viewport & Device Matrix](pw-vr-viewport-matrix.md)
- [Screenshot Options](pw-vr-screenshot-options.md)
- [Stability Controls](pw-vr-stability-controls.md)
- Reference: [playwright.config.ts reference](https://playwright.dev/docs/test-configuration)
