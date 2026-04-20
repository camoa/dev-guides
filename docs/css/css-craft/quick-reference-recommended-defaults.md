---
description: Complete CSS craft token set — copy-paste easing, duration, shadow, opacity, state overlay, and skeleton defaults for any project
tldr: "Copy this complete token set into any project as a starting point. All values are based on MD3 motion tokens, cross-design-system opacity standards, and layered shadow methodology."
---

# Quick Reference: Recommended Defaults

## When to Use

> Copy this complete token set into any project as a starting point. All values are based on MD3 motion tokens, cross-design-system opacity standards, and layered shadow methodology.

## Decision

| What | Value | Notes |
|------|-------|-------|
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
| **Glass blur** | 10-16px | Max 20px desktop; 6-8px mobile |
| **Glass elements/viewport** | 3-5 max | 10+ causes lag |
| **3D max tilt** | 8-12° | Beyond 15° looks broken |
| **Spring easing** | Use a generator tool | Never hand-write `linear()` |
| **Skeleton speed** | 1.5s shimmer, 2s pulse | 2s for reduced-motion |

## Pattern

```css
:root {
  /* Easing Curves */
  --ease-default:  cubic-bezier(0.2, 0, 0, 1);
  --ease-enter:    cubic-bezier(0.05, 0.7, 0.1, 1);
  --ease-exit:     cubic-bezier(0.3, 0, 0.8, 0.15);
  --ease-decel:    cubic-bezier(0, 0, 0, 1);
  --ease-accel:    cubic-bezier(0.3, 0, 1, 1);

  /* Duration Scale */
  --duration-instant:  50ms;
  --duration-micro:   100ms;
  --duration-fast:    150ms;
  --duration-normal:  200ms;
  --duration-medium:  300ms;
  --duration-slow:    400ms;
  --duration-slower:  500ms;

  /* Reveal / Interaction */
  --reveal-distance:  20px;
  --hover-lift:        2px;
  --active-scale:     0.97;

  /* Shadow System */
  --shadow-color:    220deg 60% 50%;
  --shadow-strength: 0.1;

  /* Text Hierarchy (alpha) */
  --alpha-primary:   1.0;
  --alpha-secondary: 0.7;
  --alpha-tertiary:  0.5;
  --alpha-disabled:  0.38;

  /* State Overlays (alpha) */
  --state-hover:    0.08;
  --state-focus:    0.12;
  --state-pressed:  0.16;
  --state-disabled: 0.38;

  /* Structural */
  --divider:       0.12;
  --overlay-scrim: 0.32;

  /* Skeleton */
  --skeleton-bg:    hsl(220 15% 90%);
  --skeleton-shine: hsl(220 15% 97%);
  --skeleton-speed: 1.5s;
}

[data-theme="dark"] {
  --shadow-color:    220deg 40% 2%;
  --shadow-strength: 0.25;
  --skeleton-bg:    hsl(220 15% 18%);
  --skeleton-shine: hsl(220 15% 25%);
}
```

## Common Mistakes

- **Wrong**: Copying tokens without adjusting `--shadow-color` to match your project's background hue — **Right**: Tinted shadows should harmonize with the palette
- **Wrong**: Using all tokens at once — **Right**: Start with easing + duration + shadows; add hierarchy alpha and state overlays as the design matures
- **Wrong**: Overriding token values in component CSS — **Right**: Use the tokens; overriding defeats the tuneable system

## See Also

- [Motion Design Tokens](motion-design-tokens.md) — detailed rationale for each easing and duration value
- [Elevation and Shadows](elevation-and-shadows.md) — how to use the shadow system
- [Opacity and Visual Hierarchy](opacity-and-visual-hierarchy.md) — how to apply alpha tokens
