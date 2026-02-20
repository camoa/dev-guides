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
| Referenced entity's rendered view | `{{ content.field_ref }}` | Renders with view mode config, access-checked, **cache tags bubble correctly** |
| Referenced entity's label | `node.field_ref.entity.label` | `label()` is sandbox-whitelisted — but **cache tags do NOT bubble** (see warning below) |
| Referenced entity's ID | `node.field_ref.target_id` | Avoids loading entity just for ID |
| Check access before loading | Preprocess function | Access checks belong in PHP, not templates |
| Deep chain (node → media → file) | Preprocess with `addCacheableDependency()` | Twig traversal skips cache metadata — [see Accessing Field Values](accessing-field-values.md#cache-invalidation-warning-entity-traversal-in-twig-bypasses-cache-metadata) |

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

### Cache Warning

Every `.entity` traversal in Twig loads an entity **outside the render array pipeline**. The loaded entity's cache tags never bubble into the page's cache metadata. If that entity changes, cached pages serving the old data are not invalidated.

This affects all patterns on this page. For quick prototyping it's fine, but for production templates — especially on cached pages — move entity traversal to preprocess and use `CacheableMetadata::addCacheableDependency()` to bubble the tags. See [Accessing Field Values — Cache Invalidation Warning](accessing-field-values.md#cache-invalidation-warning-entity-traversal-in-twig-bypasses-cache-metadata) for the full explanation and correct preprocess pattern.

### Common Mistakes
- Chaining without null checks: `{{ node.field_ref.entity.field_image.entity.fileUri }}` — one empty field breaks the chain with a fatal error
- **Using `.entity` chains for display output** — cache tags from loaded entities don't bubble; page serves stale content after the referenced entity changes. Move to preprocess with `addCacheableDependency()`
- Calling `->get()` vs property access: in Twig `node.field_name` works (Twig tries property access then method call), but `node.get('field_name')` also works explicitly
- Expecting full entity load on `target_id` — `target_id` is just the integer ID, not the entity; use `.entity` to load
- Accessing `entity.field_name.value` without checking `entity` exists first — null pointer error

### See Also
- Field value access & cache warning → [Accessing Field Values](accessing-field-values.md)
- Sandbox restrictions → [Twig Overview](twig-overview.md)
- Cache metadata bubbling → [BubbleableMetadata & Cache Bubbling](../caching/bubbleable-metadata-cache-bubbling.md)
