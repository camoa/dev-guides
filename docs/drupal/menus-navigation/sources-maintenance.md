---
description: "Source references and maintenance manifest for the menus navigation guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install
Path: /home/camoa/workspace/contrib/web

## Web Sources
| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Navigation module documentation | https://www.drupal.org/docs/develop/core-modules-and-themes/core-modules/navigation-module | - | 2026-07-03 |
| Menu API | https://www.drupal.org/docs/drupal-apis/menu-api | menu-system-fundamentals | 2026-07-03 |
| Providing module-defined menu links | https://www.drupal.org/docs/drupal-apis/menu-api/providing-module-defined-menu-links | programmatic-menu-links-and-alter-hooks | 2026-07-03 |

## Code Sources
| Module | Relative Path | Guide Sections | Version |
|--------|---------------|----------------|---------|
| System (menu config schema) | core/modules/system/config/schema/system.schema.yml | menu-system-fundamentals | 11.4.5 |
| Menu Link Content | core/modules/menu_link_content/src/Entity/MenuLinkContent.php | menu-system-fundamentals, menu-access-and-permissions | 11.4.5 |
| Menu Link Content (access) | core/modules/menu_link_content/src/MenuLinkContentAccessControlHandler.php | menu-access-and-permissions | 11.4.5 |
| Core Menu library | core/lib/Drupal/Core/Menu/MenuLinkTree.php | menu-system-fundamentals | 11.4.5 |
| Core Menu library | core/lib/Drupal/Core/Menu/menu.api.php | menu-system-fundamentals, programmatic-menu-links-and-alter-hooks | 11.4.5 |
| System (menu block plugin) | core/modules/system/src/Plugin/Block/SystemMenuBlock.php | menu-blocks-and-placement, menu-caching-and-performance | 11.4.5 |
| Navigation | core/modules/navigation/ | - (scope note only) | 11.4.5 |

## Version History
| Date | Change |
|------|--------|
| 2026-07-03 | Manifest reconstructed from the guide's own citations and the installed source. |
