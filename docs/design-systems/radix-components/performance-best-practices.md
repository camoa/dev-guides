---
description: Optimizing front-end performance when building/overriding components
---

# Performance Best Practices

## When to Use

> Optimizing front-end performance when building/overriding components.

## Best Practices

| Practice | Implementation | Why |
|----------|----------------|-----|
| SDC auto-loading | Place CSS/JS with `.component.yml` | Assets load only when component renders |
| Bootstrap utilities | Use `*_utility_classes` props | Reuses loaded CSS; better cache |
| Lazy load images | `loading="lazy"` attribute | Defers off-screen images |
| Minimize overrides | Only override modified templates | Fewer files, easier upgrades |
| Responsive images | Use Drupal image styles | Smaller files, automatic optimization |

## Pattern

```twig
{# GOOD #}
{%
  include 'radix:card' with {
    card_utility_classes: ['shadow-sm', 'mb-4']
  }
%}

{# BAD: Custom wrapper forces extra CSS #}
<div class="custom-wrapper">
  {% include 'radix:card' %}
</div>
```

## See Also

- Reference: https://web.dev/fast/
