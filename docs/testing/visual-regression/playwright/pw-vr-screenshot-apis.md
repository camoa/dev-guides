---
description: Choose between toHaveScreenshot(), toMatchSnapshot(), and page.screenshot() for visual regression.
tldr: Use `expect(page).toHaveScreenshot()` for all VR assertions — it auto-retries for stability and diffs against a baseline. `page.screenshot()` captures only; `toMatchSnapshot()` diffs but skips the stability retry.
---

# Screenshot APIs

## When to Use

> Use `toHaveScreenshot()` for all VR work. Use `page.screenshot()` only when you need a raw buffer for non-test purposes. Use `toMatchSnapshot()` only when you already have a buffer and need to diff it.

## Decision

| API | Type | Auto-retry stability | Baseline diffing | Use for |
|---|---|---|---|---|
| `expect(page).toHaveScreenshot()` | Assertion | Yes — waits for two consecutive matching frames | Yes (pixelmatch) | **Primary VR API** |
| `expect(buffer).toMatchSnapshot()` | Assertion | No | Yes for images | Generic snapshot; buffer already captured |
| `page.screenshot()` | Action | No | No | Raw capture; returns `Buffer` or writes file |

## Pattern

### Minimal VR test

```ts
import { test, expect } from '@playwright/test';

test('homepage', async ({ page }) => {
  await page.goto('https://playwright.dev');
  await expect(page).toHaveScreenshot();
});
```

### Element-level (preferred for components)

```ts
await expect(page.locator('.header')).toHaveScreenshot('header.png');
```

## Common Mistakes

- **Wrong**: Using `page.screenshot()` for VR → **Right**: it produces a file but does no comparison; the test always passes
- **Wrong**: Using `toMatchSnapshot()` on a buffer when you wanted `toHaveScreenshot()` → **Right**: you lose the auto-retry stability check
- **Wrong**: Inconsistent naming — `toHaveScreenshot('thing')` vs `toHaveScreenshot('Thing.png')` → **Right**: name consistently; casing produces different baseline filenames

## See Also

- [Screenshot Options](pw-vr-screenshot-options.md)
- [Baseline Files](pw-vr-baseline-files.md)
- Reference: [Playwright Visual Comparisons](https://playwright.dev/docs/test-snapshots)
