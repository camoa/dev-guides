---
description: Create Plus Suite-compatible block content types — BlockPropertiesEvent pattern, example blocks, and PlaceBlockEvent defaults
drupal_version: "11.x"
---

# Custom Block Types

## When to Use

> Create custom block types for every design component. Use event subscribers to set placement defaults and add design options. Configure sample values on every field.

## Decision

| Need | Approach |
|------|----------|
| Simple text + image | Standard block type with sample values |
| Configurable display options | `BlockPropertiesEvent` for extra settings |
| Complex nested content | `layout_block` type |
| Reusable component | Save to Section Library |

## Pattern

**Creating a Plus Suite-compatible block type:**
1. Create block_content type (Structure → Block Types)
2. Add fields (text, image, entity reference)
3. Configure Field Sample Value generators per field
4. Set Edit+ third-party settings (handle type per field)
5. Promote the block in LB+ Promoted Blocks
6. Create event subscriber for `PlaceBlockEvent`/`BlockPropertiesEvent`

**Block Properties event pattern:**

```php
class MyBlockProperties implements EventSubscriberInterface {

  public static function getSubscribedEvents(): array {
    return [
      PlaceBlockEvent::class => 'onPlaceBlock',
      BlockPropertiesEvent::class => 'onBlockProperties',
    ];
  }

  public function onPlaceBlock(PlaceBlockEvent $event): void {
    if ($event->getPluginId() === 'inline_block:my_block') {
      // Set defaults on first placement.
      $event->getBlockContent()->set('field_layout', 'default');
    }
  }

  public function onBlockProperties(BlockPropertiesEvent $event): void {
    $block_content = $event->getBlockContent();
    if ($block_content->bundle() !== 'my_block') {
      return;
    }
    $event->addBlockProperty([
      '#type' => 'select',
      '#title' => t('Background color'),
      '#options' => ['light' => 'Light', 'dark' => 'Dark'],
      '#default_value' => $event->getInlineBlockConfiguration()['background'] ?? 'light',
      '#attributes' => ['data-auto-submit' => 'true'],
    ]);
  }
}
```

**Example block sub-modules** (included in recipe):
- `edit_plus_header_block` — alignment, title size, link enabled, URL
- `edit_plus_cta_block` — sets card_right view mode on placement
- `edit_plus_teaser_block` — same properties as header block

## Common Mistakes

- **Wrong**: Putting business logic in block templates → **Right**: Use event subscribers for block property management
- **Wrong**: Creating block types without sample value generators → **Right**: Empty blocks on placement provide poor UX and defeat Plus Suite's purpose
- **Wrong**: Adding block properties without `data-auto-submit: true` → **Right**: Users expect instant preview when changing design options

## See Also

- [Field Sample Value](field-sample-value.md)
- [Place Block & Promoted Blocks](place-block-promoted-blocks.md)
- [End-to-End Component Creation](end-to-end-component.md)
- [Events & Event Subscribers](events-event-subscribers.md)
