---
description: Slots System — multiple sources per slot, slot source plugins, Twig access
drupal_version: "11.x"
---

# Slots System

## When to Use

> Use slots for renderables — blocks, other components, WYSIWYG content, field formatter output. Use props for typed scalar/structured data.

## Decision

| Content Type | Use | Reason |
|-------------|-----|--------|
| Block output, rendered markup | Slot | Renderables need the render pipeline |
| Plain text, numbers, booleans | Prop | Strictly typed, validated by JSON Schema |
| Multiple stacked renderables in one area | Slot | Slots support multiple sources, props do not |
| Navigation links | Prop (`links` type) | Structured data with a defined schema |

## Pattern

### Slot definition

```yaml
slots:
  content:
    title: "Main Content"
    description: "The primary content area"
  sidebar:
    title: "Sidebar"
```

### Built-in slot sources

| Source | What It Does |
|--------|-------------|
| `component` | Embeds another SDC component |
| `block` | Embeds a Drupal block plugin |
| `wysiwyg` | Rich text via CKEditor |
| `field_formatter` | Renders a field using a Drupal field formatter |

String-type sources (textfield, token) also work via the `slot <- string` conversion path.

### Accessing slots in Twig

```twig
<div class="card">
  <div class="card__body">{{ content }}</div>
  {% if sidebar %}
    <aside class="card__sidebar">{{ sidebar }}</aside>
  {% endif %}
</div>
```

Unlike props (one source per prop), slots support **multiple sources**. Site-builders can stack a component + a block + WYSIWYG text in a single slot; they render in sequence.

## Common Mistakes

- **Wrong**: `{% for item in content %}` to loop a slot → **Right**: Render arrays are iterable over their keys (`#theme`, `#cache`), not child elements; output the slot variable directly
- **Wrong**: Correlating indices across multiple slots (images + captions) → **Right**: Use a single slot with a sub-component that pairs them
- **Wrong**: Applying filters to slot output → **Right**: Only approved slot filters (`add_class`, `set_attribute`) are safe; other filters may break render arrays

## See Also

- [Source Plugins](source-plugins.md)
- [Defining Components](defining-components.md)
- [Best Practices & Anti-Patterns](best-practices-and-anti-patterns.md)
