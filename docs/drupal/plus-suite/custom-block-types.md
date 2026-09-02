---
description: Create Plus Suite-compatible block content types — BlockPropertiesEvent pattern, example blocks, and PlaceBlockEvent defaults
tldr: "Create custom block types for every design component. Use event subscribers to set placement defaults and add design options."
drupal_version: "11.x"
---

# Custom Block Types

## When to Use

> When creating block types that integrate with Plus Suite's inline editing, sample values, and block properties system.

## Example Blocks in Plus Suite

The recipe includes three example block sub-modules that demonstrate the pattern:

**Header Block** (`edit_plus_header_block`) — adds to `inline_block:header` blocks:

- **Alignment** select (left, center, right)
- **Title size** select (jumbo, large)
- **Link enabled** checkbox
- **URL** field (with path/URL validation)

Implementation: `Heading` event subscriber listens to `PlaceBlockEvent` and `BlockPropertiesEvent`.

**CTA Block** (`edit_plus_cta_block`) — sets `card_right` view mode and visible label display on placement.

Implementation: `CtaBlockProperties` event subscriber listens to `PlaceBlockEvent`.

**Teaser Block** (`edit_plus_teaser_block`) — same properties as Header (alignment, size, link).

Implementation: `Teaser` event subscriber.

## Pattern: Block Properties Event

Custom block properties (beyond field values) are added via the `BlockPropertiesEvent`:

```php
namespace Drupal\my_module\EventSubscriber;

use Drupal\edit_plus\Event\BlockPropertiesEvent;
use Drupal\lb_plus\Event\PlaceBlockEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class MyBlockProperties implements EventSubscriberInterface {

  public static function getSubscribedEvents(): array {
    return [
      PlaceBlockEvent::class => 'onPlaceBlock',
      BlockPropertiesEvent::class => 'onBlockProperties',
    ];
  }

  public function onPlaceBlock(PlaceBlockEvent $event): void {
    // Set defaults when block is first placed
    if ($event->getPluginId() === 'inline_block:my_block') {
      $event->getBlockContent()->set('field_layout', 'default');
    }
  }

  public function onBlockProperties(BlockPropertiesEvent $event): void {
    $block_content = $event->getBlockContent();
    if ($block_content->bundle() !== 'my_block') {
      return;
    }

    // Add custom property form elements
    $event->addBlockProperty([
      '#type' => 'select',
      '#title' => t('Background color'),
      '#options' => ['light' => 'Light', 'dark' => 'Dark'],
      '#default_value' => $event->getInlineBlockConfiguration()['background'] ?? 'light',
    ]);
  }
}
```

## Pattern: Creating a Plus Suite-Compatible Block Type

1. Create block_content type (Structure → Block Types)
2. Add fields (text, image, entity reference)
3. Configure Field Sample Value generators per field
4. Add Edit+ third-party settings (handle type per field)
5. Promote the block in LB+ Promoted Blocks
6. Optionally: create event subscriber for PlaceBlockEvent/BlockPropertiesEvent

## Decision: Block Type Design

| Need | Approach |
|---|---|
| Simple text + image | Standard block type with sample values |
| Configurable display options | Use BlockPropertiesEvent for extra settings |
| Complex nested content | Use layout_block type |
| Reusable component | Save to Section Library |

## Common Mistakes

- **Do not put business logic in block templates** — use event subscribers for block property management.
- **Do not create block types without configuring sample value generators** — empty blocks provide poor UX.

## See Also

- [Field Sample Value](field-sample-value.md)
- [Place Block & Promoted Blocks](place-block-promoted-blocks.md)
- [End-to-End Component Creation](end-to-end-component.md)
- [Events & Event Subscribers](events-event-subscribers.md)
