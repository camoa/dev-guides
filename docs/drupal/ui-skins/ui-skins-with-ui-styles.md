---
description: Combining UI Skins (design token values) with UI Styles (per-block class selection) on the same site.
tldr: UI Skins and UI Styles are orthogonal. UI Skins controls the value of CSS variables (theme-wide), UI Styles controls which utility classes are applied to individual blocks. The pattern is: UI Skins sets `--brand-primary`, UI Styles applies `text-primary` to a block, CSS links them via `var(--brand-primary)`.
drupal_version: "11.x"
---

# UI Skins + UI Styles Together

## When to Use

> Use both modules when a site needs site-builder-tunable design tokens (UI Skins) AND curated per-block class options (UI Styles). The two modules are orthogonal and complementary.

## Decision

| Question | Answer |
|---|---|
| Does the value change per-block? | UI Styles (a class chooser) |
| Does the value need to be globally configurable? | UI Skins (a variable widget) |
| Both? | UI Skins for the value, UI Styles for the class that consumes it |

## Pattern

| Concern | Module | Lives at |
|---|---|---|
| Brand color values | UI Skins (`ui_skins_alpha_color` variable) | Theme settings; injects `:root { --brand-primary: ... }` |
| "Use brand primary as text color" choice on a block | UI Styles | Block config; injects `text-primary` class |
| Active theme variant (light/dark/brand-A) | UI Skins (theme plugin) | Theme settings; toggles class/`data-theme` on body/html |
| Section background style on a Layout Builder section | UI Styles + `ui_styles_layout_builder` | Per-section in LB; injects `bg-neutral` |

The CSS that backs them:

```css
:root { --brand-primary: #0066cc; }
body.theme-dark { --brand-primary: #3399ff; }

.text-primary { color: var(--brand-primary); }
```

A site builder:
1. Sets `--brand-primary` to the company hex via UI Skins
2. Picks "Dark" as active theme via UI Skins (which adds `body.theme-dark`)
3. Applies `text-primary` to a specific block via UI Styles

The block reads the right color in the right mode.

## Common Mistakes

- **Trying to make UI Skins per-block** → Wrong tool. Either use UI Styles, or scope per-section via Layout Builder + a custom CSS class
- **Defining brand color hex codes inside UI Styles options** → Loses the runtime adjustability. The class should reference a variable, and the variable's value is set by UI Skins

## See Also

- [UI Skins Overview](ui-skins-overview.md)
- [drupal/ui-suite-daisyui — UI Styles Integration](../ui-suite-daisyui/ui-styles-integration.md)
- Reference: `drupal/ui_styles` module
