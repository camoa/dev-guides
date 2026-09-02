---
description: Implement multi-theme support, light/dark mode, per-page themes, and custom brand themes using DaisyUI's data-theme system
tldr: "Use DaisyUI theming for multi-theme support, light/dark mode switching, brand color customization, or white-labeling. The `data-theme` attribute switches the entire palette with no JavaScript class manipulation required. All themes must be registered at build time; per-page scoping works by placing `data-theme` on any container element."
---

# Theming System

## When to Use

> Implementing multi-theme support, light/dark mode, brand color customization, or white-labeling.

## Decision: Where the Theme Lives

| Situation | Choose | Why |
|-----------|--------|-----|
| Switching theme globally | `data-theme` on `<html>` | Entire page switches at once |
| Scoping a theme to one section | `data-theme` on any container | CSS variable scope is inherited by descendants |
| CSS-only theme toggle | `.theme-controller` on checkbox/select | DaisyUI handles the `:root:has(...)` selector |
| Per-page / per-section stable identity | `data-theme` on page wrapper element | Different product lines or audience landing pages with distinct, non-user-toggled palettes |
| Persisting theme across sessions | JS + `localStorage` + `setAttribute` | DaisyUI reads the attribute; persistence is your responsibility |

## How Themes Work

DaisyUI themes are sets of CSS custom properties applied to selectors. Theme switching works via the `data-theme` attribute — no JavaScript class manipulation required.

```html
<!-- Applied to html, body, or any container -->
<html data-theme="dark">
<div data-theme="cupcake">  <!-- Scoped theme — only this subtree changes -->
```

The plugin applies themes as:

```css
:root, [data-theme=light] { --color-primary: oklch(45% 0.24 277.023); ... }
[data-theme=dark] { --color-primary: oklch(65.69% 0.196 275.75); ... }
@media (prefers-color-scheme: dark) { :root:not([data-theme]) { ... } }
```

## Built-in Themes (35 in v5)

`light` `dark` `cupcake` `bumblebee` `emerald` `corporate` `synthwave` `retro` `cyberpunk` `valentine` `halloween` `garden` `forest` `aqua` `lofi` `pastel` `fantasy` `wireframe` `black` `luxury` `dracula` `cmyk` `autumn` `business` `acid` `lemonade` `night` `coffee` `winter` `dim` `nord` `sunset` `caramellatte` `abyss` `silk`

## Creating a Custom Theme

```css
/* globals.css — define theme as CSS custom properties */
@plugin "daisyui" {
  themes: light --default, dark --prefersdark, brand;
}

@plugin "daisyui/theme" {
  name: "brand";
  default: false;
  color-scheme: light;
  --color-primary: oklch(58% 0.22 255);
  --color-primary-content: oklch(98% 0.01 255);
  --color-secondary: oklch(72% 0.18 330);
  --color-secondary-content: oklch(98% 0.01 330);
  --color-accent: oklch(78% 0.16 85);
  --color-accent-content: oklch(20% 0.05 85);
  --color-base-100: oklch(100% 0 0);
  --color-base-200: oklch(96% 0 0);
  --color-base-300: oklch(92% 0 0);
  --color-base-content: oklch(18% 0.005 250);
  --radius-box: 0.75rem;
  --radius-field: 0.375rem;
  --radius-selector: 0.375rem;
}
```

## Theme Controller (JavaScript-free Theme Switching)

```html
<!-- Checkbox approach — theme switches on check -->
<input type="checkbox" class="theme-controller" value="dark" aria-label="Dark mode" />

<!-- Select approach -->
<select class="theme-controller" onchange="document.documentElement.setAttribute('data-theme', this.value)">
  <option value="light">Light</option>
  <option value="dark">Dark</option>
</select>
```

The `.theme-controller` class is a DaisyUI utility. When a `input.theme-controller[value=dark]` is `:checked`, DaisyUI's CSS selects the dark theme via `:root:has(input.theme-controller[value=dark]:checked)`.

## Persisting Theme Choice Across Sessions

DaisyUI only reads whatever value is on the `data-theme` attribute — it has no memory of a user's choice between page loads. A `.theme-controller` checkbox resets to its default state on the next render unless the application also persists the choice:

