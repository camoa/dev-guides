---
description: Slots — renderables, multiple sources, and normalization for component placeholders
drupal_version: "10.3+ / 11"
---

## Slots System

### How Slots Work

Slots are named placeholders in a component that accept Drupal render arrays. Unlike props (typed scalar/structured data), slots hold renderables: blocks, other components, WYSIWYG content, or field formatter output.

Internally, the `slot` prop type is a special PropType plugin that normalizes any input into a render array via `SlotPropType::normalize()`:

- Strings become `['#children' => Markup::create($string)]`
- Objects implementing `RenderableInterface` are converted via `->toRenderable()`
- `MarkupInterface` objects become `['#children' => $value]`
- Arrays pass through as render arrays (with cleanup for non-list keys)

### Slot Definition in YAML

```yaml
slots:
  content:
    title: "Main Content"
    description: "The primary content area of the card"
  sidebar:
    title: "Sidebar"
    description: "Optional sidebar content"
```

Slots do not have JSON Schema types. Their only metadata is `title` and `description`. UI Patterns automatically adds `title` from the slot key if missing.

### Multiple Sources Per Slot

Unlike props (one source per prop), slots support **multiple sources**. In the UI, site-builders can add several sources to a single slot (e.g., a component + a block + WYSIWYG text), and they render in sequence:

```php
// In ComponentElementBuilder::buildSlot()
foreach ($configuration['sources'] as $source_configuration) {
    $build = $this->buildSource($build, $slot_id, $definition, $source_configuration, $contexts);
}
```

### Slot Sources

Built-in sources that work with slots (`prop_types: ['slot']`):

| Source | What It Does |
|---|---|
| `component` | Embeds another SDC component (nesting) |
| `block` | Embeds a Drupal block plugin |
| `wysiwyg` | Rich text via CKEditor text_format element |
| `field_formatter` | Renders a field using a Drupal field formatter |

String-type sources (textfield, token, etc.) also work via the `slot <- string` conversion path.

### Accessing Slots in Twig

Slots appear as Twig variables matching their YAML key names:

```twig
<div class="card">
  <div class="card__body">{{ content }}</div>
  {% if sidebar %}
    <aside class="card__sidebar">{{ sidebar }}</aside>
  {% endif %}
</div>
```

### Common Mistakes

| Mistake | Why It Is Wrong |
|---|---|
| Looping over a slot variable | Render arrays are iterable in Twig, so `{% for item in content %}` may iterate over render array keys (`#theme`, `#cache`) instead of child elements. Only loop if you have verified the slot is a sequence of renderables. |
| Correlating indices across multiple slots | If you have `images` and `captions` slots, there is no guarantee they have matching indices. Use a single slot with a sub-component that pairs them. |
| Applying filters to slot output | Slots should pass through unmodified. Filtering slot content (except approved slot filters like `add_class` and `set_attribute`) may break render arrays. |

### See Also

- [Source Plugins](#source-plugins)
- [Defining Components](#defining-components)
- [Best Practices & Anti-Patterns](#best-practices--anti-patterns)