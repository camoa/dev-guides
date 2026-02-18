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

### Common Mistakes
- `{{ node.field_body.value|raw }}` — RAW FILTER on user content is XSS. Use `{{ content.field_body }}` instead
- `{{ content.field_name.value }}` — the `content` array holds render arrays, not field objects. Access raw values via `{{ node.field_name.value }}`
- `{% if content.field_name %}` — content render arrays are always truthy even if empty. Use `{% if node.field_name.value is not empty %}`
- Skipping empty check on entity references → `node.field_reference.entity` will throw an error if field is empty
- Using `{{ node.body }}` instead of `{{ node.field_body }}` — base fields use their machine name which may not have `field_` prefix (e.g., `body`, `title`, `uid`)
- Printing `{{ node.field_image.entity.fileUri }}` directly — outputs `public://path/to/file.jpg`, not a web URL. Use `file_url(node.field_image.entity.fileUri)`

### See Also
- Multi-value field iteration → [Multi-Value Fields](multi-value-fields.md)
- Entity reference traversal → [Entity Reference Traversal](entity-reference-traversal.md)
- Why `|raw` is dangerous → [Security & Performance](security-performance.md)
