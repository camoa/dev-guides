---
description: "Source references and maintenance manifest for the ui icons guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install
Path: /home/camoa/workspace/contrib/web

## Web Sources
| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| UI Icons Example (community pack catalog) | https://gitlab.com/ui-icons/ui-icons-example | 14 | 2026-08-16 |

The guide's other two `http`/`https` strings are placeholder values inside YAML sample code (`https://my-icon-source.example` in the `links:` example, `https://opensource.org/licenses/MIT` in the `license:` example), not cited sources. They are omitted from this table.

## Code Sources
| Module | Relative Path | Guide Sections | Version |
|--------|---------------|----------------|---------|
| UI Icons (base) | modules/contrib/ui_icons/ | 1-3, 5, 12-16 | 1.1.2 |
| UI Icons Field | modules/contrib/ui_icons/modules/ui_icons_field/ | 2, 6 | 1.1.2 |
| UI Icons CKEditor 5 | modules/contrib/ui_icons/modules/ui_icons_ckeditor5/ | 2, 7 | 1.1.2 |
| UI Icons Text | modules/contrib/ui_icons/modules/ui_icons_text/ | 2, 7 | 1.1.2 |
| UI Icons Patterns | modules/contrib/ui_icons/modules/ui_icons_patterns/ | 2, 8 | 1.1.2 |
| UI Icons Menu | modules/contrib/ui_icons/modules/ui_icons_menu/ | 2, 9 | 1.1.2 |
| UI Icons Media | modules/contrib/ui_icons/modules/ui_icons_media/ | 2, 11 | 1.1.2 |
| UI Icons Library | modules/contrib/ui_icons/modules/ui_icons_library/ | 2, 12 | 1.1.2 |
| UI Icons Font | modules/contrib/ui_icons/modules/ui_icons_font/ | 2, 4 | 1.1.2 |
| UI Icons Picker | modules/contrib/ui_icons/modules/ui_icons_picker/ | 2 | 1.1.2 |
| UI Icons Backport (deprecated placeholder) | modules/contrib/ui_icons/modules/ui_icons_backport/ | 2 | 1.1.2 |
| UI Icons Iconify API (deprecated placeholder) | modules/contrib/ui_icons/modules/ui_icons_iconify_api/ | 2 | 1.1.2 |
| Drupal core Icon API | core/lib/Drupal/Core/Theme/Icon/ | 1, 10 | 11.4.5 |
| Drupal core icon extractors (path, svg, svg_sprite) | core/lib/Drupal/Core/Theme/Plugin/IconExtractor/ | 4 | 11.4.5 |
| Drupal Canvas | modules/contrib/canvas/ | 6 | 1.10.1 |

`ui_icons_canvas` is cited throughout the guide (Sections 1, 6, 16) as an unverified 2.0.0 claim. No such directory exists under the installed 1.1.2 tree, so it has no row above — its absence is itself part of the evidence the guide records.

This guide documents `ui_icons` 2.0.0, but 2.0.0 cannot be installed on the research site (see the verification note in Section 1: `ui_suite_daisyui` pins `drupal/ui_icons: ^1.1`). Every row above reflects what was actually read on disk — UI Icons 1.1.2, Drupal core 11.4.5, Drupal Canvas 1.10.1 — not the 2.0.0 target. Claims that are 2.0.0-only and unverified are flagged inline in the guide body, not listed here as if code-verified.

## Version History
| Date | Change |
|------|--------|
| 2026-08-16 | Manifest reconstructed from the guide's own citations and the installed source. |
