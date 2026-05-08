---
description: Writing maintainable VR tests with reusable helpers, data-vrt-mask, and the navigate+stabilize+capture macro.
tldr: Extract a waitForStableLayout helper and a vrSnapshot macro so most tests are 1–3 lines. Use data-vrt-mask in Twig markup to decouple volatility masking from test files. Prefer dedicated fixture routes over real content pages for SDC atoms.
---

# Authoring Patterns

## When to Use

> Use these patterns when writing VR tests that need to hold up over time. The assertion line should be the most visible part of any test.

## Decision

| Pattern | Pros | Cons |
|---------|------|------|
| Real-page fixtures (`/node/123`) | Tests what users see | Drags in editorial content, navigation chrome, sidebar blocks; every content change ripples |
| Component fixtures (a dedicated `/vrt-fixtures/<component>` route) | Isolated, stable, fast to update | Requires a custom controller; doesn't catch integration regressions |

For shared SDC/atoms: use dedicated fixture routes — the Drupal equivalent of Storybook stories.

## Pattern

`waitForStableLayout` helper:

```ts
export async function waitForStableLayout(page: Page) {
  await page.waitForLoadState('domcontentloaded');
  await page.waitForLoadState('networkidle');
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(200); // settle
}
```

`data-vrt-mask` in Twig — editorial code marks volatile regions:

```twig
<span data-vrt-mask class="timestamp">{{ node.created.value|format_date }}</span>
```

Tests pick it up automatically:

```ts
await expect(page).toHaveScreenshot({
  mask: [page.locator('[data-vrt-mask]')],
});
```

Navigate + stabilize + capture macro:

```ts
export async function vrSnapshot(page: Page, url: string, name: string) {
  await page.goto(url);
  await waitForStableLayout(page);
  await expect(page).toHaveScreenshot(`${name}.png`, {
    fullPage: true,
    mask: [page.locator('[data-vrt-mask]')],
  });
}
```

Most VR tests become 1–3 lines:

```ts
test('homepage desktop', async ({ page }) => {
  await vrSnapshot(page, '/', 'homepage');
});
```

## Common Mistakes

- **Wrong**: long copy-pasted setup in every test → **Right**: extract to a helper; the assertion line should be the most visible part
- **Wrong**: tests that depend on editorial content (real nodes with timestamps) → **Right**: moves the goalposts every content change
- **Wrong**: single tests asserting multiple unrelated screenshots → **Right**: split into separate tests per state

## See Also

- [Stability Checklist](vr-stability-checklist.md)
- [Drupal & DDEV Procedure](vr-drupal-ddev-procedure.md)
- [Baseline Update Workflow](vr-baseline-update-workflow.md)
