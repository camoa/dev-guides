---
description: Work with BlockContent entities — load, create, update, and render fieldable content blocks
drupal_version: "11.x"
---

# Content Block Entities

## When to Use

> Use when working programmatically with instances of block content (content entities created from block types). Distinct from Block config entities — `BlockContent` is the content; `Block` is the placement.

## Decision

| At this step... | If... | Then... |
|-----------------|-------|---------|
| Step 2 (create) | Block appears on one page only | Use non-reusable (inline block) |
| Step 2 (create) | Block appears on multiple pages | Use reusable block |
| Step 3 (load) | Loading many blocks | Use `loadMultiple()` for efficiency |
| Step 4 (update) | Changing reusable block | Understand it updates everywhere it's placed |
| Step 5 (access) | Field might be empty | Check `->isEmpty()` before accessing `->value` |

## Pattern

**Reusable vs non-reusable:**

```php
// Reusable block (appears in block library)
$block = BlockContent::create([
  'type' => 'basic',
  'info' => 'About Us',
  'reusable' => TRUE, // Can be placed multiple times
]);

// Non-reusable block (Layout Builder inline block)
$block = BlockContent::create([
  'type' => 'basic',
  'info' => 'Inline content',
  'reusable' => FALSE, // Owned by specific layout
]);
```

**Working with block content:**

```php
// Load and render
$block = BlockContent::load(1);
$view_builder = \Drupal::entityTypeManager()->getViewBuilder('block_content');
$build = $view_builder->view($block, 'full');

// Load by properties
$blocks = \Drupal::entityTypeManager()
  ->getStorage('block_content')
  ->loadByProperties(['type' => 'call_to_action']);

// Access fields safely
if (!$block->field_image->isEmpty()) {
  $image_uri = $block->field_image->entity->getFileUri();
}

// Update
$block->set('field_title', 'New Title');
$block->save();

// Delete
$block->delete();
```

**Reference:** `core/modules/block_content/src/Entity/BlockContent.php`, `core/modules/block_content/src/Plugin/Block/BlockContentBlock.php`

## Common Mistakes

- **Wrong**: Confusing `BlockContent` (entity) with `Block` (config entity for placement) → **Right**: Two different things; `Block` references a plugin which may wrap `BlockContent`
- **Wrong**: Editing non-reusable blocks outside Layout Builder → **Right**: They're not in the block library; use Layout Builder UI
- **Wrong**: Not checking `reusable` flag before placing → **Right**: Non-reusable blocks shouldn't be placed in traditional regions
- **Wrong**: Hardcoding block content IDs → **Right**: Use labels or UUIDs for portability across environments
- **Wrong**: Not handling deleted content block references → **Right**: Placed blocks will error if content entity deleted

## See Also

- [Custom Block Types](custom-block-types.md)
- [Block Placement & Configuration](block-placement.md)
- [Programmatic Block Operations](programmatic-operations.md)
- Reference: https://www.drupal.org/docs/drupal-apis/entity-api
