---
description: Adding visual regression on top of ATK's E2E tests — ATK doesn't ship VR, so layer Playwright's native toHaveScreenshot() or Lullabot's VisualDiffTestCases.
tldr: ATK's test catalog is functional E2E only — no VR assertions. Layer visual regression using Playwright's native toHaveScreenshot() combined with ATK's loginAsRole() for auth setup. Keep VR in dedicated test files separate from functional tests.
drupal_version: "11.x"
---

# ATK Visual Regression Layering

## When to Use

> Use this guide when adding visual regression on top of an ATK-using project.

## Decision

| Need | Approach |
|---|---|
| Homepage / landing pages | Native `toHaveScreenshot()` (per the VR guides) |
| Component-level VR with Drupal-aware helpers | Lullabot's `VisualDiffTestCases` |
| Cross-runner VR (need Cypress + Playwright VR) | ATK won't help; pick one runner for VR |

### VR sources

| Layer | Source |
|---|---|
| Native Playwright VR | `expect(page).toHaveScreenshot()` — see [Playwright Screenshot APIs](../visual-regression/playwright/pw-vr-screenshot-apis.md) |
| VR procedure (workflow, baselines, threshold tuning) | See [Visual Regression Workflow](../visual-regression/workflow/index.md) |
| Lullabot's `VisualDiffTestCases` | `@lullabot/playwright-drupal` |
| Custom pixelmatch script | See [Pixelmatch Image Diff](../visual-regression/pixelmatch/index.md) |
| Triage UI for VR diffs | [Playwright HTML Report — VR Diff Panel](../visual-regression/html-report/pw-report-vr-diff-panel.md) |

## Pattern

ATK's `loginAsRole()` sets up the auth; Playwright's native API does the VR:

```ts
import { test, expect } from '@playwright/test';
import { loginAsRole } from '../helpers/atk';

test('homepage visual regression', async ({ page }) => {
  await page.goto('/');
  await page.evaluate(() => document.fonts.ready);
  await expect(page).toHaveScreenshot({
    fullPage: true,
    mask: [page.locator('[data-vrt-mask]')],
  });
});

test('admin dashboard visual regression', async ({ page }) => {
  await loginAsRole(page, 'site_admin');
  await page.goto('/admin');
  await expect(page).toHaveScreenshot({
    mask: [
      page.locator('time[datetime]'),
      page.locator('[data-contextual-id]'),
    ],
  });
});
```

## Common Mistakes

- **Wrong**: Expecting ATK to do VR out of the box → **Right**: it doesn't; layer on Playwright's native API
- **Wrong**: Using `cy-image-snapshot` or similar Cypress VR plugins alongside Playwright VR → **Right**: different baselines, different OS sensitivity; pick one
- **Wrong**: Mixing ATK functional tests and VR assertions in the same test → **Right**: separate concerns; keep VR in dedicated test files

## See Also

- [ATK Overview](atk-overview.md)
- [Playwright Screenshot APIs](../visual-regression/playwright/pw-vr-screenshot-apis.md)
- [Visual Regression Workflow](../visual-regression/workflow/index.md)
- [Pixelmatch](../visual-regression/pixelmatch/index.md)
