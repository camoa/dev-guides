---
description: Choose SVG delivery method — CSS mask-image, inline SVG, img tag, or sprite sheet — with accessibility patterns and SVGO optimization
tldr: "Use `css mask-image` for single-color icon systems — it separates shape from color and works with dark mode. Use inline `<svg>` with `currentColor` for multi-color icons or when you need animation."
---

# SVG Craft

## When to Use

> Icons, logos, illustrations, and any graphic that needs to scale without quality loss. SVG decisions center on three axes: delivery method, color control, and animation.

## Delivery Method Decision

| If you need... | Use... | Why |
|---|---|---|
| Multi-color icon or complex illustration | Inline `<svg>` in HTML | Full CSS access to internal paths/groups |
| Single-color icon with hover color changes | CSS `mask-image` + `background: currentColor` | No SVG markup in HTML; theming via `color` property |
| Single-color icon, simpler but less flexible | Inline `<svg>` with `currentColor` fills | Direct color control; more HTML weight |
| Static decorative image, no color control needed | `<img src="icon.svg">` | Cached; clean HTML; no color theming possible |
| CSS background pattern or decoration | `background-image: url(pattern.svg)` | Clean separation; cached; cannot use `currentColor` |
| Icon used repeatedly across pages | SVG sprite sheet + `<use>` | One HTTP request; per-instance color via `currentColor` |

## CSS `mask-image` Icon Pattern

The cleanest approach for single-color icon systems in 2024+:

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
<!-- Icon inherits parent's color; hover changes color automatically -->
<a href="/next" class="btn">
  Continue <span class="icon icon-arrow" aria-hidden="true"></span>
</a>
```

Benefits: SVG cached separately from HTML; color controlled by CSS `color` property; works with dark mode and forced colors mode; separates icon shape from icon color completely.

Limitation: Single color only. For multi-color icons, use inline `<svg>`.

## Inline SVG with `currentColor`

```html
<svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
  <path fill="currentColor" d="M12 2L2 7l10 5 10-5-10-5z"/>
</svg>
```

Use `currentColor` as the `fill` value so the icon inherits its parent's text color. Combined with CSS `color` changes on hover/focus, this provides theme-adaptive icons without additional attributes.

## Accessibility

| Use case | Required attributes | Pattern |
|---|---|---|
| Decorative icon (adjacent text explains it) | `aria-hidden="true"` | `<svg aria-hidden="true" focusable="false">` |
| Standalone meaningful icon (no adjacent text) | `role="img"` + `<title>` | `<svg role="img"><title>Close dialog</title>...</svg>` |
| Icon inside button/link | `aria-label` on the button, `aria-hidden` on SVG | `<button aria-label="Close"><svg aria-hidden="true">` |
| Inline SVG with description | `<title>` + `<desc>` + `aria-labelledby` | `<svg aria-labelledby="icon-title icon-desc">` |

**`focusable="false"`** is required on inline SVGs in IE/Edge — without it, SVGs receive keyboard focus separately from their container.

## SVG Optimization with SVGO

Run SVGO on all SVG files before shipping. Key settings:
- **Keep**: `viewBox` (required for responsive scaling), `<title>` if present for accessibility
- **Remove**: Adobe Illustrator/Figma metadata, editor namespaces, comments, empty groups
- **SVGO v4 change**: `removeViewBox` and `removeTitle` are no longer applied by default — this is correct behavior

```bash
# Single file
npx svgo --config svgo.config.js icon.svg

# Directory
npx svgo --config svgo.config.js -f ./icons/
```

```js
// svgo.config.js
export default {
  plugins: [
    { name: 'preset-default', params: { overrides: {
      removeViewBox: false, // Keep viewBox for responsive scaling
      removeTitle: false,   // Keep <title> for accessibility
    }}},
    'removeXMLNS',
    'removeEditorsNSData',
  ]
};
```

## Responsive SVG

SVGs without explicit `width`/`height` but with `viewBox` scale to fill their container:
```html
<!-- Scales to fill any container; aspect-ratio preserved by viewBox -->
<svg viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
```
```css
.svg-container svg { width: 100%; height: auto; }
```

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

## Common Mistakes

- Using `<img src="icon.svg">` and expecting color changes via CSS — `currentColor` and CSS only work on inline SVG or mask-image
- Forgetting `focusable="false"` on inline SVGs in button/link elements — SVG receives tab focus separately in some browsers
- Skipping `aria-hidden` on decorative icons — screen readers announce the SVG as an unlabeled image
- Not running SVGO — Figma/Illustrator export SVGs with 2–5x more bytes than needed
- Omitting `viewBox` — SVG will not scale; always set `viewBox` on exportable icons

## See Also

- [Image Format Strategy](image-format-strategy.md) — when SVG vs raster
- [Image Effects Craft](image-effects-craft.md) — CSS effects applied to SVG containers
- Reference: `css-craft.md` → `clip-path-and-masks` for masking patterns
- Reference: [dbushell SVG Icons with CSS Masks](https://dbushell.com/2024/01/19/svg-icons-with-css-masks/)
- Reference: [Smashing Magazine Accessible SVG Patterns](https://www.smashingmagazine.com/2021/05/accessible-svg-patterns-comparison/)
- Reference: [SVGO documentation](https://svgo.dev/)
