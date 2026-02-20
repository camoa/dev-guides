---
description: Component definition structure — YAML keys, JSON Schema props, and required fields
drupal_version: "10.3+ / 11"
---

## Defining Components

### Component Definition Structure

UI Patterns components are standard SDC components. The component YAML file (`{name}.component.yml`) is the single source of truth:

```yaml
name: "Card"
group: "Content"           # Optional: UI grouping category
status: "stable"           # experimental | stable | deprecated | obsolete
noUi: false                # true hides from UI Patterns forms
replaces: "theme:old-card" # SDC component replacement

links:
  - url: "https://example.com/design"
    title: "Design spec"
tags: [Content, Cards]     # Documentation-only categorization

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
    description: "Main content area"
  footer:
    title: "Card footer"
```

### Key YAML Properties

| Property | Type | Purpose |
|---|---|---|
| `name` | string | Human-readable label (mandatory) |
| `group` | string | Category for grouping in UI forms |
| `noUi` | boolean | Hides component from site-builder UIs |
| `replaces` | string | SDC component ID this replaces (theme overrides) |
| `variants` | object | Named visual variants (become `variant` prop) |
| `props` | object | JSON Schema object defining typed properties |
| `slots` | object | Named placeholders for render arrays |
| `links` | array | Documentation links |
| `tags` | array | Documentation-only tags |
| `status` | string | Lifecycle status |

### Props Definition with JSON Schema

Props use JSON Schema. For complex or Drupal-specific types, use `$ref` shortcuts:

```yaml
# Simple JSON Schema types
title:
  title: "Title"
  type: "string"
count:
  title: "Count"
  type: "integer"
  minimum: 0
  maximum: 100

# UI Patterns shortcut references
url:
  title: "Link URL"
  "$ref": "ui-patterns://url"
is_active:
  title: "Active"
  "$ref": "ui-patterns://boolean"
nav_links:
  title: "Navigation"
  "$ref": "ui-patterns://links"
```

### Required Props

Unlike standard JSON Schema where `required` is at the object level, UI Patterns reads `required` and annotates each prop individually:

```yaml
props:
  type: object
  required:
    - title    # This prop will show as required in forms
  properties:
    title:
      type: "string"
```

### The `default` Property

The `default` value pre-fills form widgets via `#default_value`. It does **not** enforce defaults during rendering. Use Twig's `|default()` filter for render-time defaults:

```twig
<h2>{{ title|default('Untitled') }}</h2>
```

### Common Mistakes

| Mistake | Why It Is Wrong |
|---|---|
| Relying on `default` in YAML for render-time fallbacks | `default` only affects form pre-fill. If a source returns empty, the template gets nothing unless you use `\|default()` in Twig. |
| Defining props without `title` | While not strictly required by JSON Schema, UI Patterns uses `title` for form labels. Missing titles result in machine names as labels. |
| Using PHP class names as `type` | `type: 'Drupal\Core\Template\Attribute'` is handled specially as an attributes prop but is non-standard. Prefer `"$ref": "ui-patterns://attributes"`. |
| Putting renderables in props | Props are strictly typed data. Renderables (blocks, components, markup) belong in slots. |

### See Also

- [Props System](#props-system)
- [Variants](#variants)
- SDC Development Guide