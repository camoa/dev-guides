---
description: Switch between 35 DaisyUI themes and customize 28 CSS design tokens via the admin UI
---

# UI Skins Integration

## What UI Skins Provides

UI Skins allows themes to expose CSS variables and theme switching (data-attribute themes) as configurable settings in the Drupal admin UI. UI Suite DaisyUI uses two UI Skins plugin types:

1. **CSS Variables** (`ui_suite_daisyui.ui_skins.css_variables.yml`) -- 28 DaisyUI design tokens
2. **Themes** (`ui_suite_daisyui.ui_skins.themes.yml`) -- 35 DaisyUI color themes

## CSS Variables (28 Tokens)

Configurable at `/admin/appearance/css-variables`:

| Category | Variable | Description |
|---|---|---|
| **Colors** | `color-primary` | Primary brand color |
| | `color-primary-content` | Foreground on primary |
| | `color-secondary` | Secondary brand color |
| | `color-secondary-content` | Foreground on secondary |
| | `color-accent` | Accent brand color |
| | `color-accent-content` | Foreground on accent |
| | `color-neutral` | Neutral dark color |
| | `color-neutral-content` | Foreground on neutral |
| | `color-base-100` | Base page background |
| | `color-base-200` | Base darker shade |
| | `color-base-300` | Base darkest shade |
| | `color-base-content` | Foreground on base |
| | `color-info` | Info color |
| | `color-info-content` | Foreground on info |
| | `color-success` | Success color |
| | `color-success-content` | Foreground on success |
| | `color-warning` | Warning color |
| | `color-warning-content` | Foreground on warning |
| | `color-error` | Error color |
| | `color-error-content` | Foreground on error |
| **Border Radius** | `radius-selector` | Checkbox, toggle, badge radius |
| | `radius-field` | Input, select, tab radius |
| | `radius-box` | Card, modal, alert radius |
| **Sizes** | `size-selector` | Base scale for selectors |
| | `size-field` | Base scale for fields |
| **Borders** | `border` | Border width for all components |
| **Effects** | `depth` | Binary depth effect |
| | `noise` | Binary background noise effect |

All variables target `:root` and accept textfield input. Values override the active DaisyUI theme's defaults.

## Theme Switching (35 Themes)

Configurable at `/admin/appearance/settings/ui_suite_daisyui`:

Each theme sets the `data-theme` attribute on the `<html>` element.

**Light themes**: light, cupcake, bumblebee, emerald, corporate, garden, lofi, pastel, fantasy, wireframe, cmyk, autumn, acid, lemonade, winter, caramellatte, silk

**Dark themes**: dark, synthwave, retro, cyberpunk, valentine, halloween, forest, aqua, luxury, dracula, night, coffee, business, dim, nord, sunset, abyss, black

## How Themes Work

1. The theme YAML defines each theme with `key: "data-theme"` and `target: html`
2. UI Skins adds the selected theme name as `data-theme="themename"` on `<html>`
3. DaisyUI's theme definitions (compiled into `dist/css/app.css`) provide CSS variable overrides scoped to each `[data-theme]` selector
4. All components automatically re-color because they use DaisyUI semantic color classes

## Common Mistakes

- **Setting CSS variables without understanding precedence** -- CSS variable overrides via UI Skins apply to `:root`, but DaisyUI themes use `[data-theme]` selectors with higher specificity. WHY: A `[data-theme="dark"]` rule will override your `:root` variable. Use CSS variables for fine-tuning within a chosen theme, or create a custom theme.
- **Disabling the `daisyui` library without replacement** -- Without the compiled CSS, the `data-theme` attribute has no effect. A sub-theme that overrides the library must provide its own compiled CSS containing DaisyUI theme definitions. WHY: DaisyUI themes are pure CSS compiled into `dist/css/app.css`; removing it removes all 35 theme definitions.

## See Also

- `design-system-daisyui.md` -- DaisyUI theme customization
- [DaisyUI Themes](https://daisyui.com/docs/themes/) -- Official theme documentation
