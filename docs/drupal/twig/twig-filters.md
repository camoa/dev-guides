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

#### `|striptags`
**Description:** Strips HTML/XML tags from a string. Twig native filter, commonly used in Drupal for plain-text output.
**Usage:**
```twig
{{ node.field_body.value|striptags }}
{{ content.field_body|render|striptags|trim }}
```
**Gotchas:** Strips ALL tags including safe ones. Use `|striptags('<p><br>')` to allow specific tags. For user content, prefer Drupal's text format system over `|striptags`.

### Commonly Used Twig Native Filters

These are built into Twig (not Drupal-specific) but frequently needed in Drupal templates:

| Filter | Usage | Description |
|---|---|---|
| `\|trim` | `{{ content.field_body\|render\|trim }}` | Removes whitespace from both ends. Essential for empty-checking rendered fields. |
| `\|default('fallback')` | `{{ node.field_subtitle.value\|default('No subtitle') }}` | Returns fallback if variable is empty/null/undefined. |
| `\|first` / `\|last` | `{{ items\|first }}` | Returns first/last element of array or string. |
| `\|length` | `{% if items\|length > 3 %}` | Returns the number of items in array or string length. |
| `\|slice(start, length)` | `{{ items\|slice(0, 3) }}` | Extracts a subset of array or string. Same as `items[0:3]`. |
| `\|merge(array)` | `{{ classes\|merge(['extra-class']) }}` | Merges two arrays. For Attribute objects, use `attributes.addClass()` instead. |
| `\|keys` | `{% for key in items\|keys %}` | Returns array keys. |
| `\|sort` | `{{ items\|sort }}` | Sorts an array. For objects, use arrow function: `\|sort((a,b) => a.weight <=> b.weight)`. |
| `\|column('property')` | `{{ items\|column('title') }}` | Extracts a column from array of arrays/objects (like PHP `array_column`). |
| `\|batch(size)` | `{% for row in items\|batch(3) %}` | Splits array into groups (useful for grid layouts). |
| `\|map(arrow)` | `{{ items\|map(i => i.title) }}` | Transforms each element. Twig 3.x arrow function syntax. |
| `\|filter(arrow)` | `{{ items\|filter(i => i.status) }}` | Filters array elements by condition. |
| `\|reduce(arrow)` | `{{ items\|reduce((carry, i) => carry + i.count, 0) }}` | Reduces array to single value. |
| `\|number_format(decimals, dec_point, thousands_sep)` | `{{ price\|number_format(2, '.', ',') }}` | Formats a number. |
| `\|nl2br` | `{{ text\|nl2br }}` | Converts newlines to `<br>` tags. |
| `\|escape('html_attr')` | `{{ value\|escape('html_attr') }}` | Escapes for specific context (html, html_attr, js, css, url). Alias: `\|e`. |
| `\|split(delimiter)` | `{{ 'a,b,c'\|split(',') }}` | Splits string into array. |
| `\|replace({from: to})` | `{{ text\|replace({'old': 'new'}) }}` | Replaces substrings. |
| `\|upper` / `\|lower` | `{{ text\|upper }}` | Case conversion. |
| `\|capitalize` | `{{ text\|capitalize }}` | Capitalizes first letter. |
| `\|title` | `{{ text\|title }}` | Capitalizes first letter of each word. |
| `\|reverse` | `{{ items\|reverse }}` | Reverses an array or string. |
| `\|json_encode` | `{{ data\|json_encode }}` | JSON-encodes a value. Useful for `data-*` attributes. |
| `\|date(format)` | `{{ 'now'\|date('Y-m-d') }}` | Formats a date string. For Drupal timestamps, prefer `\|format_date` which respects site timezone/locale. |
| `\|abs` | `{{ number\|abs }}` | Absolute value. |
| `\|round` | `{{ number\|round(2) }}` | Rounds a number. |
| `\|url_encode` | `{{ text\|url_encode }}` | URL-encodes a string. |
| `\|raw` | `{{ trusted_markup\|raw }}` | **Bypasses auto-escaping. DANGEROUS.** See entry above. |

### Twig Tags Commonly Used in Drupal

| Tag | Usage | Description |
|---|---|---|
| `{% verbatim %}...{% endverbatim %}` | Outputs raw Twig syntax without parsing | Replaces deprecated `{% raw %}` in Twig 2+. |
| `{% trans %}...{% endtrans %}` | Translation block | See `\|t` entry above. |
| `{% set var = value %}` | Variable assignment | Scoped to current template context. |
| `{% block name %}...{% endblock %}` | Template inheritance block | Override in child templates. |
| `{% extends 'base.html.twig' %}` | Template inheritance | Extends a parent template. |
| `{% include 'partial.html.twig' %}` | Includes another template | Can pass variables with `with`. |
| `{% embed 'component.html.twig' %}` | Include with block overrides | Combines `include` + `extends`. |
| `{% apply filter %}...{% endapply %}` | Applies filter to block | `{% apply upper %}text{% endapply %}`. |
| `{% macro name(args) %}...{% endmacro %}` | Reusable template function | Call with `{{ _self.name(args) }}` or import. |
| `{% deprecated 'message' %}` | Marks template as deprecated | Triggers E_USER_DEPRECATED when template is used. |

### Sandbox Policy — What Methods You Can Call on Objects

Drupal's Twig sandbox restricts method calls. These are allowed by default:

| Rule | Example | Notes |
|---|---|---|
| Methods starting with `get` | `entity.getTitle()`, `node.getCreatedTime()` | Any `get*` prefix works |
| Methods starting with `has` | `entity.hasField('field_body')` | Any `has*` prefix works |
| Methods starting with `is` | `node.isPublished()`, `node.isNew()` | Any `is*` prefix works |
| Exact methods: `id`, `label`, `bundle`, `get`, `__toString`, `toString` | `node.id()`, `node.label()`, `node.bundle()` | Always allowed |
| All methods on `Attribute` class | `attributes.addClass()`, `attributes.hasClass()` | Full unrestricted access |
| Methods with `#[TwigAllowed]` attribute | Custom methods annotated by module developers | Drupal 11+ |

### Common Mistakes
- `{{ node.field_body.value|raw }}` — this outputs raw, unfiltered user HTML. Use `{{ content.field_body }}` for formatted output or `{{ node.field_body.processed }}` for filter-applied HTML (still not `|raw`)
- `{{ 'text'|t|raw }}` — redundant and dangerous habit; `|t` already returns `MarkupInterface`
- Using `{{ content|without }}` without arguments — no-op, does nothing
- `|format_date` on a DateTime object instead of a timestamp → pass `node.getCreatedTime()` (Unix timestamp), not a date string
- Using `|striptags` on user content for sanitization → use Drupal text formats instead; `|striptags` is for display, not security
- Calling `node.save()` or other write methods in templates → blocked by sandbox; use preprocess or controllers
- Using `|date` for Drupal timestamps → use `|format_date` which respects site timezone and locale

### See Also
- Twig functions → [Drupal Twig Functions](twig-functions.md)
- Security details → [Security & Performance](security-performance.md)
- Core source: `core/lib/Drupal/Core/Template/TwigExtension.php`
- Reference: [Twig 3.x documentation](https://twig.symfony.com/doc/3.x/)
