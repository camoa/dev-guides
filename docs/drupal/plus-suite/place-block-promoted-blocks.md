---
description: "PlaceBlock tool and promoted blocks — configure sidebar blocks, custom icons, drag-and-drop flow, and DropZones controller endpoints"
tldr: "Configure which blocks appear in the drag-and-drop sidebar, customize their icons, and understand the block placement flow."
drupal_version: "11.x"
---

# PlaceBlock Tool & Promoted Blocks

## When to Use

> When configuring which blocks appear in the drag-and-drop sidebar, customizing their icons, or understanding the block placement flow.

## How PlaceBlock Works

The PlaceBlock tool renders a two-tab sidebar:
1. **Promoted tab** — curated list of frequently-used blocks with custom icons
2. **Other tab** — searchable list of all available blocks, organized by category

When the user drags a block from either tab:
1. JavaScript shows drop zones on the page
2. User drops block in desired location
3. AJAX request to `DropZones::placeBlock()` controller
4. Controller creates block plugin with context mapping
5. If `field_sample_value` module is installed, fields are auto-populated with sample content
6. Layout is rebuilt via AJAX and rendered inline

## Pattern: Configuring Promoted Blocks

Navigate to the content type's **Manage Display** page, then find the LB+ Promoted Blocks configuration.

Promoted blocks are stored as third-party settings on `entity_view_display`:

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
```

## Block Placement in Nested Contexts

When inside a nested layout block, PlaceBlock:
- Detects `layout_block_uuid` from the request
- Scopes the block list to the nested context
- Merges parent entity's field blocks (any block definition containing `field_block:`)
- Restricts drop zones to the nested layout's regions

## DropZones Controller Endpoints

| Route | Method | Purpose |
|---|---|---|
| `lb_plus.js.place_block` | `placeBlock()` | Place new block from sidebar |
| `lb_plus.js.move_block` | `moveBlock()` | Move existing block between regions |
| `lb_plus.js.move_section_drop_zone` | `moveSection()` | Reorder sections |
| `lb_plus.js.add_section_drop_zone` | `addEmptySection()` | Add new empty section |

## Sample Content Generation on Placement

When a block is placed, the `Dropzones` service:
1. Creates `block_content` entity via `createBlockContent()`
2. If `field_sample_value` module exists, calls `SampleValueEntityGenerator::populateWithSampleValues()`
3. Otherwise, falls back to Drupal core's `generateSampleItems()` method
4. Block appears on page with realistic placeholder text, images, etc.

## Decision

| Block Type | Promote? | Reason |
|---|---|---|
| Basic (text) | Yes | Most common block |
| Image | Yes | Frequently needed |
| Layout Block | Yes | Enables nesting |
| Custom block types | Yes, if frequently used | Reduces search time |
| System blocks (breadcrumb, etc.) | Usually no | Rarely used in page building |
| Views blocks | Selectively | Only if commonly placed |

## Common Mistakes

- **Do not** promote too many blocks — defeats the purpose of curation. 5-10 is ideal.
- **Do not** forget to configure custom icons for promoted blocks — they help users identify blocks quickly.

## See Also

- [Nested Layouts](nested-layouts.md)
- [Field Sample Value](field-sample-value.md)
- [Custom Block Types](custom-block-types.md)
- Reference: `lb_plus/src/Controller/DropZones.php`
