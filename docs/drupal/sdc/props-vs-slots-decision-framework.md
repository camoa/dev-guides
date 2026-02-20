---
description: Decision framework for choosing between props and slots in component design
drupal_version: "11.x"
---

# Props vs Slots Decision Framework

## When to Use

> Use this when designing a component API, deciding if something should be a prop or slot, or debugging schema validation errors.

## Decision

| Use Props When | Use Slots When |
|----------------|----------------|
| Data is structured and typed (string, boolean, number, enum, object, array) | Content is unstructured renderables (HTML, Drupal render arrays, nested components) |
| Data needs validation against JSON Schema | Content type cannot be known in advance |
| Data drives component logic (variants, states, configuration) | Content implements RenderableInterface, MarkupInterface, or Stringable |
| Data is scalar or simple objects | No validation needed, only existence check |
| Example: `variant: 'primary'`, `disabled: true` | Example: main content area, header region, action buttons area |

## Pattern

**Props for Configuration:**
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

**Slots for Content:**
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

**Mixed Props and Slots:**
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

- **Wrong**: Using props for HTML/renderable content → **Right**: Use slots (props must validate against JSON Schema)
- **Wrong**: Using slots for simple text/boolean/enum values → **Right**: Use validated props for type safety
- **Wrong**: Applying logic to slot content beyond existence checks → **Right**: Only check `if slot` or `slot|length`

## See Also

- Reference: `/themes/contrib/radix/components/button/button.component.yml` - Props example
- Reference: `/core/themes/olivero/components/teaser/teaser.component.yml` - Slots example
- [Component YAML Schema](component-yaml-schema.md)
- [Twig Templates in SDCs](twig-templates-in-sdcs.md)
- [Official Props and Slots Documentation](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components/what-are-props-and-slots-in-drupal-sdc-theming)
