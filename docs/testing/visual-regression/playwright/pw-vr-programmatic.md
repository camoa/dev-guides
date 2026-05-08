---
description: Use the Playwright programmatic API outside the test runner for audit galleries and custom capture scripts.
tldr: Use the `playwright` package (not `@playwright/test`) for standalone scripts. `toHaveScreenshot()` and `toMatchSnapshot()` only work inside the test runner — for diffing in custom scripts, call pixelmatch directly.
---

# Programmatic API

## When to Use

> Use this for custom scripts that capture screenshots outside the test runner — design audit galleries, baseline-generation scripts, or integration with non-Playwright test runners.

## Decision

| Package | Use |
|---|---|
| `playwright` | Programmatic browser control; no test runner |
| `@playwright/test` | The test runner; ships `expect(...).toHaveScreenshot()` etc. |

`expect(page).toHaveScreenshot()` and `expect(buf).toMatchSnapshot()` **only work inside the test runner**.

## Pattern

### Standalone capture script

```ts
import { chromium, devices } from 'playwright';

const browser = await chromium.launch();
const context = await browser.newContext({
  ...devices['Desktop Chrome'],
  ignoreHTTPSErrors: true,
  viewport: { width: 1440, height: 900 },
});
const page = await context.newPage();
await page.goto('https://mysite.ddev.site');
await page.screenshot({ path: 'home.png', fullPage: true });
await browser.close();
```

For diffing in custom scripts, call `pixelmatch` directly — see the Pixelmatch guide.

## Common Mistakes

- **Wrong**: Importing `@playwright/test` and calling screenshot assertions outside the runner → **Right**: assertions throw; use the `playwright` package instead
- **Wrong**: Forgetting `await browser.close()` → **Right**: leaves Chromium processes hanging
- **Wrong**: `chromium.launch({ headless: false })` in CI → **Right**: fails (no display); use headless only

## See Also

- [Screenshot APIs](pw-vr-screenshot-apis.md)
- Reference: [Playwright API](https://playwright.dev/docs/api/class-playwright)
