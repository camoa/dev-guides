---
description: SDC integration — how UI Patterns decorates, extends, and maintains SDC compatibility
tldr: "SDC integration — how UI Patterns decorates, extends, and maintains SDC compatibility"
drupal_version: "11.x"
---

# SDC Integration

## How UI Patterns Extends SDC

UI Patterns does not fork or replace SDC. It integrates through three mechanisms:

**1. Service Decoration**

`Drupal\ui_patterns\ComponentPluginManager` decorates `plugin.manager.sdc`, intercepting component discovery to annotate props and slots with `ui_patterns` metadata:

```yaml
# ui_patterns.services.yml
Drupal\ui_patterns\ComponentPluginManager:
  decorates: plugin.manager.sdc
  parent: plugin.manager.sdc
```

**2. Render Element Hooks**

Via `hook_element_info_alter()`, two `#pre_render` callbacks are prepended to the `component` render element:

```php
// ui_patterns.module — hook_element_info_alter()
// Note array_unshift, and note the reversed call order: the alter callback is
// pushed to the front first, then the builder is pushed in front of it, so the
// final order is [builder, alter, ...core].
array_unshift($types['component']['#pre_render'], 'ui_patterns.component_element_alter:alter');
array_unshift($types['component']['#pre_render'], 'ui_patterns.component_element_builder:build');
```

These process `#ui_patterns` configuration into `#props` and `#slots` before SDC's own rendering. If you add your own `#pre_render` to the `component` element, appending it with `[] =` puts it *after* SDC's callbacks, not after UI Patterns' — unshift if you need to run in the UI Patterns window.

**3. Twig Node Visitors**

The `TwigExtension` adds node visitors that inject normalization (`_ui_patterns_normalize_props`) before SDC's validation and preprocessing (`_ui_patterns_preprocess_props`) after validation.

## What UI Patterns Adds to Each Component

During discovery, every prop gets an `ui_patterns` annotation:

```php
$prop['ui_patterns'] = [
  'type_definition' => $propTypeInstance,  // PropTypeInterface
  'summary' => [...],                       // Human-readable constraints
  'required' => TRUE,                       // Present ONLY when required
  'prop_type_adapter' => 'adapter_id',     // Optional adapter
];
```

`ComponentPluginManager::annotateProps()` walks the component's `props.required` list and writes `['ui_patterns']['required'] = TRUE` on just those props. There is no `FALSE` branch — an optional prop has no `required` key at all. Custom code must read it as `$prop['ui_patterns']['required'] ?? FALSE`.

Two "magic" props are always added:
- **`attributes`** -- Always present, uses `ui-patterns://attributes` ref
- **`variant`** -- Present when `variants` are defined, uses `ui-patterns://variant` ref

## SDC Compatibility

Components work identically with or without UI Patterns:

- **With UI Patterns**: `#ui_patterns` configuration is resolved into `#props`/`#slots` by sources
- **Without UI Patterns**: `#props` and `#slots` are passed directly as in standard SDC usage
- **In Twig**: `{% include 'theme:component' %}` works normally; UI Patterns normalizes props regardless of how the component is invoked

## Schema References

UI Patterns registers a `ui-patterns://` stream wrapper for JSON Schema `$ref` resolution. When a prop uses `"$ref": "ui-patterns://boolean"`, the `ReferencesResolver` service resolves it to the schema defined in the `boolean` PropType plugin.

## Common Mistakes

| Mistake | Why It Is Wrong |
|---|---|
| Using UI Patterns render properties in non-UI Patterns contexts | `#ui_patterns` and `#source_contexts` are only processed when UI Patterns is installed. Standard SDC code should use `#props` and `#slots` directly. |
| Expecting UI Patterns to modify SDC validation | SDC validation runs on the normalized values. UI Patterns normalizes before validation, but validation rules are SDC's own JSON Schema validation. |

## See Also

- [Architecture](architecture.md)
- SDC Development Guide