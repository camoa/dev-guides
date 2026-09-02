---
description: Gradient text, animated gradients, knockout text, and layered text-shadows for display type — background-clip technique, @property animation, blend mode knockout
tldr: "Use text effects on display type only: hero headlines, pull quotes, section titles. Body copy with gradient text or heavy shadows destroys readability."
---

# Text Effects

## When to Use
Text effects — gradient fills, animated gradients, shadows, knockout — should be reserved for display type: hero headlines, pull quotes, section titles. Body copy with gradient text or heavy shadows destroys readability. The craft question is: does this effect serve the content hierarchy, or is it decoration for its own sake?

## Decision
| If you need... | Use... | Why |
|---|---|---|
| Gradient-filled text | `background-clip: text` + `color: transparent` | No SVG, works on any text |
| Animated gradient text | `@property` registered color + animation, or `background-position` shift | `@property` interpolates colors cleanly; position shift is simpler |
| Text that punches a hole in a color | `mix-blend-mode: destination-out` pattern | Text becomes transparent, background shows through |
| Letterpress / emboss shadow | Multiple `text-shadow` layers | Stacked shadows with opposing offsets |
| Long text shadow (retro) | Stacked `text-shadow` via CSS custom property | Comma-separated layers create depth |
| Text over image (contrast) | `text-shadow: 0 1px 3px hsl(0 0% 0% / 0.6)` | Minimal but effective; avoid thick text shadows on body copy |

## Pattern

**Gradient text — static:**

```css
.gradient-heading {
  --grad-start: hsl(250 80% 60%);
  --grad-end: hsl(340 80% 60%);

  background: linear-gradient(135deg, var(--grad-start), var(--grad-end));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  /* Fallback for older browsers */
  @supports not (-webkit-background-clip: text) {
    color: var(--grad-start);
    background: none;
  }
}
```

**Animated gradient text — background-position shift** (simpler, wider support):

```css
.animated-gradient-text {
  --bg-size: 400%;
  --color-one: hsl(15 90% 55%);
  --color-two: hsl(250 90% 60%);

  background: linear-gradient(
    90deg,
    var(--color-one),
    var(--color-two),
    var(--color-one)
  ) 0 0 / var(--bg-size) 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;

  @media (prefers-reduced-motion: no-preference) {
    animation: gradient-shift 8s linear infinite;
  }
}

@keyframes gradient-shift {
  to { background-position: var(--bg-size) 0; }
}
```

**Animated gradient text — `@property` approach** (cleaner color interpolation):

> **Feature reference:** See [modern-css → at-property](../modern-css/at-property.md) for `@property` syntax and browser support.

```css
@property --text-grad-start {
  syntax: "<color>";
  initial-value: hsl(15 90% 55%);
  inherits: false;
}

.shimmer-text {
  background: linear-gradient(90deg, var(--text-grad-start), hsl(250 90% 60%));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;

  @media (prefers-reduced-motion: no-preference) {
    animation: shift-color 3s var(--ease-standard) infinite alternate;
  }
}

@keyframes shift-color {
  to { --text-grad-start: hsl(250 90% 60%); }
}
```

**Knockout text** — text punches a hole through a colored layer to reveal what's behind:

```css
.knockout-wrapper {
  position: relative;
  isolation: isolate;
  background: url('image.jpg') center / cover;
}

.knockout-text {
  position: relative;
  background: var(--color-primary);
  mix-blend-mode: destination-out; /* Text becomes transparent */
  font-size: clamp(3rem, 8vw, 8rem);
  font-weight: 900;
  color: black; /* Color value controls opacity of knockout */
}
```

**Layered text-shadow** — depth effect for display type:

```css
.shadow-heading {
  --shadow-color: hsl(220 60% 15%);

  text-shadow:
    1px 1px 0   var(--shadow-color),
    2px 2px 0   var(--shadow-color),
    3px 3px 0   var(--shadow-color),
    4px 4px 0   var(--shadow-color),
    5px 5px 10px hsl(0 0% 0% / 0.3);
}
```

## Common Mistakes
- Applying gradient text to body copy — illegible at small sizes; screen readers read it fine but low-vision users cannot
- Missing `-webkit-background-clip` — required in Safari even in 2025 alongside the standard `background-clip`
- Forgetting `color: transparent` — without it the gradient is hidden behind the text color fill
- Animating `background-clip: text` without `@property` — browsers cannot interpolate unregistered custom properties in gradients, they snap
- Multiple `text-shadow` layers exceeding 10px blur on body text — performance cost and visual noise; reserve for display sizes only
- `mix-blend-mode: destination-out` knockout without `isolation: isolate` on the wrapper — the knockout punches through the entire page instead of just the container

## See Also
- [Blend Modes and Visual Effects](blend-modes-and-visual-effects.md) — `mix-blend-mode` values explained
- [Gradient Craft](gradient-craft.md) — animated gradients using `@property`
- [Accessibility and Motion](accessibility-and-motion.md) — `prefers-reduced-motion` for animated text
- Reference: [web.dev: Animated Gradient Text](https://web.dev/articles/speedy-css-tip-animated-gradient-text)
- Reference: [MDN: background-clip](https://developer.mozilla.org/en-US/docs/Web/CSS/background-clip)
- Reference: [CSS-Tricks: Knockout Text Techniques](https://css-tricks.com/css-techniques-and-effects-for-knockout-text/)
