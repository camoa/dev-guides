---
description: Create reusable fieldable block types managed by content editors
drupal_version: "11.x"
---

# Custom Block Types

## When to Use

Creating reusable, fieldable block types that content editors can manage without code changes.

## Decision

| At this step... | If... | Then... |
|-----------------|-------|---------|
| Step 1 (create type) | Need multiple similar types | Use consistent naming convention |
| Step 2 (fields) | Fields shared across types | Consider field reuse or base fields |
| Step 3 (display) | Block appears in multiple contexts | Create multiple view modes |
| Step 4 (instances) | Content specific to one page | Consider inline block instead |
| Step 5 (placement) | Same block on many pages | Use visibility conditions instead of multiple placements |

## Pattern

**Via UI:**
1. Navigate to `/admin/structure/block-content/types`
2. Add block type, add fields
3. Create instances at `/block/add/{type}`
4. Place via `/admin/structure/block`

**Programmatically:**

```php
use Drupal\block_content\Entity\BlockContentType;
use Drupal\block_content\Entity\BlockContent;

// Create block type
$block_type = BlockContentType::create([
  'id' => 'call_to_action',
  'label' => 'Call to Action',
  'description' => 'Promotional block with title, text, and button',
]);
$block_type->save();

// Create block content instance
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

- **Wrong**: Creating block types when block plugin is more appropriate → **Right**: Use plugins for logic/dynamic content
- **Wrong**: Making non-reusable blocks via UI instead of inline blocks → **Right**: Use Layout Builder inline blocks for one-off content
- **Wrong**: Not planning field reuse across block types → **Right**: Leads to field proliferation and maintenance issues
- **Wrong**: Forgetting to set "Reusable" checkbox → **Right**: Block won't appear in block library
- **Wrong**: Over-using block content for simple static content → **Right**: Consider static blocks or page content instead

## See Also

- [Block Type Decision Matrix](block-type-decision.md)
- [Content Block Entities](content-blocks.md)
- [Layout Builder Integration](layout-builder-blocks.md)
- Reference: https://www.drupal.org/docs/core-modules-and-themes/core-modules/block-content-module