```js
// On toggle
document.documentElement.setAttribute('data-theme', next);
localStorage.setItem('theme', next);

// On page load — read before first paint to avoid a flash of the wrong theme
const saved = localStorage.getItem('theme');
if (saved) document.documentElement.setAttribute('data-theme', saved);
```

This is a separate concern from the CSS-only toggle above: `.theme-controller` handles the instant, no-JS switch within a page; `localStorage` handles remembering that choice for the next visit. Runtime theme switching driven by user preference needs both.

## Per-Page Theme Switching for Multi-Section Marketing Sites

### When to use per-page theme switching

Marketing sites where sibling pages or top-level sections have intentionally distinct, stable visual identities — for example, a "Products" section in a darker brand variant while "About" uses the standard brand theme. This is a build-time concern: all themes must be registered at build time and mapped to routes or page wrappers by the application layer.

**Use for:**

- Product-line differentiation (each product line has a registered theme applied to its page wrapper)
- Audience-specific landing pages with distinct palettes
- Sections with stable, non-user-toggled visual identity

**Do NOT use for:**

- User-toggled light/dark mode — that pattern uses `data-theme` on `<html>` driven by `.theme-controller` (see "Theme Controller" above)
- Runtime theme switching based on user preference — use the toggle pattern documented above

### Mechanism of per-page theme scoping

`data-theme` can be placed on **any element**, not just `<html>`. DaisyUI CSS variables are scoped to that element's subtree via the CSS cascade. Every descendant inherits the theme's custom property values without touching the global theme.

```html
<!-- Global theme stays on <html> -->
<html data-theme="brand">

  <!-- Product section uses a distinct registered theme -->
  <div data-theme="brand-dark">
    <!-- All DaisyUI components here render with brand-dark palette -->
    <button class="btn btn-primary">Buy Now</button>
  </div>

  <!-- About section uses the global brand theme — no data-theme needed -->
  <div>
    <button class="btn btn-primary">Learn More</button>
  </div>

</html>
```

### Registration requirement for scoped themes

All themes used in per-page scoping must be registered in the build config — they are not dynamic. For Tailwind v4:

```css
@plugin "daisyui" {
  themes: brand --default, brand-dark, brand-enterprise;
}
```

For how to define each theme's token values, see [Custom DaisyUI Theme Definition](../tailwind-tokens/custom-daisyui-theme-definition.md).

### Variable inheritance between theme scopes

Each `data-theme` scope provides the full DaisyUI CSS variable inventory to its subtree — the same 25+ variables documented in [Color System and Design Tokens](color-system-design-tokens.md). A nested `data-theme` fully overrides the parent scope for all variables; there is no partial inheritance between theme scopes.

For the complete variable inventory each theme scope provides, see [DaisyUI CSS Variable Reference](../tailwind-tokens/daisyui-css-variable-reference.md).

### Downstream tooling note

Page-composer tools (such as a `target_theme` field in a design-intelligence plugin) map directly to this pattern: the `target_theme` value is a registered DaisyUI theme name applied as `data-theme` on the page wrapper element. The theme must exist in the build config for the variables to resolve.

## Common Mistakes

- Using hex/rgb colors in themes — DaisyUI v5 uses `oklch()` exclusively. Other color spaces break the `color-mix()` calculations DaisyUI uses internally
- Defining only primary/secondary and leaving neutral/base undefined — base colors control backgrounds, text, and borders across all components
- Missing `color-scheme: light|dark` in custom themes — this tells the browser whether scrollbars, form controls, and OS-level elements should render light or dark
- Using a theme in per-page scoping without registering it in the build config — all themes must be registered at build time; `data-theme` on a container won't resolve without it

## See Also

- [Color System and Design Tokens](color-system-design-tokens.md) — full CSS variable reference
- [Installation and Configuration](installation-configuration.md)
- Reference: [Custom DaisyUI Theme Definition](../tailwind-tokens/custom-daisyui-theme-definition.md)
- Reference: [DaisyUI CSS Variable Reference](../tailwind-tokens/daisyui-css-variable-reference.md)
- Reference: `design-system-tailwind.md` Section 9 — dark mode in Tailwind
