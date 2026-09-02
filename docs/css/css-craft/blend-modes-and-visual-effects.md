---
description: Apply CSS blend modes for duotone, tinted overlays, knockout text, and background compositing — isolation, mix-blend-mode vs background-blend-mode
tldr: "Use CSS blend modes for image color treatment (duotone, tinted overlays), text knockout effects, or creative layering without image editing. Always set `isolation: isolate` on the container to control which stacking context the blend…"
---

# Blend Modes and Visual Effects

## When to Use
CSS blend modes (`mix-blend-mode`, `background-blend-mode`) let you apply Photoshop-style compositing without image editing. Reach for them when you need image color treatment (duotone, tinted overlays), text knockout effects, or creative layering. They are a rendering hint — the browser composites on the GPU, but stacking contexts matter and debugging can be non-obvious.

## Decision
| If you need... | Use... | Why |
|---|---|---|
| Two-color image treatment (duotone) | `mix-blend-mode: multiply` + `screen` on pseudo-elements | Classic duotone without SVG filters |
| Tinted image overlay | `mix-blend-mode: color` on an overlay element | Preserves image luminosity, applies hue/saturation |
| Text that punches through a background | `mix-blend-mode: destination-out` or `screen` technique | Text becomes transparent window into what's below |
| Multiply two backgrounds | `background-blend-mode: multiply` | Blend gradient over image in CSS only, no extra elements |
| Soft light treatment | `mix-blend-mode: soft-light` on overlay | Lightens/darkens based on overlay, photographic feel |

## Blend Mode Reference

| Mode | What it does | Good for |
|---|---|---|
| `multiply` | Darkens (black × anything = black) | Dark color overlays, shadows, duotone dark channel |
| `screen` | Lightens (white × anything = white) | Light overlays, duotone light channel, knockout text |
| `overlay` | Contrast boost (multiply darks, screen lights) | Texture overlays, photo grading |
| `soft-light` | Gentle overlay variant | Subtle grading, less harsh than overlay |
| `color` | Hue + saturation from top, luminosity from bottom | Colorizing grayscale images |
| `luminosity` | Luminosity from top, hue/saturation from bottom | Inverse of `color` |
| `darken` | Picks darker of two pixels | Photo blending without mixing |
| `lighten` | Picks lighter of two pixels | Duotone, light leak effects |
| `difference` | Absolute difference (black = same) | Psychedelic inversion effects |
| `exclusion` | Low-contrast difference | Soft inversion, sepia-like |

## Pattern

**Duotone effect** — two-color image treatment using layered pseudo-elements:

```css
.duotone {
  --duotone-shadow: hsl(240 80% 30%); /* Dark color — fills shadows */
  --duotone-highlight: hsl(40 90% 70%); /* Light color — fills highlights */
  position: relative;
  isolation: isolate;
}

.duotone img {
  filter: grayscale(1);
}

/* Dark channel: multiply darkens image with shadow color */
.duotone::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--duotone-shadow);
  mix-blend-mode: multiply;
}

/* Light channel: screen lightens image with highlight color */
.duotone::after {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--duotone-highlight);
  mix-blend-mode: screen;
}
```

**Color overlay on image:**

```css
.tinted-image {
  --tint: hsl(var(--color-primary-hsl) / 0.6);
  position: relative;
  isolation: isolate;
}

.tinted-image::after {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--tint);
  mix-blend-mode: color;  /* Preserves image details */
}
```

**Background-blend-mode** — single element, no extra DOM:

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
- Forgetting `isolation: isolate` on the container — without it, blend modes composite against everything in the stacking context, not just siblings; results are unpredictable
- Using blend modes on `fixed` or `sticky` positioned elements — compositing behavior can be browser-inconsistent
- `background-blend-mode` and `mix-blend-mode` are not the same — `background-blend-mode` blends multiple backgrounds within the element; `mix-blend-mode` blends the entire element against what's behind it
- Testing only on white backgrounds — duotone and tint effects look completely different on dark or colored page backgrounds
- Animating blend mode values — CSS does not interpolate between blend mode keywords; they snap immediately

## See Also
- [Glassmorphism and Frosted Glass](glassmorphism-and-frosted-glass.md) — `backdrop-filter` for blending with background
- [Text Effects](text-effects.md) — knockout text using blend modes
- Reference: [web.dev: CSS Blend Modes](https://web.dev/learn/css/blend-modes)
- Reference: [MDN: mix-blend-mode](https://developer.mozilla.org/en-US/docs/Web/CSS/mix-blend-mode)
