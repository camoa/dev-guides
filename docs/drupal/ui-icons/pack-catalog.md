---
description: "Off-the-shelf icon pack YAML declarations to adapt, plus which UI Suite themes bundle a pack already."
tldr: "The community UI Icons Example repository provides starting-point *.icons.yml declarations for Bootstrap Icons, Heroicons, Lucide, FontAwesome, and more — copy, adapt, add the icon files. Several UI Suite themes already bundle a pack."
drupal_version: "11.x"
---

# Pre-built Pack Catalog

## When to Use

> Picking off-the-shelf icon packs instead of authoring one.

## Pattern

The community **UI Icons Example** repository (https://gitlab.com/ui-icons/ui-icons-example) ships example `*.icons.yml` declarations for popular packs — starting points to adapt, not drop-in packs. Copy the YAML into your theme/module, adjust the `sources` globs and template to your layout, and add the upstream icon files yourself.

## Catalog

| Pack | Source | Extractor | License |
|---|---|---|---|
| Bootstrap Icons | icons.getbootstrap.com | svg | MIT |
| Heroicons | heroicons.com | svg | MIT |
| Lucide | lucide.dev | svg | ISC |
| Tabler Icons | tabler-icons.io | svg | MIT |
| Phosphor | phosphoricons.com | svg | MIT |
| Remix Icons | remixicon.com | svg | Apache 2.0 |
| Feather | feathericons.com | svg | MIT |
| Octicons | primer.style | svg | MIT |
| Material Symbols | fonts.google.com/icons | font (web) or svg | Apache 2.0 |
| FontAwesome (free) | fontawesome.com | font with codepoints | CC-BY 4.0 + SIL OFL |
| Maki | labs.mapbox.com/maki-icons | svg | CC0 |
| Evil | evil-icons.io | svg | MIT |
| Delta | delta-icons.github.io | svg | MIT |

## Pre-bundled in UI Suite Themes

| UI Suite theme | Icon pack(s) included |
|---|---|
| `ui_suite_bootstrap` | Bootstrap Icons |
| `ui_suite_dsfr` | DSFR icons (French gov) |
| `ui_suite_uswds` | USWDS icons (US federal, 243 icons) |
| `ui_suite_daisyui` | Heroicons |

## Decision: copy assets vs link to CDN

| Approach | Pros | Cons |
|---|---|---|
| Copy SVG files into the module/theme | Offline, version-pinned, no CORS | Repo size grows |
| Reference CDN URLs in `path` extractor | Tiny repo | Network dependency, cache concerns, possible CORS |

For production sites, copying assets is the safer default.

## Common Mistakes

- **Wrong**: mixing licenses without attribution → **Right**: CC-BY (FontAwesome free) requires attribution; read each pack's license
- **Wrong**: importing all 1000+ icons of a pack when 30 are used → **Right**: restrict to a subdirectory in the source glob; a huge pack hurts admin Library page performance

## See Also

- [Icon Pack Format](pack-format.md)
- [Extractors](extractors.md)
- [UI Suite DaisyUI guide](../ui-suite-daisyui/index.md)
