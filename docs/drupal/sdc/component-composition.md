---
description: "Choosing between include(), embed, and render arrays to compose components, and the embed precondition on the child's Twig"
tldr: "Use include() for props-only inclusion (with with_context = false); use embed only when the child renders that slot through {% block name %} — if it prints a bare {{ name }} or wraps it in {% if %}, your block override is silently discarded. Render arrays are for preprocessing/controllers/hooks."
drupal_version: "11.x"
---

# Component Composition

## When to Use

> Use this when you're including one component in another, deciding between `include()`, `embed`, or render arrays, or nesting components.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Simple prop-only inclusion | `include()` with `with_context = false` | Isolated, predictable, lowest overhead |
| To fill a slot via a Twig block | `embed` | Only tag that can override a `{% block %}` — but only if the child renders that slot as a block |
| Programmatic composition (preprocess, controller, form, hook) | Render array (`#type: component`) | The only path that sets both a block override and a context variable for every slot |

`include()` can also fill a slot, but only if the component template prints it as a variable (`{{ header }}`) rather than as a `{% block %}`. It cannot override blocks. That is the whole reason `embed` exists.

**Precondition for `embed`:** the component you are embedding must render that slot through `{% block name %}`. If its template prints a bare `{{ name }}` instead, or wraps the block in `{% if name %}`, your block override is silently discarded — see [Twig Templates in SDCs](twig-templates-in-sdcs.md). Open the component's `.twig` before you write the embed.

## Pattern

**`include()` — most common:**

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

**WHY `with_context = false`:** Prevents automatic variable leakage into the component, keeping components isolated and predictable.

**`embed` — only for filling slots via blocks.** Reference (component side): `/core/themes/olivero/components/teaser/teaser.twig`

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

**Render arrays — programmatic:**

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

**Nested components:**

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

- **Wrong**: Using `embed` when `include()` is sufficient → **Right**: `embed` has overhead and complexity. Only use it when you need to populate slots with Twig blocks. For props-only components, use `include()`.
- **Wrong**: Hardcoding child components instead of using slots → **Right**: Reduces flexibility. Slots allow different child components in different contexts. Hardcoding couples the parent to specific children.

## See Also

- [Twig Templates in SDCs](twig-templates-in-sdcs.md)
- [Props vs Slots Decision Framework](props-vs-slots-decision-framework.md)
- [Twig Template System](https://twig.symfony.com/doc/3.x/tags/include.html)
