---
description: Migrating traditional Twig templates to SDC with theme overrides and field formatters
drupal_version: "11.x"
---

# Replacing Templates with SDCs

## When to Use

> Use this when migrating existing Twig templates to SDC, overriding contrib module/theme components, or implementing field formatters with components.

## Decision: Template Replacement Strategy

| Situation | Pattern | Constraint |
|-----------|---------|------------|
| Override theme/module component | `replaces` directive in theme | Must have identical props/slots schemas |
| Custom field formatter | ComponentFieldFormatter class | Use render arrays with `#type => 'component'` |
| Migrate traditional template | Create SDC, update includes | Test with schema validation enabled |

**CRITICAL**: Only themes can use `replaces` directive. Modules cannot override components.

## Pattern

Theme override with `replaces` (identical schema required):

```yaml
# themes/my_theme/components/enhanced-button/enhanced-button.component.yml
$schema: https://git.drupalcode.org/project/drupal/-/raw/HEAD/core/assets/schemas/v1/metadata.schema.json
name: 'Enhanced Button'
replaces: 'radix:button'

# MUST match radix:button schema exactly
props:
  type: object
  properties:
    # ... identical schema ...

slots:
  # ... identical slots ...
```

**WHY identical schemas**: Ensures components are drop-in replacements. Calling code expects same API.

Custom field formatter:

```php
// Custom field formatter using components
class ComponentFieldFormatter extends FormatterBase {

  public function viewElements(FieldItemListInterface $items, $langcode) {
    $elements = [];

    foreach ($items as $delta => $item) {
      $elements[$delta] = [
        '#type' => 'component',
        '#component' => 'my_theme:field-card',
        '#props' => [
          'title' => $item->title,
          'variant' => $this->getSetting('variant'),
        ],
        '#slots' => [
          'content' => [
            '#markup' => $item->value,
          ],
        ],
      ];
    }

    return $elements;
  }
}
```

Migration path from traditional templates:

1. Create SDC with equivalent structure
2. Update calling templates to use `include('provider:component')`
3. Test in development with schema validation enabled
4. For complete replacement, use `replaces` directive (themes only)

## Common Mistakes

- **Wrong**: Trying to override components from modules → **Right**: Only themes can use `replaces` directive. Modules cannot override components.
- **Wrong**: Changing schema when using `replaces` → **Right**: Replacement must be API-compatible. Schema validation enforces this in development.

## See Also

- [SDC Architecture](sdc-architecture.md)
- [Component YAML Schema](component-yaml-schema.md)
- [UI Patterns Module](https://www.drupal.org/project/ui_patterns) - Component integration
