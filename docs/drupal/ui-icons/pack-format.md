---
description: "Author an *.icons.yml icon pack: schema, naming convention, and discovery rules."
tldr: "Declare pack_id, extractor, config.sources, optional settings, and a required Twig template in {module|theme}.icons.yml at the extension root. Prefix pack_id with the theme/module name; the old *.ui_icons.yml filename is not discovered."
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
- **Wrong**: omitting `template` → **Right**: icons are discoverable but render empty markup without it

## See Also

- [Extractors](extractors.md)
- [Settings & Rendering](settings-rendering.md)
- [Authoring & Distribution](authoring.md)
- Reference: `core/lib/Drupal/Core/Theme/IconPackManager.php`
