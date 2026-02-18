---
topic: drupal/twig
guide: attribute-system
---

## The Attribute System

### When to Use
When you need to add, remove, or modify HTML attributes in a template — particularly CSS classes, data attributes, ARIA attributes, and custom element attributes.

### Decision
| If you need... | Use... | Why |
|---|---|---|
| Add class to existing element | `{{ attributes.addClass('my-class') }}` | Merges with existing classes safely |
| Add conditional class | `attributes.addClass(condition ? 'class' : '')` | Empty strings are ignored |
| Set arbitrary attribute | `attributes.setAttribute('data-type', value)` | Chainable, safe |
| Remove a class | `attributes.removeClass('unwanted')` | Non-destructive removal |
| Check if class exists | `attributes.hasClass('some-class')` | Returns boolean |
| Remove entire attribute | `attributes.removeAttribute('id')` | Use carefully |
| Create new Attribute object | `create_attribute({'class': ['my-el']})` | For new elements |
| Separate class from other attrs | `{{ attributes\|without('class') }}` | Print class separately |

### Pattern

**Adding classes in templates:**
```twig
{# Standard pattern — chain methods, then print #}
<article{{ attributes.addClass('node', 'node--' ~ node.bundle) }}>

{# Conditional classes using Twig set #}
{% set classes = [
  'card',
  view_mode == 'teaser' ? 'card--teaser',
  node.isPromoted() ? 'card--featured',
] %}
<div{{ attributes.addClass(classes) }}>
```

**Creating new attribute objects for custom elements:**
```twig
{# create_attribute() for elements not managed by Drupal #}
<div{{ create_attribute({'class': ['my-wrapper', 'is-active'], 'aria-label': 'Navigation'|t}) }}>

{# Separating class from other attributes #}
<div class="hardcoded {{ attributes.class }}"{{ attributes|without('class') }}>
```

**Modifying attributes in preprocess (PHP side):**
```php
// In a preprocess function
$variables['attributes']['data-entity-id'] = $node->id();
$variables['attributes']['class'][] = 'js-animated';
// Or using the Attribute object if it exists
if ($variables['attributes'] instanceof Attribute) {
    $variables['attributes']->addClass('theme-' . $node->bundle());
}
```

### Attribute Object Methods Reference
| Method | Signature | Returns |
|---|---|---|
| `addClass` | `addClass(...$args)` | `$this` (chainable) |
| `removeClass` | `removeClass(...$args)` | `$this` (chainable) |
| `setAttribute` | `setAttribute($attribute, $value)` | `$this` (chainable) |
| `removeAttribute` | `removeAttribute(...$args)` | `$this` (chainable) |
| `hasAttribute` | `hasAttribute($name)` | `bool` |
| `hasClass` | `hasClass($class)` | `bool` |
| `offsetGet` | `['class']` | `AttributeArray` |

**Default attribute variables in templates:**
- `attributes` — main element wrapper
- `title_attributes` — title/label element
- `content_attributes` — content wrapper element
- `author_attributes` — author info element (node only)
- `title_prefix` / `title_suffix` — render arrays (not Attribute objects)

### BEM Pattern with Attributes
```twig
{# BEM block + modifier classes #}
{% set block_class = 'card' %}
{% set modifiers = [view_mode] %}
<div{{ attributes.addClass(block_class, modifiers|map(m => block_class ~ '--' ~ m)) }}>
  <div class="{{ block_class }}__body">
    {{ content }}
  </div>
</div>
```

### Common Mistakes
- Printing `{{ attributes.class }}` without the rest: `<div class="{{ attributes.class }}">` misses `id`, `data-*`, etc. Use `<div class="{{ attributes.class }}"{{ attributes|without('class') }}>`
- `attributes.addClass()` returns `$this` — you can chain but do not re-assign
- Setting `attributes['class'] = 'single-class'` directly in preprocess — use an array: `$variables['attributes']['class'][] = 'my-class'`
- Accessing `{{ attributes.class }}` when no class is set returns an empty string, not null — safe but print nothing useful

### See Also
- Preprocess functions for PHP-side attribute modification → [Preprocess Functions](preprocess-functions.md)
- Core source: `core/lib/Drupal/Core/Template/Attribute.php`
