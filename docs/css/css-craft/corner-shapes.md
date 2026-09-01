---
description: Corner shapes — squircle, scooped corners, notched/beveled cuts with corner-shape (Chrome 2025+) and clip-path fallbacks
tldr: "Use `corner-shape: squircle` for iOS-style superellipse corners on Chrome 2025+. Use `clip-path: polygon()` for notched/beveled corners across all browsers."
---

# Corner Shapes

## When to Use

> Use `corner-shape: squircle` for iOS-style superellipse corners on Chrome 2025+. Use `clip-path: polygon()` for notched/beveled corners across all browsers. Always provide `@supports` fallbacks.

## Decision

| Client asks for... | Use... | Why |
|---|---|---|
| iOS-style squircle | `corner-shape: squircle` (Chrome 2025+) | Native, no SVG or mask needed |
| Scooped/concave corners | `corner-shape: scoop` (Chrome 2025+) | Inward-curving corners |
| Notched/cut corners | `clip-path: polygon()` | Angled cuts at corners |
| Beveled corners | `clip-path: polygon()` | Chamfered edges |
| Cross-browser squircle now | `mask-image` with SVG superellipse | Works everywhere |
| Asymmetric rounding | 8-value `border-radius` | e.g., `30% 70% 70% 30% / 30% 30% 70% 70%` |

## Pattern: Native Squircle (Chrome 2025+)

```css
.card {
  border-radius: 20px;
  corner-shape: squircle; /* Superellipse — smoother than circular */
}

/* Scooped corners */
.badge {
  border-radius: 16px;
  corner-shape: scoop; /* Concave/inward curve */
}

/* Per-corner control */
.notch-card {
  border-radius: 20px;
  corner-shape: round squircle round squircle; /* Mixed corners */
}
```

## Pattern

```css
/* Native squircle — Chrome 2025+ */
.card {
  border-radius: 20px;
  corner-shape: squircle;
}

/* Progressive enhancement with fallback */
.squircle {
  mask-image: url("data:image/svg+xml,...");
  mask-size: cover;
}
@supports (corner-shape: squircle) {
  .squircle {
    mask-image: none;
    border-radius: 20px;
    corner-shape: squircle;
  }
}

/* Notched corners — all browsers */
.notched {
  --notch: 12px;
  clip-path: polygon(
    var(--notch) 0, calc(100% - var(--notch)) 0,
    100% var(--notch), 100% calc(100% - var(--notch)),
    calc(100% - var(--notch)) 100%, var(--notch) 100%,
    0 calc(100% - var(--notch)), 0 var(--notch)
  );
}

/* Single top-right notch */
.ticket {
  clip-path: polygon(0 0, calc(100% - 20px) 0, 100% 20px, 100% 100%, 0 100%);
}
```

## Common Mistakes

- **Using `corner-shape` without `border-radius`** — `corner-shape` modifies how `border-radius` renders; it needs a radius to work
- **Expecting `corner-shape` in Firefox/Safari** — Chromium-only; provide `@supports` fallback
- **Using clip-path for simple rounding** — `border-radius` is simpler, more performant, and supports box-shadow

## See Also

- [CSS Shapes & Decorative Geometry](css-shapes.md) → broader shape techniques
- [3D Transforms](3d-transforms.md) → perspective on shaped cards
- Reference: [Chrome: corner-shape](https://developer.chrome.com/blog/css-corner-shape)
