---
description: "Enum props vs separate components vs the Component Variants API (11.2+), and exactly what variants: does at runtime"
tldr: "The Component Variants API landed in Drupal 11.2, not 11.1 — variants: is silently ignored on 11.1 and earlier. #variant only copies into $props['variant'] and adds a data-component-variant attribute; it never declares or restricts a variant prop, so declare variant as an enum prop too if you want it validated."
drupal_version: "11.x"
---

# Component Variants

## When to Use

> - You need multiple visual variations of a component
> - You're deciding between prop-based variants vs separate components
> - You're implementing the variants API (Drupal 11.2+)

## Decision

| Situation | Choose | Why |
|---|---|---|
| Variations share structure/slots, differ only in styling/behavior | Enum props | Single component handles all variations; easier to maintain, better for design-system consistency |
| Variations have fundamentally different structure/props/slots | Separate components | Trying to handle via props leads to complex conditionals and hard-to-maintain templates |
| You want named, titled/described variants surfaced to component pickers (Drupal 11.2+) | Component Variants API (`variants:`) | Metadata layer on top of an enum prop — see below for what it actually does |

**Component Variants API version note.** `variants` is absent from `metadata.schema.json` on 11.0.x and 11.1.x and present from 11.2.x; `ComponentMetadata::$variants` and `ComponentElement`'s `#variant` land in the same release. **On 11.1 or earlier a `variants:` block is accepted without error and does nothing**, because neither schema file sets `additionalProperties: false` at the top level.

**What `variants:` actually does.** Very little, and knowing the boundary keeps you from over-trusting it:

- `#variant` is copied into `$props['variant']` unless the caller already set a `variant` prop (`ComponentElement.php:57-59`). From `{% embed %}` / `include()` you just pass `variant: 'hero'` yourself; there is no separate mechanism.
- Core adds `data-component-variant="hero"` to the component's `attributes` object (`ComponentsTwigExtension.php:81-83`), and prints the variant in the HTML debug comment when Twig debug is on.
- **`variants:` does not declare a `variant` prop, and does not restrict the value.** `parseSchemaInfo()` never touches it. A variant name absent from the `variants:` map is passed straight through.

So `variants:` is metadata for component pickers and for humans. **The styling still comes from your Twig and CSS reading the `variant` variable**, and if you want the value validated you must also declare `variant` as an `enum` prop. Declaring both is the usual choice.

## Pattern

**Pattern 1: Enum Props (Recommended for Minor Variations)**

Use when variations share same structure/slots, differ only in styling/behavior.

Reference: `/themes/contrib/radix/components/button/button.component.yml`

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

**WHY:** Single component handles all variations via props. Easier to maintain, better for design system consistency.

**Pattern 2: Separate Components (for Major Variations)**

Use when variations have fundamentally different structure/props/slots.

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

**WHY:** Different structures require separate components. Trying to handle via props leads to complex conditionals and hard-to-maintain templates.

**Pattern 3: Component Variants API (Drupal 11.2+)**

Non-breaking API for named variants with titles/descriptions.

Reference: [Component Variants Issue](https://www.drupal.org/project/drupal/issues/3514072)

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

**Common Mistake:** Creating separate components for minor style variations.
**WHY:** Duplicates structure and maintenance. Use enum props for variations that differ only in styling.

**Common Mistake:** Using props to handle fundamentally different structures.
**WHY:** Leads to complex Twig conditionals. Create separate components when structure differs significantly.

- **Shipping a `variants:` block targeting Drupal 11.1 or earlier** — `variants` is absent from `metadata.schema.json` on 11.0.x and 11.1.x; `ComponentMetadata::$variants` and `ComponentElement`'s `#variant` land only from 11.2.x. On 11.1 or earlier the block is accepted without error and does nothing.
- **Relying on `variants:` to restrict which variant values are accepted** — `variants:` does not declare a `variant` prop and does not restrict the value; `parseSchemaInfo()` never touches it, so a variant name absent from the `variants:` map is passed straight through. Declare `variant` as an `enum` prop as well if you need the value validated.

## See Also

- [Props vs Slots Decision Framework](props-vs-slots-decision-framework.md)
- [Component Variants in Core](https://www.thedroptimes.com/49944/drupal-core-single-directory-components-introduce-component-variants)
