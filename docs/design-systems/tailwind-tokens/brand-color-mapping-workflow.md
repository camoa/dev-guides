---
description: Map brand guidelines to DaisyUI semantic color system
---

# Brand Color Mapping Workflow

## When to Use

> Use this when you receive brand guidelines (hex colors, Pantone, etc.) and need to map them to DaisyUI's semantic color system.

## Decision

| Brand Asset | DaisyUI Role | Rationale |
|---|---|---|
| Primary brand color | --color-primary | CTAs, main actions |
| Secondary brand color | --color-secondary | Supporting actions |
| Accent / highlight | --color-accent | Emphasis, decorative |
| Darkest neutral | --color-neutral | Footer, navbar |
| Lightest background | --color-base-100 | Page background |
| Card/section bg | --color-base-200 | Elevated surfaces |
| Border/divider gray | --color-base-300 | Subtle separators |
| Default text color | --color-base-content | Body copy |

## Pattern

**Step 1: Extract brand colors from source**

Gather primary, secondary, and accent colors from brand assets. Note: you typically receive hex values.

**Step 2: Convert to oklch**

DaisyUI v5 built-in themes use oklch. Custom themes can use any format, but oklch is recommended for perceptually uniform lightness adjustments.

```javascript
// Browser DevTools or Node.js with culori library
import { oklch, parse } from 'culori';
const result = oklch(parse('#3b82f6'));
// { mode: 'oklch', l: 0.6232, c: 0.2135, h: 259.53 }
// → oklch(62.32% 0.2135 259.53)
```

Online tool: oklch.com provides interactive conversion with visual feedback.

**Step 3: Generate content colors**

Rule of thumb: dark background (lightness < 50%) gets light content (~95-98%), light background (>= 50%) gets dark content (~15-25%). Keep the hue angle the same as the parent for tonal harmony.

```css
--color-primary: oklch(45% 0.3 240);         /* dark bg */
--color-primary-content: oklch(97% 0.01 240); /* light text */
```

**Step 4: Test contrast ratios**

Verify WCAG 2.1 AA compliance (4.5:1 for normal text, 3:1 for large text) between each color and its -content pair.

## Common Mistakes

- **Wrong**: Using the same lightness for base-100, base-200, base-300. **Right**: Progressive darkening creates visual hierarchy.
- **Wrong**: Skipping -content colors and relying on auto-generation. **Right**: Auto-generated content colors may not match brand guidelines.

## See Also

- [DaisyUI v5 Color Token System](daisyui-v5-color-token-system.md)
- [Custom DaisyUI Theme Definition](custom-daisyui-theme-definition.md)
- Reference: https://oklch.com/
