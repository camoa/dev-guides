---
description: Use grid components as Layout Builder layouts with UI Styles for section and block styling
---

# Layout Builder Integration

## How It Works

UI Suite DaisyUI's grid components (`grid_1_region` through `grid_4_regions`, `grid_cols`) automatically register as Layout Builder layouts through UI Patterns. This means:

1. Grid components appear in the "Choose a layout" dialog when adding sections
2. Grid component props become layout configuration options (container type, columns, gaps, background)
3. Grid component slots become layout regions where blocks can be placed

## Using Grid Layouts in Layout Builder

When adding a Layout Builder section:

1. Select a grid layout (e.g., "Grid 2 regions")
2. Configure the layout:
   - **Container type**: Container (centered), Breakout (full-width), or Bg breakout (background full-width)
   - **Grid columns**: Responsive column counts per breakpoint
   - **Column spans**: How each region spans within the grid per breakpoint
   - **Gap**: Spacing between columns per breakpoint
   - **Background**: Image URL, size, position, repeat
3. Place blocks into the grid's column slots

## Applying Styles in Layout Builder

With `ui_styles_layout_builder` enabled, the Style dropdown appears on:

- **Section level**: Apply styles to the entire grid section
- **Block level**: Apply styles to individual blocks within the section

Available style categories include all 30+ defined in `ui_suite_daisyui.ui_styles.yml`: colors, typography, spacing, sizing, effects, layout, flexbox/grid, and DaisyUI effects.

## Common Mistakes

- **Expecting all DaisyUI components in Layout Builder** -- Only grid components register as layouts. Other components (card, button, hero) are available as field formatters and views plugins but not directly as LB sections. Use blocks or custom block types to render them. WHY: Layout Builder sections require components with `icon_map` slots that define a visual region layout.
- **Setting background images without `bg-cover`** -- Using `background_image` without `background_size: bg-cover` often produces tiled or cropped backgrounds. WHY: The default `background-size` is `auto`, which shows the image at its natural size.

## See Also

- `drupal-ui-patterns.md` -- Pattern-to-Layout-Builder integration details
