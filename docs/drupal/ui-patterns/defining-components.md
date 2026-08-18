---
description: Component definition structure — YAML keys, JSON Schema props, and required fields
tldr: "Component definition structure — YAML keys, JSON Schema props, and required fields"
drupal_version: "11.x"
---

# Defining Components

## Component Definition Structure

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

## Key YAML Properties

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

## Props Definition with JSON Schema

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

## Required Props

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

## The `default` Property

Where `default:` applies depends entirely on *which code reads the prop*, and the answer differs between plain SDC and UI Patterns.

**Plain SDC ignores it.** Core validates props against the YAML schema but never injects `default:` — the validator runs in type-cast mode only. Render a component with `#type: component` and no value for the prop and the Twig receives nothing.

**UI Patterns widget sources do apply it, at render time.** `SourcePluginPropValue::getSetting('value')` falls back to `getDefaultFromPropDefinition()` when the stored value is NULL, and `getPropValue()` returns that. So once a widget source (textfield, select, number, …) is selected for the prop — even with an empty value — the YAML `default:` reaches the template.

**But a prop with no source configured at all gets nothing.** `ComponentElementBuilder::buildSource()` returns early on `empty($configuration['source_id'])`, so no source means no value, default or not.

The practical rule is unchanged: never rely on `default:` for correctness. Put the fallback in the Twig, where it holds in every path:

```twig
<h2>{{ title|default('Untitled') }}</h2>
```

One special case: for an `enum` prop, `EnumTrait::enumDefaultValue()` falls back to `default:` and then, if the prop is **required**, to the *first value in the `enum` array*. Order your enum values so the first one is a sane default.

## Common Mistakes

| Mistake | Why It Is Wrong |
|---|---|
| Relying on `default` in YAML for render-time fallbacks | It holds only when a widget source is selected for the prop. With no source configured — or when the component is rendered as plain SDC — the template gets nothing. Put the fallback in Twig with `\|default()`. |
| Defining props without `title` | While not strictly required by JSON Schema, UI Patterns uses `title` for form labels. Missing titles result in machine names as labels. |
| Using PHP class names as `type` | `type: 'Drupal\Core\Template\Attribute'` is handled specially as an attributes prop but is non-standard. Prefer `"$ref": "ui-patterns://attributes"`. |
| Putting renderables in props | Props are strictly typed data. Renderables (blocks, components, markup) belong in slots. |

## See Also

- [Props System](props-system.md)
- [Variants](variants.md)
- SDC Development Guide