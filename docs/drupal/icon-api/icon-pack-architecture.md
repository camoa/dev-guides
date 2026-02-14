---
description: Icon pack discovery, loading, and rendering lifecycle for efficient icon systems
drupal_version: "11.x"
---

# Icon Pack Architecture

## When to Use

You need to understand how icon packs are discovered, loaded, and rendered to design efficient icon systems or troubleshoot icon discovery issues.

## Decision

| Component | Purpose | When to customize |
|---|---|---|
| YAML definition (`*.icons.yml`) | Declares icon packs | Every theme/module with icons |
| Extractor plugin | Discovers and loads icons | Custom icon sources (API, database, computed) |
| Template | Renders icon markup | Custom HTML structure, CSS classes, attributes |
| Settings schema | User-configurable options | Icons need runtime customization (size, color, style) |
| Library | CSS/JS dependencies | Icon fonts, custom styling, JavaScript interactions |

## Pattern

Icon pack lifecycle:

```
1. Discovery: Drupal scans *.icons.yml files
2. Validation: Schema validation against core/assets/schemas/v1/metadata.schema.json
3. Plugin creation: IconPackManager creates IconPackInterface instances
4. Extraction: Extractor discovers icons from sources
5. Caching: Definitions cached with 'icon_pack_plugin' tag
6. Rendering: Template receives variables from extractor + settings
7. Output: Render array with cache tags for invalidation
```

Access via service container:

```php
$icon_manager = \Drupal::service('plugin.manager.icon_pack');
$definitions = $icon_manager->getDefinitions();
$icon = $icon_manager->getIcon('pack_id:icon_id');
```

Reference: `/core/lib/Drupal/Core/Theme/Icon/` for interfaces and base classes.

## Common Mistakes

- **Wrong**: Defining icons in `config/install/` → **Right**: Use `*.icons.yml` in root for YAML discovery
- **Wrong**: Forgetting cache tags → **Right**: Icons won't update on config changes
- **Wrong**: Complex logic in templates → **Right**: Keep templates lean, move logic to preprocess or extractor
- **Wrong**: Missing schema validation → **Right**: Use `$schema` property for IDE validation and error detection
- **Wrong**: Hardcoded library dependencies → **Right**: Use `library` property for automatic attachment

## See Also

- [What is Icon API](what-is-icon-api.md)
- [Icon Pack Definition](icon-pack-definition.md)
- Reference: `/core/lib/Drupal/Core/Theme/Icon/Plugin/IconPackInterface.php`
