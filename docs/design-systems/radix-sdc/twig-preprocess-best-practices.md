---
description: Twig and preprocess best practices — logic placement, template inheritance, attributes object, performance
drupal_version: "11.x"
---

# Twig and Preprocess Best Practices

## When to Use

> Use this when deciding whether logic belongs in Twig or preprocess, needing guidance on template inheritance (extend vs include vs embed), or working with the Drupal attributes object.

## Decision

**Preprocess vs Twig:**

| Task | Preprocess Function | Twig Template | WHY |
|------|---------------------|---------------|-----|
| Data transformation | ✅ | ❌ | Complex logic doesn't belong in templates |
| Array manipulation | ✅ | ❌ | PHP is better at array operations |
| Database queries | ✅ | ❌ | Never query in templates |
| Conditional logic | ❌ | ✅ | Simple conditionals are fine in Twig |
| Loops | ❌ | ✅ | Twig is designed for iteration |
| Filters (t, url, date) | ❌ | ✅ | Twig filters optimize better than PHP |
| Adding CSS classes | ✅ | ✅ | Both work; preprocess for complex logic |
| Render arrays | ✅ | ❌ | Return render arrays, don't call drupal_render() |

**Template Inheritance:**

| Method | Use When | Can Modify Parent? |
|--------|----------|-------------------|
| `{% extends %}` | Base template with blocks | ✅ Override blocks |
| `{% include %}` | Drop in component/snippet | ❌ No |
| `{% embed %}` | Include + override blocks | ✅ Override blocks in embedded template |

## Pattern

**Preprocess Functions (`THEME_NAME.theme`):**

```php
<?php

/**
 * Implements hook_preprocess_node().
 */
function THEME_NAME_preprocess_node(&$variables) {
  $node = $variables['node'];

  // GOOD: Data transformation
  $variables['formatted_date'] = \Drupal::service('date.formatter')
    ->format($node->getCreatedTime(), 'custom', 'F j, Y');

  // GOOD: Complex conditional class logic
  $variables['attributes']['class'][] = 'node';
  $variables['attributes']['class'][] = 'node--type-' . $node->bundle();
  if (!$node->isPublished()) {
    $variables['attributes']['class'][] = 'node--unpublished';
  }

  // GOOD: Adding contextual information
  $variables['author_name'] = $node->getOwner()->getDisplayName();

  // GOOD: Preparing render arrays for template
  $variables['share_buttons'] = [
    '#theme' => 'share_buttons',
    '#node' => $node,
  ];

  // BAD: Don't render in preprocess
  // $variables['content'] = \Drupal::service('renderer')->render($content);
}
```

**Twig Templates:**

```twig
{# GOOD: Simple conditional rendering #}
{% if author_name %}
  <div class="node__author">{{ 'By @name'|t({'@name': author_name}) }}</div>
{% endif %}

{# GOOD: Using Twig filters #}
<time datetime="{{ node.created.value|date('c') }}">
  {{ formatted_date }}
</time>

{# GOOD: Looping through content #}
{% for item in content.field_tags %}
  <span class="tag">{{ item }}</span>
{% endfor %}

{# BAD: Don't do complex logic in Twig #}
{% set complex_calculation = some_value * 100 / total_value %}
{# This should be in preprocess #}
```

**Template Inheritance — {% extends %}:**

**Base template:**

```twig
{# templates/layout/page--base.html.twig #}
<div class="page-wrapper">
  <header class="page-header">
    {% block header %}
      {# Default header content #}
    {% endblock %}
  </header>

  <main class="page-content">
    {% block content %}
      {# Default content #}
    {% endblock %}
  </main>
</div>
```

**Child template:**

```twig
{# templates/layout/page--front.html.twig #}
{% extends "page--base.html.twig" %}

{% block header %}
  <div class="hero-section">
    {{ page.header }}
  </div>
{% endblock %}

{% block content %}
  {{ parent() }}  {# Keep parent content #}
  <div class="featured-content">...</div>
{% endblock %}
```

**Template Inheritance — {% include %}:**

```twig
{# Include share buttons component #}
{% include 'THEME_NAME:share-buttons' with {
  'url': url('entity.node.canonical', {'node': node.id}),
  'title': label,
} only %}

{# 'only' keyword = don't pass parent context #}
```

**Template Inheritance — {% embed %}:**

```twig
{# Embed Radix card and override blocks #}
{% embed 'radix:card' with {
  'card_title': node.label,
} %}
  {% block card_body %}
    {# Custom body content #}
    {{ content.body }}
  {% endblock %}

  {% block card_footer %}
    {# Custom footer #}
    <a href="{{ url }}">{{ 'Read more'|t }}</a>
  {% endblock %}
{% endembed %}
```

**Drupal Attributes Object:**

```twig
{# Attributes object can: #}
{# 1. Add classes #}
{%
  set classes = [
    'my-component',
    variant ? 'my-component--' ~ variant : '',
  ]
%}
<div {{ attributes.addClass(classes) }}>

{# 2. Remove classes #}
<div {{ attributes.removeClass('unwanted-class') }}>

{# 3. Set attributes #}
<div {{ attributes.setAttribute('data-id', node.id) }}>

{# 4. Remove attributes #}
<div {{ attributes.removeAttribute('style') }}>

{# 5. Check if class exists #}
{% if attributes.hasClass('featured') %}
  {# Do something #}
{% endif %}

{# 6. Get specific attribute #}
{% set id = attributes.id %}
```

**Performance:**

```twig
{# GOOD: Twig filters optimize better (lazy evaluation) #}
{{ 'Hello @name'|t({'@name': author}) }}

{# BAD: Don't call functions repeatedly in loops #}
{% for item in items %}
  {{ some_expensive_function(item) }}  {# Processed on every iteration #}
{% endfor %}

{# GOOD: Process once before loop (in preprocess) #}
{# Preprocess: $variables['processed_items'] = array_map(..., $items); #}
{% for item in processed_items %}
  {{ item }}
{% endfor %}
```

## Common Mistakes

- **Wrong**: Complex logic in Twig → **Right**: Data transformation in preprocess
- **Wrong**: Database queries in templates → **Right**: Always query in preprocess
- **Wrong**: Calling `drupal_render()` in preprocess → **Right**: Return render arrays
- **Wrong**: Using `{% extends %}` after other tags → **Right**: Must be first tag in template
- **Wrong**: Multiple `{% extends %}` → **Right**: Can only extend ONE parent
- **Wrong**: Not using `only` keyword with `{% include %}` → **Right**: Use `only` to prevent context pollution
- **Wrong**: Hardcoded classes in template → **Right**: Merge with attributes object
- **Wrong**: Not checking if attribute exists → **Right**: Use `attributes.hasClass()`
- **Wrong**: Processing expensive operations in loops → **Right**: Process once in preprocess
- **Wrong**: Using `|raw` filter carelessly → **Right**: Only when absolutely necessary (security risk)

## See Also

- [SDC Component Development](sdc-component-development.md)
- [SDC Component Best Practices](sdc-component-best-practices.md)
- [Templates Drupal Theme Layer](templates-drupal-theme-layer.md)
- Drupal Twig Documentation: https://www.drupal.org/docs/theming-drupal/twig-in-drupal
