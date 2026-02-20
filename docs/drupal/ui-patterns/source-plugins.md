---
description: Source plugins — widgets, API sources, and context-dependent data for component props/slots
drupal_version: "10.3+ / 11"
---

## Source Plugins

### What Sources Are

Source plugins provide data to props and slots. They are the mechanism by which Drupal's data (entity fields, menus, blocks, user input) flows into component props and slots. Every prop and slot value in a UI Patterns configuration comes from a source plugin.

Sources fall into three categories:

1. **Widgets** -- Direct user input (textfield, checkbox, select, number, URL, WYSIWYG). Tagged `widget`. Store values directly in configuration.
2. **Drupal API sources** -- Pull data from Drupal systems. Context-independent (menu, breadcrumb, path) or context-dependent (entity fields, entity links, field labels, field formatters, blocks).
3. **Context switchers** -- Change the available context without providing a value themselves (e.g., selecting an entity reference field switches context to the referenced entity, making its fields available as sources).

### Source Discovery and Matching

The `SourcePluginManager` filters available sources for each prop/slot based on:

1. **Prop type compatibility** -- Sources declare `prop_types` in their `#[Source]` attribute. Only sources matching the prop's type (or a convertible type) appear.
2. **Context requirements** -- Sources can require specific contexts (entity, bundle, field items) via `context_requirements`. Only sources whose context is satisfied appear.
3. **Tag filtering** -- Sources are filtered by tags (e.g., `widget` sources are excluded from some contexts).

```php
// Source attribute example:
#[Source(
  id: 'textfield',
  label: new TranslatableMarkup('Textfield'),
  prop_types: ['string', 'identifier'],  // Works with these prop types
  tags: ['widget']                         // Categorization tag
)]
```

### Built-in Source Plugins

| Source ID | Category | Prop Types | Context Required | Description |
|---|---|---|---|---|
| `textfield` | Widget | string, identifier | No | Single-line text input |
| `number` | Widget | number | No | Numeric input |
| `checkbox` | Widget | boolean | No | Boolean toggle |
| `select` | Widget | enum | No | Dropdown select |
| `selects` | Widget | enum_list | No | Multiple select |
| `checkboxes` | Widget | enum_set | No | Checkbox group |
| `url` | Widget | url | No | URL input field |
| `attributes` | Widget | attributes | No | Key-value attribute pairs |
| `class_attribute` | Widget | attributes | No | CSS class input |
| `list_textarea` | Widget | list | No | Multi-line list input |
| `wysiwyg` | Widget | slot | No | CKEditor rich text |
| `component` | Source | slot | No | Nested SDC component |
| `block` | Source | slot | No | Drupal block plugin |
| `menu` | Source | links | No | Menu tree |
| `breadcrumb` | Source | links | No | Breadcrumb trail |
| `path` | Source | url, string | No | Current path |
| `token` | Source | string | Entity (optional) | Token replacement |
| `field_property` | Source | (derived) | Entity + Field | Entity field property value |
| `field_formatter` | Source | slot | Entity + Field | Field rendered through formatter |
| `field_label` | Source | string | Entity + Field | Field label text |
| `entity_link` | Source | url, links | Entity | Entity canonical/edit URLs |
| `entity_field` | Source | slot | Entity + Field | Entity field rendered as slot content |
| `entity_reference` | Source | (derived) | Entity + Field | Switches context to a referenced entity |

### Context System

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

### Common Mistakes

| Mistake | Why It Is Wrong |
|---|---|
| Expecting field sources without entity context | Field-based sources are derived per entity type + bundle + field. They only appear when entity context is available (Layout Builder, field formatters, Views with entity base). |
| Confusing prop_types with JSON Schema types | Source `prop_types` refer to UI Patterns prop type plugin IDs (`string`, `url`, `boolean`), not JSON Schema types (`string`, `number`, `integer`). |
| Not understanding source derivation | Field sources use derivers (`FieldPropertySourceDeriver`, `FieldFormatterSourceDeriver`) to create one source plugin per entity-type/bundle/field combination. The base source ID is just the template. |

### See Also

- [Creating Custom Source Plugins](#creating-custom-source-plugins)
- [Props System](#props-system)
- [Slots System](#slots-system)