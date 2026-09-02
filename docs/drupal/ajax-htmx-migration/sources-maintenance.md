---
description: "Source references and maintenance manifest for the ajax htmx migration guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install
Claims here were checked against a local Drupal install of core and the modules named below, rather than quoted from documentation.
## Web Sources
| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| AJAX subsystem now includes HTMX (Change Record) | https://www.drupal.org/node/3539472 | 1.1 | 2026-06-07 |
| AJAX API to HTMX Migration Guide | https://www.drupal.org/docs/develop/drupal-apis/htmx/ajax-api-to-htmx | 1.2 | 2026-06-07 |
| HTMX API Documentation | https://www.drupal.org/docs/develop/drupal-apis/htmx | All | 2026-06-07 |
| Replace AJAX API with HTMX Initiative | https://www.drupal.org/community-initiatives/replace-ajax-api-with-htmx | 1.1 | 2026-06-07 |
| New trait for HTMX (Change Record) | https://www.drupal.org/node/3549174 | 2.3 | 2026-06-07 |
| HTMX Official Reference | https://htmx.org/reference/ | 1.2, 8.1 | 2026-06-07 |
| HTMX Events Reference | https://htmx.org/reference/#events | 8.1 | 2026-06-07 |
| HTMX Swap Strategies | https://htmx.org/attributes/hx-swap/ | 1.2, 3.1-7.1 | 2026-06-07 |
| ARIA Live Regions | https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/ARIA_Live_Regions | 10.1 | 2026-06-07 |
| Drupal once API Change Record | https://www.drupal.org/node/3158256 | 9.1 | 2026-06-07 |

## Code Sources
| Module | Relative Path | Guide Sections | Drupal Version |
|--------|---------------|----------------|----------------|
| Drupal Core HTMX | core/lib/Drupal/Core/Htmx/ | 1.1, 1.2, 2.1-7.1, 8.2 | 11.3.11 |
| HTMX Renderer | core/lib/Drupal/Core/Render/MainContent/HtmxRenderer.php | 1.2, 4.1, 10.1 | 11.3.11 |
| HTMX JavaScript | core/misc/htmx/ | 8.1, 9.1, 10.1 | 11.3.11 |
| HTMX Test Module | core/modules/system/tests/modules/test_htmx/ | 2.1, 11.1 | 11.3.11 |
| Config Single Export Form | core/modules/config/src/Form/ConfigSingleExportForm.php | 2.1, 3.1 | 11.3.11 |
| Core AJAX Commands | core/lib/Drupal/Core/Ajax/ | 1.2, 11.1 | 11.3.11 |
