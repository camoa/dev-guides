---
description: Source Plugins — built-in sources, context system, source discovery and matching
drupal_version: "11.x"
---

# Source Plugins

## When to Use

> Reference this guide when choosing which source to use for a prop or slot, when debugging why a source is not appearing in the UI, or when understanding context requirements.

## Decision

Sources fall into three categories:

| Category | Description | Context Required |
|----------|-------------|-----------------|
| **Widgets** | Direct user input (textfield, checkbox, select, url) | No |
| **Drupal API sources** | Pull from menus, breadcrumbs, paths, entity fields | Sometimes |
| **Context switchers** | Change available context (entity_reference switches to referenced entity) | Yes |

## Pattern

### Built-in sources

| Source ID | Category | Prop Types | Context Required |
|-----------|----------|------------|-----------------|
| `textfield` | Widget | string, identifier | No |
| `number` | Widget | number | No |
| `checkbox` | Widget | boolean | No |
| `select` | Widget | enum | No |
| `url` | Widget | url | No |
| `attributes` | Widget | attributes | No |
| `wysiwyg` | Widget | slot | No |
| `component` | Source | slot | No |
| `block` | Source | slot | No |
| `menu` | Source | links | No |
| `token` | Source | string | Entity (optional) |
| `field_property` | Source | (derived) | Entity + Field |
| `field_formatter` | Source | slot | Entity + Field |
| `entity_link` | Source | url, links | Entity |
| `entity_field` | Source | slot | Entity + Field |
| `entity_reference` | Source | (derived) | Entity + Field |

### Source attribute declaration

```php
#[Source(
  id: 'textfield',
  label: new TranslatableMarkup('Textfield'),
  prop_types: ['string', 'identifier'],
  tags: ['widget']
)]
```

### Passing entity context

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

## Common Mistakes

- **Wrong**: Expecting field sources without entity context → **Right**: Field-based sources only appear when entity context is available (Layout Builder, field formatters, Views with entity base)
- **Wrong**: Confusing `prop_types` with JSON Schema types → **Right**: Source `prop_types` refer to UI Patterns prop type plugin IDs (`string`, `url`), not JSON Schema types
- **Wrong**: Calling a source's `getPropValue()` directly → **Right**: Use `SourcePluginManager::getSource()` to properly initialize context and configuration

## See Also

- [Creating Custom Source Plugins](creating-custom-source-plugins.md)
- [Props System](props-system.md)
- [Slots System](slots-system.md)
- Reference: [Source Plugins](https://project.pages.drupalcode.org/ui_patterns/3-devs/1-source-plugins/)
- Reference: [Component Form](https://project.pages.drupalcode.org/ui_patterns/1-users/0-component-form/)
