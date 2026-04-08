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

## Common Mistakes

- **Wrong**: Nesting more than 2–3 levels → **Right**: Performance degrades and UX becomes confusing; limit depth
- **Wrong**: Forgetting `bubbleChangesToRoot()` in programmatic code → **Right**: Changes to nested layouts must bubble up to the root entity
- **Wrong**: Using nested layouts for simple two-column content → **Right**: Use section layouts for column arrangements

## See Also

- [Place Block & Promoted Blocks](place-block-promoted-blocks.md)
- [Section Library](section-library.md)
- [Tempstore Strategy Pattern](tempstore-strategy.md)
- Reference: `lb_plus/src/NestedAwareSectionStorage.php`, `lb_plus/src/TreeIndex.php`
