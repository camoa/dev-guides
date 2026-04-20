---
description: Apply CSS blend modes for duotone, tinted overlays, knockout text, and background compositing — isolation, mix-blend-mode vs background-blend-mode
tldr: "Use CSS blend modes for image color treatment (duotone, tinted overlays), text knockout effects, or creative layering without image editing. Always set `isolation: isolate` on the container to control which stacking context the blend…"
---

# Blend Modes and Visual Effects

## When to Use

> Use CSS blend modes for image color treatment (duotone, tinted overlays), text knockout effects, or creative layering without image editing. Always set `isolation: isolate` on the container to control which stacking context the blend composites against.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Two-color image treatment (duotone) | `mix-blend-mode: multiply` + `screen` on pseudo-elements | Classic duotone without SVG filters |
| Tinted image overlay | `mix-blend-mode: color` on an overlay element | Preserves image luminosity, applies hue/saturation |
| Text that punches through a background | `mix-blend-mode: destination-out` or `screen` | Text becomes a transparent window into what's below |
| Multiply two backgrounds | `background-blend-mode: multiply` | Blend gradient over image in CSS only, no extra elements |
| Soft light treatment | `mix-blend-mode: soft-light` on overlay | Lightens/darkens based on overlay, photographic feel |

### Blend Mode Reference

| Mode | What it does | Good for |
|------|-------------|----------|
| `multiply` | Darkens (black × anything = black) | Dark color overlays, duotone dark channel |
| `screen` | Lightens (white × anything = white) | Light overlays, duotone light channel, knockout text |
| `overlay` | Contrast boost | Texture overlays, photo grading |
| `soft-light` | Gentle overlay variant | Subtle grading |
| `color` | Hue + saturation from top, luminosity from bottom | Colorizing grayscale images |
| `darken` / `lighten` | Picks darker/lighter pixel | Photo blending |
| `difference` | Absolute difference | Psychedelic inversion |

## Pattern

**Duotone effect:**
```css
.duotone { position: relative; isolation: isolate; }
.duotone img { filter: grayscale(1); }
.duotone::before {
  content: ''; position: absolute; inset: 0;
  background: hsl(240 80% 30%); /* Dark channel */
  mix-blend-mode: multiply;
}
.duotone::after {
  content: ''; position: absolute; inset: 0;
  background: hsl(40 90% 70%); /* Light channel */
  mix-blend-mode: screen;
}
```

**Color overlay on image:**
```css
.tinted-image { position: relative; isolation: isolate; }
.tinted-image::after {
  content: ''; position: absolute; inset: 0;
  background: hsl(var(--color-primary-hsl) / 0.6);
  mix-blend-mode: color; /* Preserves image details */
}
```

**Background-blend-mode — single element, no extra DOM:**
```css
.gradient-over-image {
  background-image:
    linear-gradient(135deg, hsl(240 80% 40%), hsl(320 70% 50%)),
    url('texture.jpg');
  background-blend-mode: multiply;
  background-size: cover;
}
```

## Common Mistakes

- **Wrong**: Forgetting `isolation: isolate` on the container — **Right**: Without it, blend modes composite against everything in the stacking context
- **Wrong**: Using blend modes on `fixed` or `sticky` elements — **Right**: Compositing behavior can be browser-inconsistent
- **Wrong**: Confusing `background-blend-mode` and `mix-blend-mode` — **Right**: `background-blend-mode` blends multiple backgrounds within the element; `mix-blend-mode` blends the element against what's behind it
- **Wrong**: Testing only on white backgrounds — **Right**: Duotone effects look completely different on dark page backgrounds
- **Wrong**: Animating blend mode values — **Right**: CSS does not interpolate between blend mode keywords; they snap

## See Also

- [Glassmorphism and Frosted Glass](glassmorphism-and-frosted-glass.md) — `backdrop-filter` for blending with background
- [Text Effects](text-effects.md) — knockout text using blend modes
- Reference: [web.dev: CSS Blend Modes](https://web.dev/learn/css/blend-modes)
- Reference: [MDN: mix-blend-mode](https://developer.mozilla.org/en-US/docs/Web/CSS/mix-blend-mode)
