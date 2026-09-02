---
description: "How icon packs are discovered, validated, extracted, cached, and rendered — and which cache tags actually invalidate them"
tldr: "You need to understand how icon packs are discovered, loaded, and rendered; schema validation only runs when justinrainbow/json-schema is installed, and the render element carries no #cache of its own."
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
| Settings schema | Builds the admin settings **form** | Site builders need to pick size/color per placement |
| Library | CSS/JS dependencies | Icon fonts, custom styling, JavaScript interactions |

`settings:` never injects values into the template. It is consumed by `IconExtractorSettingsForm::generateSettingsForm()` to build Form API elements for contrib integrations (field widget, CKEditor, menu). The template gets whatever the caller passed as the third `icon()` argument, so every template must supply its own fallbacks with `|default()`.

## Pattern

Icon pack lifecycle:

```
1. Discovery: YamlDiscovery scans EXTENSION.icons.yml at each module/theme root.
   Every top-level key becomes an icon-pack plugin ID.
2. Validation: IconPackManager::validateDefinition() checks the definition against
   core/assets/schemas/v1/icon_pack.schema.json -- but ONLY if the optional
   justinrainbow/json-schema library is installed. Without it, validation is skipped
   entirely and bad definitions fail later, at render time.
3. Extraction: IconPackManager::processDefinition() instantiates the extractor plugin
   and stores the full icon list in $definition['icons'], keyed by "pack_id:icon_id".
4. Caching: definitions cached in cache.discovery under the cid 'icon_pack',
   tagged 'icon_pack_plugin' and 'icon_pack_collector'.
5. Loading: IconCollector (cache bin 'icon_info') calls the extractor's loadIcon()
   on first use of a specific icon and returns an IconDefinition.
6. Rendering: Render\Element\Icon::preRenderIcon() builds an inline_template whose
   context is extractor data + #settings + icon_id/source, and attaches `library:`.
```

Access via service container:

```php
$icon_manager = \Drupal::service('plugin.manager.icon_pack');
$definitions = $icon_manager->getDefinitions();
$icon = $icon_manager->getIcon('pack_id:icon_id');
```

Reference: `/core/lib/Drupal/Core/Theme/Icon/` for interfaces and base classes.

## Common Mistakes

- Defining icons in `config/install/` → Use `*.icons.yml` in the extension root for YAML discovery
- Adding a top-level `$schema:` key to `*.icons.yml` → Fatal. Plugin YamlDiscovery turns *every* top-level key into a plugin ID, so `$schema` is treated as an icon pack. None of the 15 `*.icons.yml` files shipped by core and contrib carry one
- Expecting the rendered icon to carry cache tags → `Render\Element\Icon` adds no `#cache` at all; invalidation happens at the plugin-definition layer, via the `icon_pack_plugin` / `icon_pack_collector` tags
- Complex logic in templates → Keep templates lean, move logic to preprocess or extractor
- Hardcoded library dependencies → Use the `library` property; `preRenderIcon()` attaches it automatically

## See Also

- [What is Icon API](what-is-icon-api.md)
- [Icon Pack Definition](icon-pack-definition.md)
- Reference: `/core/lib/Drupal/Core/Theme/Icon/Plugin/IconPackManagerInterface.php`
