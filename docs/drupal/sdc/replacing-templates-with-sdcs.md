---
description: Strategies for migrating Twig templates to SDC and overriding components
drupal_version: "11.x"
---

# Replacing Templates with SDCs

## When to Use

> Use this when migrating existing Twig templates to SDC, overriding contrib module/theme components, or implementing field formatters with components.

## Decision

| Method | Use Case | Restriction |
|--------|----------|-------------|
| `replaces` directive | Override existing component | Themes only, must have identical schema |
| Custom field formatter | Component-based field rendering | Requires custom PHP plugin |
| Include/embed in templates | Gradual migration | No restrictions |

## Pattern

**Theme Override with `replaces`:**
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

**Custom Field Formatter:**
```php
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

**Migration Path:**
1. Create SDC with equivalent structure
2. Update calling templates to use `include('provider:component')`
3. Test in development with schema validation enabled
4. For complete replacement, use `replaces` directive (themes only)

## Common Mistakes

- **Wrong**: Trying to override components from modules → **Right**: Only themes can use `replaces` directive
- **Wrong**: Changing schema when using `replaces` → **Right**: Replacement must be API-compatible (schema validation enforces this)

## See Also

- [SDC Architecture](sdc-architecture.md)
- [Component YAML Schema](component-yaml-schema.md)
- [UI Patterns Module](https://www.drupal.org/project/ui_patterns) - Component integration
