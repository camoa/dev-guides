---
description: Variable font animation — weight/width hover transitions, scroll-linked font-variation-settings, and per-character weight wave
tldr: "Use `font-variation-settings` transitions for typography that changes weight, width, or slant on interaction. Requires a variable font — standard fonts ignore these properties."
---

# Variable Font Animation

## When to Use
When a client wants typography that "breathes," morphs, or responds to interaction — weight changing on hover, width animating on scroll, or custom axes shifting per character.

## Decision
| Client asks for... | Use... | Why |
|---|---|---|
| Weight change on hover | `transition: font-variation-settings` | Smooth weight interpolation |
| Scroll-linked font weight | `animation-timeline: scroll()` on font-variation-settings | Heavier text as you scroll down |
| Per-character weight wave | JS text split + `animation-delay` per character | Ripple/wave effect |
| Width squeeze/stretch | `font-variation-settings: 'wdth'` animation | Fluid width change |
| Custom axis animation | `font-variation-settings: 'CUSTOM'` | Depends on the variable font |

## Pattern: Weight Change on Hover
```css
.variable-heading {
  font-family: 'Inter Variable', sans-serif;
  font-variation-settings: 'wght' 400;
  transition: font-variation-settings 0.4s var(--ease-standard);
}

.variable-heading:hover {
  font-variation-settings: 'wght' 700;
}
```

## Pattern: Scroll-Linked Weight
```css
.scroll-weight {
  animation: weight-shift linear;
  animation-timeline: scroll(root);
}

@keyframes weight-shift {
  from { font-variation-settings: 'wght' 300; }
  to { font-variation-settings: 'wght' 900; }
}
```

## Pattern: Per-Character Weight Wave
```css
/* After JS text splitting */
.wave-text .char {
  display: inline-block;
  animation: weight-wave 2s ease-in-out infinite;
  animation-delay: calc(var(--i) * 0.05s);
}

@keyframes weight-wave {
  0%, 100% { font-variation-settings: 'wght' 300; }
  50% { font-variation-settings: 'wght' 900; }
}
```

## Common Variable Font Axes
| Axis | Tag | Range Example | Use |
|---|---|---|---|
| Weight | `wght` | 100-900 | Bold on hover/scroll |
| Width | `wdth` | 75-125 | Squeeze/stretch |
| Slant | `slnt` | -12-0 | Italic on interaction |
| Optical Size | `opsz` | 8-144 | Auto-adjusts to font size |
| Custom | varies | font-dependent | Check font docs |

**Popular variable fonts:** Inter, Roboto Flex, Source Sans 3, Recursive, Fraunces (dramatic wght/opsz), Anybody (extreme wdth).

**Browser support:** `font-variation-settings` transitions: all browsers. Production-ready.

## Common Mistakes
- **Using a non-variable font** — standard fonts ignore `font-variation-settings`; check font files for variable axes
- **Animating `font-weight` instead of `font-variation-settings`** — `font-weight` only interpolates between available static weights; `font-variation-settings: 'wght'` interpolates smoothly across the full axis range
- **Heavy per-character animation on mobile** — variable font rendering + many spans = CPU-intensive; limit to key headings

## See Also
- [Text Reveal Animations](text-reveal.md) → combine with text split for reveal + weight animation
- [Micro-Interactions](micro-interactions.md) → hover state weight changes
- Reference: [MDN: font-variation-settings](https://developer.mozilla.org/en-US/docs/Web/CSS/font-variation-settings)
- Reference: [Variable Fonts](https://v-fonts.com/) — searchable variable font catalog
