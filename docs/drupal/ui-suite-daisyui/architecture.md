---
description: How UI Patterns, UI Styles, UI Skins, and UI Icons integrate with DaisyUI components in the theme
---

# Architecture

## How the Pieces Fit Together

```
DaisyUI 5 (CSS classes)
    |
    v
UI Suite DaisyUI theme (51 SDC components)
    |
    +-- ui_patterns (2.x): Component discovery + rendering engine
    |     +-- Props: typed component inputs (JSON Schema)
    |     +-- Slots: named content regions
    |     +-- Variants: component style variations
    |     +-- Sources: map Drupal data to component props/slots
    |
    +-- ui_styles: Utility class styles (30+ categories)
    |     +-- ui_styles_block: Apply styles to blocks
    |     +-- ui_styles_layout_builder: Apply styles to LB sections
    |     +-- ui_styles_ui_patterns: Styles on pattern instances
    |
    +-- ui_skins: Design tokens & theme switching
    |     +-- CSS Variables: 25 DaisyUI variables (colors, radius, etc.)
    |     +-- Themes: 35 DaisyUI themes via data-theme attribute
    |
    +-- ui_icons: Icon packs (Heroicons 16/20/24 solid + 24 outline)
```

## Component Discovery Flow

1. Each component lives in `components/{name}/{name}.component.yml`
2. UI Patterns reads `.component.yml` and registers the component as an SDC
3. Props (typed inputs) and slots (content regions) are defined in YAML using JSON Schema
4. Variants map to DaisyUI modifier classes (e.g., `btn-primary`, `alert-error`)
5. The Twig template (`{name}.twig`) applies DaisyUI classes based on prop values
6. Components become available in Layout Builder, field formatters, views row plugins, and Twig `include()`

## Theme Regions

The theme defines six regions:

| Region | Machine Name | Usage |
|---|---|---|
| Navbar start | `navbar_start` | Site branding (left side of navbar) |
| Navbar center | `navbar_center` | Main menu (center of navbar) |
| Navbar end | `navbar_end` | Account menu (right side of navbar) |
| Content | `content` | Main page content, breadcrumbs, tabs, messages |
| Sidebar | `sidebar` | Optional sidebar (triggers 2-column grid layout) |
| Footer | `footer` | Page footer |

## Page Layout Logic

The `page.html.twig` template uses the theme's own grid components:

- **With sidebar**: Uses `grid_2_regions` (sidebar 3 cols / content 9 cols at `lg:`)
- **Without sidebar**: Uses `grid_1_region` (single column)
- **Footer**: Uses `grid_1_region` with `breakout` container type (full-width)
- **Navbar**: Uses the `navbar` component directly

## Common Mistakes

- **Confusing DaisyUI components with Drupal components** -- DaisyUI components are CSS classes; UI Suite DaisyUI wraps them as Drupal SDCs. The Drupal component adds props, slots, and Drupal integration that raw DaisyUI lacks. WHY: Understanding this distinction prevents mixing approaches and breaking the rendering pipeline.
- **Skipping `with_context: false` on includes** -- The theme templates consistently use `with_context: false` to prevent Drupal variables from leaking into component scope. WHY: Context leakage can cause unexpected variable collisions and rendering issues.

## See Also

- `drupal-ui-patterns.md` -- Full component system documentation
