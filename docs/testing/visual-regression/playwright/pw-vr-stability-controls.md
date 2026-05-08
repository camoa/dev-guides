---
description: Make Playwright VR captures deterministic with animation disabling, font waits, masking, and a global screenshot.css.
tldr: Add `document.fonts.ready`, `animations: 'disabled'`, and a `stylePath` injecting `screenshot.css` to eliminate the three most common sources of VR flake: font swap, CSS animation frames, and dynamic content regions.
---

# Stability Controls

## When to Use

> Use this when screenshots produce inconsistent results across runs due to animations, fonts, dynamic content, or scroll state.

## Pattern

### Animations and caret (defaults — verify they are on)

```ts
expect: {
  toHaveScreenshot: { animations: 'disabled', caret: 'hide' },
}
```

### Wait for fonts

```ts
await page.evaluate(() => document.fonts.ready);
```

Without this, the first screenshot captures the fallback font; the second captures the web font — baselines drift.

### Wait for network idle

```ts
await page.goto('/', { waitUntil: 'networkidle' });
// or after load:
await page.waitForLoadState('networkidle');
```

Caveat: hangs on long-poll/SSE connections. Use `'domcontentloaded'` + explicit `waitForResponse` in those cases.

### Mask volatile regions

```ts
await expect(page).toHaveScreenshot({
  mask: [
    page.locator('[data-testid="last-updated"]'),
    page.locator('.user-avatar'),
    page.locator('iframe'),
  ],
});
```

Masks paint solid `#FF00FF` over the bounding box. Content inside cannot cause diffs.

### `stylePath` — global stabilization CSS

`tests/playwright/screenshot.css`:

```css
*, *::before, *::after {
  animation: none !important;
  transition: none !important;
  caret-color: transparent !important;
}
iframe { visibility: hidden; }
.has-dynamic-counter { visibility: hidden; }
[data-vrt-mask] { visibility: hidden; }
```

```ts
expect: { toHaveScreenshot: { stylePath: './screenshot.css' } }
```

Pierces Shadow DOM and inner frames — works for SDC components and Olivero embedded content.

### Scroll position normalization

```ts
await page.evaluate(() => window.scrollTo(0, 0));
// For element shots:
await locator.scrollIntoViewIfNeeded();
```

### Lazy images / video posters

```ts
await page.evaluate(() =>
  document.querySelectorAll('img[loading="lazy"]')
    .forEach(img => (img.loading = 'eager'))
);
await page.waitForLoadState('networkidle');
```

## Common Mistakes

- **Wrong**: Skipping `document.fonts.ready` → **Right**: first screenshot captures fallback font; baselines drift on every subsequent run
- **Wrong**: `networkidle` on long-poll/SSE pages → **Right**: hangs the test; use explicit waits
- **Wrong**: Masks using CSS classes that are dynamically applied → **Right**: use stable attributes (`data-vrt-mask`) so masking is consistent

## See Also

- [Screenshot Options](pw-vr-screenshot-options.md)
- [Anti-Patterns](pw-vr-anti-patterns.md)
- [Drupal & DDEV](pw-vr-drupal-ddev.md)
- Reference: [Playwright toHaveScreenshot options](https://playwright.dev/docs/api/class-pageassertions#page-assertions-to-have-screenshot-1)
