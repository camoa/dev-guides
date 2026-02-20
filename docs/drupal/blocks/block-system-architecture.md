---
description: Drupal's 4-layer block system — Block Plugin API, placement entities, content entities, Layout Builder
drupal_version: "11.x"
---

# Block System Architecture

## When to Use

> Understand the 4 layers before starting any block development. Use this to orient yourself when deciding which layer to work with.

## Decision

| Layer | Purpose | Location | Key Classes |
|-------|---------|----------|-------------|
| Block Plugin API | Plugin foundation for all blocks | `core/lib/Drupal/Core/Block/` | `BlockBase`, `BlockPluginInterface`, `#[Block]` |
| Block module | Placement system (config entities) | `core/modules/block/` | `Block` entity, `BlockRepository`, `BlockViewBuilder` |
| Block Content module | Fieldable content entities | `core/modules/block_content/` | `BlockContent`, `BlockContentType`, `BlockContentBlock` plugin |
| Layout Builder | Inline blocks for layouts | `core/modules/layout_builder/` | `InlineBlock`, `FieldBlock`, `ExtraFieldBlock` |

**How the layers interact:**

1. **Block Plugin API** defines the plugin interface that all blocks must implement
2. **Block module** creates config entities (`Block`) that reference block plugins and control placement (region, theme, visibility)
3. **Block Content module** provides a special block plugin (`BlockContentBlock`) that wraps content entities, allowing fieldable blocks
4. **Layout Builder** creates its own block plugins for inline blocks and exposes entity fields as blocks

## Pattern

```php
use Drupal\Core\Block\Attribute\Block;
use Drupal\Core\Block\BlockBase;

#[Block(
  id: "my_block",
  admin_label: new TranslatableMarkup("My Block"),
  category: new TranslatableMarkup("Custom"),
)]
class MyBlock extends BlockBase {
  public function build() {
    return ['#markup' => 'Content'];
  }
}
```

**Reference:** `core/lib/Drupal/Core/Block/Plugin/Block/PageTitleBlock.php`

## Common Mistakes

- **Wrong**: Confusing block plugins (programmatic) with content blocks (fieldable entities) → **Right**: Use block plugins for logic, content blocks for editor-managed content
- **Wrong**: Placing blocks via code when config entity placement is appropriate → **Right**: Use `Block` config entities for standard placement
- **Wrong**: Not understanding that `BlockContent` entities are wrapped by `BlockContentBlock` plugin → **Right**: Content blocks use BOTH layers
- **Wrong**: Treating Layout Builder inline blocks like regular blocks → **Right**: Inline blocks are non-reusable and owned by the layout

## See Also

- [Block Type Decision Matrix](block-type-decision.md)
- Reference: https://www.drupal.org/docs/drupal-apis/block-api/block-api-overview
