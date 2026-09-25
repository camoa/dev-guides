---
description: "Source references and maintenance manifest for the config management guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install
Claims here were checked against a local Drupal install of core and the modules named below, rather than quoted from documentation.
## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Configuration Management Overview | https://www.drupal.org/docs/administering-a-drupal-site/configuration-management | 1.0, 10.0 | 2026-02-14 |
| Configuration API Documentation | https://www.drupal.org/docs/drupal-apis/configuration-api | 1.0, 6.0, 22.0 | 2026-02-14 |
| Configuration Schema/Metadata | https://www.drupal.org/docs/drupal-apis/configuration-api/configuration-schemametadata | 3.0, 4.0, 5.0 | 2026-02-14 |
| Managing Your Site's Configuration | https://www.drupal.org/docs/administering-a-drupal-site/configuration-management/managing-your-sites-configuration | 10.0, 17.0 | 2026-02-14 |
| Configuration Data Types | https://drupalize.me/tutorial/configuration-data-types | 2.0, 4.0 | 2026-02-14 |
| What Are Configuration Entities? | https://drupalize.me/tutorial/what-are-configuration-entities | 2.0, 7.0 | 2026-02-14 |
| Creating a Configuration Entity Type | https://www.drupal.org/docs/drupal-apis/configuration-api/creating-a-configuration-entity-type | 7.0, 8.0 | 2026-02-14 |
| Configuration Entity Dependencies | https://www.drupal.org/docs/drupal-apis/configuration-api/configuration-entity-dependencies | 14.0 | 2026-02-14 |
| Config Dependencies Can Optionally Be Enforced | https://www.drupal.org/node/2404447 | 14.0 | 2026-02-14 |
| Configuration Split Documentation | https://www.drupal.org/docs/contributed-modules/configuration-split | 13.0 | 2026-02-14 |
| Creating a Simple Split Configuration | https://www.drupal.org/docs/contributed-modules/configuration-split/creating-a-simple-split-configuration-dev-modules-only-in-dev-environments | 13.0 | 2026-02-14 |
| Understanding Drupal Configuration Synchronisation | https://www.specbee.com/blogs/understanding-drupal-configuration-synchronisation | 1.0, 10.0 | 2026-02-14 |
| Drupal Configuration Management Best Practices | https://it.umn.edu/services-technologies/how-tos/drupal-configuration-management | 19.0 | 2026-02-14 |
| Stricter Validation for Config Schema | https://www.drupal.org/node/3404425 | 3.0, 5.0, 21.0 | 2026-02-14 |
| Configuration Override System | https://www.drupal.org/docs/drupal-apis/configuration-api/configuration-override-system | 12.0 | 2026-02-14 |
| Providing Default Configuration | https://www.drupal.org/docs/drupal-apis/configuration-api/providing-default-configuration | 16.0 | 2026-02-14 |
| Recipes Initiative | https://www.drupal.org/project/distributions_recipes | 18.0 | 2026-02-14 |
| Drush Deploy Command | https://www.drush.org/latest/commands/deploy/ | 17.0 | 2026-09-24 |
| Update Hooks Changing Config (Issue #3110362) | https://www.drupal.org/project/drupal/issues/3110362 | 17.0, 17.1 | 2026-09-24 |
| Drush Deploy (update function types) | https://www.drush.org/13.x/deploycommand/ | 17.1 | 2026-09-24 |
| hook_update_N() API | https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Extension!module.api.php/function/hook_update_N | 17.1 | 2026-09-24 |
| hook_post_update_NAME() API | https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Extension!module.api.php/function/hook_post_update_NAME | 17.1 | 2026-09-24 |

## Code Sources

| Module | Relative Path | Guide Sections | Drupal Version |
|--------|---------------|----------------|----------------|
| Core Config API | `core/lib/Drupal/Core/Config/` | 1.0, 6.0, 9.0, 10.0, 12.0, 15.0, 22.0 | 11.x |
| Core Config Entity | `core/lib/Drupal/Core/Config/Entity/` | 7.0, 8.0, 14.0, 22.0 | 11.x |
| Core Config Schema | `core/lib/Drupal/Core/Config/Schema/` | 3.0, 4.0, 5.0, 22.0 | 11.x |
| Core Config Module | `core/modules/config/` | 10.0, 11.0, 22.0 | 11.x |
| System Module | `core/modules/system/` | 3.0, 4.0, 5.0 | 11.x |
| Field Module | `core/modules/field/` | 8.0, 22.0 | 11.x |
| Views Module | `core/modules/views/` | 8.0, 22.0 | 11.x |
| Language Module | `core/modules/language/` | 12.0, 22.0 | 11.x |
| Config Split (Contrib) | `modules/contrib/config_split/` | 13.0 | 2.x |
| Core Update API | `core/lib/Drupal/Core/Update/`, `core/lib/Drupal/Core/Extension/module.api.php`, `core/includes/update.inc` | 17.1 | 11.4.5 |
| Core Hook Collector | `core/lib/Drupal/Core/Hook/HookCollectorPass.php` | 17.1 | 11.4.5 |
| System Module (update requirements) | `core/modules/system/src/Hook/SystemRequirementsHooks.php` | 17.1 | 11.4.5 |
| Drush | `vendor/drush/drush/` (`src/Commands/core/DeployCommands.php`, `UpdateDBCommands.php`, `DeployHookCommands.php`, `drush.api.php`) | 17.0, 17.1 | Drush 13.7.6 |
| Output Formatters | `vendor/consolidation/output-formatters/` (`TableFormatter.php`, `TsvFormatter.php`) | 17.1 | 4.7.1 |

---

## Version History

- 2026-09-24 — Added 17.1 Update Functions: the three kinds of update function, their order around `config:import`, and why their config changes are exported.

**Version:** 1.2
**Last Updated:** 2026-09-24
**Drupal Version:** 11.x
**Guide Type:** Atomic-Ready Single File
