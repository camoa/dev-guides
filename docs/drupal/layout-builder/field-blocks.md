---
description: Using field and extra field blocks in layouts
drupal_version: "11.x"
---

# Field & Extra Field Blocks

### When to Use

When exposing entity field data or extra fields (pseudo-fields) as blocks in Layout Builder layouts.

### Items

#### FieldBlock Plugin

**Description:** Derivative block plugin that exposes entity fields as blocks

**Plugin ID Format:** `field_block:{entity_type}:{bundle}:{field_name}`

**Configuration:**
| Key | Type | Description |
|-----|------|-------------|
| label_display | string | '0' (hidden) or '1' (visible) |
| formatter | mapping | Field formatter configuration (type, label, settings) |
| context_mapping | mapping | Maps entity context to block |

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

**Usage:**
```php
$component = new SectionComponent(
  \Drupal::service('uuid')->generate(),
  'content',
  [
    'id' => 'field_block:node:article:body',
    'label_display' => '0',
    'context_mapping' => ['entity' => 'layout_builder.entity'],
    'formatter' => [
      'label' => 'hidden',
      'type' => 'text_default',
      'settings' => [],
      'third_party_settings' => [],
    ],
  ]
);
```

**Gotchas:**
- Field must exist on entity_type/bundle or block breaks
- Formatter settings same structure as view display component
- Block respects field access — won't render if user can't view field
- Empty fields with no default value don't render (access check fails)
- Enabling Layout Builder auto-converts existing fields to field blocks in default section

#### ExtraFieldBlock Plugin

**Description:** Derivative block plugin for extra fields (pseudo-fields like node links, author info)

**Plugin ID Format:** `extra_field_block:{entity_type}:{bundle}:{extra_field_name}`

**Configuration:**
| Key | Type | Description |
|-----|------|-------------|
| label_display | string | '0' or '1' |
| context_mapping | mapping | Maps entity context |

**Example:**
```yaml
configuration:
  id: 'extra_field_block:node:article:links'
  label_display: '0'
  context_mapping:
    entity: 'layout_builder.entity'
```

**Common Extra Fields:**
- `links` — Node edit/delete links
- `display_submitted` — Author and date info
- Module-provided extra fields (e.g., `flag` module adds flag links)

**Gotchas:**
- Extra fields defined by `hook_entity_extra_field_info()`
- Not real fields — no field storage, just render arrays
- Configuration simpler than field blocks (no formatter)

#### Field Block Availability

**Description:** Which fields become available as field blocks

**Automatic Discovery:**
- Layout Builder scans entity_type/bundle for fields
- Only configurable display fields become blocks
- Base fields (title, created, etc.) included if configurable

**Customization:**
```php
// Limit field blocks in layout builder
function mymodule_layout_builder_field_block_alter(array &$definitions) {
  // Remove specific field block
  unset($definitions['field_block:node:article:field_internal']);

  // Modify field block label
  if (isset($definitions['field_block:node:article:body'])) {
    $definitions['field_block:node:article:body']['admin_label'] = 'Article Content';
  }
}
```

**Gotchas:**
- All configurable display fields exposed by default (can overwhelm editors)
- Use Layout Builder Restrictions module to limit available blocks
- Removing field from entity doesn't immediately remove field block (cached definitions)

#### Field Formatter Integration

**Description:** Field blocks use field formatter plugins for rendering

**Formatter Configuration:**
```php
'formatter' => [
  'label' => 'above',        // above, hidden, inline, visually_hidden
  'type' => 'image',         // Formatter plugin ID
  'settings' => [            // Formatter-specific settings
    'image_style' => 'large',
    'image_link' => 'content',
  ],
  'third_party_settings' => [],  // Module extensions
]
```

**Changing Formatter:**
- Via UI: Layout Builder block configuration form provides formatter selector
- Via code: Modify `formatter` array in component configuration

**Gotchas:**
- Formatter must be applicable to field type
- Invalid formatter falls back to default or causes error
- Third-party settings from modules like `field_group` carry over

### Common Mistakes

- **Wrong derivative format** → Must be `field_block:entity_type:bundle:field_name` exactly. Typos = block doesn't exist
- **Missing context mapping** → Field blocks REQUIRE entity context. Without it, no entity to get field data from
- **Assuming all fields available** → Only configurable display fields. Computed fields, non-display fields excluded unless custom code exposes them
- **Not handling field access** → Field blocks respect field access. Protected fields won't render for unprivileged users, no error shown
- **Mixing up field blocks and inline blocks** → Field blocks display entity field data. Inline blocks are custom block content. Completely different plugins
- **Forgetting formatter settings** → Missing or invalid formatter config can break rendering. Always validate formatter exists for field type
- **Not restricting field blocks** → All fields exposed by default. Use Layout Builder Restrictions or alter hooks to prevent editor overwhelm

### See Also

- Section 6: Block Placement (adding field blocks to layouts)
- Section 10: Layout Builder Restrictions (limiting available blocks)
- Reference: `/core/modules/layout_builder/src/Plugin/Block/FieldBlock.php`
- Reference: `/core/modules/layout_builder/src/Plugin/Block/ExtraFieldBlock.php`
