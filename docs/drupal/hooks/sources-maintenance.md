---
description: "Source references and maintenance manifest for the hooks guides — web sources, code sources, and version history"
---

# Sources & Maintenance

Last verified 2026-09-14 against core 11.4.5. Newest stable at verification: 11.4.6; 12.0.0-alpha1 released 2026-09-02.

## Drupal Research Install

Claims here were checked against a local install of core 11.4.5 rather than quoted from documentation. Code source paths below are relative to the Drupal root.

## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| CR: OOP hook implementations using autowired services | https://www.drupal.org/node/3442349 | hook-implementation-decision, hook-attribute-anatomy, hooks-deprecation-timeline | 2026-09-14 |
| CR: Procedural hooks ordered before OOP hooks per module | https://www.drupal.org/node/3515207 | hook-ordering, hooks-deprecation-timeline | 2026-09-14 |
| CR: `#[ReorderHook]` | https://www.drupal.org/node/3497308 | hook-ordering, hooks-deprecation-timeline | 2026-09-14 |
| CR: Extending the Hook attribute no longer supported (`#[FormAlter]`, `#[Preprocess]` removed) | https://www.drupal.org/node/3524585 | hook-implementation-decision, hook-attribute-anatomy, hooks-deprecation-timeline | 2026-09-14 |
| CR: Legacy hooks no longer collected outside the main extension file | https://www.drupal.org/node/3613767 | migrating-to-oop-hooks, hooks-deprecation-timeline, hooks-best-practices | 2026-09-14 |
| CR: Hooks in themes can be OOP | https://www.drupal.org/node/3551652 | theme-hooks-oop, hooks-deprecation-timeline | 2026-09-14 |
| CR: `.theme` file extension deprecated | https://www.drupal.org/node/3581222 | theme-hooks-oop, migrating-to-oop-hooks, hooks-deprecation-timeline | 2026-09-14 |
| CR: `hook_requirements` deprecated in favor of runtime/update hooks and install checks | https://www.drupal.org/node/3549685 | procedural-only-hooks, hooks-deprecation-timeline | 2026-09-14 |
| CR: `hook_requirements()` deprecated | https://www.drupal.org/node/3512364 | procedural-only-hooks, hooks-deprecation-timeline | 2026-09-14 |
| CR: Requirement severities as enum | https://www.drupal.org/node/3410939 | procedural-only-hooks, hooks-deprecation-timeline | 2026-09-14 |
| CR: Hook implementations ordered with an order parameter | https://www.drupal.org/node/3493962 | hook-ordering, hooks-deprecation-timeline | 2026-09-14 |
| CR: `#[RemoveHook]` | https://www.drupal.org/node/3496786 | hook-ordering, hooks-deprecation-timeline | 2026-09-14 |
| CR: `hook_module_implements_alter` requires `#[LegacyModuleImplementsAlter]` | https://www.drupal.org/node/3496788 | hook-ordering, procedural-only-hooks, hooks-deprecation-timeline | 2026-09-14 |
| CR: Includes for `hook_hook_info` deprecated | https://www.drupal.org/node/3489765 | procedural-only-hooks, migrating-to-oop-hooks, hooks-deprecation-timeline | 2026-09-14 |
| CR: Preventing unnecessary scanning of procedural hooks | https://www.drupal.org/node/3490771 | procedural-scan-performance, hooks-deprecation-timeline | 2026-09-14 |
| CR: Most procedural hook implementations converted to a hook class | https://www.drupal.org/node/3486534 | hooks-deprecation-timeline | 2026-09-14 |
| CR: Additional hook implementations using `#[Hook]` | https://www.drupal.org/node/3486506 | hooks-deprecation-timeline | 2026-09-14 |
| CR: Kernel tests can use hook attributes | https://www.drupal.org/node/3553794 | migrating-to-oop-hooks, hooks-deprecation-timeline | 2026-09-14 |
| CR: `ModuleHandler::addModule()`/`addProfile()`/`add()` deprecated | https://www.drupal.org/node/3491200 | hooks-deprecation-timeline | 2026-09-14 |
| CR: `ModuleHandler::loadAllIncludes()` deprecated | https://www.drupal.org/node/3536432 | hooks-deprecation-timeline | 2026-09-14 |
| CR: `ModuleHandler::getName()` deprecated | https://www.drupal.org/node/3310017 | hooks-deprecation-timeline | 2026-09-14 |
| CR: `hook_install`/`hook_uninstall` receive `$is_syncing` | https://www.drupal.org/node/3098920 | procedural-only-hooks | 2026-09-14 |
| Plan issue: Determine how to deprecate procedural hooks | https://www.drupal.org/project/drupal/issues/3481555 | procedural-only-hooks, hooks-deprecation-timeline, hooks-best-practices | 2026-09-14 |
| api.drupal.org: `Hook` attribute class (11.x) | https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Hook%21Attribute%21Hook.php/class/Hook/11.x | hook-attribute-anatomy | 2026-09-14 |
| drupal.org: Understanding hooks (updated 27 Sep 2025) | https://www.drupal.org/docs/develop/creating-modules/understanding-hooks | hook-implementation-decision, hook-ordering | 2026-09-14 |
| Rector rule + DDEV script for theme conversion | https://gitlab.com/-/snippets/5975084 | migrating-to-oop-hooks | 2026-09-14 |
| Drupal core releases | https://www.drupal.org/project/drupal/releases | hooks-deprecation-timeline | 2026-09-14 |
| Change record listing filtered to "hook" | https://www.drupal.org/list-changes/drupal?keywords_description=hook | hooks-deprecation-timeline | 2026-09-14 |

