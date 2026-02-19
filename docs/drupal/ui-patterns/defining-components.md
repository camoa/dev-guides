---
description: Defining Components — YAML structure, props JSON Schema, slots, variants, noUi
drupal_version: "11.x"
---

# Defining Components

## When to Use

> Reference this guide when writing or editing a `{name}.component.yml` file for use with UI Patterns.

## Decision

| Property | Type | Purpose |
|----------|------|---------|
| `name` | string | Human-readable label (mandatory) |
| `group` | string | Category for grouping in UI forms |
| `noUi` | boolean | Hides component from site-builder UIs |
| `replaces` | string | SDC component ID this replaces |
| `variants` | object | Named visual variants (become `variant` prop) |
| `props` | object | JSON Schema object defining typed properties |
| `slots` | object | Named placeholders for render arrays |
| `status` | string | `experimental` \| `stable` \| `deprecated` \| `obsolete` |

## Pattern

```yaml
name: "Card"
group: "Content"
status: "stable"
noUi: false

variants:
  default:
    title: "Default"
  highlighted:
    title: "Highlighted"

props:
  type: object
  required:
    - title
  properties:
    title:
      title: "Card title"
      type: "string"
    image_url:
      title: "Image URL"
      "$ref": "ui-patterns://url"
    badge:
      title: "Badge"
      "$ref": "ui-patterns://enum"
      enum: ["new", "sale", "featured"]
      "meta:enum":
        new: "New"
        sale: "On Sale"
        featured: "Featured"
    card_attributes:
      title: "Card Attributes"
      "$ref": "ui-patterns://attributes"

slots:
  content:
    title: "Card body"
  footer:
    title: "Card footer"
```

The `default` value pre-fills form widgets via `#default_value` only. Use Twig's `|default()` filter for render-time defaults.

## Common Mistakes

- **Wrong**: Relying on `default` in YAML for render-time fallbacks → **Right**: Use `{{ title|default('Untitled') }}` in Twig
- **Wrong**: Defining props without `title` → **Right**: Always set `title`; UI Patterns uses it for form labels
- **Wrong**: Using `type: 'Drupal\Core\Template\Attribute'` → **Right**: Use `"$ref": "ui-patterns://attributes"`
- **Wrong**: Putting renderables (blocks, markup) in props → **Right**: Renderables belong in slots

## See Also

- [Props System](props-system.md)
- [Slots System](slots-system.md)
- [Variants](variants.md)
- Reference: [Authoring a Component](https://project.pages.drupalcode.org/ui_patterns/2-authors/0-authoring-a-component/)
