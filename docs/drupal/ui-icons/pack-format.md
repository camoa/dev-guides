---
description: Author a *.icons.yml icon pack declaration for a Drupal theme or module.
tldr: Place {name}.icons.yml at the theme/module root (not a subdirectory); declare pack_id, extractor, config.sources, optional settings, and a Twig template. Prefix pack_id with the theme/module name to avoid collisions; omitting template leaves icons discoverable but rendering as empty markup.
drupal_version: "11.x"
---

# Icon Pack Format

## When to Use

> Authoring `*.icons.yml` (or `*.ui_icons.yml`) at the root of a module or theme to declare an icon pack.

## Decision: file extension

| File | Discovered? | Notes |
|---|---|---|
| `my_theme.icons.yml` | Yes | Recommended (newer convention) |
| `my_theme.ui_icons.yml` | Yes | Legacy/alternate; works the same |

## Pattern

```yaml
pack_id:                            # machine name; appears as `pack_id:icon_id` in references
  enabled: true                     # optional, default true
  label: "Pack label"               # optional, translatable
  description: "Pack description"   # optional

  extractor: svg                    # REQUIRED — one of path | svg | svg_sprite | font
  config:                           # REQUIRED
    sources:
      - icons/*.svg

  settings:                         # optional per-icon configurable properties
    size:
      title: "Size"
      type: integer                 # integer | string | boolean | number
      default: 24
      minimum: 8
      maximum: 96
      multipleOf: 4
    color:
      title: "Color"
      type: string
      format: color                 # renders color picker
    decorative:
      title: "Decorative"
      type: boolean
      default: false
    variant:
      title: "Variant"
      type: string
      enum: ["solid", "outline", "duotone"]

  template: >                       # REQUIRED — Twig string interpolated at render time
    <svg xmlns="http://www.w3.org/2000/svg"
         width="{{ size|default(24) }}"
         height="{{ size|default(24) }}"
         {% if color %}fill="{{ color }}"{% endif %}
         {% if decorative %}aria-hidden="true"{% endif %}>
      {{ content|raw }}
    </svg>

  preview: ""                       # optional — distinct template for admin preview
```

## Naming Convention

- **pack_id**: lowercase, underscored, prefixed with theme/module name (`my_theme_icons`, not `icons`)
- **icon_id**: derived from filename, codepoint key, or symbol id (lowercase, hyphens preferred)

## Discovery

Drupal's plugin discovery scans `*.icons.yml` and `*.ui_icons.yml` at module/theme **root** only — not subdirectories. Clear cache after adding or changing pack files.

## Common Mistakes

- **Wrong**: putting the YAML file in a subdirectory (`icons/my_theme.icons.yml`) → **Right**: place it at the module/theme root
- **Wrong**: using a generic `pack_id` like `icons` → **Right**: always prefix with the theme/module name to avoid collisions
- **Wrong**: omitting `template` → **Right**: icons are discoverable but render as empty markup without it

## See Also

- [Extractors](extractors.md)
- [Settings & Rendering](settings-rendering.md)
- [Authoring & Distribution](authoring.md)
