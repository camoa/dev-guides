---
description: Configure Playwright browser projects for cross-browser VR testing and decide which browsers to include.
tldr: Define one project per browser in `playwright.config.ts` using `devices` presets; the project name flows into baseline filenames. Start with Chromium-only for VR — adding browsers multiplies baselines 2-3x and should only be done when your suite is stable.
---

# Browser Projects

## When to Use

> Use this when running VR tests across multiple browsers or deciding which browsers to include in your matrix.

## Decision

| Browser set | When to use |
|---|---|
| Chromium only | Default for most teams — same engine, same antialiasing, lowest maintenance |
| + WebKit | Audience is meaningfully Safari-skewed, or CSS known to differ |
| + Firefox | Rare for VR; only when shipping Firefox-specific CSS APIs |

Adding a browser multiplies baselines by 2–3x. See the [Viewport & Device Matrix](pw-vr-viewport-matrix.md) guide for full matrix design.

## Pattern

### Standard browsers

```ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox',  use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit',   use: { ...devices['Desktop Safari'] } },
  ],
});
```

### Branded channels (system-installed browser)

```ts
projects: [
  { name: 'Microsoft Edge', use: { channel: 'msedge' } },
  { name: 'Google Chrome',  use: { channel: 'chrome' } },
]
```

Prefer bundled browsers over channels for VR — channels depend on what is installed on the host.

### Run a single project

```bash
npx playwright test --project=chromium
npx playwright test --project=chromium --project=firefox
```

## Baseline Filename Suffixing

Pattern: `<test-name>-<ordinal>-<projectName>-<platform>.png`

- `homepage-1-chromium-linux.png`
- `homepage-1-firefox-linux.png`

## Common Mistakes

- **Wrong**: Running all three browsers from day one → **Right**: start with Chromium only; add browsers only after the suite is stable
- **Wrong**: Forgetting to recapture baselines after enabling a new project → **Right**: first run for a new project will be all "writing actual"; that is expected

## See Also

- [Viewport & Device Matrix](pw-vr-viewport-matrix.md)
- [Determinism](pw-vr-determinism.md)
- Reference: [Playwright Projects](https://playwright.dev/docs/test-projects)
