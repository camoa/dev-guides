---
description: Work with BlockContent entities — load, create, update, and render fieldable content blocks
tldr: "Use when working programmatically with instances of block content (content entities created from block types). Distinct from Block config entities — `BlockContent` is the content; `Block` is the placement."
drupal_version: "11.x"
---

# Content Block Entities

## When to Use

> Working with instances of block content (content entities created from block types).

## Steps

1. **Understanding BlockContent entity**
   - Content entity with bundle (block type)
   - Fieldable, translatable, revisionable
   - Two modes: reusable vs non-reusable

2. **Creating content blocks**
   - Via UI: `/block/add/{type}`
   - Programmatically: `BlockContent::create([])`
   - Via inline form in Layout Builder

3. **Loading content blocks**
   ```php
   $block = BlockContent::load($id);
   $blocks = \Drupal::entityTypeManager()
     ->getStorage('block_content')
     ->loadByProperties(['type' => 'call_to_action']);
   ```

4. **Updating content blocks**
   ```php
   $block->set('field_title', 'New Title');
   $block->save();
   ```

5. **Accessing fields**
   ```php
   $title = $block->field_title->value;
   $image_url = $block->field_image->entity->createFileUrl();
   ```

## Decision Points

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

// Access fields safely
if (!$block->field_image->isEmpty()) {
  $image_uri = $block->field_image->entity->getFileUri();
}

// Delete
$block->delete();
```

**Reference:** `core/modules/block_content/src/Entity/BlockContent.php`, `core/modules/block_content/src/Plugin/Block/BlockContentBlock.php`

## Common Mistakes

- Confusing `BlockContent` (entity) with `Block` (config entity for placement) → Two different things; `Block` references a plugin which may wrap `BlockContent`
- Editing non-reusable blocks outside Layout Builder → They're not in the block library; use Layout Builder UI
- Not checking `reusable` flag before placing → Non-reusable blocks shouldn't be placed in traditional regions
- Hardcoding block content IDs → Use labels or UUIDs for portability across environments
- Not handling deleted content block references → Placed blocks will error if content entity deleted

## See Also

- [Custom Block Types](custom-block-types.md)
- [Block Placement & Configuration](block-placement.md) (placing content blocks)
- [Programmatic Block Operations](programmatic-operations.md)
- Reference: https://www.drupal.org/docs/drupal-apis/entity-api
