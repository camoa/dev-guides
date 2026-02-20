---
description: Strategies for implementing component variants using enums or separate components
drupal_version: "11.x"
---

# Component Variants

## When to Use

> Use this when you need multiple visual variations of a component, deciding between prop-based variants vs separate components, or implementing the new variants API (Drupal 11.1+).

## Decision

| Strategy | Use Case | Why |
|----------|----------|-----|
| Enum props | Minor variations (same structure/slots, different styling) | Single component, easier maintenance, design system consistency |
| Separate components | Major variations (fundamentally different structure/props/slots) | Different structures need separate components |
| Variants API (11.1+) | Named variants with titles/descriptions | Better admin UX, non-breaking API |

## Pattern

**Pattern 1: Enum Props (Recommended for Minor Variations):**
```yaml
props:
  type: object
  properties:
    color:
      type: string
      enum: [primary, secondary, success, danger, warning]
      default: primary
    size:
      type: string
      enum: [small, medium, large]
      default: medium
    outline:
      type: boolean
      default: false
```

**Pattern 2: Separate Components (for Major Variations):**
```
components/
├── card-basic/
│   ├── card-basic.component.yml
│   └── card-basic.twig
├── card-featured/
│   ├── card-featured.component.yml    # Different props/slots
│   └── card-featured.twig
└── card-product/
    ├── card-product.component.yml     # Different props/slots
    └── card-product.twig
```

**Pattern 3: Component Variants API (Drupal 11.1+):**
```yaml
name: 'Call to Action'
variants:
  default:
    title: 'Default CTA'
    description: 'Standard call-to-action style'
  hero:
    title: 'Hero CTA'
    description: 'Large hero section CTA'
  inline:
    title: 'Inline CTA'
    description: 'Compact inline CTA'
```

```php
// Using variants in render arrays
$build = [
  '#type' => 'component',
  '#component' => 'my_theme:cta',
  '#variant' => 'hero',
  '#props' => [...],
];
```

## Common Mistakes

- **Wrong**: Creating separate components for minor style variations → **Right**: Use enum props for variations that differ only in styling
- **Wrong**: Using props to handle fundamentally different structures → **Right**: Create separate components when structure differs significantly

## See Also

- Reference: `/themes/contrib/radix/components/button/button.component.yml`
- [Props vs Slots Decision Framework](props-vs-slots-decision-framework.md)
- [Component Variants in Core](https://www.thedroptimes.com/49944/drupal-core-single-directory-components-introduce-component-variants)
