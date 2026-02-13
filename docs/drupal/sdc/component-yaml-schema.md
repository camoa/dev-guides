---
description: Defining component metadata, props, slots, and library dependencies in YAML schema
drupal_version: "11.x"
---

# Component YAML Schema

## When to Use

> Use this when defining component metadata, specifying props and slots, or configuring library dependencies.

## Decision: Schema Definition Requirements

| Field | Required | Purpose |
|-------|----------|---------|
| `$schema` | Recommended | JSON Schema URL for IDE validation |
| `name` | Required | Human-readable component name |
| `status` | Required | experimental, stable, deprecated, obsolete |
| `description` | Optional | Component purpose |
| `group` | Optional | Organizational category |
| `replaces` | Optional | Override directive (themes only, must match schemas) |
| `props` | Optional | JSON Schema for typed data |
| `slots` | Optional | Content insertion points |
| `libraryDependencies` | Optional | Simple dependency array |
| `libraryOverrides` | Optional | Advanced library configuration |

## Pattern

Minimum required schema:

```yaml
$schema: https://git.drupalcode.org/project/drupal/-/raw/HEAD/core/assets/schemas/v1/metadata.schema.json
name: 'Component Name'
status: stable
```

Props definition (strictly typed, validated data):

```yaml
props:
  type: object
  required:
    - text
  properties:
    text:
      type: string
      title: 'Button Text'
      minLength: 2
    variant:
      type: string
      title: 'Visual Variant'
      enum: [primary, secondary, danger]
      default: primary
    disabled:
      type: boolean
      title: 'Disabled State'
      default: false
```

Slots definition (unstructured content areas):

```yaml
slots:
  content:
    title: 'Main Content'
    required: true
    description: 'Primary content area'
  header:
    title: 'Header Content'
    required: false
    description: 'Optional header region'
```

Library dependencies:

```yaml
libraryDependencies:
  - core/drupal
  - core/once
  - my_theme/utilities

libraryOverrides:
  js:
    custom.js:
      attributes: { defer: true }
      preprocess: false
  dependencies:
    - core/jquery
```

## Common Mistakes

- **Wrong**: Not including `$schema` URL → **Right**: Without schema URL, IDEs can't provide validation/autocomplete, and developers lose development-time error checking.
- **Wrong**: Using `type: array` for `card_title_prefix` when it should be a slot → **Right**: Arrays of renderable content should be slots, not props. Props are for typed scalar/object data that validates against JSON Schema.

## See Also

- Reference: `/core/assets/schemas/v1/metadata.schema.json` - Official JSON Schema
- Reference: `/core/modules/system/tests/modules/sdc_test/components/my-button/my-button.component.yml`
- Reference: `/core/themes/olivero/components/teaser/teaser.component.yml`
- [Props vs Slots Decision Framework](props-vs-slots-decision-framework.md)
- [Component YAML Reference](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components/annotated-example-componentyml)
