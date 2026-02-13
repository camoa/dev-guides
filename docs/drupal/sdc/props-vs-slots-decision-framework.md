---
description: Deciding when to use props (typed data) vs slots (renderable content) in component API design
drupal_version: "11.x"
---

# Props vs Slots Decision Framework

## When to Use

> Use this when designing a component API, deciding if something should be a prop or slot, or debugging schema validation errors.

## Decision: Props or Slots?

| Situation | Choose | Why |
|-----------|--------|-----|
| Structured and typed data (string, boolean, number, enum, object, array) | Props | Validates against JSON Schema, drives component logic |
| Data needs validation | Props | JSON Schema provides type safety and error messages |
| Scalar or simple objects | Props | Configuration values like `variant: 'primary'`, `disabled: true` |
| Unstructured renderables (HTML, render arrays, nested components) | Slots | Content type can't be known in advance |
| Content implements RenderableInterface, MarkupInterface, or Stringable | Slots | No validation needed, only existence check |
| Main content area, header region, action buttons area | Slots | Arbitrary renderable content |

## Pattern

Props for configuration (strictly typed):

```yaml
props:
  type: object
  properties:
    variant:
      type: string
      enum: [primary, secondary, danger]
      default: primary
    size:
      type: string
      enum: [small, medium, large]
      default: medium
    disabled:
      type: boolean
      default: false
```

Slots for content (unstructured renderables):

```yaml
slots:
  content:
    title: 'Content'
    required: true
  image:
    title: 'Image'
    required: false
  meta:
    title: 'Metadata'
    required: false
```

Mixed props and slots (most components):

```yaml
# Alert component example
props:
  type: object
  properties:
    variant:
      type: string
      enum: [success, warning, danger, info]
    dismissible:
      type: boolean
      default: false

slots:
  heading:
    title: 'Alert Heading'
    required: false
  message:
    title: 'Alert Message'
    required: true
```

## Common Mistakes

- **Wrong**: Using props for HTML/renderable content → **Right**: Props must validate against JSON Schema. HTML/render arrays don't have predictable schemas. Use slots instead.
- **Wrong**: Using slots for simple text/boolean/enum values → **Right**: Slots bypass validation. Simple values should be validated props for better error messages and type safety.
- **Wrong**: Applying logic to slot content in templates beyond existence checks → **Right**: Slots contain arbitrary renderables. Can't reliably check their properties. Only check `if slot` or `slot|length`.

## See Also

- Reference: `/themes/contrib/radix/components/button/button.component.yml`
- Reference: `/core/themes/olivero/components/teaser/teaser.component.yml`
- [Component YAML Schema](component-yaml-schema.md)
- [Twig Templates in SDCs](twig-templates-in-sdcs.md)
- [Props and Slots Documentation](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components/what-are-props-and-slots-in-drupal-sdc-theming)
