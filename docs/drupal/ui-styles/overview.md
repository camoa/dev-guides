---
description: When to use UI Styles module vs alternatives — curated CSS class choices for site builders in Drupal's editor UIs.
tldr: Use UI Styles when site builders need curated, named CSS class options in block/LB/Views UIs without freeform input. It injects classes at render time from YAML-defined plugins; it is not a CSS generator and does not replace UI Skins or UI Patterns.
drupal_version: "11.x"
---

# UI Styles Overview

## When to Use

> Use UI Styles when your design system provides utility classes and you want site builders — not developers — to apply them to specific elements via Drupal's admin UI. Use an alternative when you need freeform class input, CSS variable control (UI Skins), or component structure (UI Patterns).

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Curated, named class choices in editor UIs | UI Styles | YAML-defined options, grouped by category, rendered as checkbox/toolbar/select |
| Per-block freeform CSS classes | Core Block layout's class field or LB Styles | UI Styles is for curated options, not arbitrary input |
| Per-section layout class control | UI Styles + `ui_styles_layout_builder` | Explicit form on every block/section in LB |
| Theme-wide CSS variable values (brand colors, fonts) | UI Skins | UI Styles applies classes; UI Skins sets design-token values |
| Enforce component structure (markup + props) | UI Patterns / SDC | UI Styles complements, doesn't replace, component systems |
| Replace Layout Builder Styles entirely | UI Styles + `ui_styles_layout_builder` | Modern successor; richer form widgets and broader integration |

## Pattern

A style is a YAML plugin: an ID, label, category, and `options` list (CSS class → label). Sub-modules expose `ui_styles_styles` form elements wherever site builders configure render output.

```yaml
# my_theme.ui_styles.yml
text_color:
  label: "Text color"
  category: "Typography"
  options:
    text-primary: "Primary"
    text-secondary: "Secondary"
    text-muted: "Muted"
```

When a site builder selects "Primary", UI Styles injects `text-primary` into the block's `#attributes['class']` at render time. The class must exist in CSS the theme already loads — UI Styles generates class application UIs, not CSS.

## Common Mistakes

- **Confusing UI Styles with UI Skins** → Styles apply CSS classes per-element; Skins set CSS variable values theme-wide
- **Expecting style options to behave like multi-select** → Each style is single-choice. Define separate styles for orthogonal axes (text-color vs background-color)
- **Declaring options whose classes aren't in any loaded CSS** → The class injects but produces no visual effect. Confirm the class is in a library-attached CSS file

## UI Suite Family

UI Styles is part of the **UI Suite** family of complementary modules:

| Module | Purpose |
|---|---|
| [UI Patterns](../ui-patterns/index.md) | Component definitions (props, slots, variants) backed by SDC |
| **UI Styles** | Curated CSS-class options applied per element (this topic) |
| [UI Skins](../ui-skins/index.md) | CSS variable values + theme variants set via theme settings |
| [UI Icons](../ui-icons/index.md) | Icon-pack registry shared across fields, CKEditor, components |
| [UI Suite DaisyUI](../ui-suite-daisyui/index.md) | DaisyUI starter using the suite |

Use UI Styles for classes, UI Skins for token values, UI Patterns for component structure, UI Icons for iconography. They overlap deliberately at integration points (e.g., styles + patterns via `ui_styles_ui_patterns`).

## See Also

- [Installation](installation.md)
- [Style Definition Format](definition-format.md)
- Reference: `drupal/ui_styles` on drupal.org
