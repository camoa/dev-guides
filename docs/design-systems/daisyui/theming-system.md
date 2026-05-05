---
description: Implement multi-theme support, light/dark mode, per-page themes, and custom brand themes using DaisyUI's data-theme system
tldr: "Use DaisyUI theming for multi-theme support, light/dark mode switching, brand color customization, or white-labeling. The `data-theme` attribute switches the entire palette with no JavaScript class manipulation required. All themes must be registered at build time; per-page scoping works by placing `data-theme` on any container element."
---

# Theming System

## When to Use

> Use DaisyUI theming for multi-theme support, light/dark mode switching, brand color customization, or white-labeling. The `data-theme` attribute switches the entire palette with no JavaScript class manipulation required.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Switching theme globally | `data-theme` on `<html>` | Entire page switches at once |
| Scoping a theme to one section | `data-theme` on any container | CSS variable scope is inherited by descendants |
| CSS-only theme toggle | `.theme-controller` on checkbox/select | DaisyUI handles the `:root:has(...)` selector |
| Per-page / per-section stable identity | `data-theme` on page wrapper element | Different product lines or audience landing pages with distinct, non-user-toggled palettes |
| Persisting theme across sessions | JS + `localStorage` + `setAttribute` | DaisyUI reads the attribute; persistence is your responsibility |

## Pattern

**Applying a theme:**

```html
<html data-theme="dark">
<div data-theme="cupcake">  <!-- Scoped to subtree only -->
```

**Creating a custom theme:**

```css
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
  --color-base-100: oklch(100% 0 0);
  --color-base-200: oklch(96% 0 0);
  --color-base-300: oklch(92% 0 0);
  --color-base-content: oklch(18% 0.005 250);
  --radius-box: 0.75rem;
}
```

**CSS-only theme controller:**

```html
<!-- Checkbox toggles dark theme on check -->
<input type="checkbox" class="theme-controller" value="dark" aria-label="Dark mode" />
```

DaisyUI uses `:root:has(input.theme-controller[value=dark]:checked)` to apply the theme.

**Per-page theme scoping:**

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

All themes used for per-page scoping must be registered in the build config:

```css
@plugin "daisyui" {
  themes: brand --default, brand-dark, brand-enterprise;
}
```

For per-page theme token definitions, see `design-systems/tailwind-tokens/custom-daisyui-theme-definition.md`.

## When to Use Per-Page Theme Scoping

Use for:
- Product-line differentiation (each product line has a registered theme applied to its page wrapper)
- Audience-specific landing pages with distinct palettes
- Sections with stable, non-user-toggled visual identity

Do NOT use for:
- User-toggled light/dark mode — use the `.theme-controller` toggle pattern above
- Runtime theme switching based on user preference — use JS + `localStorage`

A nested `data-theme` fully overrides the parent scope for all variables; there is no partial inheritance between theme scopes.

## Built-in Themes (35 in v5)

`light` `dark` `cupcake` `bumblebee` `emerald` `corporate` `synthwave` `retro` `cyberpunk` `valentine` `halloween` `garden` `forest` `aqua` `lofi` `pastel` `fantasy` `wireframe` `black` `luxury` `dracula` `cmyk` `autumn` `business` `acid` `lemonade` `night` `coffee` `winter` `dim` `nord` `sunset` `caramellatte` `abyss` `silk`

## Common Mistakes

- **Wrong**: Using hex/rgb colors in custom themes — **Right**: DaisyUI v5 uses `oklch()` exclusively; other color spaces break internal `color-mix()` calculations
- **Wrong**: Defining only primary/secondary and leaving base undefined — **Right**: Base colors (`base-100`, `base-content`) control backgrounds, text, and borders across all components
- **Wrong**: Missing `color-scheme: light|dark` in custom themes — **Right**: This tells the browser whether scrollbars and OS-level elements should render light or dark
- **Wrong**: Using a theme in per-page scoping without registering it in the build config — **Right**: All themes must be registered at build time; `data-theme` on a container won't resolve without it

## See Also

- [Color System and Design Tokens](color-system-design-tokens.md)
- [Installation and Configuration](installation-configuration.md)
- Reference: `design-systems/tailwind-tokens/custom-daisyui-theme-definition.md`
- Reference: `design-systems/tailwind-tokens/daisyui-css-variable-reference.md`
- Reference: `design-system-tailwind.md` Section 9 — dark mode in Tailwind
