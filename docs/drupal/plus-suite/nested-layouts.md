---
description: Nested layouts (layout blocks) — TreeIndex architecture, NestedAwareSectionStorage, block duplication, and when to use nesting
drupal_version: "11.x"
---

# Nested Layouts

## When to Use

> Use nested layouts when you need blocks-within-blocks as a reusable unit. Use section layouts for simple column arrangements.

## Decision

| Use Case | Nested Layout? | Reason |
|----------|---------------|--------|
| Hero section (heading + image + CTA) | Yes | Treat as reusable unit |
| Two-column text section | No | Use section layout instead |
| Card grid with varying card layouts | Yes | Each card can have its own layout |
| Simple text + image side-by-side | No | Use two-column section |
| Complex component reused across pages | Yes | Save to Section Library |

## Pattern

A "layout block" is an `inline_block` of type `layout_block` with its own `layout_builder__layout` field — blocks within blocks.

**NestedAwareSectionStorage API:**

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

**TreeIndex** provides O(1) lookups across the entire nested tree:
```
uuid → {
  path: [section_index, block_uuid, section_index, ...],
  type: 'block' | 'section',
}
```

**Nested editing flow:**
1. User selects layout block → clicks "Edit Layout Block Layout"
2. Current layout builders set to inactive
3. Nested `LayoutBuilderPlus` element renders with `layout_block_uuid` parameter
4. PlaceBlock sidebar refreshes with nested context
5. Exit button returns to parent layout level

**Programmatic save** — must call `bubbleChangesToRoot()` explicitly when saving nested changes.

## Setting Up Layout Blocks (Manual Setup)

The recipe creates the `layout_block` block type automatically. For manual setup:

1. Go to **Structure → Block Types → Add block type** (`/admin/structure/block-content`)
2. Name: **"Layout Block"**, machine name: `layout_block`
3. **Remove the body field** — layout blocks should only contain nested blocks, not their own content
4. Go to the block type's **Manage Display**
5. Check **"Use Layout builder"**
6. Check **"Allow each content item to have its layout customized"**
7. Click **Save** and configure a **default One Column layout section**
8. **Critical**: A default layout MUST be configured. Without it → "Undefined array key 'layout_plugin'" error
9. Go to your content type's **Manage Display** and **promote the Layout Block** in the LB+ promoted blocks section

## Common Mistakes

- **Wrong**: Nesting more than 2–3 levels → **Right**: Performance degrades and UX becomes confusing; limit depth
- **Wrong**: Forgetting `bubbleChangesToRoot()` in programmatic code → **Right**: Changes to nested layouts must bubble up to the root entity
- **Wrong**: Using nested layouts for simple two-column content → **Right**: Use section layouts for column arrangements
- **Wrong**: Leaving body field on Layout Block type → **Right**: Remove it; it takes up space and serves no purpose inside nested layouts
- **Wrong**: Skipping default layout configuration on Layout Block type → **Right**: Configure a default One Column layout or get a fatal error

## See Also

- [Place Block & Promoted Blocks](place-block-promoted-blocks.md)
- [Section Library](section-library.md)
- [Tempstore Strategy Pattern](tempstore-strategy.md)
- [Installation & Setup](installation-setup.md) — Step 7 covers manual Layout Block setup
- Reference: `lb_plus/src/NestedAwareSectionStorage.php`, `lb_plus/src/TreeIndex.php`
