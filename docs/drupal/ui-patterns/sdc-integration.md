---
description: SDC Integration — service decoration, pre_render hooks, Twig node visitors
drupal_version: "11.x"
---

# SDC Integration

## When to Use

> Reference this guide when understanding how UI Patterns hooks into Drupal core SDC without forking it, or when ensuring components remain compatible with both SDC-only and UI Patterns contexts.

## Decision

| Mechanism | What It Does |
|-----------|-------------|
| Service decoration | Intercepts SDC plugin discovery to annotate props/slots with `ui_patterns` metadata |
| `#pre_render` hooks | Processes `#ui_patterns` config into `#props`/`#slots` before SDC renders |
| Twig node visitors | Injects normalize/preprocess steps around SDC's validation |

## Pattern

### Service decoration

```yaml
# ui_patterns.services.yml
Drupal\ui_patterns\ComponentPluginManager:
  decorates: plugin.manager.sdc
  parent: plugin.manager.sdc
```

### Pre-render hooks (registered via `hook_element_info_alter`)

```php
$types['component']['#pre_render'][] = 'ui_patterns.component_element_builder:build';
$types['component']['#pre_render'][] = 'ui_patterns.component_element_alter:alter';
```

### Magic props added to every component

- **`attributes`** — Always present, uses `ui-patterns://attributes` ref
- **`variant`** — Present when `variants` are defined, uses `ui-patterns://variant` ref

### SDC compatibility

- **With UI Patterns**: `#ui_patterns` configuration resolved into `#props`/`#slots` by sources
- **Without UI Patterns**: `#props` and `#slots` passed directly as in standard SDC
- **In Twig**: `{% include 'theme:component' %}` works normally; UI Patterns normalizes props regardless of invocation method

## Common Mistakes

- **Wrong**: Using `#ui_patterns` and `#source_contexts` in code that runs without UI Patterns installed → **Right**: Standard SDC code should use `#props` and `#slots` directly
- **Wrong**: Expecting UI Patterns to modify SDC JSON Schema validation rules → **Right**: UI Patterns normalizes before validation; validation rules remain SDC's own

## See Also

- [Architecture](architecture.md)
- Reference: `modules/contrib/ui_patterns/src/ComponentPluginManager.php`
- Reference: [UI Patterns FAQ](https://project.pages.drupalcode.org/ui_patterns/faq/)
