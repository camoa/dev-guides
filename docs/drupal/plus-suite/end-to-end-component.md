---
description: End-to-end component creation in Plus Suite — complete 9-step walkthrough creating a Testimonial block with all features integrated
drupal_version: "11.x"
---

# End-to-End Component Creation

## When to Use

> Follow this walkthrough when creating any new Plus Suite component from scratch. Use the checklist at the end to verify completeness.

## Decision

| Feature | Required? | Effort |
|---------|-----------|--------|
| Block content type + fields | Yes | Low |
| Sample value generators | Yes (for good UX) | Low |
| Promoted block + icon | Recommended | Low |
| Block properties | Optional | Medium |
| Custom template | Recommended | Low |
| Custom sample value plugin | Optional (branded content) | Medium |
| Layout plugin (for sections) | Optional | Medium |
| Custom tool plugin | Rare | High |

## Pattern

**Component checklist** — verify all before shipping:

- [ ] Block content type created with appropriate fields
- [ ] Sample value generators configured for all fields
- [ ] Block promoted with custom SVG icon (40x40px)
- [ ] Event subscriber for `PlaceBlockEvent` (defaults) and `BlockPropertiesEvent` (design options)
- [ ] Edit+ handle types configured per field
- [ ] Block template created with design variant support
- [ ] CSS styles cover all design variants
- [ ] Inline editing works for all editable fields
- [ ] Sample content appears on first placement
- [ ] Design options update preview immediately (`data-auto-submit`)

**Module structure for a companion module:**

```yaml
# my_theme_plus.services.yml
services:
  my_theme_plus.testimonial_properties:
    class: Drupal\my_theme_plus\EventSubscriber\TestimonialProperties
    tags:
      - { name: event_subscriber }
```

**Event subscriber (condensed):**
```php
class TestimonialProperties implements EventSubscriberInterface {

  public static function getSubscribedEvents(): array {
    return [
      PlaceBlockEvent::class => 'onPlaceBlock',
      BlockPropertiesEvent::class => 'onBlockProperties',
    ];
  }

  public function onPlaceBlock(PlaceBlockEvent $event): void {
    $block = $event->getBlockContent();
    if (!$block || $block->bundle() !== 'testimonial') return;
    $block->set('field_rating', 5);
  }

  public function onBlockProperties(BlockPropertiesEvent $event): void {
    $block = $event->getBlockContent();
    if (!$block || $block->bundle() !== 'testimonial') return;
    $event->addBlockProperty([
      '#type' => 'select',
      '#title' => t('Style'),
      '#options' => ['card' => 'Card', 'quote' => 'Large Quote'],
      '#default_value' => $event->getInlineBlockConfiguration()['style'] ?? 'card',
      '#attributes' => ['data-auto-submit' => 'true'],
    ]);
  }
}
```

**Block template using configuration:**
```twig
{# block--inline-block--testimonial.html.twig #}
{% set style = configuration.testimonial_style|default('card') %}
<div{{ attributes.addClass('testimonial', 'testimonial--' ~ style) }}>
  <blockquote class="testimonial__quote">{{ content.field_quote }}</blockquote>
  <cite class="testimonial__author">{{ content.field_author }}</cite>
</div>
```

## Common Mistakes

- **Wrong**: Skipping sample value generators → **Right**: Empty blocks on placement defeat the purpose of Plus Suite's "Drag. Drop. Done." philosophy
- **Wrong**: Block properties without `data-auto-submit` → **Right**: Users expect instant preview; manual save creates poor UX
- **Wrong**: Forgetting to test inline editing on every field → **Right**: Handle type mismatches cause JS to target wrong elements

## See Also

- [Custom Block Types](custom-block-types.md)
- [Field Sample Value](field-sample-value.md)
- [Custom Design System Integration](custom-design-system.md)
- [Custom Layout Plugins](custom-layout-plugins.md)
