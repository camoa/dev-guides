---
description: UI Patterns plugin system — managers, services, and rendering pipeline
drupal_version: "10.3+ / 11"
---

## Architecture

### Plugin System Overview

UI Patterns introduces four plugin types managed by dedicated plugin managers:

| Plugin Type | Manager Service | Attribute | Namespace |
|---|---|---|---|
| **Source** | `plugin.manager.ui_patterns_source` | `#[Source]` | `Plugin/UiPatterns/Source` |
| **PropType** | `plugin.manager.ui_patterns_prop_type` | `#[PropType]` | `Plugin/UiPatterns/PropType` |
| **PropTypeAdapter** | `plugin.manager.ui_patterns_prop_type_adapter` | `#[PropTypeAdapter]` | `Plugin/UiPatterns/PropTypeAdapter` |
| **DerivableContext** | `plugin.manager.ui_patterns_derivable_context` | `#[DerivableContext]` | `Plugin/UiPatterns/DerivableContext` |

Additionally, the core SDC plugin manager is **decorated**:

```
Drupal\ui_patterns\ComponentPluginManager
  decorates: plugin.manager.sdc
  parent: plugin.manager.sdc
```

This decoration intercepts `alterDefinition()` to annotate every prop and slot with `ui_patterns` metadata (type_definition, summary, required status, prop_type_adapter).

### Rendering Pipeline

The rendering pipeline for a UI Patterns component:

1. An integration (block, layout, formatter, views) builds a render array:
   ```php
   ['#type' => 'component', '#component' => $id, '#ui_patterns' => $config, '#source_contexts' => $contexts]
   ```
2. `ComponentElementBuilder::build()` fires as a `#pre_render` callback (registered via `hook_element_info_alter()`).
3. For each prop/slot, it instantiates the configured **source plugin** and calls `$source->getValue($prop_type)`.
4. Source values pass through `hook_ui_patterns_source_value_alter()`.
5. Values are added to `#props` (typed data) or `#slots` (render arrays).
6. `ComponentElementAlter::alter()` fires next, normalizing slots and processing `#attributes`.
7. The Twig extension's `normalizeProps()` runs before SDC's validator, converting values via `PropType::normalize()`.
8. After validation, `preprocessProps()` runs `PropType::preprocess()` to prepare template-ready values.
9. SDC's Twig template receives the processed props and slots.

### Service Architecture

Key services from `ui_patterns.services.yml`:

```yaml
# Decorates core SDC manager -- the central entry point
Drupal\ui_patterns\ComponentPluginManager:
  decorates: plugin.manager.sdc

# Builds render elements from configuration + sources
ui_patterns.component_element_builder:
  class: Drupal\ui_patterns\Element\ComponentElementBuilder

# Post-build normalization (slots, attributes)
ui_patterns.component_element_alter:
  class: Drupal\ui_patterns\Element\ComponentElementAlter

# JSON schema resolution for ui-patterns:// refs
ui_patterns.schema_stream_wrapper:
  tags: [{ name: stream_wrapper, scheme: ui-patterns }]

# Schema compatibility checking (prop type guessing)
ui_patterns.schema_compatibility_checker:
  class: Drupal\ui_patterns\SchemaManager\CompatibilityChecker

# Twig extension: normalize/preprocess + add_class/set_attribute filters
ui_patterns.twig.extension:
  class: Drupal\ui_patterns\Template\TwigExtension
```

### Common Mistakes

| Mistake | Why It Is Wrong |
|---|---|
| Assuming UI Patterns replaces SDC | UI Patterns decorates SDC; components are still SDC components. Removing UI Patterns should not break templates. |
| Calling source plugins directly in custom code | Sources are managed by `SourcePluginManager`; use `getSource()` to properly initialize context and configuration. |
| Not clearing caches after adding/changing components | The decorated `ComponentPluginManager` caches definitions; use `drush cr` when component YAML changes. |

### See Also

- [Source Plugins](#source-plugins)
- [Props System](#props-system)
- SDC Development Guide