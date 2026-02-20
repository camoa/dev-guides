---
description: Map design tokens to Drupal SDC component props
---

# Drupal SDC Token Integration

## When to Use

> Use this when mapping design tokens to Drupal Single Directory Component (SDC) props so component consumers can select token-based values.

## Decision

| Approach | When to Use | Example |
|---|---|---|
| Semantic enum props | Component consumers choose by intent | color_variant: [primary, secondary, accent] |
| Direct CSS variable access | Component CSS references tokens | var(--color-primary) |
| Utility class mapping | Twig maps prop to classes | bg-{{ color_variant }} |
| Token value passthrough | Allow any token value | Pass oklch() string directly |

## Pattern

**SDC Prop Schema with Token Values**

```yaml
# components/card/card.component.yml
name: Card
props:
  type: object
  properties:
    color_variant:
      type: string
      title: Color Variant
      enum: [primary, secondary, accent, neutral]
      default: primary
    radius:
      type: string
      title: Border Radius
      enum: [sm, md, lg]
      default: md
```

**Twig Template Using Tokens**

```twig
{# components/card/card.html.twig #}
{% set color_class = 'bg-' ~ color_variant ~ ' text-' ~ color_variant ~ '-content' %}
<div class="card {{ color_class }} rounded-{{ radius }}">
  {{ content }}
</div>
```

**CSS Variable Access in SDC**

```css
/* components/card/card.pcss */
.card {
  background-color: var(--color-primary);
  border-radius: var(--radius-box);
  border: var(--border) solid var(--color-base-300);
}
```

## Common Mistakes

- **Wrong**: Hardcoding color values in SDC CSS. **Right**: Reference DaisyUI CSS variables for theme switching.
- **Wrong**: Exposing raw CSS variable names as SDC props. **Right**: Use semantic enum values (primary, secondary) and map to classes in the template.

## See Also

- [DaisyUI CSS Variable Reference](daisyui-css-variable-reference.md)
- [Token Consumption Patterns](token-consumption-patterns.md)
- Reference: https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components
