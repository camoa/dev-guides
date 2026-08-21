---
description: "Every slotted component -- not just the grids -- registers as a Layout Builder layout; UI Styles applies section and block styling on top"
tldr: "All 51 components register as Layout Builder layouts once ui_patterns_layouts is enabled -- icon_map only draws the picker thumbnail on the grids, it does not gate registration. Pick by slot shape (card's header/body/footer suit LB regions; button's single label slot does not)."
---

# Layout Builder Integration

## How It Works

**Every** component the theme exposes registers as a Layout Builder layout -- not just the grids. `ui_patterns_layouts`' `ComponentLayout::getDerivativeDefinitions()` iterates all negotiated component definitions and mints a layout for each one; `buildLayoutDefinition()` turns each `slots:` entry into a region. So `card`, `hero`, `navbar` and the rest all appear in "Choose a layout" alongside the grids, and a component with no slots produces a layout with no regions.

What the grids have that the others do not is `icon_map:`, which is applied only inside `if (isset($definition['icon_map']))`. That draws the little region diagram in the layout picker -- it is a **thumbnail, not a gate**. Note that `grid_cols` has no `icon_map` either, so it registers like every other component but shows no diagram.

For any of this to happen, `ui_patterns_layouts` must be enabled. It is a separate submodule of UI Patterns and is not a dependency of the theme.

1. Components appear in the "Choose a layout" dialog when adding sections
2. Component props become layout configuration options (container type, columns, gaps, background on the grids)
3. Component slots become layout regions where blocks can be placed

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

The dropdown offers exactly the 10 plugins defined in `ui_suite_daisyui.ui_styles.yml`: background color, text color, font size, box shadow, width, padding top, padding bottom, margin bottom, glass and mask. There are no layout, flexbox/grid, height or horizontal-spacing styles -- add them in your sub-theme's own `*.ui_styles.yml` if you need them.

## Common Mistakes

- **Assuming only the grids are available as layouts** -- All 51 register. The practical filter is whether a component's slots make sense as Layout Builder regions: `card`'s `header`/`body`/`footer` do, `button`'s single label slot does not. Pick by slot shape, not by an imagined `icon_map` requirement.
- **Reaching for a grid layout before enabling `ui_patterns_layouts`** -- The dialog is empty of DaisyUI layouts until that submodule is on. WHY: the layouts are plugin derivatives it provides; the theme itself registers none.
- **Setting background images without `bg-cover`** -- Using `background_image` without `background_size: bg-cover` often produces tiled or cropped backgrounds. WHY: The default `background-size` is `auto`, which shows the image at its natural size.

## See Also

- `drupal-ui-patterns.md` -- Pattern-to-Layout-Builder integration details
