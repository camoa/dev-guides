---
topic: drupal/twig
guide: accessing-field-values
---

## Accessing Field Values

### When to Use
This is the most critical section for day-to-day theming. Whenever you need to output, check, or manipulate field data in a Twig template.

### Decision
| If you need... | Use... | Why |
|---|---|---|
| Display field with its formatters | `{{ content.field_name }}` | Safe, includes cache metadata, respects field display config |
| Raw string/text value | `{{ node.field_name.value }}` | Bypasses formatters — for conditions/logic, not display |
| Check if field has a value | `{% if node.field_name.value is not empty %}` | `.value` returns null/empty for empty fields |
| Hide one field from content | `{{ content\|without('field_name') }}` | Removes from content render array, renders rest |
| Field label | `{{ content.field_name['#title'] }}` | Comes from render array, translated |
| Entity reference label | `{{ node.field_reference.entity.label }}` | Traverses to referenced entity, sandbox-safe |
| Entity reference ID | `{{ node.field_reference.target_id }}` | Gets ID without loading entity |
| Image alt text | `{{ node.field_image.alt }}` | Field property access |
| Image URI | `{{ node.field_image.entity.fileUri }}` | Traverses to file entity |
| Link URI | `{{ node.field_link.uri }}` | Raw URI, needs `file_url()` for file URIs |
| Loop over multi-value | `{% for item in node.field_tags %}` | Iterates each entity reference |
| Rendered field via twig_tweak | `{{ drupal_field('field_name', 'node', node.id()) }}` | Full render outside normal context |

### Pattern

**Safe rendered output (preferred for display):**
```twig
{# Renders with all formatters, cache metadata, display settings #}
{{ content.field_body }}

{# Hide field from the catch-all content output #}
<div class="body">{{ content.field_body }}</div>
<div class="other-fields">{{ content|without('field_body', 'field_tags') }}</div>
```

**Raw value access (for conditions and logic):**
```twig
{# Check before rendering — use node object, not content array #}
{% if node.field_summary.value %}
  <p class="summary">{{ node.field_summary.value }}</p>
{% else %}
  {{ content.field_body }}
{% endif %}

{# For text fields: .value gives raw text, .processed gives filtered HTML #}
{% set has_intro = node.field_intro.value is not empty %}
```

**Entity reference access:**
```twig
{# Single reference — access referenced entity #}
{% set category = node.field_category.entity %}
{% if category %}
  <span class="category">{{ category.label }}</span>
{% endif %}

{# Image field — get the file URI for use in file_url() #}
{% set image = node.field_hero_image %}
{% if image.entity %}
  <img src="{{ file_url(image.entity.fileUri) }}" alt="{{ image.alt }}">
{% endif %}
```

### Field Property Reference
Common field type properties accessible via `node.field_name.*`:

| Field type | Property | Returns |
|---|---|---|
| text/string | `.value` | Raw text string |
| text_long / text_with_summary | `.value` | Raw HTML string |
| text_long / text_with_summary | `.processed` | Filtered HTML (safe) |
| text_with_summary | `.summary` | Summary text |
| integer/decimal/float | `.value` | Numeric value |
| boolean | `.value` | `'0'` or `'1'` (string) |
| datetime | `.value` | ISO 8601 date string |
| entity_reference | `.target_id` | Referenced entity ID |
| entity_reference | `.entity` | Loaded entity object |
| link | `.uri` | URI string |
| link | `.title` | Link title text |
| link | `.options` | Options array |
| image | `.target_id` | File entity ID |
| image | `.alt` | Alt text |
| image | `.title` | Title text |
| image | `.width` / `.height` | Dimensions |
| image | `.entity` | File entity |
| file | `.target_id` | File entity ID |
| file | `.entity.fileUri` | `public://...` URI |
| address | `.country_code`, `.locality`, etc. | Address components |

### Cache Invalidation Warning: Entity Traversal in Twig Bypasses Cache Metadata

When you use `{{ content.field_name }}`, Drupal's renderer renders the field through its formatter, producing a render array with `#cache` metadata (tags, contexts, max-age). This metadata **bubbles up** through the render tree, so when the referenced data changes, every cached page that included it gets invalidated.

When you bypass the render array by accessing `{{ node.field_name.value }}` or traversing entity references directly in Twig, **none of the loaded entities' cache tags enter the render tree**. The page caches fine — but it never invalidates when the underlying data changes.

**What goes wrong — stale pages:**

