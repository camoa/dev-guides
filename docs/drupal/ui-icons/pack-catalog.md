---
description: Pick off-the-shelf icon packs (Bootstrap Icons, Heroicons, FontAwesome, etc.) instead of authoring a custom pack.
tldr: The UI Icons Example repository provides ready-to-use *.icons.yml declarations for popular packs — drop the YAML and icon files into your theme. Several UI Suite themes bundle packs by default (Bootstrap Icons, Heroicons, USWDS). Copy assets locally rather than referencing CDN URLs for production reliability.
drupal_version: "11.x"
---

# Pre-built Pack Catalog

## When to Use

> Picking off-the-shelf icon packs instead of authoring a custom pack.

## Pattern

The community **UI Icons Example** repository ships ready-to-use `*.icons.yml` declarations:
https://gitlab.com/ui-icons/ui-icons-example

Drop the YAML into your theme/module alongside the upstream icon files.

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
| Material Symbols | fonts.google.com/icons | font or svg | Apache 2.0 |
| FontAwesome (free) | fontawesome.com | font with codepoints | CC-BY 4.0 + SIL OFL |
| Maki | labs.mapbox.com/maki-icons | svg | CC0 |
| Evil | evil-icons.io | svg | MIT |
| Delta | delta-icons.github.io | svg | MIT |

## Pre-bundled in UI Suite Themes

| UI Suite theme | Icon pack(s) included |
|---|---|
| `ui_suite_bootstrap` | Bootstrap Icons |
| `ui_suite_dsfr` | DSFR icons (French gov) |
| `ui_suite_uswds` | USWDS icons (243 icons) |
| `ui_suite_daisyui` | Heroicons |

## Decision: copy assets vs link to CDN

| Approach | Pros | Cons |
|---|---|---|
| Copy SVG files into module/theme | Offline, version-pinned, no CORS | Repo size grows |
| Reference CDN URLs in `path` extractor | Tiny repo | Network dependency, cache concerns, possible CORS |

For production sites, copying assets is the safer default.

## Common Mistakes

- **Wrong**: mixing licenses without attribution → **Right**: CC-BY (FontAwesome free) requires attribution; read each pack's license
- **Wrong**: importing all 1000+ icons of a pack when 30 are used → **Right**: restrict to a subdirectory in the source glob to keep the admin Library page performant

## See Also

- [Authoring & Distribution](authoring.md)
- [Extractors](extractors.md)
- Reference: https://gitlab.com/ui-icons/ui-icons-example
