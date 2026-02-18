---
topic: drupal/twig
guide: twig-filters
---

## Drupal Twig Filters

### When to Use
When you need to transform, escape, translate, or manipulate variables in Twig templates.

### Items

#### `|t` / `|trans`
**Description:** Translates a string. Identical to PHP `t()`.
**Usage:**
```twig
{{ 'Read more'|t }}
{{ 'Hello @name'|t({'@name': user.name}) }}
```
**Gotchas:** Only for static strings — do not translate user-provided content. The `{% trans %}` block tag is for multi-word or complex translations.

#### `{% trans %}` block tag
**Description:** Translates multi-word blocks, supports pluralization.
**Usage:**
```twig
{% trans %}Submitted by {{ author_name }} on {{ date }}{% endtrans %}
{% trans %}
  One item
{% plural count %}
  {{ count }} items
{% endtrans %}
```

#### `|placeholder`
**Description:** Wraps a value in `<em class="placeholder">` for use in translated strings.
**Usage:**
```twig
{% trans %}File {{ filename|placeholder }} not found{% endtrans %}
```

#### `|without`
**Description:** Removes specified keys from a render array. Used to print `content` minus specific fields.
**Usage:**
```twig
{# Print everything except field_body and field_tags #}
{{ content|without('field_body', 'field_tags') }}
```
**Gotchas:** Works on render arrays and `ArrayAccess` objects. Returns a copy — original is unchanged.

#### `|clean_class`
**Description:** Converts a string to a valid CSS class name (removes invalid characters, lowercases).
**Usage:**
```twig
<div class="node--type-{{ node.bundle|clean_class }}">
```

#### `|clean_id`
**Description:** Converts a string to a valid HTML ID.
**Usage:**
```twig
<section id="{{ 'Section ' ~ node.id()|clean_id }}">
```

#### `|clean_unique_id`
**Description:** Generates a unique HTML ID from a string (adds incrementing counter if collision).

#### `|safe_join`
**Description:** Joins an array with a delimiter, escaping each item.
**Usage:**
```twig
{{ head_title|safe_join(' | ') }}
{{ classes|safe_join(' ') }}
```
**Gotchas:** Unlike standard Twig `join`, items are HTML-escaped. The glue string is NOT escaped — must be trusted.

#### `|render`
**Description:** Forces rendering of a render array to a string. Useful for checking if content is empty after rendering.
**Usage:**
```twig
{% set body = content.field_body|render %}
{% if body|trim %}
  <div class="body">{{ body }}</div>
{% endif %}
```

#### `|format_date`
**Description:** Formats a timestamp using Drupal date formatter.
**Usage:**
```twig
{{ node.getCreatedTime()|format_date('medium') }}
{{ node.getCreatedTime()|format_date('custom', 'Y-m-d') }}
```

#### `|add_class`
**Description:** Adds CSS classes to a render element's `#attributes`.
**Usage:**
```twig
{{ content.field_body|add_class('rich-text') }}
```
**Gotchas:** Returns modified render array — print it or it does nothing.

#### `|set_attribute`
**Description:** Sets an attribute on a render element.
**Usage:**
```twig
{{ content.field_image|set_attribute('loading', 'lazy') }}
```

#### `|add_suggestion`
**Description:** Adds a theme suggestion to a render element. Drupal 10.1+.
**Usage:**
```twig
{{ content.field_body|add_suggestion('article') }}
{# Uses field--text-long--article.html.twig instead of field--text-long.html.twig #}
```

#### `|raw`
**Description:** Marks a string as safe HTML, bypassing auto-escaping. **Use with extreme caution.**
**Usage:**
```twig
{# ONLY when value is guaranteed safe (already sanitized MarkupInterface) #}
{{ my_trusted_markup|raw }}
```
**Gotchas:** NEVER use on user-provided content. NEVER use on field values (use `content.field_name` instead). `MarkupInterface` objects don't need `|raw` — they bypass escaping automatically.

### Common Mistakes
- `{{ node.field_body.value|raw }}` — this outputs raw, unfiltered user HTML. Use `{{ content.field_body }}` for formatted output or `{{ node.field_body.processed }}` for filter-applied HTML (still not `|raw`)
- `{{ 'text'|t|raw }}` — redundant and dangerous habit; `|t` already returns `MarkupInterface`
- Using `{{ content|without }}` without arguments — no-op, does nothing
- `|format_date` on a DateTime object instead of a timestamp → pass `node.getCreatedTime()` (Unix timestamp), not a date string

### See Also
- Twig functions → [Drupal Twig Functions](twig-functions.md)
- Security details → [Security & Performance](security-performance.md)
- Core source: `core/lib/Drupal/Core/Template/TwigExtension.php`
