---
topic: drupal/twig
guide: entity-reference-traversal
---

## Entity Reference Traversal

### When to Use
When a field references another entity (taxonomy term, media, user, paragraph, another node) and you need to access the referenced entity's data in Twig.

### Decision
| If you need... | Use... | Why |
|---|---|---|
| Referenced entity's label | `node.field_ref.entity.label` | `label()` is sandbox-whitelisted |
| Referenced entity's ID | `node.field_ref.target_id` | Avoids loading entity just for ID |
| Check access before loading | Preprocess function | Access checks belong in PHP, not templates |
| Referenced entity's rendered view | `{{ content.field_ref }}` | Renders with view mode config, access-checked |
| Deep chain (node → media → file) | Step-by-step with null checks | One missing link throws error |

### Pattern

**Safe traversal with null checks:**
```twig
{# Taxonomy term reference #}
{% set term = node.field_tags.0.entity %}
{% if term %}
  <a href="{{ path('entity.taxonomy_term.canonical', {taxonomy_term: term.id()}) }}">
    {{ term.label }}
  </a>
{% endif %}

{# Media entity → file entity → URI #}
{% set media = node.field_hero_media.entity %}
{% if media and media.field_media_image.entity %}
  {% set file = media.field_media_image.entity %}
  <img src="{{ file_url(file.fileUri) }}" alt="{{ media.field_media_image.alt }}">
{% endif %}
```

**Sandbox-allowed methods on entities:**
- `entity.id()` — entity ID
- `entity.label()` — entity label (title, name, etc.)
- `entity.bundle()` — entity bundle (content type, vocabulary, etc.)
- `entity.get('field_name')` — field item list object
- Any method starting with `get`, `has`, `is`
- Example: `node.isPublished()`, `node.hasField('field_example')`, `user.getDisplayName()`

**Methods that will throw SecurityError:**
- `entity.delete()`, `entity.save()` — mutating methods
- Custom methods that don't start with `get`/`has`/`is` and don't have `#[TwigAllowed]`

### Common Mistakes
- Chaining without null checks: `{{ node.field_ref.entity.field_image.entity.fileUri }}` — one empty field breaks the chain with a fatal error
- Calling `->get()` vs property access: in Twig `node.field_name` works (Twig tries property access then method call), but `node.get('field_name')` also works explicitly
- Expecting full entity load on `target_id` — `target_id` is just the integer ID, not the entity; use `.entity` to load
- Accessing `entity.field_name.value` without checking `entity` exists first — null pointer error

### See Also
- Field value access → [Accessing Field Values](accessing-field-values.md)
- Sandbox restrictions → [Twig Overview](twig-overview.md)
