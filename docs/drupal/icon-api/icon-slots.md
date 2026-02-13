---
description: Maximum flexibility for icon content using SDC slots
drupal_version: "11.x"
---

# Icon Slots

## When to Use

> Use when your component needs maximum flexibility for icon content, including custom SVG, multiple icons, or complex icon compositions.

## Decision

| Use slots when... | Use props when... |
|---|---|
| Icon content varies significantly | Icon is simple, single identifier |
| Multiple icons in one component | One icon per component |
| Custom SVG/HTML needed | Standard icon rendering sufficient |
| Icon with surrounding markup | Icon standalone |

## Pattern

Slot-based icon in component:

```yaml
# components/alert/alert.component.yml
name: Alert
props:
  type: object
  properties:
    variant:
      type: string
      enum: [success, warning, error, info]
slots:
  icon:
    title: Alert Icon
    description: Icon displayed before alert message
  default:
    title: Alert Content
```

Component template:

```twig
{# components/alert/alert.twig #}
<div class="alert alert--{{ variant|default('info') }}">
  {% if icon %}
    <div class="alert__icon">
      {{ icon }}
    </div>
  {% endif %}

  <div class="alert__content">
    {{ content }}
  </div>
</div>
```

Usage with embed:

```twig
{% embed 'my_theme:alert' with {variant: 'success'} %}
  {% block icon %}
    {{ icon('my_theme:check-circle', {
      size: 24,
      color: 'var(--bs-success)'
    }) }}
  {% endblock %}

  {% block default %}
    Operation completed successfully!
  {% endblock %}
{% endembed %}
```

Usage with include (slot as variable):

```twig
{{ include('my_theme:alert', {
  variant: 'warning',
  icon: icon('my_theme:alert-triangle', { size: 24 }),
  content: 'Please review your input.'
}) }}
```

Reference: `/core/modules/sdc/` for slots documentation.

## Common Mistakes

- **Wrong**: Using slots for simple icons → **Right**: Props are simpler for standard icon rendering
- **Wrong**: Not providing default slot content → **Right**: Gracefully handle missing icons with `{% if icon %}`
- **Wrong**: Rendering slot without escaping → **Right**: Slots auto-escape, trust only from controlled sources
- **Wrong**: Overly complex slot structures → **Right**: Keep slots focused on single responsibility
- **Wrong**: Missing slot documentation → **Right**: Document expected slot content in component description

## See Also

- [SDC Icon Props](sdc-icon-props.md)
- [IconPackManager Service](iconpackmanager-service.md)
- Reference: [SDC slots documentation](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components/slots)
