---
topic: drupal/twig
guide: multi-value-fields
---

## Multi-Value Fields & Collections

### When to Use
When a field is configured to allow multiple values and you need to iterate, count, slice, or conditionally access individual items.

### Decision
| If you need... | Use... | Why |
|---|---|---|
| Iterate all values | `{% for item in node.field_tags %}` | FieldItemList is iterable |
| Iterate rendered items | `{% for item in content.field_tags['#items'] %}` | Use sparingly — complex |
| First value only | `{{ node.field_tags.0.entity.label }}` | Zero-indexed access |
| Count values | `{{ node.field_tags\|length }}` | Twig length filter on FieldItemList |
| First N items | `{% for item in node.field_tags\|slice(0, 3) %}` | Standard Twig slice |
| Display rendered field | `{{ content.field_tags }}` | Let Drupal handle it — safest |

### Pattern

**Iterating raw field items:**
```twig
{# Loop over taxonomy term references #}
{% if node.field_tags is not empty %}
  <ul class="tags">
    {% for item in node.field_tags %}
      {% set term = item.entity %}
      {% if term %}
        <li>{{ term.label }}</li>
      {% endif %}
    {% endfor %}
  </ul>
{% endif %}

{# First item only, with fallback #}
{% set primary_cat = node.field_categories.0.entity %}
{% if primary_cat %}
  <span class="primary-category">{{ primary_cat.label }}</span>
{% endif %}
```

**Counting and limiting:**
```twig
{# Show count then limit display #}
{% set tag_count = node.field_tags|length %}
{% if tag_count > 0 %}
  <p>{{ tag_count }} tags</p>
  {% for item in node.field_tags|slice(0, 5) %}
    <span>{{ item.entity.label }}</span>
  {% endfor %}
{% endif %}
```

**Using rendered output (preferred when formatters matter):**
```twig
{# The formatter handles rendering — comma lists, links, etc. #}
{{ content.field_tags }}

{# Access individual rendered items from field template context #}
{# In field.html.twig: #}
{% for item in items %}
  <div{{ item.attributes }}>{{ item.content }}</div>
{% endfor %}
```

### Common Mistakes
- `{% if content.field_tags %}` — always truthy even for empty fields. Use `{% if node.field_tags is not empty %}` or `{% if content.field_tags['#items']|length > 0 %}`
- Confusing `node.field_tags` (FieldItemList, raw) with `content.field_tags` (render array)
- Iterating `content.field_tags` — not directly iterable as expected; iterate `node.field_tags` instead
- Not checking `item.entity` before accessing entity properties — entity reference items may have null entities (deleted references)

### See Also
- Field access → [Accessing Field Values](accessing-field-values.md)
- Entity reference traversal → [Entity Reference Traversal](entity-reference-traversal.md)
