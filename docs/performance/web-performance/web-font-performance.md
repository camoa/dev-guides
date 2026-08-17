---
description: Eliminate FOIT and FOUT by coordinating font-display strategy, preload, and fallback metric overrides.
tldr: "Use `font-display: swap` for body text with fallback metric overrides (`size-adjust`, `ascent-override`) to minimize CLS; preload only the primary weight of above-fold fonts; always include `crossorigin` on font preloads or the preload is silently ignored."
---

# Web Font Performance

## When to Use

> Apply whenever loading custom web fonts. Critical above-fold text fonts need aggressive prioritization; secondary or decorative fonts can be deferred. Web fonts are a common source of both render-blocking (FOIT) and layout shift (FOUT/CLS).

## Decision: font-display Strategy

| Value | FOIT block | Swap period | CLS risk | Use for |
|-------|-----------|-------------|----------|---------|
| `block` | ~3 seconds | Infinite | High | Avoid — invisible text for up to 3s |
| `swap` | None | Infinite | High | Body text where invisible text is unacceptable; pair with metric overrides to reduce CLS |
| `fallback` | ~100ms | ~3 seconds | Low-medium | Good default for most body fonts |
| `optional` | ~100ms | None | Minimal | Non-critical fonts; best CLS score; may show fallback on slow connections |

## Decision: When to Preload

| Font scenario | Recommendation |
|---------------|----------------|
| Above-fold heading font via `@font-face` | `<link rel="preload" as="font" crossorigin>` — browser won't discover @font-face fonts until CSSOM is built |
| Body text font needed immediately | Preload the primary weight/style only; defer italic/bold variants |
| Decorative or below-fold font | Skip preload; `font-display: optional` handles deferral gracefully |
| More than 3 font preloads on one page | Stop — preload contention starves LCP image; subset aggressively instead |

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
     eliminating CLS during the swap period. Tune by comparing layouts. */
  ascent-override: 90%;
  descent-override: 22%;
  line-gap-override: 0%;
  size-adjust: 104%;
}

body { font-family: 'Brand', Arial, sans-serif; }
```

```css
/* Zero CLS: font-display optional never swaps after initial load window */
@font-face {
  font-family: 'Decorative';
  src: url('/fonts/decorative.woff2') format('woff2');
  font-display: optional;
}
```

## Common Mistakes

- **Wrong**: `<link rel="preload" as="font">` without `crossorigin` → **Right**: Font preload is silently ignored without `crossorigin`, even for same-origin fonts
- **Wrong**: Preloading all font weights and styles → **Right**: A single family can have 10+ files; only preload the regular weight for the primary typeface
- **Wrong**: `font-display: block` → **Right**: Causes up to 3 seconds of invisible text (FOIT); only use for icon fonts where fallback characters are meaningless
- **Wrong**: Not subsetting fonts → **Right**: A full-character-set woff2 can be 200–400KB; subset to the character ranges your content uses
- **Wrong**: Loading fonts from multiple origins → **Right**: Each origin requires DNS + TLS handshake; self-host or use `preconnect` for third-party foundries

## See Also

- [Resource Hints](resource-hints.md) — `preconnect` for Google Fonts CDN; `preload` priority coordination
- [Core Web Vitals Overview](core-web-vitals-overview.md) — CLS thresholds; font swap contributes directly to CLS
- Reference: [web.dev: Best practices for fonts](https://web.dev/articles/font-best-practices)
- Reference: [web.dev: CSS size-adjust for fallback fonts](https://web.dev/articles/css-size-adjust)
