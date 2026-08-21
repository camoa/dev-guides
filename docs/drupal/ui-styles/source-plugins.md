---
description: "How UI Styles auto-selects the form widget (Checkbox, Toolbar, Select) for each style definition."
tldr: "UI Styles picks the widget automatically — 1 option becomes a Checkbox, all options with icons become a Toolbar, everything else falls back to a Select dropdown. To force Toolbar, every option must have an icon field; to force Checkbox, declare exactly one option."
drupal_version: "11.x"
---

# Source Plugins (Form Widget Selection)

## When to Use

> Use this guide when you need to understand which form widget your style will render as, or how to control the widget choice.

## Decision

UI Styles auto-selects a source plugin per style, in this priority order:

| Source plugin | Selected when | Rendered as |
|---|---|---|
| `Checkbox` | Style has exactly **1 option** | On/off toggle |
| `Toolbar` | **Every option** has an `icon` field | Icon-button toolbar |
| `Select` | Fallback (always applicable) | Dropdown with optional preview thumbnail |

## Pattern

Force a **toolbar** — give every option an `icon`:

```yaml
text_alignment:
  label: "Alignment"
  category: "Typography"
  options:
    text-start:   { label: "Start",   icon: "mdi-format-align-left" }
    text-center:  { label: "Center",  icon: "mdi-format-align-center" }
    text-end:     { label: "End",     icon: "mdi-format-align-right" }
```

Force a **checkbox** — declare a single option:

```yaml
shadow:
  label: "Drop shadow"
  options:
    shadow-md: "Shadow"
```

Use a **select with rich preview** — 2+ options without all having icons, and set `previewed_as: aside`.

## Common Mistakes

- **Missing icons on some options of an otherwise-toolbar style** → Falls back to select. Either icon them all or explicitly avoid icons
- **Wanting a multi-select widget** → Not supported. Decompose into multiple single-choice styles

## See Also

- [Style Definition Format](definition-format.md)
- Reference: `src/Plugin/UiStyles/Source/` in the UI Styles module
