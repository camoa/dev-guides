---
description: Gradient text, animated gradients, knockout text, and layered text-shadows for display type — background-clip technique, @property animation, blend mode knockout
---

# Text Effects

## When to Use

> Use text effects on display type only: hero headlines, pull quotes, section titles. Body copy with gradient text or heavy shadows destroys readability. The craft question: does this effect serve content hierarchy, or is it decoration for its own sake?

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Gradient-filled text | `background-clip: text` + `color: transparent` | No SVG, works on any text |
| Animated gradient text | `background-position` shift or `@property` registered color | Position shift is simpler; `@property` interpolates colors cleanly |
| Text that punches a hole in a color | `mix-blend-mode: destination-out` pattern | Text becomes transparent, background shows through |
| Letterpress / emboss shadow | Multiple `text-shadow` layers | Stacked shadows with opposing offsets |
| Text over image (contrast) | `text-shadow: 0 1px 3px hsl(0 0% 0% / 0.6)` | Minimal but effective |

## Pattern

**Gradient text — static:**
```css
.gradient-heading {
  background: linear-gradient(135deg, hsl(250 80% 60%), hsl(340 80% 60%));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
```

**Animated gradient text — background-position shift:**
```css
.animated-gradient-text {
  background: linear-gradient(90deg, hsl(15 90% 55%), hsl(250 90% 60%), hsl(15 90% 55%)) 0 0 / 400% 100%;
  -webkit-background-clip: text; background-clip: text; color: transparent;
  @media (prefers-reduced-motion: no-preference) { animation: gradient-shift 8s linear infinite; }
}
@keyframes gradient-shift { to { background-position: 400% 0; } }
```

**Animated gradient text — `@property` approach (cleaner interpolation):**
```css
@property --text-grad-start { syntax: "<color>"; initial-value: hsl(15 90% 55%); inherits: false; }
.shimmer-text {
  background: linear-gradient(90deg, var(--text-grad-start), hsl(250 90% 60%));
  -webkit-background-clip: text; background-clip: text; color: transparent;
  @media (prefers-reduced-motion: no-preference) { animation: shift-color 3s var(--ease-standard) infinite alternate; }
}
@keyframes shift-color { to { --text-grad-start: hsl(250 90% 60%); } }
```

**Knockout text:**
```css
.knockout-wrapper { position: relative; isolation: isolate; background: url('image.jpg') center / cover; }
.knockout-text {
  background: var(--color-primary);
  mix-blend-mode: destination-out; /* Text becomes transparent */
  font-size: clamp(3rem, 8vw, 8rem); font-weight: 900;
  color: black; /* Controls opacity of knockout */
}
```

**Layered text-shadow for display type:**
```css
.shadow-heading {
  text-shadow: 1px 1px 0 hsl(220 60% 15%), 2px 2px 0 hsl(220 60% 15%),
               3px 3px 0 hsl(220 60% 15%), 4px 4px 0 hsl(220 60% 15%),
               5px 5px 10px hsl(0 0% 0% / 0.3);
}
```

## Common Mistakes

- **Wrong**: Gradient text on body copy — **Right**: Illegible at small sizes; reserve for display sizes only
- **Wrong**: Missing `-webkit-background-clip` — **Right**: Required in Safari even in 2025
- **Wrong**: Forgetting `color: transparent` — **Right**: Without it the gradient is hidden behind the text fill
- **Wrong**: Animating gradient text without `@property` — **Right**: Browsers snap unregistered custom properties in gradients
- **Wrong**: `mix-blend-mode: destination-out` without `isolation: isolate` — **Right**: The knockout punches through the entire page

## See Also

- [Blend Modes and Visual Effects](blend-modes-and-visual-effects.md) — `mix-blend-mode` values explained
- [Gradient Craft](gradient-craft.md) — animated gradients using `@property`
- [Accessibility and Motion](accessibility-and-motion.md) — `prefers-reduced-motion` for animated text
- Reference: [web.dev: Animated Gradient Text](https://web.dev/articles/speedy-css-tip-animated-gradient-text)
- Reference: [MDN: background-clip](https://developer.mozilla.org/en-US/docs/Web/CSS/background-clip)
- Reference: [CSS-Tricks: Knockout Text Techniques](https://css-tricks.com/css-techniques-and-effects-for-knockout-text/)
