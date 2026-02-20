---
description: Source references and maintenance manifest for Drupal Blocks guides
---

# Sources & Maintenance — Drupal Blocks

## Drupal Research Install

Path: /home/camoa/workspace/contrib/web

## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Block API Overview | https://www.drupal.org/docs/drupal-apis/block-api/block-api-overview | block-system-architecture, code-reference-map | 2026-02-14 |
| Creating Custom Blocks | https://www.drupal.org/docs/creating-modules/creating-custom-blocks | creating-block-plugins, code-reference-map | 2026-02-14 |
| Create Block Plugin | https://www.drupal.org/docs/creating-modules/creating-custom-blocks/create-a-custom-block-plugin | creating-block-plugins | 2026-02-14 |
| Managing Blocks | https://www.drupal.org/docs/core-modules-and-themes/core-modules/block-module/managing-blocks | block-placement | 2026-02-14 |
| DI in Block Plugins | https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/dependency-injection-in-plugin-block | dependency-injection | 2026-02-14 |
| Drupalize.me Hello World Block | https://drupalize.me/tutorial/create-custom-hello-world-block | creating-block-plugins | 2026-02-14 |
| Specbee Programmatic Blocks | https://www.specbee.com/blogs/programmatically-creating-block-in-drupal | programmatic-operations | 2026-02-14 |
| Cache Max-Age | https://www.drupal.org/docs/drupal-apis/cache-api/cache-max-age | block-caching | 2026-02-14 |
| Cache Contexts | https://www.drupal.org/docs/drupal-apis/cache-api/cache-contexts | block-caching | 2026-02-14 |
| Block Caching Examples | https://gorannikolovski.com/blog/block-caching-examples | block-caching | 2026-02-14 |
| QED42 Block Caching | https://www.qed42.com/insights/mastering-page-and-block-caching-in-drupal | block-caching | 2026-02-14 |
| Custom Visibility Conditions | https://www.jaypan.com/tutorial/custom-drupal-block-visibility-plugins-and-condition-plugin-api | visibility-conditions | 2026-02-14 |
| Condition Plugins Visibility | https://www.therussianlullaby.com/blog/condition-plugins-for-visibility-in-drupal/ | visibility-conditions | 2026-02-14 |
| Block Content Module Docs | https://www.drupal.org/docs/core-modules-and-themes/core-modules/block-content-module | custom-block-types | 2026-02-14 |
| Layout Builder Module | https://www.drupal.org/docs/core-modules-and-themes/core-modules/layout-builder-module | layout-builder-blocks | 2026-02-14 |
| Configuration Management | https://www.drupal.org/docs/configuration-management | config-recipes | 2026-02-14 |
| Recipes Documentation | https://www.drupal.org/docs/distributions-modules-and-themes/creating-distributions/how-to-write-a-recipe | config-recipes | 2026-02-14 |
| Component Block Module | https://www.drupal.org/project/component_block | sdc-component-blocks | 2026-02-14 |
| SDC Documentation | https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components | sdc-component-blocks | 2026-02-14 |
| Drupal Security | https://www.drupal.org/docs/security | security-performance | 2026-02-14 |
| Writing Secure Code | https://www.drupal.org/docs/security/writing-secure-code | security-performance | 2026-02-14 |
| OWASP Drupal Security | https://cheatsheetseries.owasp.org/cheatsheets/Drupal_Security_Cheat_Sheet.html | security-performance | 2026-02-14 |
| Drupal Coding Standards | https://www.drupal.org/docs/develop/coding-standards | best-practices, anti-patterns | 2026-02-14 |
| Block API Reference | https://api.drupal.org/api/drupal/core%21modules%21block%21block.api.php/group/block_api | block-events-hooks, code-reference-map | 2026-02-14 |
| Core Block API | https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Block/ | code-reference-map | 2026-02-14 |
| Twig in Drupal | https://www.drupal.org/docs/theming-drupal/twig-in-drupal | block-rendering | 2026-02-14 |
| Entity API | https://www.drupal.org/docs/drupal-apis/entity-api | content-blocks, programmatic-operations | 2026-02-14 |
| Form API | https://www.drupal.org/docs/drupal-apis/form-api | block-configuration | 2026-02-14 |
| Plugin API | https://www.drupal.org/docs/drupal-apis/plugin-api/plugin-api-overview | visibility-conditions | 2026-02-14 |

## Code Sources

| Module/Component | Relative Path | Guide Files | Drupal Version |
|------------------|---------------|-------------|----------------|
| Core Block API | core/lib/Drupal/Core/Block/ | block-system-architecture, creating-block-plugins, block-configuration, block-access-control, block-caching, dependency-injection, code-reference-map | 11.x |
| Block Module | core/modules/block/ | block-system-architecture, block-placement, block-rendering, block-events-hooks, config-recipes, code-reference-map | 11.x |
| Block Content Module | core/modules/block_content/ | block-system-architecture, custom-block-types, content-blocks, programmatic-operations, layout-builder-blocks, code-reference-map | 11.x |
| Layout Builder Module | core/modules/layout_builder/ | block-system-architecture, layout-builder-blocks, code-reference-map | 11.x |
| System Module Blocks | core/modules/system/src/Plugin/Block/ | creating-block-plugins, block-configuration, block-caching, core-block-plugins, dependency-injection, best-practices, code-reference-map | 11.x |
| User Module Blocks | core/modules/user/src/Plugin/Block/ | block-access-control, core-block-plugins, dependency-injection, code-reference-map | 11.x |
| Views Module Blocks | core/modules/views/src/Plugin/Block/ | core-block-plugins, code-reference-map | 11.x |
| Search Module Blocks | core/modules/search/src/Plugin/Block/ | core-block-plugins, code-reference-map | 11.x |
| Help Module Blocks | core/modules/help/src/Plugin/Block/ | core-block-plugins | 11.x |
| Condition Plugins | core/lib/Drupal/Core/Condition/ | visibility-conditions, code-reference-map | 11.x |
| User Condition Plugin | core/modules/user/src/Plugin/Condition/ | visibility-conditions | 11.x |
| System Condition Plugins | core/modules/system/src/Plugin/Condition/ | visibility-conditions | 11.x |
| Block Templates | core/modules/block/templates/ | block-rendering | 11.x |
| Component Render Element | core/lib/Drupal/Core/Render/Element/Component.php | sdc-component-blocks | 11.x |

---

**Source Guide Version:** 1.0
**Source Last Updated:** 2026-02-14
**Partitioned:** 2026-02-19
**Target Drupal Version:** 11.x
**Total Partitions:** 22
