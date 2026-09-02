---
description: Integrate a custom design system with Plus Suite — block types, sample values, promoted blocks, block properties, CSS, and where to put customizations
tldr: "Follow this guide when building Plus Suite for a branded site — custom block types, promoted block icons, sample content generators, and block properties that match your design system."
drupal_version: "11.x"
---

# Custom Design System Integration

## When to Use

> When you need to make Plus Suite use your own design system — custom block types with branded styling, custom promoted block icons, custom sample content generators, and custom sidebar elements that match your design language.

## The Complete Integration Stack

To make Plus Suite "yours", you need to customize at these layers:

```
1. Block Content Types ──── Your design components (Hero, Card, Testimonial, etc.)
2. Field Sample Values ──── Branded placeholder content per component
3. Promoted Blocks ──────── Curated sidebar with custom icons per component
4. Block Properties ──────── Design-system-specific options (variant, color scheme, spacing)
5. Layout Plugins ─────────── Custom section layouts matching your grid system
6. CSS/JS Libraries ───────── Your theme's styles applied in Edit Mode
7. Tool Plugins ──────────── Optional custom tools for design-specific actions
```

## Step 1: Create Design-System Block Types

Create block_content types for each component in your design system:

```bash
# Via Drush or admin UI
drush generate block-content-type
```

Example: a "Hero" block type with fields:

- `field_heading` (text) — headline
- `field_subheading` (text_long) — subheading text
- `field_media` (entity_reference to media) — background image
- `field_cta_text` (text) — button label
- `field_cta_url` (link) — button URL
- `field_variant` (list_string) — design variant (light, dark, gradient)

## Step 2: Configure Sample Values Per Component

For each field, set a sample value generator that produces branded content:

```php
// Custom sample value generator for branded headlines
namespace Drupal\my_theme\Plugin\Field\SampleValueGenerator;

use Drupal\field_sample_value\Annotation\SampleValueGenerator;
use Drupal\field_sample_value\SampleValueGeneratorBase;
use Drupal\Core\Field\FieldItemListInterface;

/**
 * @SampleValueGenerator(
 *   id = "branded_headline",
 *   title = @Translation("Branded Headline"),
 *   field_types = {"text", "string"},
 *   weight = 20,
 * )
 */
class BrandedHeadline extends SampleValueGeneratorBase {

  protected array $headlines = [
    'Transform Your Business Today',
    'Innovate Without Limits',
    'Built for the Future',
    'Your Success, Our Mission',
  ];

  public function generateSampleValue(FieldItemListInterface $field): void {
    $field->setValue([
      'value' => $this->headlines[array_rand($this->headlines)],
    ]);
  }
}
```

Configure via field settings UI or recipe config actions:

```yaml
field.field.block_content.hero.field_heading:
  setThirdPartySettings:
    - module: field_sample_value
      key: id
      value: branded_headline
```

## Step 3: Configure Promoted Blocks with Custom Icons

Create SVG icons for each design component (40x40px recommended):

```
my_theme/
  assets/
    block-icons/
      hero.svg
      card.svg
      testimonial.svg
      cta-banner.svg
      feature-grid.svg
```

Configure on the entity view display:

```yaml
third_party_settings:
  lb_plus:
    promoted_blocks:
      - 'inline_block:hero'
      - 'inline_block:card'
      - 'inline_block:testimonial'
      - 'inline_block:cta_banner'
      - 'inline_block:feature_grid'
    block_config:
      icon:
        'inline_block:hero': '/themes/custom/my_theme/assets/block-icons/hero.svg'
        'inline_block:card': '/themes/custom/my_theme/assets/block-icons/card.svg'
        'inline_block:testimonial': '/themes/custom/my_theme/assets/block-icons/testimonial.svg'
```

## Step 4: Add Design-System Block Properties

Create an event subscriber module for your design system options:

