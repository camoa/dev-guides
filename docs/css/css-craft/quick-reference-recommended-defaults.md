---
description: Complete CSS craft token set — copy-paste easing, duration, shadow, opacity, state overlay, and skeleton defaults for any project
tldr: "Copy this complete token set into any project as a starting point. All values are based on MD3 motion tokens, cross-design-system opacity standards, and layered shadow methodology."
---

# Quick Reference: Recommended Defaults

## When to Use
Copy this complete token set into any project as a starting point. All values are based on MD3 motion tokens, cross-design-system opacity standards, and layered shadow methodology.

## Complete Token Set

```css
:root {
  /* ===========================
     EASING CURVES (MD3-aligned)
     =========================== */
  --ease-default:          cubic-bezier(0.2, 0, 0, 1);     /* General UI */
  --ease-enter:            cubic-bezier(0.05, 0.7, 0.1, 1); /* Elements entering */
  --ease-exit:             cubic-bezier(0.3, 0, 0.8, 0.15); /* Elements leaving */
  --ease-decel:            cubic-bezier(0, 0, 0, 1);        /* Standard decelerate */
  --ease-accel:            cubic-bezier(0.3, 0, 1, 1);      /* Standard accelerate */

  /* ===========================
     DURATION SCALE (50ms steps)
     =========================== */
  --duration-instant:  50ms;    /* Micro-feedback (ripple) */
  --duration-micro:   100ms;    /* State changes (checkbox, toggle) */
  --duration-fast:    150ms;    /* Hover/active states */
  --duration-normal:  200ms;    /* Small component transitions */
  --duration-medium:  300ms;    /* Component enter/exit (modal, popover) */
  --duration-slow:    400ms;    /* Larger transitions */
  --duration-slower:  500ms;    /* Complex choreographed motion */

  /* ===========================
     REVEAL DISTANCES
     =========================== */
  --reveal-distance:    20px;   /* Entrance animation translate */
  --hover-lift:          2px;   /* Card hover translateY */
  --active-scale:       0.97;   /* Button active scale */

  /* ===========================
     SHADOW SYSTEM
     =========================== */
  --shadow-color:     220deg 60% 50%;
  --shadow-strength:  0.1;

  /* ===========================
     TEXT HIERARCHY (alpha)
     =========================== */
  --alpha-primary:     1.0;     /* Headlines, body, primary labels */
  --alpha-secondary:   0.7;     /* Subtitles, descriptions, metadata */
  --alpha-tertiary:    0.5;     /* Captions, hints, timestamps */
  --alpha-disabled:    0.38;    /* Disabled labels, inactive controls */

  /* ===========================
     STATE OVERLAYS (alpha)
     =========================== */
  --state-hover:    0.08;
  --state-focus:    0.12;
  --state-pressed:  0.16;
  --state-disabled: 0.38;

  /* ===========================
     STRUCTURAL OPACITY
     =========================== */
  --divider:        0.12;
  --overlay-scrim:  0.32;

  /* ===========================
     SKELETON LOADING
     =========================== */
  --skeleton-bg:    hsl(220 15% 90%);
  --skeleton-shine: hsl(220 15% 97%);
  --skeleton-speed: 1.5s;
}

/* Dark mode adjustments */
[data-theme="dark"] {
  --shadow-color:    220deg 40% 2%;
  --shadow-strength: 0.25;
  --skeleton-bg:    hsl(220 15% 18%);
  --skeleton-shine: hsl(220 15% 25%);
}
```

## Cheat Sheet

| What | Value | Notes |
|---|---|---|
| **Hover translate** | `translateY(-2px)` | Never more than 4px |
| **Active press** | `scale(0.97)` | Duration: instant (50ms) |
| **Hover duration** | 150ms | With `--ease-default` |
| **Enter duration** | 300ms | With `--ease-enter` (decel) |
| **Exit duration** | 200ms | With `--ease-exit` (accel) |
| **Reveal distance** | 16-24px | `translateY(20px)` is the sweet spot |
| **Stagger delay** | 75ms per item | Max total: 400ms |
| **Max single animation** | 600ms | Beyond this feels slow |
| **Animate only** | transform, opacity, filter, clip-path | Compositor-only = 60fps |
| **Shadow layers** | 2 (rest), 3 (hover), 5 (modal) | Progressive blur + offset |
| **Text secondary alpha** | 0.7 (light), 0.6 (dark) | Color channel, not `opacity` |
| **Reduced motion** | Replace motion with crossfade | Not a kill switch |
| **Focus ring** | 2px solid, 3:1 contrast | With `forced-colors` fallback |
| **Parallax layers** | 2-3 max | More = nauseating |
| **Glass blur** | 10-16px | Max 20px on desktop; 6-8px on mobile |
| **Glass elements per viewport** | 3-5 max | 10+ causes lag on mid-range phones |
| **3D max tilt** | 8-12° | Beyond 15° looks broken |
| **Spring easing** | Use a generator tool | Never hand-write `linear()` |
| **Skeleton speed** | 1.5s shimmer, 2s pulse (reduced motion) | |

## Common Mistakes
- Copying tokens without adjusting `--shadow-color` to match the project's background hue — tinted shadows should harmonize with the palette
- Using all tokens at once — start with easing + duration + shadows; add hierarchy alpha and state overlays as the design matures
- Overriding token values in component CSS instead of using them — defeats the purpose of a tuneable system

## See Also
- [Motion Design Tokens](motion-design-tokens.md) — detailed rationale for each value
- [Elevation and Shadows](elevation-and-shadows.md) — how to use the shadow system
- [Opacity and Visual Hierarchy](opacity-and-visual-hierarchy.md) — how to apply alpha tokens
