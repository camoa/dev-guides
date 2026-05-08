---
description: Writing project-specific tests on top of ATK's catalog — directory structure, helper imports, test tagging for selective runs.
tldr: Put project-specific tests in e2e/content/ or e2e/workflows/ separate from ATK's copied catalog. Use ATK helpers (loginAsRole, runDrush) and selector hooks (data-qa-id) in your custom tests. Tag tests with @smoke and @auth for selective CI runs.
drupal_version: "11.x"
---

# ATK Custom Tests

## When to Use

> Use this guide when writing project-specific tests on top of ATK's catalog.

## Decision

| Test scope | Location |
|---|---|
| Pure ATK use case (login, generic content) | Already in ATK catalog — don't duplicate |
| Project-specific content type or workflow | `e2e/content/` or `e2e/workflows/` |
| Project-specific helper | `helpers/project/` |
| Modification of an ATK behavior | Copy the ATK test into `e2e/atk-overrides/`, modify; don't edit upstream |

## Pattern

### Directory structure

```
tests/playwright/
├── e2e/
│   ├── atk/                    # ATK's shipped tests (copied or symlinked)
│   ├── smoke/                  # Your project's smoke set
│   ├── content/                # Project-specific content tests
│   └── workflows/              # End-to-end workflow tests
├── helpers/
│   ├── atk/                    # ATK's helpers (copied or symlinked)
│   └── project/                # Your project's helpers
└── playwright.config.js
```

### A custom test using ATK helpers

```ts
import { test, expect } from '@playwright/test';
import { loginAsRole } from '../helpers/atk';

test.describe('custom workflow', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsRole(page, 'editor');
  });

  test('editor publishes a curated landing page', async ({ page }) => {
    await page.goto('/node/add/landing_page');
    await page.fill('[data-qa-id="landing-title"]', 'Spring 2026 Campaign');
    await page.click('[data-qa-id="landing-publish"]');
    await expect(page.locator('.messages--status')).toContainText('saved');
  });
});
```

For Playwright fixtures, web-first assertions, locator strategies, and DDEV specifics, see [Playwright for Visual Regression](../visual-regression/playwright/index.md) — the same knowledge applies to ATK functional tests, just without the `toHaveScreenshot()` step.

### Test tagging for selective runs

```ts
// Playwright
test('login works @smoke @auth', async ({ page }) => { /* ... */ });
```

```bash
npx playwright test --grep "@smoke"
```

```js
// Cypress
describe('login', { tags: ['@smoke', '@auth'] }, () => { /* ... */ });
```

```bash
npx cypress run --env grepTags="@smoke"
```

## Common Mistakes

- **Wrong**: Modifying ATK's shipped files in-place → **Right**: lost on next upgrade; copy and rename instead
- **Wrong**: No tagging strategy → **Right**: can't run a smoke subset without listing every test path
- **Wrong**: Helpers that only work in one runner → **Right**: write helpers shared across both when possible

## See Also

- [Test Catalog](atk-test-catalog.md)
- [Helper Functions](atk-helper-functions.md)
- [Selector Hooks](atk-selector-hooks.md)
- [Playwright for Visual Regression](../visual-regression/playwright/index.md)