```twig
{# This loads the referenced term entity in Twig. Its cache tags
   (taxonomy_term:42) never bubble into the render array.
   If the term gets renamed, cached pages still show the old name. #}
{% set category = node.field_category.entity %}
{% if category %}
  <span class="badge">{{ category.label }}</span>
{% endif %}

{# Deep chains are worse — two entities loaded, zero cache tags bubbled.
   If the media gets replaced or the file changes, stale image persists. #}
{% set media = node.field_hero_media.entity %}
{% if media and media.field_media_image.entity %}
  <img src="{{ file_url(media.field_media_image.entity.fileUri) }}"
       alt="{{ media.field_media_image.alt }}">
{% endif %}

{# Even conditions based on raw values cause stale output.
   If the referenced term changes from "Featured" to something else,
   cached pages still render the featured layout. #}
{% if node.field_category.entity.label == 'Featured' %}
  <div class="featured-layout">{{ content.field_body }}</div>
{% else %}
  {{ content.field_body }}
{% endif %}
```

**The rule:** Every entity you load via `.entity` in Twig is invisible to the cache system. Simple `.value` access on the current node's own fields is lower risk (the node's own cache tags are already in the render tree), but traversal to **other entities** is where stale pages happen.

**Correct pattern — preprocess with cache metadata bubbling:**

When you need raw data from referenced entities for display or conditional logic, load it in preprocess and bubble the cache metadata:

```php
use Drupal\Core\Cache\CacheableMetadata;

function mytheme_preprocess_node(&$variables) {
  $node = $variables['node'];

  // Start from existing render array metadata
  $cache = CacheableMetadata::createFromRenderArray($variables);

  // Category label for badge display
  if (!$node->get('field_category')->isEmpty()) {
    $term = $node->get('field_category')->entity;
    if ($term) {
      $variables['category_label'] = $term->label();
      // Bubble the term's cache tags — page invalidates when term changes
      $cache->addCacheableDependency($term);
    }
  }

  // Hero image from media reference
  if (!$node->get('field_hero_media')->isEmpty()) {
    $media = $node->get('field_hero_media')->entity;
    if ($media && !$media->get('field_media_image')->isEmpty()) {
      $file = $media->get('field_media_image')->entity;
      if ($file) {
        $variables['hero_image_url'] = \Drupal::service('file_url_generator')
          ->generateAbsoluteString($file->getFileUri());
        $variables['hero_image_alt'] = $media->get('field_media_image')->alt;
        // Bubble both media AND file cache tags
        $cache->addCacheableDependency($media);
        $cache->addCacheableDependency($file);
      }
    }
  }

  $cache->applyTo($variables);
}
```

Then in Twig, use the preprocess variables instead of entity traversal:

```twig
{# Safe — cache tags bubbled in preprocess #}
{% if category_label %}
  <span class="badge">{{ category_label }}</span>
{% endif %}

{% if hero_image_url %}
  <img src="{{ hero_image_url }}" alt="{{ hero_image_alt }}">
{% endif %}
```

**When direct Twig access is acceptable:**
- Accessing the **current node's own** scalar fields for conditions (`node.field_bool.value`, `node.field_status.value`) — the node's cache tags are already in the render tree from `{{ content }}`
- Checking `node.field_name.value is not empty` before rendering `{{ content.field_name }}` — the emptiness check itself doesn't produce output, and the rendered field handles its own metadata
- One-off prototyping where caching is disabled — but never in production templates

### Common Mistakes
- `{{ node.field_body.value|raw }}` — RAW FILTER on user content is XSS. Use `{{ content.field_body }}` instead
- `{{ content.field_name.value }}` — the `content` array holds render arrays, not field objects. Access raw values via `{{ node.field_name.value }}`
- `{% if content.field_name %}` — content render arrays are always truthy even if empty. Use `{% if node.field_name.value is not empty %}`
- Skipping empty check on entity references → `node.field_reference.entity` will throw an error if field is empty
- Using `{{ node.body }}` instead of `{{ node.field_body }}` — base fields use their machine name which may not have `field_` prefix (e.g., `body`, `title`, `uid`)
- Printing `{{ node.field_image.entity.fileUri }}` directly — outputs `public://path/to/file.jpg`, not a web URL. Use `file_url(node.field_image.entity.fileUri)`
- **Traversing `.entity` chains in Twig for display** — loads referenced entities without bubbling cache tags. The page caches correctly once, then serves stale content when the referenced entity changes. Move traversal to preprocess and call `$cache->addCacheableDependency($entity)` for every loaded entity

### See Also
- Multi-value field iteration → [Multi-Value Fields](multi-value-fields.md)
- Entity reference traversal → [Entity Reference Traversal](entity-reference-traversal.md)
- Why `|raw` is dangerous → [Security & Performance](security-performance.md)
- Cache metadata bubbling → [Cache Metadata in Render Arrays](../render-api/cache-metadata-render-arrays.md)
- BubbleableMetadata → [BubbleableMetadata & Cache Bubbling](../caching/bubbleable-metadata-cache-bubbling.md)
