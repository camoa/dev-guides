---
description: UI Patterns Architecture — 4 plugin types, service decoration, rendering pipeline
drupal_version: "11.x"
---

# UI Patterns Architecture

## When to Use

> Reference this guide when debugging the rendering pipeline, understanding how UI Patterns hooks into SDC, or troubleshooting source plugin discovery.

## Decision

| Plugin Type | Manager Service | Attribute | Namespace |
|-------------|-----------------|-----------|-----------|
| **Source** | `plugin.manager.ui_patterns_source` | `#[Source]` | `Plugin/UiPatterns/Source` |
| **PropType** | `plugin.manager.ui_patterns_prop_type` | `#[PropType]` | `Plugin/UiPatterns/PropType` |
| **PropTypeAdapter** | `plugin.manager.ui_patterns_prop_type_adapter` | `#[PropTypeAdapter]` | `Plugin/UiPatterns/PropTypeAdapter` |
| **DerivableContext** | `plugin.manager.ui_patterns_derivable_context` | `#[DerivableContext]` | `Plugin/UiPatterns/DerivableContext` |

## Pattern

### Service decoration

```yaml
# ui_patterns.services.yml
Drupal\ui_patterns\ComponentPluginManager:
  decorates: plugin.manager.sdc
  parent: plugin.manager.sdc
```

The decoration intercepts `alterDefinition()` to annotate every prop and slot with `ui_patterns` metadata.

### Rendering pipeline

1. Integration builds render array: `['#type' => 'component', '#component' => $id, '#ui_patterns' => $config, '#source_contexts' => $contexts]`
2. `ComponentElementBuilder::build()` fires as `#pre_render` callback
3. For each prop/slot, instantiates the configured source plugin and calls `$source->getValue($prop_type)`
4. Source values pass through `hook_ui_patterns_source_value_alter()`
5. Values added to `#props` (typed data) or `#slots` (render arrays)
6. `ComponentElementAlter::alter()` normalizes slots and processes `#attributes`
7. `normalizeProps()` runs before SDC validation, converting values via `PropType::normalize()`
8. After validation, `preprocessProps()` runs `PropType::preprocess()`
9. SDC's Twig template receives processed props and slots

## Common Mistakes

- **Wrong**: Assuming UI Patterns replaces SDC → **Right**: UI Patterns decorates SDC; components are still SDC components
- **Wrong**: Calling source plugins directly in custom code → **Right**: Use `SourcePluginManager::getSource()` to properly initialize context and configuration
- **Wrong**: Not clearing caches after adding/changing components → **Right**: Use `drush cr`; the decorated `ComponentPluginManager` caches definitions

## See Also

- [Source Plugins](source-plugins.md)
- [Props System](props-system.md)
- [SDC Integration](sdc-integration.md)
- Reference: `modules/contrib/ui_patterns/src/`
