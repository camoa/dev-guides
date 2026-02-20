---
description: Methods for including, embedding, and nesting components
drupal_version: "11.x"
---

# Component Composition

## When to Use

> Use this when including one component in another, deciding between `include()`, `embed`, or render arrays, or nesting components.

## Decision

| Method | Use Case | When to Use |
|--------|----------|-------------|
| `include()` | Simple component inclusion | Props-only components |
| `{% embed %}` | Populating slots via Twig blocks | Components with slots that need custom content |
| Render arrays | Programmatic rendering | PHP code (preprocessing, controllers, forms) |
| Nested components | Complex compositions | Building organisms from molecules |

## Pattern

**include() Function (Most Common):**
```twig
{# Simple inclusion #}
{{ include('my_theme:button', {
  text: 'Click Me',
  variant: 'primary',
  disabled: false
}) }}

{# With context isolation (recommended) #}
{{ include('my_theme:button', {
  text: 'Save',
  variant: 'primary'
}, with_context = false) }}
```

**embed Tag (Only for Slots):**
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

**Render Arrays (Programmatic):**
```php
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

## Common Mistakes

- **Wrong**: Using `embed` for props-only components → **Right**: Use `include()` (simpler, less overhead)
- **Wrong**: Not using `with_context = false` → **Right**: Prevent variable leakage for predictable components
- **Wrong**: Hardcoding child components → **Right**: Use slots for flexibility

## See Also

- Reference: `/core/themes/olivero/components/teaser/teaser.twig`
- [Twig Templates in SDCs](twig-templates-in-sdcs.md)
- [Props vs Slots Decision Framework](props-vs-slots-decision-framework.md)
- [Twig Template System](https://twig.symfony.com/doc/3.x/tags/include.html)
