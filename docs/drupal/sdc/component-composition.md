---
description: Including components within components using include(), embed, or render arrays
drupal_version: "11.x"
---

# Component Composition

## When to Use

> Use this when including one component in another, deciding between `include()`, `embed`, or render arrays, or nesting components.

## Decision: Composition Methods

| Method | Use Case | When to Use |
|--------|----------|-------------|
| `include()` | Simple component with props only | Most common, no slots needed |
| `{% embed %}` | Component with slots via Twig blocks | Only when populating slots |
| Render arrays | Programmatic composition | Preprocessing, controllers, forms, hooks |

## Pattern

include() function (most common):

```twig
{# Simple inclusion #}
{{ include('my_theme:button', {
  text: 'Click Me',
  variant: 'primary',
  disabled: false
}) }}

{# With context control (recommended) #}
{{ include('my_theme:button', {
  text: 'Save',
  variant: 'primary'
}, with_context = false) }}
```

**WHY `with_context = false`**: Prevents automatic variable leakage into component, keeping components isolated and predictable.

embed tag (only for slots):

```twig
{% embed 'my_theme:card' with {
  title: node.label,
  variant: 'featured'
} only %}

  {% block content %}
    {{ content.body }}
    {{ include('my_theme:button', {
      text: 'Read More',
      url: node.url
    }) }}
  {% endblock %}

  {% block footer %}
    {{ content.field_tags }}
  {% endblock %}

{% endembed %}
```

Render arrays (programmatic):

```php
// In .theme file or controller
$build = [
  '#type' => 'component',
  '#component' => 'my_theme:card',
  '#props' => [
    'title' => $node->label(),
    'variant' => 'featured',
  ],
  '#slots' => [
    'content' => $node->body->view('teaser'),
    'footer' => $node->field_tags->view('compact'),
  ],
];
```

Nested components (components in slots):

```twig
{# Parent component with child components in slots #}
{% embed 'my_theme:hero-banner' with { variant: 'primary' } only %}

  {% block content %}
    <h1>{{ title }}</h1>
    {{ include('my_theme:button', {
      text: 'Get Started',
      variant: 'primary',
      size: 'large'
    }) }}
  {% endblock %}

{% endembed %}
```

## Common Mistakes

- **Wrong**: Using `embed` when `include()` is sufficient → **Right**: `embed` has overhead and complexity. Only use when you need to populate slots with Twig blocks. For props-only components, use `include()`.
- **Wrong**: Hardcoding child components instead of using slots → **Right**: Reduces flexibility. Slots allow different child components in different contexts. Hardcoding couples parent to specific children.

## See Also

- Reference: `/core/themes/olivero/components/teaser/teaser.twig`
- [Twig Templates in SDCs](twig-templates-in-sdcs.md)
- [Props vs Slots Decision Framework](props-vs-slots-decision-framework.md)
- [Twig Template System](https://twig.symfony.com/doc/3.x/tags/include.html)
