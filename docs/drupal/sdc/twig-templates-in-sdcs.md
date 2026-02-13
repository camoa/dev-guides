---
description: Writing Twig templates for SDCs with props, slots, and attributes object
drupal_version: "11.x"
---

# Twig Templates in SDCs

## When to Use

> Use this when writing component Twig templates, accessing props and rendering slots, or working with the `attributes` object.

## Decision: Template Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| Props as variables | Access component configuration | `{{ variant }}`, `{{ disabled }}` |
| `{% block %}` syntax | Render slots with `{% embed %}` | `{% block content %}{% endblock %}` |
| Variables | Render slots with `include()` | `{{ content }}` |
| `attributes` object | Safe attribute merging | `{{ attributes.addClass('component') }}` |

## Pattern

Accessing props (available as Twig variables):

```twig
{# Props available as variables #}
{% set button_html_tag = button_html_tag ?? 'button' %}
{% set size = size ? [size] : [] %}
{% set disabled_classes = disabled ? ['disabled'] : [] %}
```

Rendering slots (via `{% block %}` with `{% embed %}`):

```twig
{# Slot rendering with conditional check #}
<header>
  {% block prefix %}{% endblock %}
  <div class="teaser__meta">
    {% block meta %}{% endblock %}
  </div>
</header>

{# Required slot #}
<div class="teaser__content">
  {% block content %}{% endblock %}
</div>
```

Attributes object (type `Drupal\Core\Template\Attribute`):

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

Conditional slot rendering (check before rendering wrapper):

```twig
{# Check slot before rendering wrapper #}
{% if header %}
  <header class="component__header">
    {{ header }}
  </header>
{% endif %}

{# Provide default for missing content #}
{{ content|default('No content provided.') }}
```

## Common Mistakes

- **Wrong**: Not checking if slots are empty before rendering wrapper elements → **Right**: Empty wrapper elements create invalid HTML and accessibility issues. Always use `{% if slot %}` conditionals.
- **Wrong**: Applying complex logic to slot content → **Right**: Slots contain arbitrary renderables. Only check existence (`if slot`) or count (`if slot|length`). All logic should be in props.

## See Also

- Reference: `/core/lib/Drupal/Core/Template/Attribute.php` - Attribute class
- Reference: `/core/themes/olivero/components/teaser/teaser.twig`
- Reference: `/themes/contrib/radix/components/button/button.twig`
- [Component Composition](component-composition.md)
- [Props vs Slots Decision Framework](props-vs-slots-decision-framework.md)
