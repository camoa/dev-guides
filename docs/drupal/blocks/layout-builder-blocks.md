---
description: Inline blocks, field blocks, and extra field blocks in Layout Builder
drupal_version: "11.x"
---

# Layout Builder Integration

## When to Use

Understanding how Layout Builder uses blocks differently: inline blocks, field blocks, and extra field blocks.

## Decision

| If you need... | Use... | Why |
|----------------|--------|-----|
| One-off content specific to this layout | Inline Block | Non-reusable, owned by layout, no block library clutter |
| Entity field displayed as block in layout | Field Block | Native entity display, automatic updates when entity changes |
| Pseudo-field (like "author" or "submitted by") as block | Extra Field Block | Exposes hook_entity_extra_field_info() items as blocks |
| Reusable block in Layout Builder | Regular Block Plugin | Can be placed via Layout Builder and traditional regions |
| Block content that might become reusable later | Start with Inline Block, convert if needed | Easier to promote to reusable than demote from reusable |

## Pattern

**Inline Block (InlineBlock plugin):**
```php
// Automatically created when using Layout Builder UI
// Non-reusable BlockContent entity with reusable = FALSE
// Config stored in layout section:
[
  'type' => 'inline_block:basic',
  'block_revision_id' => 123,
  'block_serialized' => NULL,
]
```

**Field Block (FieldBlock plugin):**
```php
// Automatically available for all entity fields
// Plugin ID format: field_block:{entity_type}:{bundle}:{field_name}
// Example: field_block:node:article:field_image

// Usage in Layout Builder adds section component:
[
  'type' => 'field_block:node:article:body',
  'configuration' => [
    'label' => 'Body',
    'formatter' => [
      'type' => 'text_default',
      'settings' => [],
    ],
  ],
]
```

**Extra Field Block (ExtraFieldBlock plugin):**
```php
// Exposes extra fields defined via hook_entity_extra_field_info()
// Plugin ID format: extra_field_block:{entity_type}:{bundle}:{field_name}
// Example: extra_field_block:node:article:links

function mymodule_entity_extra_field_info() {
  $extra['node']['article']['display']['author_info'] = [
    'label' => t('Author information'),
    'description' => t('Author name and bio'),
    'weight' => 10,
  ];
  return $extra;
}
```

**Custom block plugin for Layout Builder:**
```php
// Regular block plugin works in Layout Builder
#[Block(
  id: "my_layout_block",
  admin_label: new TranslatableMarkup("My Layout Block"),
  category: new TranslatableMarkup("Custom"),
)]
class MyLayoutBlock extends BlockBase {
  public function build() {
    return ['#markup' => 'Available in Layout Builder'];
  }
}
```

**Reference:** `core/modules/layout_builder/src/Plugin/Block/InlineBlock.php`, `core/modules/layout_builder/src/Plugin/Block/FieldBlock.php`

## Common Mistakes

- **Wrong**: Trying to edit inline blocks from block library → **Right**: They're not reusable; must edit in Layout Builder
- **Wrong**: Creating reusable content blocks when inline blocks suffice → **Right**: Clutters block library unnecessarily
- **Wrong**: Not understanding inline blocks are BlockContent entities → **Right**: Same entity type, different `reusable` flag
- **Wrong**: Deleting node/entity without handling inline blocks → **Right**: Orphaned BlockContent entities; consider cleanup
- **Wrong**: Expecting field blocks to work outside Layout Builder → **Right**: They require entity context from layout

## See Also

- [Block Type Decision Matrix](block-type-decision.md)
- [Custom Block Types](custom-block-types.md)
- [Content Block Entities](content-blocks.md)
- Reference: https://www.drupal.org/docs/core-modules-and-themes/core-modules/layout-builder-module
