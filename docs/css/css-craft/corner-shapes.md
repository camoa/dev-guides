---
description: Corner shapes — squircle, scooped corners, notched/beveled cuts with corner-shape (Chrome 2025+) and clip-path fallbacks
tldr: "Use `corner-shape: squircle` for iOS-style superellipse corners on Chrome 2025+. Use `clip-path: polygon()` for notched/beveled corners across all browsers."
---

# Corner Shapes

## When to Use
When a client wants squircle corners (Apple/iOS style), scooped/notched corners, or other non-circular border radius effects.

## Decision
| Client asks for... | Use... | Why |
|---|---|---|
| iOS-style squircle (superellipse) | `corner-shape: squircle` (Chrome 2025+) | Native, no SVG or mask needed |
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

## Pattern: Cross-Browser Squircle (Fallback)
```css
.squircle {
  /* SVG-based mask fallback for non-Chrome */
  mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'%3E%3Crect width='200' height='200' rx='40' ry='40' style='paint-order:stroke'/%3E%3C/svg%3E");
  mask-size: cover;
}

/* With @supports progressive enhancement */
@supports (corner-shape: squircle) {
  .squircle {
    mask-image: none;
    border-radius: 20px;
    corner-shape: squircle;
  }
}
```

## Pattern: Notched Corners with clip-path
```css
/* Cut corners (tech/gaming style) */
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

**Browser support:** `corner-shape`: Chrome/Edge only (2025+). `clip-path` notches: all browsers. Use progressive enhancement.

## Common Mistakes
- **Using `corner-shape` without `border-radius`** — `corner-shape` modifies how `border-radius` curves render; it needs a radius to work on
- **Expecting `corner-shape` in Firefox/Safari** — Chromium-only; provide `@supports` fallback
- **Using clip-path for simple rounding** — `border-radius` is simpler, more performant, and supports box-shadow

## See Also
- [CSS Shapes & Decorative Geometry](css-shapes.md) → broader shape techniques
- [3D Transforms](3d-transforms.md) → perspective on shaped cards
- Reference: [Chrome: corner-shape](https://developer.chrome.com/blog/css-corner-shape)
