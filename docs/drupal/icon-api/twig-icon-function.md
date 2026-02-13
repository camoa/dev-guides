---
description: Render icons in Twig templates with type safety, caching, and settings
drupal_version: "11.x"
---

# Twig Icon Function

## When to Use

> Use when you need to render icons in Twig templates with type safety, caching, and settings support.

## Decision

| Syntax | Use when... | Example |
|---|---|---|
| `icon('pack:id')` | Simple icon, no settings | `{{ icon('core:home') }}` |
| `icon('pack:id', {...})` | Icon with settings | `{{ icon('core:home', {size: 32}) }}` |
| `icon('pack', 'id', {...})` | Programmatic pack/id | `{{ icon(pack_var, icon_var, settings) }}` |

## Pattern

Basic icon rendering:

```twig
{# Simple icon #}
{{ icon('my_theme:home') }}

{# Icon with size #}
{{ icon('my_theme:home', { size: 32 }) }}

{# Icon with multiple settings #}
{{ icon('my_theme:home', {
  size: 32,
  color: '#007bff',
  class: 'me-2'
}) }}

{# Conditional icon #}
{% if user.isAuthenticated %}
  {{ icon('my_theme:user', { size: 24 }) }}
{% else %}
  {{ icon('my_theme:user-guest', { size: 24 }) }}
{% endif %}

{# Dynamic icon ID #}
{% set status_icons = {
  'success': 'check-circle',
  'error': 'x-circle',
  'warning': 'alert-circle'
} %}
{{ icon('my_theme:' ~ status_icons[status], { size: 20 }) }}
```

Semantic icons with labels:

```twig
<a href="/search">
  {{ icon('my_theme:search', {
    size: 20,
    decorative: false,
    aria_label: 'Search'
  }) }}
  <span class="visually-hidden">Search</span>
</a>
```

Reference: `/core/modules/system/system.module` for icon() Twig function definition.

## Common Mistakes

- **Wrong**: Missing pack ID → **Right**: Format is `pack_id:icon_id`, not just `icon_id`
- **Wrong**: Settings as third argument when using combined syntax → **Right**: Use `icon('pack:id', {...})` not `icon('pack:id', 'icon', {...})`
- **Wrong**: Rendering icons without caching → **Right**: Icon API automatically participates in render caching
- **Wrong**: Not providing text alternatives → **Right**: Decorative icons need `aria-hidden`, semantic icons need labels
- **Wrong**: Hardcoding icon IDs in loops → **Right**: Store mappings in variables for maintainability

## See Also

- [Template Variables](template-variables.md)
- [SDC Icon Props](sdc-icon-props.md)
- Reference: [Icon API Twig documentation](https://www.drupal.org/docs/develop/drupal-apis/icon-api)
