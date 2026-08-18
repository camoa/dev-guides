---
description: "Render every SDC slot with {% block name %}{% endblock %} — a bare {{ slot }} variable only works under include(), never embed()"
tldr: "Your component needs maximum icon flexibility via slots; under {% embed %} a slot value arrives as a Twig block, so {% if icon %}{{ icon }}{% endif %} is silently false — render every slot as {% block name %}{% endblock %}."
drupal_version: "11.x"
---

# Icon Slots

## When to Use

Your component needs maximum flexibility for icon content, including custom SVG, multiple icons, or complex icon compositions.

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
  content:
    title: Alert Content
```

Slot names are arbitrary keys. There is no implicit "default" slot in core SDC, and `content` is not special — a slot declared as `default:` must be rendered as `{% block default %}`, which is why the pair above is named `icon` and `content` to match the template.

Component template. **Render every slot with `{% block name %}{% endblock %}`, not as a bare variable.** Only the render-element path (`#type: component` with `#slots`) sets a slot-named context variable; under `{% embed %}` the value arrives as a Twig block, so `{% if icon %}{{ icon }}{% endif %}` is false and the caller's content vanishes with no error:

```twig
{# components/alert/alert.twig #}
<div class="alert alert--{{ variant|default('info') }}">
  <div class="alert__icon">
    {% block icon %}{% endblock %}
  </div>

  <div class="alert__content">
    {% block content %}{% endblock %}
  </div>
</div>
```

Usage with embed — this is the form the template above is written for:

```twig
{% embed 'my_theme:alert' with {variant: 'success'} %}
  {% block icon %}
    {{ icon('my_theme', 'check-circle', {
      size: 24,
      color: 'var(--bs-success)'
    }) }}
  {% endblock %}

  {% block content %}
    Operation completed successfully!
  {% endblock %}
{% endembed %}
```

Usage with include. Here the slot values *are* context variables, so a template written with `{% block %}` will not pick them up — pick one calling convention per component and document it:

```twig
{{ include('my_theme:alert', {
  variant: 'warning',
  icon: icon('my_theme', 'alert-triangle', { size: 24 }),
  content: 'Please review your input.'
}) }}
```

Reference: `core/lib/Drupal/Core/Template/ComponentNodeVisitor.php` for how slots are validated; `core/themes/olivero/components/teaser/` for a core component whose `.component.yml` slot keys line up one-for-one with its `{% block %}` names.

## Common Mistakes

- **Wrong**: Rendering a slot as `{{ slot_name }}` → **Right**: Works only via `include()`. Under `{% embed %}` it is undefined and the content silently disappears
- **Wrong**: Declaring a slot `default:` and printing `{{ content }}` → **Right**: Two different names; nothing renders
- **Wrong**: Assuming `required: true` on a slot is enforced → **Right**: `ComponentNodeVisitor::validateSlots()` reports *undeclared* slots, never missing ones
- **Wrong**: Using slots for simple icons → **Right**: Props are simpler for standard icon rendering
- **Wrong**: Missing slot documentation → **Right**: Document expected slot content in the component description

## See Also

- [SDC Icon Props](sdc-icon-props.md)
- [IconPackManager Service](iconpackmanager-service.md)
- Reference: [SDC slots documentation](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components/slots)
