---
description: Integrate a custom design system with Plus Suite — block types, sample values, promoted blocks, block properties, CSS, and where to put customizations
tldr: "Follow this guide when building Plus Suite for a branded site — custom block types, promoted block icons, sample content generators, and block properties that match your design system."
drupal_version: "11.x"
---

# Custom Design System Integration

## When to Use

> Follow this guide when building Plus Suite for a branded site — custom block types, promoted block icons, sample content generators, and block properties that match your design system.

## Decision

| Customization | Where | Why |
|---------------|-------|-----|
| Block content types | Module (config) | Portable across themes |
| Sample value generators | Module (plugins) | PHP code, not theme-layer |
| Block properties event subscriber | Module (services) | PHP code, not theme-layer |
| Promoted block icons | Theme (assets) | Design-specific |
| CSS overrides | Theme (library) | Design-specific |
| Custom layout plugins | Module (plugins) | Layout is structural |
| Custom tool plugins | Module (plugins) | PHP code |

## Pattern

**The complete integration stack:**
```
1. Block Content Types ──── Your design components
2. Field Sample Values ──── Branded placeholder content per component
3. Promoted Blocks ──────── Curated sidebar with custom icons
4. Block Properties ──────── Design-system options (variant, color, spacing)
5. Layout Plugins ─────────── Custom section layouts for your grid
6. CSS/JS Libraries ───────── Theme styles applied in Edit Mode
```

**Custom sample value generator:**
```php
/**
 * @SampleValueGenerator(
 *   id = "branded_headline",
 *   field_types = {"text", "string"},
 *   weight = 20,
 * )
 */
class BrandedHeadline extends SampleValueGeneratorBase {
  protected array $headlines = [
    'Transform Your Business Today',
    'Innovate Without Limits',
  ];
  public function generateSampleValue(FieldItemListInterface $field): void {
    $field->setValue(['value' => $this->headlines[array_rand($this->headlines)]]);
  }
}
```

**Promoted blocks with custom icons:**
```yaml
third_party_settings:
  lb_plus:
    promoted_blocks:
      - 'inline_block:hero'
      - 'inline_block:card'
    block_config:
      icon:
        'inline_block:hero': '/themes/custom/my_theme/assets/block-icons/hero.svg'
        'inline_block:card': '/themes/custom/my_theme/assets/block-icons/card.svg'
```

**Block properties for design options:**
```php
public function onBlockProperties(BlockPropertiesEvent $event): void {
  $event->addBlockProperty([
    '#type' => 'select',
    '#title' => t('Spacing'),
    '#options' => ['compact' => 'Compact', 'normal' => 'Normal', 'spacious' => 'Spacious'],
    '#default_value' => $config['spacing'] ?? 'normal',
    '#attributes' => ['data-auto-submit' => 'true'],
  ]);
}
```

**Edit+ handle types per field:**

| Field Type | Handle |
|------------|--------|
| Single text/heading | `form_item` |
| Media reference | `wrapper` |
| Entity reference | `wrapper` |
| Link field | `wrapper` |
| List/select field | `form_item` |

## Common Mistakes

- **Wrong**: Putting block property logic in theme files → **Right**: Use a companion module for PHP services
- **Wrong**: Creating sample value generators that depend on theme configuration → **Right**: Generators run in admin context; keep them self-contained
- **Wrong**: Skipping the promoted blocks configuration → **Right**: Curated promoted blocks are the primary UX improvement over standard LB

## See Also

- [Custom Block Types](custom-block-types.md)
- [Field Sample Value](field-sample-value.md)
- [Custom Layout Plugins](custom-layout-plugins.md)
- [End-to-End Component Creation](end-to-end-component.md)
