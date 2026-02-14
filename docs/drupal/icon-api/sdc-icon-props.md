---
description: Building Single Directory Components with configurable icons as props for reusable component APIs
drupal_version: "11.x"
---

# SDC Icon Props

## When to Use

You're building Single Directory Components that need configurable icons as props for reusable, flexible component APIs.

## Decision

| Pattern | Use when... | Flexibility | Type safety |
|---|---|---|---|
| Object prop (recommended) | Full icon control needed | High | Medium |
| Enum prop | Limited icon set | Low | High |
| String prop | Icon ID only | Medium | Low |
| UI Patterns `$ref` | Using UI Icons module | High | High |

## Pattern

Object-based icon prop (recommended):

```yaml
# components/card/card.component.yml
$schema: https://git.drupalcode.org/project/drupal/-/raw/11.x/core/modules/sdc/src/metadata.schema.json
name: Card
props:
  type: object
  properties:
    icon:
      title: Icon
      type: object
      properties:
        pack_id:
          type: string
          default: "my_theme"
        icon_id:
          type: string
        settings:
          type: object
          default:
            size: 24
      required:
        - icon_id
    title:
      type: string
```

Component template:

```twig
{# components/card/card.twig #}
<div class="card">
  {% if icon and icon.icon_id %}
    <div class="card__icon">
      {{ icon(
        icon.pack_id|default('my_theme'),
        icon.icon_id,
        icon.settings|default({})
      ) }}
    </div>
  {% endif %}

  {% if title %}
    <h3 class="card__title">{{ title }}</h3>
  {% endif %}

  {{ content }}
</div>
```

Usage:

```twig
{{ include('my_theme:card', {
  title: 'Welcome',
  icon: {
    icon_id: 'home',
    settings: { size: 32, color: '#007bff' }
  }
}) }}
```

Enum-based prop for limited sets:

```yaml
props:
  type: object
  properties:
    status_icon:
      type: string
      enum:
        - success
        - warning
        - error
      default: "success"
```

```twig
{{ icon('my_theme:' ~ status_icon, { size: 20 }) }}
```

Reference: `/core/modules/sdc/src/metadata.schema.json` for component schema.

## Common Mistakes

- **Wrong**: Hardcoded pack_id in template → **Right**: Make configurable via prop with default
- **Wrong**: No default settings → **Right**: Provide sensible defaults for size, color
- **Wrong**: Missing required validation → **Right**: Mark `icon_id` as required when icon is mandatory
- **Wrong**: Not handling missing icons gracefully → **Right**: Use `{% if icon and icon.icon_id %}` checks
- **Wrong**: Complex nested objects → **Right**: Keep icon prop structure flat for easier usage

## See Also

- [Twig Icon Function](twig-icon-function.md)
- [Icon Slots](icon-slots.md)
- Reference: [SDC documentation](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components)