```php
namespace Drupal\my_theme_plus\EventSubscriber;

use Drupal\edit_plus\Event\BlockPropertiesEvent;
use Drupal\lb_plus\Event\PlaceBlockEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class DesignSystemBlockProperties implements EventSubscriberInterface {

  public static function getSubscribedEvents(): array {
    return [
      PlaceBlockEvent::class => 'onPlaceBlock',
      BlockPropertiesEvent::class => 'onBlockProperties',
    ];
  }

  public function onPlaceBlock(PlaceBlockEvent $event): void {
    $block = $event->getBlockContent();
    if (!$block) {
      return;
    }

    // Set default variant for hero blocks.
    if ($block->bundle() === 'hero') {
      $block->set('field_variant', 'light');
    }

    // Set default spacing for all design system blocks.
    $design_bundles = ['hero', 'card', 'testimonial', 'cta_banner'];
    if (in_array($block->bundle(), $design_bundles)) {
      // Store spacing in block config (not fields).
      $config = $event->getConfiguration();
      $config['spacing'] = 'normal';
      $event->setConfiguration($config);
    }
  }

  public function onBlockProperties(BlockPropertiesEvent $event): void {
    $block = $event->getBlockContent();
    if (!$block) {
      return;
    }

    $design_bundles = ['hero', 'card', 'testimonial', 'cta_banner', 'feature_grid'];
    if (!in_array($block->bundle(), $design_bundles)) {
      return;
    }

    $config = $event->getInlineBlockConfiguration();

    // Add spacing control (applies to all design system blocks).
    $event->addBlockProperty([
      '#type' => 'select',
      '#title' => t('Spacing'),
      '#options' => [
        'compact' => t('Compact'),
        'normal' => t('Normal'),
        'spacious' => t('Spacious'),
      ],
      '#default_value' => $config['spacing'] ?? 'normal',
      '#attributes' => [
        'data-auto-submit' => 'true',
      ],
    ]);

    // Add color scheme for hero blocks.
    if ($block->bundle() === 'hero') {
      $event->addBlockProperty([
        '#type' => 'select',
        '#title' => t('Color Scheme'),
        '#options' => [
          'brand-primary' => t('Brand Primary'),
          'brand-secondary' => t('Brand Secondary'),
          'neutral' => t('Neutral'),
          'dark' => t('Dark'),
        ],
        '#default_value' => $config['color_scheme'] ?? 'brand-primary',
        '#attributes' => [
          'data-auto-submit' => 'true',
        ],
      ]);
    }
  }
}
```

## Step 5: Apply Design System CSS in Edit Mode

Your theme must load styles that work in both Edit Mode and published view:

```yaml
# my_theme.libraries.yml
design-system:
  css:
    theme:
      css/design-system.css: {}
```

```php
// In your .theme file
function my_theme_page_attachments_alter(array &$attachments) {
  // Ensure design system CSS loads in Edit Mode.
  $attachments['#attached']['library'][] = 'my_theme/design-system';
}
```

## Step 6: Configure Field Handle Types

For each field on your design-system blocks, set the Edit+ handle type:

| Field Type | Handle | Reason |
|---|---|---|
| Single text/heading | `form_item` | Replace just the text element |
| Media reference | `wrapper` | Replace entire media widget |
| Entity reference | `wrapper` | Replace entire reference widget |
| Link field | `wrapper` | URL + title need wrapper |
| List/select field | `form_item` | Replace the select element |

## Decision: Module vs Theme for Customizations

| Customization | Where | Why |
|---|---|---|
| Block content types | Module (config) | Portable across themes |
| Sample value generators | Module (plugins) | PHP code, not theme-layer |
| Block properties event subscriber | Module (services) | PHP code, not theme-layer |
| Promoted block icons | Theme (assets) | Design-specific |
| CSS overrides | Theme (library) | Design-specific |
| Custom layout plugins | Module (plugins) | Layout is structural |
| Custom tool plugins | Module (plugins) | PHP code |

## Common Mistakes

- **Do not put block property logic in theme files** — use a companion module.
- **Do not create sample value generators that depend on theme configuration** — they run in admin context too.
- **Do not skip the promoted blocks configuration** — it's the primary UX improvement over standard LB.

## See Also

- [Custom Block Types](custom-block-types.md)
- [Field Sample Value](field-sample-value.md)
- [Custom Layout Plugins](custom-layout-plugins.md)
- [End-to-End Component Creation](end-to-end-component.md)
