---
description: "Model an icon SDC prop as {pack_id, icon_id, settings} — YAML default: and required: are never enforced at render time"
tldr: "You're building SDC components that need configurable icon props; YAML default: is never applied and required: runs behind assert(), off in production — write the Twig so it's correct with no props declared at all."
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
$schema: https://git.drupalcode.org/project/drupal/-/raw/HEAD/core/assets/schemas/v1/metadata.schema.json
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
        icon_id:
          type: string
        settings:
          type: object
      required:
        - icon_id
    title:
      type: string
```

Two things this YAML does *not* do, both of which the template below has to compensate for:

- **`default:` is never applied.** `ComponentValidator::validateProps()` runs with `CHECK_MODE_TYPE_CAST` only — it casts and validates, it never fills in defaults. The effective default is whatever the Twig writes with `??` or `|default()`.
- **Validation is not a runtime guarantee.** `ComponentsTwigExtension::validateProps()` wraps the check in `assert()` (`ComponentsTwigExtension.php:106`), so on a production `zend.assertions=-1` it does not run, and the validator takes the context by value and never strips anything. Undeclared props reach the template and work; `required: [icon_id]` will not stop a render in production.

Write the template so it is correct with no props declared at all, and treat the YAML as documentation for the component's consumers.

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

  {% block content %}{% endblock %}
</div>
```

A local variable named `icon` does not shadow the `icon()` function — Twig resolves `name(...)` as a function call at compile time — so the prop and the function can share a name safely.

The component's `card.component.yml` must also declare the slot it renders:

```yaml
slots:
  content:
    title: Content
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
{{ icon('my_theme', status_icon, { size: 20 }) }}
```

Reference: `/core/assets/schemas/v1/metadata.schema.json` for the component schema. (`core/modules/sdc/` is an empty stub since SDC moved into core proper — it holds only `sdc.info.yml`, and the `core/modules/sdc/src/metadata.schema.json` URL is a Drupal 10.1-era path.)

## Common Mistakes

- Using a `pack:id` prop and passing it straight to `icon()` → Fatal. Either model the prop as `{pack_id, icon_id}` or split the string in the template
- Relying on the YAML `default:` for `pack_id` or `settings` → Never applied; put the fallback in the Twig
- Relying on `required:` to guarantee a value at runtime → Validation is behind `assert()` and is off in production
- Not handling missing icons gracefully → Use `{% if icon and icon.icon_id %}` checks
- Complex nested objects → Keep icon prop structure flat for easier usage

## See Also

- [Twig Icon Function](twig-icon-function.md)
- [Icon Slots](icon-slots.md)
- Reference: [SDC documentation](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components)
