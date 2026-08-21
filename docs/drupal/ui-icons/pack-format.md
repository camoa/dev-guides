---
description: "Author an *.icons.yml icon pack: schema, naming convention, discovery rules, and library wiring."
tldr: "Declare pack_id, extractor, config.sources, optional settings, and a required Twig template in {module|theme}.icons.yml at the extension root. Omitting template throws an exception, not blank output; a library: key is the only way to attach CSS/@font-face to a pack."
drupal_version: "11.x"
---

# Icon Pack Format

## When to Use

> Authoring `*.icons.yml` at the root of a module or theme.

## Pattern

**File location**: `{module|theme}/{module|theme_name}.icons.yml`

**Canonical schema**:

```yaml
pack_id:                            # machine name; appears as `pack_id:icon_id` in references
  enabled: true                     # optional, default true
  label: "Pack label"               # optional, translatable
  description: "Pack description"   # optional, translatable
  links:                            # optional reference URLs
    - https://my-icon-source.example
  version: "1.0.0"                  # optional
  license:                          # optional
    name: "MIT"
    url: "https://opensource.org/licenses/MIT"
    gpl-compatible: true

  extractor: svg                    # REQUIRED — one of path | svg | svg_sprite | font
  config:                           # REQUIRED — extractor-specific
    sources:
      - icons/*.svg

  library: my_theme/icon-styles     # optional — asset library attached whenever
                                    # an icon of this pack renders. Format is
                                    # `extension/library_name`. This is the ONLY
                                    # way to ship @font-face or icon CSS with a pack

  settings:                         # optional per-icon configurable properties
    size:
      title: "Size"
      type: integer
      default: 24

  template: >                       # REQUIRED — Twig string interpolated at render time
    <svg xmlns="http://www.w3.org/2000/svg"
         width="{{ size|default(24) }}" height="{{ size|default(24) }}">
      {{ content|raw }}
    </svg>

  preview: ""                       # optional — distinct template for admin preview
```

## Naming Convention

- **pack_id**: lowercase, underscored, prefixed with theme/module name (`my_theme_icons`, not `icons`)
- **icon_id**: derived from filename, codepoint key, or symbol id (lowercase, hyphens preferred)

## Discovery

Core's `IconPackManager::getDiscovery()` builds a `YamlDiscovery('icons', …)`, which resolves to exactly `EXTENSION.icons.yml` at module/theme **root** (not subdirectories). Cache must be cleared after adding/changing pack files.

`*.ui_icons.yml` is **not** discovered. That name was dropped before 1.0.0 stable and there is no fallback — a pack declared in `my_theme.ui_icons.yml` simply never appears.

## Common Mistakes

- **Wrong**: putting the YAML file in a subdirectory (`icons/my_theme.icons.yml`) → **Right**: place it at the extension root; subdirectories are not discovered
- **Wrong**: using the old `*.ui_icons.yml` filename → **Right**: rename to `*.icons.yml`; the old name is silently ignored
- **Wrong**: using a generic `pack_id` like `icons` → **Right**: prefix with the theme/module name to avoid collisions
- **Wrong**: omitting `template` → **Right**: an exception, not blank output. `extractor` and `template` are both in the schema's `required` list (`core/assets/schemas/v1/icon_pack.schema.json`). With `justinrainbow/json-schema` installed, `IconPackManager::validateDefinition()` throws `IconPackConfigErrorException` at discovery — a WSOD on cache rebuild. Without that library the validator is skipped and the throw simply moves to render time, from `IconExtractorBase::createIcon()` ("Missing `template` in your definition…"). Either way, look for the exception, not for empty markup
- **Wrong**: declaring a CSS library in `*.libraries.yml` but not wiring it into the pack → **Right**: the library is never attached. Point the pack's `library:` key at it; `Icon::preRenderIcon()` attaches only what `IconDefinition::getLibrary()` returns

## See Also

- [Extractors](extractors.md)
- [Settings & Rendering](settings-rendering.md)
- [Authoring & Distribution](authoring.md)
- Reference: `core/lib/Drupal/Core/Theme/IconPackManager.php`
- Reference: `core/assets/schemas/v1/icon_pack.schema.json`
