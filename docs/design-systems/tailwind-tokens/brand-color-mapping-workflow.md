---
description: Map brand guidelines to DaisyUI semantic color system with WCAG contrast validation
tldr: "Use when mapping brand guidelines (hex/Pantone) to DaisyUI semantic color roles. Identify primary/secondary/accent from the palette, convert to oklch, then validate every *-content token at 4.5:1 (body text) or 3:1 (large text/UI) — adjust the content token L-channel only, never the brand background."
---

# Brand Color Mapping Workflow

## When to Use

> Use this when you receive brand guidelines (hex colors, Pantone, etc.) and need to map them to DaisyUI's semantic color system.

## Decision

**Identifying primary, secondary, and accent from a brand palette:**

| Role | What to look for in the brand palette |
|---|---|
| **Primary** | The dominant brand color — the one that appears on main CTAs, the logo's primary tone, the color most associated with the brand identity |
| **Secondary** | Supporting brand color — used on secondary buttons, badges, alternate emphasis areas. Visually distinct from primary but not competing for attention |
| **Accent** | Highlight or differentiator — used sparingly for emphasis, callouts, or to draw the eye to specific UI affordances. Often a brighter or more saturated color |

If a brand palette has only two colors, leave `--color-accent` defaulting to the same family as `--color-primary` (slightly shifted hue) rather than introducing a third unrelated color.

| Brand Asset | DaisyUI Role | Rationale |
|---|---|---|
| Primary brand color | `--color-primary` | CTAs, main actions |
| Secondary brand color | `--color-secondary` | Supporting actions |
| Accent / highlight | `--color-accent` | Emphasis, decorative |
| Darkest neutral | `--color-neutral` | Footer, navbar |
| Lightest background | `--color-base-100` | Page background |
| Card/section bg | `--color-base-200` | Elevated surfaces |
| Border/divider gray | `--color-base-300` | Subtle separators |
| Default text color | `--color-base-content` | Body copy |

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

**Step 4: Map to DaisyUI roles** — see Decision table above.

### WCAG Contrast Validation

Every `*-content` token must meet WCAG contrast thresholds against its paired background. Validate on theme generation and again on every brand-color edit.

**Standard thresholds:**

| Pairing | Minimum contrast | Applies to |
|---|---|---|
| Body text (`*-content` on `*` background) | **4.5:1** | Paragraph text, form labels, default UI labels |
| Large text (≥18pt or ≥14pt bold) and UI components | **3:1** | Headings, button text at large sizes, focus indicators, icon buttons |

**Auto-adjust pattern:**

When a `*-content` token fails its threshold, adjust the L-channel of the content token — NOT the background. Backgrounds are brand-fidelity-critical; content tokens are derived for legibility.

```css
/* Wrong: adjusting brand background to fix contrast */
--color-primary: oklch(70% 0.15 230);  /* Brand says this is primary; do not move */

/* Right: adjusting content token in L-channel */
--color-primary: oklch(70% 0.15 230);  /* Brand-fidelity, untouched */
--color-primary-content: oklch(15% 0.05 230);  /* Was 30%, lowered until contrast ≥4.5:1 */
```

**Color-blindness flag:**

When two distinct semantic roles (e.g., `--color-error` and `--color-success`) are indistinguishable under deuteranopia simulation, flag as a **manual designer review** item — do NOT auto-resolve. Tools: Stark, Chrome DevTools "Rendering → Emulate vision deficiencies", Sim Daltonism.

## Common Mistakes

- **Wrong**: Using the same lightness for `base-100`, `base-200`, `base-300`. **Right**: Progressive darkening creates visual hierarchy.
- **Wrong**: Skipping `-content` colors and relying on auto-generation. **Right**: Explicit content colors ensure brand-compliance and legibility.
- **Wrong**: Re-checking contrast only for the light theme. **Right**: Every theme variant (light, dark, brand-dark) must independently pass WCAG — a value that passes against a light background may fail against its dark variant.
- **Wrong**: Assigning primary to a decoration-only color. **Right**: `--color-primary` must support text-on-color usage — only use colors that have been validated in the brand's existing materials.

## See Also

- [DaisyUI v5 Color Token System](daisyui-v5-color-token-system.md)
- [DaisyUI CSS Variable Reference](daisyui-css-variable-reference.md) — full 28-variable inventory
- [Custom DaisyUI Theme Definition](custom-daisyui-theme-definition.md) — where validated colors land in the theme block
- Reference: https://oklch.com/
