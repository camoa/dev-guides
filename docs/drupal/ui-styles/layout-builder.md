---
description: Apply UI Styles per-block and per-section inside Layout Builder — the primary UI Styles use case for editorial sites.
tldr: Enable ui_styles_layout_builder; block placement forms and section configuration forms both gain UI Styles fieldsets. Apply background/rhythm/width classes at the section level, component-specific classes (text color, alignment) at the block level.
drupal_version: "11.x"
---

# Integration: Layout Builder

## When to Use

> Use this guide when applying styles per-section and per-block inside Layout Builder — the most common UI Styles use case for editorial sites.

## Decision: Section Styles vs Block Styles

| Apply at... | When |
|---|---|
| Section level | Styling spans a region/row — backgrounds, vertical rhythm, container width |
| Block level | Styling targets a specific component — text color, card variant, alignment of a single block |

## Pattern

Enable `ui_styles_layout_builder`. The submodule alters:

- **`layout_builder_block_form`** — block placement/configuration forms gain UI Styles fieldsets per block
- **`layout_builder_configure_section`** — section configuration form gains UI Styles fieldsets for the section wrapper

Section storage lives in the entity view display (or LB override field):

```yaml
# Excerpt from a Layout Builder section
layout_settings:
  ui_styles:
    selected:
      bg_color: "bg-neutral"
      spacing: "py-12"
    extra: ""
```

## Common Mistakes

- **Configuring identical styles on every block in a section** → Move them to the section level once
- **Using LB Styles (`layout_builder_styles`) and UI Styles together** → Both work, but the editor UX gets cluttered. Pick one; UI Styles is the modern path

## See Also

- [Integration: Block Layout](block-layout.md)
- [Integration: UI Patterns & SDC](ui-patterns-sdc.md)
- Reference: `modules/ui_styles_layout_builder/` in the UI Styles module
