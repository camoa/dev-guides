---
description: Deciding between non-reusable inline blocks and reusable block content entities in Layout Builder.
---

## 7. Inline Blocks vs Reusable Blocks

### When to Use

When deciding between non-reusable inline blocks (created within Layout Builder) and reusable block content entities.

### Decision

| If you need... | Use... | Why |
|---|---|---|
| Content unique to this layout placement | Inline block (`inline_block:*`) | Content lives with layout, not reusable, simpler for one-off content |
| Same content in multiple placements | Reusable block (`block_content:*`) | One block content entity, multiple placements reference it, changes apply everywhere |
| Content managed outside Layout Builder | Reusable block via Block Library | Separate administration, can be placed via Block Layout or LB |
| Per-entity custom content in override | Inline block | Created when editing entity override layout, belongs to that entity |
| Content that should survive layout changes | Reusable block | Inline blocks tied to component UUID, removing from layout = orphaned |
| Simpler editorial experience | Inline block | Edit content inline when editing layout, no separate interface |

### Pattern

**Inline block:**
```php
// Creating inline block component
$component = new SectionComponent(
  \Drupal::service('uuid')->generate(),
  'content',
  [
    'id' => 'inline_block:basic',  // basic = block_content type
    'label' => 'My inline block',
    'view_mode' => 'full',
    'block_serialized' => NULL,    // Set after block created
    'context_mapping' => ['entity' => 'layout_builder.entity'],
  ]
);
```

**Reusable block:**
```php
// Reference existing block content entity
$block_content = \Drupal\block_content\Entity\BlockContent::load(123);
$component = new SectionComponent(
  \Drupal::service('uuid')->generate(),
  'content',
  [
    'id' => 'block_content:' . $block_content->uuid(),
    'label_display' => '0',
  ]
);
```

Reference: `/core/modules/layout_builder/src/Plugin/Block/InlineBlock.php` for inline block implementation.

### Common Mistakes

- **Using inline for repeated content** → Creates duplicate content. Use reusable blocks when same content appears in multiple places
- **Not cleaning up inline block orphans** → Removing inline block from layout leaves orphaned block_content entity. Run cron or use cleanup module
- **Confusing block_content plugins** → `inline_block:basic` creates new non-reusable block. `block_content:{uuid}` references existing reusable block. Different plugins
- **Expecting inline blocks to be portable** → Inline blocks tied to specific layout placement via UUID. Can't easily move to different section or entity
- **Editing inline blocks in Block admin** → Inline blocks (reusable = false) don't appear in Block Content admin. Must edit through Layout Builder
- **Not considering content workflow** → Inline blocks follow entity's moderation state. Reusable blocks have own workflow. Choose based on governance needs

### See Also

- Section 6: Block Placement (creating components)
- Section 18: Security & Performance (orphan cleanup, caching)
- Reference: `/core/modules/layout_builder/src/InlineBlockUsage.php` (orphan tracking)
- Web: [Layout Builder created blocks do not clean up](https://www.drupal.org/project/drupal/issues/3042418)
