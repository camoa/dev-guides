---
description: Provide alt text, captions, and ARIA roles for images, video, audio, and SVG content so all users can access non-text content.
tldr: Calibrate alt text to context — functional images describe the action, informative images describe meaning, decorative images get `alt=""`; inline SVGs need `role="img"` + `<title>` when informative; never apply `aria-hidden="true"` to a link or button containing only an SVG.
---

# Media Alternatives

## When to Use

> Provide alternatives for all non-text content — images need alt text calibrated to context, videos need captions, and SVGs need role and title when informative.

## Decision: Alt Text by Context

| Image type | Pattern | Example alt |
|---|---|---|
| Functional (links, buttons) | Describe the destination/action | `alt="Search the platform"` |
| Informative (standalone) | Describe the meaning, not the appearance | `alt="Sales growth graph 2024"` |
| Decorative | Empty alt | `alt=""` |
| Complex (charts, infographics) | Short alt + `<figcaption>` or `aria-describedby` | Short summary in alt; full data in caption |
| Inline SVG — informative | `role="img"` + `<title>` inside SVG | — |
| Inline SVG — decorative | `aria-hidden="true"` | — |

**Avoid clichéd prefixes:** Screen readers already announce the element type. `alt="Image of a magnifying glass"` reads "image, Image of a magnifying glass." Write `alt="Search"`.

## Content Visibility Decision Matrix

| Intent | Visual | Screen reader | Focusable | Pattern |
|---|---|---|---|---|
| Visible to all | Yes | Yes | Yes (if interactive) | Standard rendering |
| Screen reader only | No | Yes | Yes (if interactive) | `.visually-hidden` |
| Visual only | Yes | No | No | `aria-hidden="true"` / `role="presentation"` |
| Hidden for all | No | No | No | `hidden` attribute / `display: none` |

**Rule:** If an element can receive keyboard focus, do NOT apply `aria-hidden="true"`.

## Pattern

```html
<!-- Decorative image -->
<img src="divider.png" alt="">

<!-- Decorative inline SVG -->
<svg aria-hidden="true" focusable="false" viewBox="0 0 24 24">
  <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
</svg>

<!-- Informative functional image -->
<a href="/search"><img src="glass.png" alt="Search the platform"></a>

<!-- Informative inline SVG -->
<svg role="img" viewBox="0 0 100 100">
  <title>Company revenue Q3 2024</title>
  <use href="#chart-bars"/>
</svg>

<!-- Complex image with full description -->
<figure>
  <img src="chart.png" alt="Sales growth graph 2024.">
  <figcaption>Sales grew 20% in Q3 due to new platform launch.</figcaption>
</figure>

<!-- Video with captions -->
<video controls>
  <source src="intro.mp4" type="video/mp4">
  <track src="caps.vtt" kind="captions" srclang="en" label="English">
</video>

<!-- Audio with transcript -->
<audio controls src="podcast.mp3" aria-details="transcript"></audio>
<details id="transcript">
  <summary>View transcript</summary>
  <div>Welcome to the show...</div>
</details>
```

## Common Mistakes

- **Wrong**: Missing `focusable="false"` on inline SVG → **Right**: Add it defensively; some older browsers add SVG to the tab order
- **Wrong**: `alt` describing appearance not purpose → **Right**: "Magnifying glass icon" vs "Search" — describe what it means, not what it looks like
- **Wrong**: Skipping captions for video → **Right**: Required for pre-recorded audio content (WCAG 1.2.2)
- **Wrong**: `aria-hidden="true"` on a link or button containing only an SVG → **Right**: The element is still in the tab order; it becomes an invisible focus trap

## See Also

- [Accessible Names](accessible-names.md) — `aria-describedby` on complex images
- Reference: https://www.w3.org/WAI/tutorials/images/
