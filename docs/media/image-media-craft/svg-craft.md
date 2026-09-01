---
description: Choose SVG delivery method — CSS mask-image, inline SVG, img tag, or sprite sheet — with accessibility patterns and SVGO optimization
tldr: "Use `css mask-image` for single-color icon systems — it separates shape from color and works with dark mode. Use inline `<svg>` with `currentColor` for multi-color icons or when you need animation."
---

# SVG Craft

## When to Use

> Use `css mask-image` for single-color icon systems — it separates shape from color and works with dark mode. Use inline `<svg>` with `currentColor` for multi-color icons or when you need animation. Use `<img src="icon.svg">` for static decorative images with no color theming.

## Inline SVG with `currentColor`

```html
<svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
  <path fill="currentColor" d="M12 2L2 7l10 5 10-5-10-5z"/>
</svg>
```

Use `currentColor` as the `fill` value so the icon inherits its parent's text color. Combined with CSS `color` changes on hover/focus, this provides theme-adaptive icons without additional attributes.

## Animated SVG

| Approach | When to Use | Trade-off |
|---|---|---|
| CSS animations on SVG elements | Simple path color, opacity, transform | Easy; hardware-accelerated transforms |
| WAAPI (Web Animations API) | Programmatic control, timeline, JS-driven | Good browser support; no library needed |
| SMIL | Legacy or path morphing only | Do not use for new work; inconsistent browser behavior |
| GSAP | Complex choreography, morphSVG | Best DX; requires library (~50KB) |

CSS `transform` on SVG elements is now hardware-accelerated in all modern browsers. Use it for hover states and entrance animations. For complex path morphing or sequencing, use GSAP's MorphSVG plugin.

```css
/* SVG hover animation — GPU composited */
.icon { transition: transform 0.15s var(--ease-standard, cubic-bezier(0.2, 0, 0, 1)); }
.icon:hover { transform: scale(1.1) rotate(10deg); }
```

Always wrap SVG animations in `@media (prefers-reduced-motion: no-preference)`.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Multi-color icon or complex illustration | Inline `<svg>` in HTML | Full CSS access to internal paths/groups |
| Single-color icon with hover color changes | CSS `mask-image` + `background: currentColor` | No SVG markup in HTML; theming via `color` property |
| Single-color icon, simpler approach | Inline `<svg>` with `currentColor` fills | Direct color control; more HTML weight |
| Static decorative image, no color control | `<img src="icon.svg">` | Cached; clean HTML; no color theming possible |
| CSS background pattern or decoration | `background-image: url(pattern.svg)` | Cached; cannot use `currentColor` |
| Icon used repeatedly across pages | SVG sprite sheet + `<use>` | One HTTP request; per-instance color via `currentColor` |

## Pattern

**CSS `mask-image` icon** (cleanest for single-color systems):
```css
.icon {
  display: inline-block;
  width: 1.5em;
  height: 1.5em;
  background: currentColor;  /* Takes the parent's text color */
  mask: url('/icons/arrow.svg') center / contain no-repeat;
  -webkit-mask: url('/icons/arrow.svg') center / contain no-repeat;
}
```
```html
<a href="/next" class="btn">
  Continue <span class="icon icon-arrow" aria-hidden="true"></span>
</a>
```

**Inline SVG with `currentColor`**:
```html
<svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
  <path fill="currentColor" d="M12 2L2 7l10 5 10-5-10-5z"/>
</svg>
```

**SVG accessibility patterns**:

| Use case | Required attributes |
|---|---|
| Decorative icon (adjacent text explains it) | `aria-hidden="true"` + `focusable="false"` |
| Standalone meaningful icon (no adjacent text) | `role="img"` + `<title>` |
| Icon inside button/link | `aria-label` on button, `aria-hidden="true"` on SVG |

`focusable="false"` is required on inline SVGs — without it, SVGs receive keyboard focus separately in some browsers.

**SVGO optimization**:
```bash
npx svgo --config svgo.config.js -f ./icons/
```
```js
// svgo.config.js
export default {
  plugins: [
    { name: 'preset-default', params: { overrides: {
      removeViewBox: false,  // Keep viewBox for responsive scaling
      removeTitle: false,    // Keep <title> for accessibility
    }}},
    'removeXMLNS',
    'removeEditorsNSData',
  ]
};
```

**SVG hover animation** (GPU-composited):
```css
.icon { transition: transform 0.15s cubic-bezier(0.2, 0, 0, 1); }
.icon:hover { transform: scale(1.1) rotate(10deg); }
@media (prefers-reduced-motion: no-preference) { /* wrap animations here */ }
```

## Common Mistakes

- **Wrong**: `<img src="icon.svg">` and expecting color changes via CSS → **Right**: `currentColor` only works on inline SVG or `mask-image`
- **Wrong**: forgetting `focusable="false"` on inline SVGs in buttons → **Right**: SVG receives tab focus separately in some browsers
- **Wrong**: skipping `aria-hidden` on decorative icons → **Right**: screen readers announce the SVG as an unlabeled image
- **Wrong**: not running SVGO → **Right**: Figma/Illustrator export SVGs with 2–5x more bytes than needed
- **Wrong**: omitting `viewBox` → **Right**: SVG will not scale; always set `viewBox` on exportable icons

## See Also

- [Image Format Strategy](image-format-strategy.md) — when SVG vs raster
- [Image Effects Craft](image-effects-craft.md) — CSS effects applied to SVG containers
- Reference: `css-craft.md` → `clip-path-and-masks` for masking patterns
- Reference: [dbushell SVG Icons with CSS Masks](https://dbushell.com/2024/01/19/svg-icons-with-css-masks/)
- Reference: [Smashing Magazine Accessible SVG Patterns](https://www.smashingmagazine.com/2021/05/accessible-svg-patterns-comparison/)
- Reference: [SVGO documentation](https://svgo.dev/)
