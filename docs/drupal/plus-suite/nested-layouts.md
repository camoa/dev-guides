---
description: "Nested layouts (layout blocks) — TreeIndex architecture, NestedAwareSectionStorage, block duplication, and when to use nesting"
tldr: "Use nested layouts when you need blocks-within-blocks that can be treated as one reusable unit. Use section layouts for simple column arrangements."
drupal_version: "11.x"
---

# Nested Layouts

## When to Use

> When you need blocks-within-blocks (e.g., a hero section containing text + image blocks that can be treated as one reusable unit).

## What Is a Layout Block?

A "layout block" is an `inline_block` of type `layout_block` that has its own `layout_builder__layout` field. This creates a block that can contain other blocks within its own Layout Builder sections — like Russian nesting dolls.

## Detection Logic

```php
// NestedAwareSectionStorage::pluginIsLayoutBlock()
// A block is a layout block if:
// 1. It's an inline_block plugin
// 2. The referenced block_content entity has a layout_builder__layout field
```

## Architecture: TreeIndex

LB+ uses a `TreeIndex` for O(1) lookups across the entire nested tree:

```
TreeIndex structure:
uuid → {
  path: [section_index, block_uuid, section_index, ...],
  type: 'block' | 'section',
  metadata: { ... }
}
```

- Sections appear at odd path indices
- Blocks appear at even path indices
- Paths trace from root to any nested element

## NestedAwareSectionStorage

Wraps any `SectionStorageInterface` to add nesting awareness:

```php
// Wrap existing storage
$nested = NestedAwareSectionStorage::wrap($section_storage);

// Scope to a specific layout block for editing
$scoped = $nested->forLayoutBlock($block_uuid);

// Find section by UUID (not delta)
$section = $nested->getSectionByUuid($uuid);

// Get section containing a specific block
$section = $nested->getSectionFor($block_uuid);
```

## Nested Editing Flow

1. User selects a layout block and clicks "Edit Layout Block Layout"
2. `EditBlockLayout::nestedLayoutBuilderUIAjaxCallback()` fires
3. Current layout builders set to inactive
4. Nested `LayoutBuilderPlus` element renders with `layout_block_uuid` parameter
5. PlaceBlock sidebar refreshes with nested context
6. Changes saved to layout block's `layout_builder__layout` field
7. Exit button returns to parent layout level

## Route Enhancement for Nesting

`NestedRouteEnhancer` (priority -10) intercepts routes to detect nested context:

| Scenario | Detection | Action |
|---|---|---|
| Block route with `{uuid}` | Looks up UUID in TreeIndex | Scopes storage, adjusts delta |
| Section route with `section_uuid` param | Derives local delta from TreeIndex | Scopes storage to layout block |

## Response Transformation

`NestedLayoutResponseSubscriber` (KernelEvents::RESPONSE, priority -50) transforms AJAX responses:
- `ReplaceCommand` targeting `#layout-builder` → changes to `[data-nested-storage-uuid='<uuid>']`
- `CloseDialogCommand` targeting `#drupal-off-canvas` → changes to `.ui-dialog-content`

## Block Duplication with Nesting

`DuplicateBlock::duplicate()` recursively clones:
1. The block component itself
2. All inline block content
3. All sections within layout blocks
4. All blocks within those sections (recursive)
5. New UUIDs generated for every cloned element

## Recipe Config: Layout Block Type

The recipe creates a `layout_block` block content type:

```yaml
# block_content.type.layout_block.yml
id: layout_block
label: 'Layout Block'
description: 'A block with a layout that holds additional blocks.'
```

## Decision

| Use Case | Nested Layout? | Reason |
|---|---|---|
| Hero section (heading + image + CTA) | Yes | Treat as reusable unit |
| Two-column text section | No | Use section layout instead |
| Card grid with varying card layouts | Yes | Each card can have its own layout |
| Simple text + image side-by-side | No | Use two-column section |
| Complex component reused across pages | Yes | Save to Section Library |

## Setting Up Layout Blocks (Required for Nesting)

The recipe creates this automatically, but if setting up manually:

1. Go to **Structure → Block Types → Add block type** (`/admin/structure/block-content`)
2. Name: **"Layout Block"**, machine name: `layout_block`
3. **Remove the body field** — Layout Blocks should only contain nested blocks, not their own content
4. Go to the block type's **Manage Display**
5. Check **"Use Layout builder"**
6. Check **"Allow each content item to have its layout customized"**
7. Click **Save** and configure a **default layout section** (One Column)
8. **Critical**: A default layout MUST be configured. Without it → "Undefined array key 'layout_plugin'" error
9. Go to your content type's **Manage Display** and **promote the Layout Block** in the LB+ promoted blocks section

## Common Mistakes

- **Do not** nest more than 2-3 levels deep — performance degrades and UX becomes confusing.
- **Do not** forget that `bubbleChangesToRoot()` must be called explicitly when saving nested changes programmatically.
- **Do not** use nested layouts for simple two-column content — section layouts handle that.
- **Do not** leave the body field on the Layout Block type — it takes up space and serves no purpose inside a nested layout.
- **Do not** skip the default layout configuration on the Layout Block type — it causes a fatal error.

## See Also

- [Place Block & Promoted Blocks](place-block-promoted-blocks.md)
- [Section Library](section-library.md)
- [Tempstore Strategy Pattern](tempstore-strategy.md)
- [Installation & Setup](installation-setup.md) — Step 7 covers manual Layout Block setup
- Reference: `lb_plus/src/SectionStorage/NestedAwareSectionStorage.php`, `lb_plus/src/SectionStorage/TreeIndex.php`
