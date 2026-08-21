---
description: Slots — renderables, multiple sources, and normalization for component placeholders
tldr: "Slots — renderables, multiple sources, and normalization for component placeholders"
drupal_version: "11.x"
---

# Slots System

## How Slots Work

Slots are named placeholders in a component that accept Drupal render arrays. Unlike props (typed scalar/structured data), slots hold renderables: blocks, other components, WYSIWYG content, or field formatter output.

Internally, the `slot` prop type is a special PropType plugin that normalizes any input into a render array via `SlotPropType::normalize()`:

- Plain strings become `['#plain_text' => $string]` — **escaped**. This reversed after 2.0.15 (issue #3611167); it used to be `['#children' => Markup::create($string)]`, i.e. raw HTML. To put raw HTML in a slot you must now hand over a trusted type: `Markup::create()`, a Twig `{% set %}` capture, or a render array.
- Objects implementing `RenderableInterface` are converted via `->toRenderable()`, then normalized again
- `MarkupInterface` (and Twig `Markup`) objects become `['#children' => $value]` and stay raw
- Other `Stringable` objects become `['#plain_text' => (string) $value]`
- Arrays pass through as render arrays; a list with no `#`-properties is re-keyed with `array_values()` so Twig's `is sequence` test works on UUID-keyed block lists

## Slot Definition in YAML

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

## Multiple Sources Per Slot

Unlike props (one source per prop), slots support **multiple sources**. In the UI, site-builders can add several sources to a single slot (e.g., a component + a block + WYSIWYG text), and they render in sequence:

```php
// In ComponentElementBuilder::buildSlot()
foreach ($configuration['sources'] as $source_configuration) {
    $build = $this->buildSource($build, $slot_id, $definition, $source_configuration, $contexts);
}
```

## Slot Sources

Built-in sources that work with slots (`prop_types: ['slot']`):

| Source | What It Does |
|---|---|
| `component` | Embeds another SDC component (nesting) |
| `block` | Embeds a Drupal block plugin |
| `wysiwyg` | Rich text via CKEditor text_format element |
| `field_formatter` | Renders a field using a Drupal field formatter (its deriver sets `prop_types: ["slot"]`) |
| `token` | Declares `slot` natively alongside `string` and `url` |
| `view_field`, `view_rows` | `ui_patterns_views` — a Views row field, or the whole set of rendered rows |
| `entity_field`, `entity_reference` | Declare no `prop_types` at all, so they are offered for slots as well as props |

Other string-type sources (`textfield` and friends) reach slots through the `slot <- string` conversion path.

## Accessing Slots in Twig

Slots appear as Twig variables matching their YAML key names:

```twig
<div class="card">
  <div class="card__body">{{ content }}</div>
  {% if sidebar %}
    <aside class="card__sidebar">{{ sidebar }}</aside>
  {% endif %}
</div>
```

## Common Mistakes

| Mistake | Why It Is Wrong |
|---|---|
| Looping over a slot variable | Render arrays are iterable in Twig, so `{% for item in content %}` may iterate over render array keys (`#theme`, `#cache`) instead of child elements. Only loop if you have verified the slot is a sequence of renderables. |
| Correlating indices across multiple slots | If you have `images` and `captions` slots, there is no guarantee they have matching indices. Use a single slot with a sub-component that pairs them. |
| Applying filters to slot output | Slots should pass through unmodified. Filtering slot content (except approved slot filters like `add_class` and `set_attribute`) may break render arrays. |

## See Also

- [Source Plugins](source-plugins.md)
- [Defining Components](defining-components.md)
- [Best Practices & Anti-Patterns](best-practices-and-anti-patterns.md)