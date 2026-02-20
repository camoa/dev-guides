---
description: UI Suite DaisyUI starterkit token organization and customization
---

# UI Suite DaisyUI Starterkit Patterns

## When to Use

> Use this when building a Drupal theme with UI Suite DaisyUI and need to understand how the starterkit organizes tokens and configuration.

## Decision

**Starterkit File Structure**

```
starterkits/ui_suite_daisyui_starterkit/css/
  tailwind.config.pcss            # @theme block -- core tokens (fonts, grid)
  base/base.pcss                  # @layer base -- HTML element defaults
  plugins/
    daisyui.config.pcss           # @plugin "daisyui" -- theme selection
    tailwindcss.typography.config.pcss  # @plugin "@tailwindcss/typography"
  utilities/
    typography.pcss               # Type scale tokens + @utility aliases
    containers.pcss               # Container width utilities
    grid.pcss                     # Grid layout utilities
    gap.pcss / margin.pcss / padding.pcss  # Responsive spacing utilities
```

## Pattern

**Customizing the Starterkit**

To brand a starterkit, modify these files:

```css
/* tailwind.config.pcss -- set font families */
@theme {
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
}
```

```css
/* daisyui.config.pcss -- limit to custom themes */
@plugin "daisyui" {
  exclude: reset;
  themes: mybrand --default, mybrand-dark;
  logs: false;
}
```

```css
/* plugins/mybrand-theme.pcss -- custom theme definition */
@plugin "daisyui/theme" {
  name: "mybrand";
  default: true;
  color-scheme: light;
  --color-primary: oklch(55% 0.3 240);
  /* ... see Custom DaisyUI Theme Definition guide for full definition */
}
```

**Build Pipeline**

Vite + PostCSS. Source .pcss files are processed by Tailwind v4 / Lightning CSS.

- Production: npm run build
- Watch mode: npm run dev

## Common Mistakes

- **Wrong**: Modifying node_modules files directly. **Right**: Override tokens in the subtheme's CSS files.
- **Wrong**: Defining duplicate tokens in multiple files. **Right**: Consolidate token definitions in tailwind.config.pcss or theme files.

## See Also

- [Custom DaisyUI Theme Definition](custom-daisyui-theme-definition.md)
- [Typography Token Mapping](typography-token-mapping.md)
- [Spacing & Layout Token System](spacing-layout-token-system.md)
- Reference: ~/workspace/contrib/web/themes/contrib/ui_suite_daisyui/starterkits/ui_suite_daisyui_starterkit/
