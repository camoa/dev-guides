---
description: Component YAML schema definition for props, slots, and dependencies
drupal_version: "11.x"
---

# Component YAML Schema

## When to Use

> Use this when defining component metadata, specifying props and slots, or configuring library dependencies.

## Decision

| Field | Required | Purpose | When to Use |
|-------|----------|---------|-------------|
| `$schema` | Recommended | JSON Schema URL for IDE validation | Always (enables autocomplete and validation) |
| `name` | Yes | Human-readable name | Always |
| `status` | Yes | experimental \| stable \| deprecated \| obsolete | Always |
| `description` | No | Component purpose | Recommended |
| `props` | No | JSON Schema for typed data | For configuration values (strings, booleans, enums) |
| `slots` | No | Content insertion points | For renderable content areas |
| `libraryDependencies` | No | Simple dependency array | When component needs other libraries |
| `replaces` | No | Override directive (themes only) | To replace another component |

## Pattern

**Minimum Required:**
```yaml
$schema: https://git.drupalcode.org/project/drupal/-/raw/HEAD/core/assets/schemas/v1/metadata.schema.json
name: 'Component Name'
status: stable
```

**Props (typed, validated data):**
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
      enum: [primary, secondary, danger]
      default: primary
```

**Slots (unstructured content):**
```yaml
slots:
  content:
    title: 'Main Content'
    required: true
  header:
    title: 'Header Content'
    required: false
```

**Library Dependencies:**
```yaml
libraryDependencies:
  - core/drupal
  - core/once
  - my_theme/utilities
```

## Common Mistakes

- **Wrong**: Omitting `$schema` URL → **Right**: Always include schema for IDE validation and autocomplete
- **Wrong**: Using `type: array` for renderable content → **Right**: Use slots for render arrays, props for typed data
- **Wrong**: No prop validation → **Right**: Define complete JSON Schema with types, enums, defaults

## See Also

- Reference: `/core/assets/schemas/v1/metadata.schema.json` - Official JSON Schema
- Reference: `/core/modules/system/tests/modules/sdc_test/components/my-button/my-button.component.yml`
- Reference: `/themes/contrib/radix/components/button/button.component.yml`
- [Props vs Slots Decision Framework](props-vs-slots-decision-framework.md)
- [Official Component YAML Reference](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components/annotated-example-componentyml)
