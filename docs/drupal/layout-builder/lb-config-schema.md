---
description: Complete Layout Builder configuration schema — sections, components, inline blocks, field blocks, and YAML structure.
---

## 3. Layout Builder Configuration Schema

### When to Use

When reading, editing, or generating Layout Builder configuration in YAML files, understanding config structure for recipes, programmatic manipulation, or debugging.

### Items

#### third_party_settings.layout_builder

**Description:** Root configuration attached to entity_view_display config entity

**Schema:**
| Key | Type | Description |
|-----|------|-------------|
| enabled | boolean | Whether Layout Builder is enabled for this display |
| allow_custom | boolean | Whether per-entity overrides are allowed |
| sections | sequence | Array of section configurations |

**Example:**
```yaml
third_party_settings:
  layout_builder:
    enabled: true
    allow_custom: false
    sections:
      - layout_id: layout_onecol
        layout_settings: {  }
        components: []
```

**Gotchas:**
- `sections` must be array (sequence), never empty object
- Removing `sections` completely different from empty array
- Config entity dependency calculation includes layout and block plugins

#### layout_builder.section

**Description:** Individual section within a layout — contains layout plugin ID, settings, and components

**Schema:**
| Key | Type | Description |
|-----|------|-------------|
| layout_id | string | Layout plugin ID (e.g., 'layout_twocol_section') |
| layout_settings | mapping | Configuration for layout plugin (varies by layout) |
| components | sequence | Array of components (blocks) in this section |
| third_party_settings | sequence | Additional settings from contrib modules |

**Example:**
```yaml
- layout_id: layout_twocol_section
  layout_settings:
    label: 'Two column layout'
    column_widths: '50-50'
  components:
    - uuid: abc-123
      region: first
      configuration:
        id: 'system_branding_block'
      weight: 0
  third_party_settings:
    layout_builder_styles:
      style:
        section_wrapper: 'container-fluid'
```

**Gotchas:**
- `layout_settings` structure depends on layout plugin class
- Third-party settings enable contrib modules to extend sections (e.g., layout_builder_styles for CSS classes)
- Sections are ordered — array order determines display order

#### layout_builder.component

**Description:** Block component within a section — wraps a block plugin instance

**Schema:**
| Key | Type | Description |
|-----|------|-------------|
| uuid | string | Unique identifier for this component instance |
| region | string | Layout region name where component renders |
| configuration | mapping | Block plugin configuration (id + settings) |
| weight | integer | Sort order within region (lower = earlier) |
| additional | ignore | Runtime data, not stored in config |

**Example:**
```yaml
uuid: f47ac10b-58cc-4372-a567-0e02b2c3d479
region: content
configuration:
  id: 'field_block:node:article:body'
  label_display: '0'
  context_mapping:
    entity: 'layout_builder.entity'
  formatter:
    label: hidden
    type: text_default
    settings: {}
weight: 10
```

**Gotchas:**
- UUIDs must be valid and unique per component
- `configuration.id` determines block plugin (field_block, inline_block, system blocks, custom)
- `context_mapping` provides entity context to blocks
- Weight determines order in region, not global order

#### inline_block configuration

**Description:** Configuration for non-reusable inline blocks (created within Layout Builder)

**Schema:**
| Key | Type | Description |
|-----|------|-------------|
| id | string | Always 'inline_block:{block_content_type}' |
| view_mode | string | View mode for rendering block content entity |
| block_id | integer | Block content entity ID (after save) |
| block_revision_id | integer | Block content revision ID (after save) |
| block_serialized | string | Serialized block entity (before save) |

**Example:**
```yaml
configuration:
  id: 'inline_block:basic'
  label: 'My inline block'
  view_mode: full
  block_id: 123
  block_revision_id: 456
  context_mapping:
    entity: 'layout_builder.entity'
```

**Gotchas:**
- Before save: `block_serialized` contains serialized entity, no IDs
- After save: `block_id` and `block_revision_id` set, serialized cleared
- Inline blocks create `block_content` entities with `reusable: false`
- Orphaned inline blocks remain in DB when removed from layout — cleaned up by cron

#### field_block configuration

**Description:** Configuration for field blocks (entity fields as blocks)

**Schema:**
| Key | Type | Description |
|-----|------|-------------|
| id | string | 'field_block:{entity_type}:{bundle}:{field_name}' |
| label_display | string | Whether to show block label ('0' or '1') |
| context_mapping | mapping | Maps entity context to block |
| formatter | mapping | Field formatter configuration |

**Example:**
```yaml
configuration:
  id: 'field_block:node:article:field_image'
  label_display: '0'
  context_mapping:
    entity: 'layout_builder.entity'
  formatter:
    label: hidden
    type: responsive_image
    settings:
      responsive_image_style: wide
    third_party_settings: {}
```

**Gotchas:**
- Derivative plugin ID encodes entity_type, bundle, field_name
- `formatter` settings same structure as entity view display component config
- Field must exist on entity type/bundle or block breaks
- Field access checks apply — blocks don't render if user can't view field

### Common Mistakes

- **Editing UUIDs** → Never change UUIDs in config. Layout Builder uses them to track components. Generate new UUIDs for new components
- **Wrong layout_id** → Must match registered layout plugin. Check `*.layouts.yml` files or layout plugin manager
- **Missing context_mapping** → Field blocks and inline blocks need `entity: 'layout_builder.entity'` to access entity context
- **Inconsistent weight** → Weights control order within region. Gaps are fine, negative weights allowed. Duplicates result in undefined order
- **Exporting with serialized blocks** → Block serialized data in config is pre-save temporary state. Export after saving so block_id/block_revision_id are set
- **Not validating against schema** → Config schema enforces structure. Validate with `drush config:inspect` to catch errors before import

### See Also

- Section 4: Sections & Layouts (layout plugins)
- Section 6: Block Placement (component structure)
- Section 7: Inline vs Reusable (block configuration differences)
- Reference: `/core/modules/layout_builder/config/schema/layout_builder.schema.yml`
