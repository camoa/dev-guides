---
description: Implementing component variations using enum props, separate components, or the variants API
drupal_version: "11.x"
---

# Component Variants

## When to Use

> Use this when you need multiple visual variations of a component, deciding between prop-based variants vs separate components, or implementing the new variants API (Drupal 11.1+).

## Decision: Variant Strategy

| Situation | Choose | Why |
|-----------|--------|-----|
| Variations share same structure/slots, differ only in styling/behavior | Enum Props | Single component handles all variations via props, easier to maintain |
| Variations have fundamentally different structure/props/slots | Separate Components | Different structures require separate components |
| Need named variants with titles/descriptions (Drupal 11.1+) | Component Variants API | Non-breaking API for variant metadata |

## Pattern

Pattern 1: Enum Props (recommended for minor variations):

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

Pattern 2: Separate Components (for major variations):

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

Pattern 3: Component Variants API (Drupal 11.1+):

```yaml
# Component with variants
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

- **Wrong**: Creating separate components for minor style variations → **Right**: Duplicates structure and maintenance. Use enum props for variations that differ only in styling.
- **Wrong**: Using props to handle fundamentally different structures → **Right**: Leads to complex Twig conditionals. Create separate components when structure differs significantly.

## See Also

- Reference: `/themes/contrib/radix/components/button/button.component.yml`
- [Props vs Slots Decision Framework](props-vs-slots-decision-framework.md)
- [Component Variants in Core](https://www.thedroptimes.com/49944/drupal-core-single-directory-components-introduce-component-variants)
- [Component Variants Issue](https://www.drupal.org/project/drupal/issues/3514072)
