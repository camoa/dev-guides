---
description: "Layering visual regression on top of ATK — native Playwright, Lullabot's VisualDiffTestCases, or pixelmatch, since ATK ships none."
tldr: "ATK ships no visual-regression layer — no test takes a screenshot baseline. Layer native Playwright toHaveScreenshot(), Lullabot's VisualDiffTestCases, or a custom pixelmatch script on top; ATK's getUserPage() handles the login, Playwright's API does the VR."
drupal_version: "11.x"
---

# ATK Visual Regression Layering

## When to Use

> Adding visual regression on top of ATK's E2E tests.

## ATK Doesn't Ship VR

ATK's catalog is functional: login, entity CRUD, page errors, contact forms, search, menus. No test takes a screenshot baseline. To add VR:

| Layer | Source |
|---|---|
| Native Playwright VR | `expect(page).toHaveScreenshot()` — see [Playwright for Visual Regression — Screenshot APIs](../visual-regression/playwright/pw-vr-screenshot-apis.md) |
| VR procedure (workflow, baselines, threshold tuning) | See [Visual Regression Workflow](../visual-regression/workflow/index.md) |
| Lullabot's `VisualDiffTestCases` | `@lullabot/playwright-drupal` — URL-driven VR cases for Drupal |
| Custom pixelmatch script | `pixelmatch` directly — see [Pixelmatch Image Diff](../visual-regression/pixelmatch/index.md) |
| Triage UI for VR diffs | [Playwright HTML Report — VR Diff Panel](../visual-regression/html-report/pw-report-vr-diff-panel.md) |

## Pattern: VR in an ATK-using project

```js
import { test, expect } from '@playwright/test'
import * as atkCommands from '../support/atk_commands'
import playwrightConfig from '../../playwright.config'
import qaUserAccounts from '../data/qaUsers.json'

const baseUrl = playwrightConfig.use.baseURL

test('homepage visual regression', async ({ page }) => {
  await page.goto(baseUrl)
  await page.evaluate(() => document.fonts.ready)
  await expect(page).toHaveScreenshot({
    fullPage: true,
    mask: [page.locator('[data-vrt-mask]')],
  })
})

test('admin dashboard visual regression', async ({ browser }) => {
  const page = await atkCommands.getUserPage(browser, qaUserAccounts.admin)
  await page.goto(`${baseUrl}admin`)
  await expect(page).toHaveScreenshot({
    mask: [page.locator('time[datetime]'), page.locator('[data-contextual-id]')],
  })
})
```

ATK's `getUserPage()` handles the login; Playwright's API does the VR.

## Decision: VR strategy

| Need | Approach |
|---|---|
| Homepage and landing pages | Native `toHaveScreenshot()` (per the VR guides) |
| URL lists with Drupal-aware defaults | Lullabot's `VisualDiffTestCases` |
| VR in both Cypress and Playwright | ATK won't help; pick one runner for VR |

## Common Mistakes

- **Expecting ATK to do VR** — it doesn't; layer Playwright's API on top
- **Using a Cypress VR plugin alongside Playwright VR** — two baseline sets; pick one
- **Mixing functional and VR assertions in one test** — keep VR in its own files

## See Also

- [ATK Overview](atk-overview.md)
- [Playwright for Visual Regression](../visual-regression/playwright/index.md)
- [Visual Regression Workflow](../visual-regression/workflow/index.md)
- [Pixelmatch Image Diff](../visual-regression/pixelmatch/index.md)
- [Playwright HTML Report](../visual-regression/html-report/index.md)
