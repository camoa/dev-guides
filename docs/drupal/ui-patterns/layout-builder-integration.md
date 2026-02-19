---
description: Layout Builder Integration — components as layout sections, region-to-slot mapping
drupal_version: "11.x"
---

# Layout Builder Integration

**Sub-module:** `ui_patterns_layouts`
**Dependencies:** `layout_discovery`, `ui_patterns`

## When to Use

> Use `ui_patterns_layouts` when you want site-builders to select SDC components as Layout Builder sections, with props configurable in the section form and slots filled by placed blocks.

## Decision

| Need | Approach |
|------|---------|
| Component slots as layout regions | Enable `ui_patterns_layouts`; each slot becomes a region |
| Configure component props per section | Done in the Layout Builder section configuration form |
| Fill component slots with content | Place blocks into the layout regions (not in the form) |
| Entity field sources in section props | Automatic via `ChainContextEntityResolver` |

## Pattern

### How component slots map to layout regions

```
Component: my_theme:two-column
  Slots: main, sidebar

Layout Plugin: ui_patterns:my_theme:two-column
  Regions: main, sidebar
```

### Workflow

```
1. Enable ui_patterns_layouts
2. Components with slots appear in Layout Builder's "Add section" dialog
3. Choosing a component layout shows props configuration
4. Place blocks into the component's slot regions
5. Props can pull from entity fields, manual input, or other sources
```

### What gets configured where

- **Props**: configured in the section configuration form (variant selector, field mappings, manual input)
- **Slots**: filled by placing blocks into the corresponding regions — not via the form

## Common Mistakes

- **Wrong**: Expecting components without slots to appear as layouts → **Right**: Layout plugins require at least one region; props-only components are not exposed as layouts
- **Wrong**: Configuring slot content in the layout form → **Right**: Slots in layouts are filled by blocks in regions
- **Wrong**: Using `ckeditor_layouts` with UI Patterns layouts → **Right**: Incompatible; `ckeditor_layouts` loads layouts through the theme manager, SDC does not

## See Also

- [Blocks Integration](blocks-integration.md)
- Reference: `modules/contrib/ui_patterns/modules/ui_patterns_layouts/`
