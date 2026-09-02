---
description: "Eliminate FOIT and FOUT by coordinating font-display strategy, preload, and fallback metric overrides."
tldr: "Use `font-display: swap` for body text with fallback metric overrides (`size-adjust`, `ascent-override`) to minimize CLS; preload only the primary weight of above-fold fonts; always include `crossorigin` on font preloads or the preload is silently ignored."
---

# Web Font Performance

## When to Use

> Web fonts are a common source of both render-blocking (FOIT — Flash of Invisible Text) and layout shift (FOUT — Flash of Unstyled Text causing CLS). Apply these patterns whenever loading custom web fonts. Critical above-fold text fonts need aggressive prioritization; secondary or decorative fonts can be deferred.

## Decision: font-display Strategy

| Value | FOIT block period | Swap period | CLS risk | Use for |
|-------|------------------|-------------|----------|---------|
| `block` | ~3 seconds | Infinite | High | Avoid — invisible text for up to 3s |
| `swap` | None | Infinite | High | Body text where invisible text is unacceptable and CLS is tolerable |
| `fallback` | ~100ms | ~3 seconds | Low-medium | Good default for most body fonts |
| `optional` | ~100ms | None (browser decides) | Minimal | Non-critical fonts; best CLS score; may show fallback on slow connections |

**Google's recommendation:** Use `font-display: optional` for non-essential decorative fonts; `font-display: swap` for body text where reading before font loads is required; pair with fallback metric adjustments (see below) to reduce CLS from both.

## Decision: When to Preload

| Font scenario | Recommendation |
|---------------|----------------|
| Above-fold heading font, loaded via `@font-face` | `<link rel="preload" as="font" crossorigin>` — browser won't discover @font-face fonts until CSSOM is built |
| Body text font needed immediately | Preload the primary weight/style only; defer italic/bold variants |
| Decorative or below-fold font | Skip preload; `font-display: optional` handles deferral gracefully |
| More than 3 font preloads on one page | Stop — preload contention starves LCP image; subset aggressively or use `font-display: optional` instead |

## Pattern

```html
<!-- MANDATORY: crossorigin even for same-origin fonts -->
<link rel="preload"
  href="/fonts/brand-regular.woff2"
  as="font" type="font/woff2"
  crossorigin>
```

```css
@font-face {
  font-family: 'Brand';
  src: url('/fonts/brand-regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;

  /* Metric overrides: adjust fallback font metrics to match Brand,
     eliminating CLS during the swap period.
     Tune these values by comparing fallback vs. web font layout. */
  ascent-override: 90%;
  descent-override: 22%;
  line-gap-override: 0%;
  size-adjust: 104%;
}

/* System font stack fallback that closely matches Brand for layout */
body {
  font-family: 'Brand', Arial, sans-serif;
}
```

## Pattern: font-display: optional (Zero CLS)

When font CLS is causing a poor CLS score, `optional` tells the browser not to swap the font after the initial load window. Users on fast connections see the web font; users on slow connections see the fallback. Layout never shifts.

```css
@font-face {
  font-family: 'Decorative';
  src: url('/fonts/decorative.woff2') format('woff2');
  font-display: optional;  /* No swap if font doesn't load in time */
}
```

Preloading a `font-display: optional` font is recommended — it increases the chance the font arrives within the initial block period and gets used:
```html
<link rel="preload" href="/fonts/decorative.woff2" as="font" type="font/woff2" crossorigin>
```

## Common Mistakes

- Preloading fonts without `crossorigin` — the preload is silently ignored, even for same-origin fonts; always include `crossorigin`
- Preloading all font weights and styles — a single font family can have 10+ files; only preload the regular weight for the primary typeface
- `font-display: block` — causes up to 3 seconds of invisible text (FOIT); only use for icon fonts where fallback characters would be meaningless
- Not subsetting fonts — a full-character-set woff2 can be 200-400KB; subset to the character ranges your content actually uses
- Loading fonts from multiple origins — each origin requires DNS + TLS handshake; self-host or use `preconnect` for third-party foundries

## See Also

- [Resource Hints](resource-hints.md) — `preconnect` for Google Fonts CDN; `preload` priority coordination
- [Core Web Vitals Overview](core-web-vitals-overview.md) — CLS thresholds; font swap contributes directly to CLS score
- Reference: [web.dev: Best practices for fonts](https://web.dev/articles/font-best-practices)
- Reference: [web.dev: CSS size-adjust for fallback fonts](https://web.dev/articles/css-size-adjust)
