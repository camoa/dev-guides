---
description: Twig template patterns for accessing props, rendering slots, and using attributes
drupal_version: "11.x"
---

# Twig Templates in SDCs

## When to Use

> Use this when writing component Twig templates, accessing props and slots, or working with the `attributes` object.

## Decision

| Element | Access Pattern | Use Case |
|---------|----------------|----------|
| Props | `{{ variable_name }}` | Typed configuration values |
| Slots | `{% block slot_name %}{% endblock %}` | Content insertion points |
| Attributes | `{{ attributes.addClass('class') }}` | Safe attribute manipulation |
| Conditional slots | `{% if slot_name %}` | Check slot existence before rendering wrapper |

## Pattern

**Accessing Props:**
```twig
{# Props available as variables directly #}
{% set button_html_tag = button_html_tag ?? 'button' %}
{% set size = size ? [size] : [] %}
{% set disabled_classes = disabled ? ['disabled'] : [] %}
```

**Rendering Slots:**
```twig
{# Optional slot with conditional wrapper #}
{% if header %}
  <header class="component__header">
    {% block header %}{% endblock %}
  </header>
{% endif %}

{# Required slot #}
<div class="component__content">
  {% block content %}{% endblock %}
</div>
```

**Attributes Object:**
```twig
{# Class addition #}
<div{{ attributes.addClass('component', 'component--' ~ variant) }}>

{# Attribute setting #}
<button{{ attributes.setAttribute('disabled', disabled).setAttribute('type', 'button') }}>

{# Multiple operations chained #}
<article{{ attributes
  .addClass(['teaser', variant ? 'teaser--' ~ variant])
  .setAttribute('role', 'article')
  .removeAttribute('id') }}>
```

## Common Mistakes

- **Wrong**: Rendering wrapper without checking slot existence → **Right**: Always use `{% if slot %}` conditionals for optional slots
- **Wrong**: Applying complex logic to slot content → **Right**: Only check existence (`if slot`) or count (`if slot|length`)
- **Wrong**: Manual attribute string concatenation → **Right**: Use `Attribute` object methods for safe attribute handling

## See Also

- Reference: `/core/lib/Drupal/Core/Template/Attribute.php` - Attribute class
- Reference: `/core/themes/olivero/components/teaser/teaser.twig`
- Reference: `/themes/contrib/radix/components/button/button.twig`
- [Component Composition](component-composition.md)
- [Props vs Slots Decision Framework](props-vs-slots-decision-framework.md)
