---
description: Create reusable fieldable block types managed by content editors
tldr: "Use custom block types when content editors need to manage block content with custom fields without code changes. Use block plugins instead for logic-driven or dynamic content."
drupal_version: "11.x"
---

# Custom Block Types

## When to Use

> Creating reusable, fieldable block types that content editors can manage without code changes.

## Steps

1. **Create block type via UI**
   - Navigate to `/admin/structure/block-content/types`
   - Click "Add block type"
   - Enter label and description
   - Save

2. **Add fields to the block type**
   - Click "Manage fields" for your block type
   - Add fields (text, image, entity reference, etc.)
   - Configure field settings and display

3. **Configure display modes**
   - "Manage display" tab
   - Arrange field order, formatters
   - Create additional view modes if needed

4. **Create block content instances**
   - Navigate to `/block/add/{block_type_machine_name}`
   - Fill in fields
   - Save
   - Mark as "Reusable" if it should appear in block library

5. **Place block instances**
   - `/admin/structure/block`
   - "Place block" → Find your content block
   - Configure region, visibility, cache

## Decision Points

| At this step... | If... | Then... |
|-----------------|-------|---------|
| Step 1 (create type) | Need multiple similar types | Use consistent naming convention |
| Step 2 (fields) | Fields shared across types | Consider field reuse or base fields |
| Step 3 (display) | Block appears in multiple contexts | Create multiple view modes |
| Step 4 (instances) | Content specific to one page | Consider inline block instead |
| Step 5 (placement) | Same block on many pages | Use visibility conditions instead of multiple placements |

## Pattern

Programmatically creating a block type:

```php
use Drupal\block_content\Entity\BlockContentType;

$block_type = BlockContentType::create([
  'id' => 'call_to_action',
  'label' => 'Call to Action',
  'description' => 'Promotional block with title, text, and button',
]);
$block_type->save();

// Add fields programmatically (see Field API)
```

Programmatically creating a block content instance:

```php
use Drupal\block_content\Entity\BlockContent;

$block = BlockContent::create([
  'type' => 'call_to_action',
  'info' => 'Homepage CTA',
  'reusable' => TRUE,
  'field_title' => 'Join Today!',
  'field_description' => 'Sign up for our newsletter',
]);
$block->save();
```

**Reference:** `core/modules/block_content/src/Entity/BlockContentType.php`, `core/modules/block_content/src/Entity/BlockContent.php`

## Common Mistakes

- Creating block types when block plugin is more appropriate → Use plugins for logic/dynamic content
- Making non-reusable blocks via UI instead of inline blocks → Use Layout Builder inline blocks for one-off content
- Not planning field reuse across block types → Leads to field proliferation and maintenance issues
- Forgetting to set "Reusable" checkbox → Block won't appear in block library
- Over-using block content for simple static content → Consider static blocks or page content instead

## See Also

- [Block Type Decision Matrix](block-type-decision.md)
- [Content Block Entities](content-blocks.md) (working with instances)
- [Layout Builder Integration](layout-builder-blocks.md) (inline blocks)
- Reference: https://www.drupal.org/docs/core-modules-and-themes/core-modules/block-content-module
