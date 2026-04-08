---
description: PlaceBlock tool and promoted blocks — configure sidebar blocks, custom icons, drag-and-drop flow, and DropZones controller endpoints
drupal_version: "11.x"
---

# PlaceBlock Tool & Promoted Blocks

## When to Use

> Configure Promoted Blocks to curate the drag-and-drop sidebar. All available blocks still appear under the "Other" tab; promoted blocks are just surfaced first with custom icons.

## Decision

| Block Type | Promote? | Reason |
|------------|---------|--------|
| Basic (text) | Yes | Most common block |
| Image | Yes | Frequently needed |
| Layout Block | Yes | Enables nesting |
| Custom block types | Yes, if frequently used | Reduces search time |
| System blocks (breadcrumb, etc.) | Usually no | Rarely used in page building |
| Views blocks | Selectively | Only if commonly placed |

## Pattern

**Configure promoted blocks** (stored as third-party settings on `entity_view_display`):

```yaml
third_party_settings:
  lb_plus:
    promoted_blocks:
      - 'inline_block:basic'
      - 'inline_block:image'
      - 'inline_block:layout_block'
    block_config:
      icon:
        'inline_block:basic': '/modules/contrib/lb_plus/assets/icons/text.svg'
        'inline_block:image': '/modules/contrib/lb_plus/assets/icons/image.svg'
```

**DropZones controller endpoints:**

| Route | Purpose |
|-------|---------|
| `lb_plus.js.place_block` | Place new block from sidebar |
| `lb_plus.js.move_block` | Move existing block between regions |
| `lb_plus.js.move_section_drop_zone` | Reorder sections |
| `lb_plus.js.add_section_drop_zone` | Add new empty section |

**Sample content on placement:** When a block is placed, `Dropzones` service:
1. Creates `block_content` entity
2. Calls `SampleValueEntityGenerator::populateWithSampleValues()`
3. Block appears with realistic placeholder content immediately

**Nested context:** Inside a layout block, PlaceBlock scopes the block list to `layout_block_uuid` context and restricts drop zones to the nested layout's regions.

## Common Mistakes

- **Wrong**: Promoting too many blocks → **Right**: 5–10 promoted blocks is ideal; more defeats the curation purpose
- **Wrong**: Forgetting custom icons for promoted blocks → **Right**: Icons help users identify blocks quickly; plain text names are slow to scan

## See Also

- [Nested Layouts](nested-layouts.md)
- [Field Sample Value](field-sample-value.md)
- [Custom Block Types](custom-block-types.md)
- Reference: `lb_plus/src/Controller/DropZones.php`
