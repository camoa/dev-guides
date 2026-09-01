---
description: "Source references and maintenance manifest for the breadcrumbs guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install
Path: ~/workspace/contrib/web/

## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Easy Breadcrumb module page | https://www.drupal.org/project/easy_breadcrumb | 4, 5 | 2026-02-26 |
| Easy Breadcrumb setup documentation | https://www.drupal.org/docs/contributed-modules/easy-breadcrumb/setting-up-easy-breadcrumb | 4, 5 | 2026-02-26 |
| Easy Breadcrumb configuration options | https://www.drupal.org/docs/contributed-modules/easy-breadcrumb | 5 | 2026-02-26 |
| Drupal issue #3459277 — enforce CacheableMetadata in applies() | https://www.drupal.org/project/drupal/issues/3459277 | 6, 11 | 2026-02-26 |
| Easy Breadcrumb issue #3500483 — Drupal 10.4 applies() second arg | https://www.drupal.org/project/easy_breadcrumb/issues/3500483 | 6, 11 | 2026-02-26 |
| hook_system_breadcrumb_alter API | https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Menu!menu.api.php/function/hook_system_breadcrumb_alter | 7 | 2026-02-26 |
| Schema.org BreadcrumbList | https://schema.org/BreadcrumbList | 8 | 2026-02-26 |
| Google structured data — breadcrumbs | https://developers.google.com/search/docs/appearance/structured-data/breadcrumb | 8 | 2026-02-26 |
| WAI-ARIA breadcrumb pattern | https://www.w3.org/WAI/ARIA/apg/patterns/breadcrumb/ | 9 | 2026-02-26 |
| WCAG G65 — breadcrumb trail technique | https://www.w3.org/WAI/WCAG21/Techniques/general/G65 | 9, 13 | 2026-02-26 |
| SystemBreadcrumbBlock API | https://api.drupal.org/api/drupal/core!modules!system!src!Plugin!Block!SystemBreadcrumbBlock.php/11.x | 12 | 2026-02-26 |
| DaisyUI breadcrumbs component | https://daisyui.com/components/breadcrumbs/ | 10 | 2026-02-26 |

## Code Sources

| Module | Relative Path | Guide Sections | Drupal Version |
|--------|---------------|----------------|----------------|
| Drupal Core — Breadcrumb API | core/lib/Drupal/Core/Breadcrumb/ | 1, 2, 3, 6, 11 | 11.x |
| System module — PathBasedBreadcrumbBuilder | core/modules/system/src/PathBasedBreadcrumbBuilder.php | 3 | 11.x |
| System module — SystemBreadcrumbBlock | core/modules/system/src/Plugin/Block/SystemBreadcrumbBlock.php | 12 | 11.x |
| System module — breadcrumb template | core/modules/system/templates/breadcrumb.html.twig | 9 | 11.x |
| Taxonomy module — TermBreadcrumbBuilder | core/modules/taxonomy/src/TermBreadcrumbBuilder.php | 3, 6 | 11.x |
| Comment module — CommentBreadcrumbBuilder | core/modules/comment/src/CommentBreadcrumbBuilder.php | 3 | 11.x |
| Help module — HelpBreadcrumbBuilder | core/modules/help/src/HelpBreadcrumbBuilder.php | 3 | 11.x |
| Demo Umami profile — breadcrumb block config | core/profiles/demo_umami/config/install/block.block.umami_breadcrumbs.yml | 12 | 11.x |
| Easy Breadcrumb module | modules/contrib/easy_breadcrumb/src/ | 4, 5, 7, 8 | 2.x |
| UI Suite DaisyUI — breadcrumbs component | themes/contrib/ui_suite_daisyui/components/breadcrumbs/ | 10 | alpha6+ |
| UI Suite DaisyUI — breadcrumb template | themes/contrib/ui_suite_daisyui/templates/system/breadcrumb.html.twig | 10 | alpha6+ |
