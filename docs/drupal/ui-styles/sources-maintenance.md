---
description: "Source references and maintenance manifest for the ui styles guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Research Install
Claims here were checked against a local Drupal install of core and the modules named below, rather than quoted from documentation.
## Web Sources
No web sources are cited in the guide body. The two `https://example.com/...` URLs in Section 3 are placeholder values inside a YAML schema example, not citations.

## Code Sources
| Module | Relative Path | Guide Sections | Version |
|--------|---------------|----------------|---------|
| UI Styles | modules/contrib/ui_styles/ | 1-4, 12-16 | 8.x-1.21 |
| UI Styles Block | modules/contrib/ui_styles/modules/ui_styles_block/ | 5 | 8.x-1.21 |
| UI Styles Layout Builder | modules/contrib/ui_styles/modules/ui_styles_layout_builder/ | 6 | 8.x-1.21 |
| UI Styles CKEditor 5 | modules/contrib/ui_styles/modules/ui_styles_ckeditor5/ | 7 | 8.x-1.21 |
| UI Styles Views | modules/contrib/ui_styles/modules/ui_styles_views/ | 8 | 8.x-1.21 |
| UI Styles Page | modules/contrib/ui_styles/modules/ui_styles_page/ | 9 | 8.x-1.21 |
| UI Styles UI Patterns | modules/contrib/ui_styles/modules/ui_styles_ui_patterns/ | 10 | 8.x-1.21 |
| UI Styles Library | modules/contrib/ui_styles/modules/ui_styles_library/ | 2 | 8.x-1.21 |
| sabberworm/php-css-parser (Composer, external) | contrib/vendor/sabberworm/ (outside the web root above) | 12 | not verified in this pass — package present, version not read from its own composer.json |

## Version History
| Date | Change |
|------|--------|
| 2026-08-20 | Manifest reconstructed from the guide's own citations and the installed source. |
