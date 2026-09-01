---
description: "Source plugins — widgets, API sources, and context-switcher sources for component props/slots in UI Patterns 2"
tldr: "Source plugins bridge Drupal data (entity fields, menus, user input) to component props/slots. Three categories — widgets (direct input), API sources (Drupal data), and context switchers (entity_field, entity_reference) that unlock sibling-field sources via a mandatory 3-level colon-keyed YAML nesting."
drupal_version: "11.x"
---

# Source Plugins

## When to Use

> Use source plugins whenever you need to map Drupal data to a component prop or slot. Use context switchers (`entity_field`, `entity_reference`) when you need data from a field that is not the formatter's trigger field.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Manual text/number/boolean input | Widget source (`textfield`, `number`, `checkbox`) | Stores value directly in config |
| Entity field value (same entity, same field) | `field_property:{entity_type}:{field_name}:{column}` | Derived source, no bundle segment, no nesting needed |
| Sibling field on same entity (per-item formatter) | `entity_field` context switcher | Scopes context to that field, then nest inner source |
| Referenced entity's fields | `entity_reference` context switcher | Follows the reference, then nest sources |
| Field rendered via a formatter (image, file) | `field_formatter` as inner source inside `entity_field` | Returns renderable slot output; ID carries a bundle segment |

## Pattern

### Built-in Source Plugins

Read this table as the `#[Source]` attributes, not as the config schema. The plugin ID is whatever the attribute's `id:` (plus its deriver) mints; the `ui_patterns_source.*` schema keys are a separate, and in one case mismatched, list.

| Source ID | Category | Prop Types | Context / Requirement | Description |
|---|---|---|---|---|
| `textfield` | Widget | string, identifier | -- | Single-line text input |
| `number` | Widget | number | -- | Numeric input |
| `checkbox` | Widget | boolean | -- | Boolean toggle |
| `select` | Widget | enum, variant | -- | Dropdown select; also the default source for `variant` |
| `selects` | Widget | enum_list | -- | Multiple select |
| `checkboxes` | Widget | enum_set | -- | Checkbox group |
| `url` | Widget | url | -- | URL input field |
| `attributes` | Widget | attributes | Entity (optional) | Key-value attribute pairs |
| `class_attribute` | Widget | attributes | -- | CSS class input. **Deprecated** since 2.0.0-rc1, removed in 3.0.0 — merged into `attributes`. Label renders as "HTML classes [Deprecated]" |
| `list_textarea` | Widget | list | -- | Multi-line list input |
| `wysiwyg` | Widget | slot | -- | CKEditor rich text |
| `component` | Source | slot | -- | Nested SDC component |
| `block` | Source | slot | -- | Drupal block plugin |
| `menu` | Source | links | -- | Menu tree |
| `breadcrumb` | Source | links | -- | Breadcrumb trail |
| `path` | Source | url | -- | Internal path. Tagged `widget:dismissible`, so it never appears as a converted source for `string` props |
| `token` | Source | slot, string, url | Entity (optional) | Token replacement — fills slots and URL props too, not just strings |
| `field_property` | Deriver | (per property, from typed data) | Entity + Field | Entity field property value. IDs: `field_property:{entity_type}:{field_name}:{property}` |
| `field_formatter` | Deriver | slot | Entity + Field | Field rendered through a formatter. IDs: `field_formatter:{entity_type}:{bundle}:{field_name}` |
| `field_label` | Source | string | `field_formatter` requirement | Field label text. **Only available inside a UI Patterns field formatter** — never in blocks, layouts or Views |
| `entity_link` | Source | url | Entity | Entity link URL. No deriver — the plugin ID is the bare `entity_link` |
| `entity_field` | Context switcher | (none declared -> all) | Entity | Switches context to a field on the same entity |
| `entity_reference` | Context switcher | (none declared -> all) | Entity | Switches context to a referenced entity |
| `view_field` | Source (`ui_patterns_views`) | slot | `views:row` requirement | A field from the current Views row |
| `view_rows` | Source (`ui_patterns_views`) | slot | `views:style` requirement | The rendered Views rows, for a wrapper component |
| `view_title` | Source (`ui_patterns_views`) | string | View entity | The title of the view |

### Context Switcher Sources (`entity_field`, `entity_reference`)

Some sources don't return values directly — they switch the available context so other sources can read data. Neither `entity_field` nor `entity_reference` declares `prop_types`, so both are offered for every prop and every slot.

When you write a context switcher in YAML config, the structure is **3 levels deep** with an unusual nested key. After you pick the field via `derivable_context`, you must repeat that exact value (with colons in the key) before nesting the inner source.

**The innermost level differs between slots and props.** `DerivableContextSourceBase::getSourcePlugins()` branches on `isSlot()`: for a slot it reads `value.sources[0]`, for a prop it reads `value` directly as the source configuration. Get the shape wrong and the method bails at `!isset($source_configuration["source_id"])` and returns no sources — the prop or slot is simply empty, with no error anywhere.

