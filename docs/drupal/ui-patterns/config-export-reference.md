---
description: Config export reference — ui_patterns_component schema, source types, and integration file locations
drupal_version: "10.3+ / 11"
---

## Config Export Reference

### When to Use

When you need to understand, construct, or debug UI Patterns configuration YAML for deployment, recipes, config management, or programmatic setup. This section documents the core schema that all four integrations share and provides a reference for all available source types.

### The ui_patterns_component Schema

Every UI Patterns integration stores its component configuration using the `ui_patterns_component` config schema. This is the canonical structure:

```yaml
ui_patterns:
  component_id: 'provider:component_name'    # Full SDC component ID
  variant_id:                                 # Optional variant selection
    source_id: select                         # Source plugin ID
    source:
      value: 'variant_key'                    # Source-specific configuration
  props:                                      # Keyed by prop machine name
    prop_name:
      source_id: source_plugin_id            # Which source provides the value
      source:                                 # Source-specific configuration
        value: 'some value'                   # (varies by source type)
  slots:                                      # Keyed by slot machine name
    slot_name:
      sources:                                # Array of sources (slots allow multiple)
        - source_id: source_plugin_id
          source:
            value: 'content'
          _weight: '0'                        # Ordering weight (string)
        - source_id: another_source
          source: {}
          _weight: '1'
```

Schema hierarchy:
- `ui_patterns_component` -- top-level mapping with `component_id`, `variant_id`, `props`, `slots`
- `ui_patterns_prop` -- each prop: `source_id` + `source` (resolved via `ui_patterns_source.[source_id]`)
- `ui_patterns_slot` -- each slot: `sources` sequence
- `ui_patterns_slot_source` -- each slot source: `source_id` + `source` + `_weight`

### Source Types Reference

| Source ID | Schema Key | Config Structure | Use For |
|---|---|---|---|
| `textfield` | `ui_patterns_source.textfield` | `value: 'string'` | Manual text for string/identifier props |
| `number` | `ui_patterns_source.number` | `value: 'string'` | Manual number (stored as string) |
| `select` | `ui_patterns_source.select` | `value: 'string'` | Enum prop selection |
| `selects` | `ui_patterns_source.selects` | `value: ['a', 'b']` | Multi-select enum_list |
| `checkbox` | `ui_patterns_source.checkbox` | `value: true` | Boolean toggle |
| `checkboxes` | `ui_patterns_source.checkboxes` | `value: ['a', 'b']` | Multi-checkbox enum_set |
| `url` | `ui_patterns_source.url` | `value: 'https://...'` | URL input |
| `path` | `ui_patterns_source.path` | `value: ...` | Current path (ignore type) |
| `attributes` | `ui_patterns_source.attributes` | `value: 'string'` | HTML attributes |
| `attributes_class` | `ui_patterns_source.attributes_class` | `value: 'string'` | CSS class string |
| `list_textarea` | `ui_patterns_source.list_textarea` | `value: 'string'` | Multi-line list |
| `wysiwyg` | `ui_patterns_source.wysiwyg` | `value: {value: 'html', format: 'format_id'}` | Rich text (text_format) |
| `component` | `ui_patterns_source.component` | `component: {ui_patterns_component}` | Nested SDC component |
| `menu` | `ui_patterns_source.menu` | `menu: 'menu_name', level: '1', depth: '2'` | Menu tree for links props |
| `token` | `ui_patterns_source.token` | `value: '[node:title]'` | Token replacement |
| `entity_link` | `ui_patterns_source.entity_link` | `template: 'canonical'` | Entity URL for url/links props |
| `field_property:*:*:*` | `ui_patterns_source.field_property` | `type: 'value'` | Entity field property value |
| `block` | `ui_patterns_source.block` | (ignore schema -- dynamic) | Drupal block in slot |
| `entity_field` | `ui_patterns_source.entity_field` | (ignore schema -- dynamic) | Full field render in slot |
| `entity_reference` | `ui_patterns_source.entity_reference` | (ignore schema -- dynamic) | Context switcher (no value) |

### Integration Config File Locations

| Integration | Config File Pattern | Schema | Settings Path |
|---|---|---|---|
| **Field Formatter** | `core.entity_view_display.{type}.{bundle}.{mode}.yml` | `field.formatter.settings.ui_patterns` | `content.{field}.settings.ui_patterns` |
| **Block** | `block.block.{block_id}.yml` | `block.settings.ui_patterns:*:*` | `settings.ui_patterns` |
| **Layout** | `core.entity_view_display.{type}.{bundle}.{mode}.yml` | `layout_plugin.settings.*` | `third_party_settings.layout_builder.sections[].layout_settings.ui_patterns` |
| **Views Style** | `views.view.{view_name}.yml` | `views.style.ui_patterns` | `display.{id}.display_options.style.options.ui_patterns.ui_patterns` |
| **Views Row** | `views.view.{view_name}.yml` | `views.row.ui_patterns` | `display.{id}.display_options.row.options.ui_patterns` |

### Export Workflow

```
1. Configure the integration via the admin UI
   - Manage Display for field formatters
   - Block Layout or Layout Builder for blocks
   - Layout Builder "Add section" for layouts
   - Views UI Format/Show settings for views
2. drush config:export
3. Find the config file based on the integration type (see table above)
4. The ui_patterns key in the exported YAML matches the ui_patterns_component schema
```

### Common Mistakes

| Mistake | Why It Is Wrong |
|---|---|
| Forgetting that field property source IDs include entity type and bundle | Source IDs are derived: `field_property:node:article:field_name`. Using just `field_property:field_name` will not resolve. |
| Missing `_weight` on slot sources | Required for ordering multiple sources within a slot. Omitting it may cause unpredictable render order. Values are strings (e.g., `'0'`, `'1'`). |
| Using wrong source type for prop type | A `textfield` source cannot serve a `boolean` prop. Match source `prop_types` to the component's prop type (see [Source Plugins](#source-plugins)). |
| Confusing Views style double nesting with row single nesting | Style config: `options.ui_patterns.ui_patterns` (double). Row config: `options.ui_patterns` (single). Getting this wrong causes schema validation failures. |
| Manually crafting `block` or `entity_reference` source config | These sources use dynamic sub-keys and have `ignore` schema types. Always configure them via the admin UI and export, rather than writing YAML by hand. |

### See Also

- [Field Formatters](#field-formatters) -- formatter config examples
- [Blocks Integration](#blocks-integration) -- block config examples
- [Layout Builder Integration](#layout-builder-integration) -- layout config examples
- [Views Integration](#views-integration) -- views config examples
- [Source Plugins](#source-plugins) -- source plugin system overview