## Code Sources

| Module | Relative Path | Guide Sections | Drupal Version |
|--------|---------------|----------------|----------------|
| Hook attributes | core/lib/Drupal/Core/Hook/Attribute/ (`Hook.php`, `LegacyHook.php`, `LegacyModuleImplementsAlter.php`, `LegacyRequirementsHook.php`, `ProceduralHookScanStop.php`, `RemoveHook.php`, `ReorderHook.php`, `HookAttributeInterface.php`) | hook-implementation-decision, hook-attribute-anatomy, hook-ordering, procedural-only-hooks, procedural-scan-performance | 11.4.5 |
| Hook ordering | core/lib/Drupal/Core/Hook/Order/ (`Order.php`, `OrderInterface.php`, `OrderBefore.php`, `OrderAfter.php`, `RelativeOrderBase.php`), core/lib/Drupal/Core/Hook/OrderOperation/ (`BeforeOrAfter.php`, `FirstOrLast.php`, `OrderOperation.php`) | hook-ordering | 11.4.5 |
| Module hook collector | core/lib/Drupal/Core/Hook/HookCollectorPass.php | hook-attribute-anatomy, hook-ordering, procedural-only-hooks, procedural-scan-performance, hooks-best-practices | 11.4.5 |
| Theme hook collector | core/lib/Drupal/Core/Hook/ThemeHookCollectorPass.php | theme-hooks-oop | 11.4.5 |
| Hook data writer | core/lib/Drupal/Core/Hook/HookCollectorKeyValueWritePass.php | hook-attribute-anatomy, procedural-scan-performance | 11.4.5 |
| Module handler | core/lib/Drupal/Core/Extension/ModuleHandler.php, ModuleHandlerInterface.php | hook-attribute-anatomy, migrating-to-oop-hooks, hooks-deprecation-timeline, hooks-best-practices | 11.4.5 |
| Module installer | core/lib/Drupal/Core/Extension/ModuleInstaller.php | procedural-only-hooks | 11.4.5 |
| Install requirements | core/lib/Drupal/Core/Extension/InstallRequirementsInterface.php, core/lib/Drupal/Core/Extension/Requirement/RequirementSeverity.php, core/includes/install.inc | procedural-only-hooks | 11.4.5 |
| Hook API docs | core/core.api.php (`@defgroup hooks`), core/lib/Drupal/Core/Extension/module.api.php | hook-ordering, procedural-only-hooks, theme-hooks-oop | 11.4.5 |
| System module hook classes | core/modules/system/src/Hook/ (`PageAttachmentsHook.php`, `SystemRequirementsHooks.php`), core/modules/system/src/Install/Requirements/SystemRequirements.php | hook-implementation-decision, procedural-only-hooks, hooks-best-practices | 11.4.5 |
| Node module hook classes | core/modules/node/src/Hook/ (`NodeHelpHooks.php`, `NodeRequirements.php`, and twelve others) | procedural-only-hooks, migrating-to-oop-hooks, hooks-best-practices | 11.4.5 |
| Dblog services | core/modules/dblog/dblog.services.yml | procedural-scan-performance | 11.4.5 |
| Claro theme hook classes | core/themes/claro/src/Hook/ (`ClaroHooks.php`, `ClaroFormHooks.php`) | theme-hooks-oop, hooks-best-practices | 11.4.5 |
| Olivero theme hook classes | core/themes/olivero/src/Hook/ (`OliveroPagePreprocessHooks.php`, `OliveroHooks.php`) | theme-hooks-oop, hooks-best-practices | 11.4.5 |
| Stable9 theme | core/themes/stable9/stable9.theme | hook-implementation-decision | 11.4.5 |