**Slot form** (note the `sources:` sequence):

```yaml
slots:
  label:
    sources:
      - source_id: entity_field
        source:
          # Level 1: which field to switch context to
          derivable_context: 'field:block_content:hero:field_label'
          # Level 2: nested key MUST equal the derivable_context value (quote it — contains colons)
          'field:block_content:hero:field_label':
            value:
              # Level 3: the actual source that produces the rendered value
              sources:
                - source_id: 'field_property:block_content:field_label:value'
                  source:
                    type: value
                  _weight: '0'
        _weight: '0'
```

**Prop form** — same first two levels, but `value` *is* the source config: no `sources:` sequence, no `_weight`.

```yaml
props:
  heading:
    source_id: entity_field
    source:
      derivable_context: 'field:block_content:hero:field_label'
      'field:block_content:hero:field_label':
        value:
          source_id: 'field_property:block_content:field_label:value'
          source:
            type: value
```

For image/file fields that need rendered output, use `field_formatter` as the inner source. `field_formatter` IDs carry a bundle segment, unlike `field_property` — `{entity_type}:{bundle}:{field_name}`, with an **empty** segment for base fields (`field_formatter:node::title`). The formatter's own settings go under `settings:`, not `formatter:`:

```yaml
slots:
  image:
    sources:
      - source_id: entity_field
        source:
          derivable_context: 'field:block_content:hero:field_image'
          'field:block_content:hero:field_image':
            value:
              sources:
                - source_id: 'field_formatter:block_content:hero:field_image'
                  source:
                    type: responsive_image
                    settings:
                      responsive_image_style: hero_responsive
                  _weight: '0'
        _weight: '0'
```

`entity_reference` uses the same 3-level structure: pick the reference field via `derivable_context`, repeat the colon-key, then nest sources that read from the referenced entity.

## Context System

Sources that need entity data rely on Drupal's context system. Contexts are passed through `#source_contexts` in the render array:

```php
$build = [
  '#type' => 'component',
  '#component' => 'my_theme:card',
  '#ui_patterns' => $configuration,
  '#source_contexts' => [
    'entity' => EntityContext::fromEntity($entity),
    'bundle' => new Context(ContextDefinition::create('string'), $entity->bundle()),
  ],
];
```

The `ChainContextEntityResolver` service attempts to discover entity context automatically in Layout Builder and Field Layout integrations.

## Common Mistakes

- **Wrong**: `field_formatter:block_content:field_image` → **Right**: `field_formatter:block_content:hero:field_image` — the ID carries a bundle segment (empty for base fields), unlike `field_property`. Writing the wrong shape yields no plugin, and `ComponentElementBuilder::buildSource()` catches only `ContextException`, so the resulting `PluginNotFoundException` escapes the `#pre_render` and takes the page down.
- **Wrong**: `formatter: { responsive_image_style: ... }` inside a `field_formatter` inner source → **Right**: `settings: { responsive_image_style: ... }`. The unknown `formatter:` key is silently ignored, so the field renders with the formatter's defaults and no warning.
- **Wrong**: `source_id: 'entity_link:node'` → **Right**: `entity_link` has no deriver — the plugin ID is always the bare string `entity_link`, regardless of entity type.
- **Wrong**: Reading plugin IDs out of `config/schema/*.yml` → **Right**: The schema records what somebody declared; the `#[Source]` attribute and its deriver mint the ID that actually resolves. They disagree at least once in this module: the schema key `ui_patterns_source.attributes_class` can never match, because the plugin ID is `class_attribute`.
- **Wrong**: Omitting the colon-keyed middle nesting in `entity_field` → **Right**: The literal `'field:entity_type:bundle:field_name'` key is required. Without it, the inner source is never reached and the slot renders empty.
- **Wrong**: Using the slot form of `entity_field` for a prop → **Right**: Slots wrap the inner source in a `sources:` sequence; props put `source_id`/`source` directly under `value`. The wrong shape returns no source plugins and the prop is silently empty.
- **Wrong**: Configuring `entity_field` by hand from scratch → **Right**: Configure via Manage Display first, export, then study the YAML.
- **Wrong**: Expecting field sources without entity context → **Right**: Field-based sources only appear when entity context is available (Layout Builder, field formatters, Views with entity base).
- **Wrong**: Mixing UI Patterns prop type IDs with JSON Schema types → **Right**: Source `prop_types` are UI Patterns IDs (`string`, `url`, `boolean`), not JSON Schema types.

## See Also

- [Field Formatters](field-formatters.md) — Source Scoping in Per-Item Formatters
- [Variants](variants.md) — Per-Instance Variants in Layout Builder
- [Creating Custom Source Plugins](creating-custom-source-plugins.md)
- Reference: `ui_patterns/src/Plugin/UiPatterns/Source/`
