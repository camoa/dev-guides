### 11.5 UI Patterns Layouts & UI Styles Integration

#### When to Use

When you want SDC components to serve as Layout Builder section layouts without writing custom `*.layouts.yml` or `LayoutDefault` plugins. Also covers UI Styles module as an alternative to Layout Builder Styles for CSS class management.

#### Decision

| If you need... | Use... | Why |
|---|---|---|
| SDC components as LB section layouts | `ui_patterns_layouts` sub-module | Auto-registers components with slots as layout plugins, zero YAML/PHP |
| CSS class selection on LB sections/blocks | UI Styles module (`ui_styles`) | Theme-defined style options via `theme.ui_styles.yml`, no contrib config entities |
| Custom layout with complex regions | Custom `*.layouts.yml` (Section 12) | Full control over template, icon_map, library |
| Reusable style config entities | Layout Builder Styles (Section 11) | Config entity system, per-style restrictions, template suggestions |

#### Pattern: UI Patterns as Layout Plugins

When `ui_patterns_layouts` is enabled, SDC components with slots become available as Layout Builder section layouts:

- Layout plugin ID pattern: `ui_patterns:namespace:component_name`
- Component **slots** become layout **regions** (where blocks are placed)
- Component **props** become layout **settings** (configured in section settings form)
- Config stored in `core.entity_view_display.*.yml` under `layout_builder.sections[].layout_id`

```yaml
# Example: SDC component used as LB layout
sections:
  - layout_id: 'ui_patterns:my_theme:two_column'
    layout_settings:
      label: 'Two Column Hero'
      gap: 'large'          # prop from component.yml
    components:
      - uuid: abc-123
        region: sidebar      # slot name from component.yml
        configuration:
          id: 'field_block:node:article:field_image'
      - uuid: def-456
        region: content      # slot name from component.yml
        configuration:
          id: 'field_block:node:article:body'
```

This replaces the need for custom `LayoutDefault` plugins for most use cases.

#### Pattern: UI Styles Module

UI Styles provides theme-defined CSS class options for LB sections and blocks. Config is defined in `THEME_NAME.ui_styles.yml`:

```yaml
# mytheme.ui_styles.yml
typography:
  label: 'Typography'
  options:
    text_left:
      label: 'Text Left'
      class: 'text-start'
    text_center:
      label: 'Text Center'
      class: 'text-center'
spacing:
  label: 'Spacing'
  options:
    padding_small:
      label: 'Small Padding'
      class: 'p-2'
    padding_large:
      label: 'Large Padding'
      class: 'p-5'
colors:
  label: 'Colors'
  options:
    bg_light:
      label: 'Light Background'
      class: 'bg-light'
    bg_dark:
      label: 'Dark Background'
      class: 'bg-dark text-white'
```

Categories with labeled options appear in the LB UI for editors to select.

#### Common Mistakes
- **Using UI Patterns layouts AND custom layouts.yml for the same component** → Choose one approach. UI Patterns auto-registers from `component.yml`; duplicate registration causes conflicts
- **Expecting UI Patterns layouts without slots** → Components need at least one slot to serve as a layout (slots become regions). Props-only components register as blocks, not layouts
- **Confusing UI Styles with LB Styles** → UI Styles is theme-YAML-driven (`theme.ui_styles.yml`). LB Styles uses config entities. Both add CSS classes but with different management approaches

#### See Also
- Section 11: Layout Builder Styles Overview (config entity approach)
- Section 12: Custom Layout Plugins (manual layout registration)
- `drupal-ui-patterns.md` — full UI Patterns documentation
- `drupal-ui-suite-daisyui.md` — DaisyUI component library integration
