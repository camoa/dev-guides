---
description: "One table, every hook-system change record: when each mechanism landed, was deprecated, and was removed."
tldr: "Reference table of every hook-system mechanism's landed, deprecated, and removed versions with its change record, verified against core 11.4.5."
drupal_version: "11.x"
---

# Hooks Deprecation Timeline

## When to Use

> You need the version a hook-system mechanism landed in, or the deprecate/remove pair for one being phased out, with the change record to cite. Verified against core 11.4.5 on 2026-09-14; 11.5.0 was unreleased.

## Items

| Mechanism | Landed | Deprecated | Removed | Change record |
|---|---|---|---|---|
| `#[Hook]` classes in `src/Hook/`, autowired | 11.1.0 | — | — | https://www.drupal.org/node/3442349 |
| `#[LegacyHook]` | 11.1.0 | — | — | https://www.drupal.org/node/3442349 |
| `ModuleHandler::getHookInfo()`, `ModuleHandler::writeCache()` | — | 11.1.0 | 12.0.0 | https://www.drupal.org/node/3442349 |
| Most core procedural hooks converted to hook classes | 11.1.0 | — | — | https://www.drupal.org/node/3486534 |
| Additional hooks gain `#[Hook]` support | 11.1.0 | — | — | https://www.drupal.org/node/3486506 |
| `hook_converted` parameter, `#[StopProceduralHookScan]` | 11.1.0 | renamed 11.2.0 | — | https://www.drupal.org/node/3490771 |
| `<module>.skip_procedural_hook_scan` parameter, `#[ProceduralHookScanStop]` | 11.2.0 | — | — | https://www.drupal.org/node/3490771 |
| `order:` on `#[Hook]`; `Order`, `OrderBefore`, `OrderAfter` | 11.2.0 | — | — | https://www.drupal.org/node/3493962 |
| `#[ReorderHook]` | 11.2.0 | — | — | https://www.drupal.org/node/3497308 |
| `#[RemoveHook]` | 11.2.0 | — | — | https://www.drupal.org/node/3496786 |
| Procedural before OOP within one module | 11.2.0 | — | — | https://www.drupal.org/node/3515207 |
| `hook_module_implements_alter()` without `#[LegacyModuleImplementsAlter]` | — | 11.2.0 | 12.0.0 | https://www.drupal.org/node/3496788 |
| `hook_hook_info()` include groups (`$module.$group.inc`) | — | 11.2.0 | 12.0.0 | https://www.drupal.org/node/3489765 |
| `hook_hook_info()` itself | — | not deprecated | support removed 12.0.0 | `core/lib/Drupal/Core/Extension/module.api.php` docblock |
| `hook_requirements()` | — | 11.2.0 | 12.0.0 | https://www.drupal.org/node/3512364 |
| Procedural `hook_requirements()` without `#[LegacyRequirementsHook]` | — | 11.3.0 | 13.0.0 | https://www.drupal.org/node/3549685 |
| `InstallRequirementsInterface`, `hook_runtime_requirements()`, `hook_update_requirements()` (+ `_alter`) | 11.2.0 (formalized 11.3.0) | — | — | https://www.drupal.org/node/3549685 |
| Integer severities in requirements arrays | — | 11.2.0 | enum required 12.0.0 | https://www.drupal.org/node/3410939 |
| `#[FormAlter]`, `#[Preprocess]` | 11.2.0-alpha1 | — | 11.2.0-beta1 | https://www.drupal.org/node/3524585 |
| `Hook::PREFIX`/`SUFFIX`, extending `Hook` | — | — | 11.2.0-beta1 | https://www.drupal.org/node/3524585 |
| `ModuleHandler::addModule()`, `addProfile()` | — | 11.2.0 | 12.0.0 | https://www.drupal.org/node/3491200 |
| `ModuleHandler::add()` | — | 11.3.0 | 12.0.0 | https://www.drupal.org/node/3491200 |
| `ModuleHandler::loadAllIncludes()` | — | 11.3.0 | 13.0.0 | https://www.drupal.org/node/3536432 |
| `ModuleHandler::getName()` | — | 10.3.0 | 12.0.0 | https://www.drupal.org/node/3310017 |
| `ModuleHandler::getImplementations()` | — | — | absent in 11.4.5 | not stated in verified sources |
| OOP hooks in themes (`ThemeHookCollectorPass`) | 11.3.0 | — | — | https://www.drupal.org/node/3551652 |
| Kernel tests declare `#[Hook]` methods | 11.3.0 | — | — | https://www.drupal.org/node/3553794 |
| `.theme` file extension | — | 11.5.0 (unreleased at verification) | not auto-loaded in 13.0.0 | https://www.drupal.org/node/3581222 |
| `#[ExtensionFileIsConverted]` (silences the `.theme` deprecation) | 11.5.0 (unreleased at verification) | — | — | https://www.drupal.org/node/3581222 |
| Legacy hooks outside the main `.module` / `.theme` / `theme-settings.php` | — | — | not collected from 12.0.0 | https://www.drupal.org/node/3613767 |
| Deprecating procedural hooks, `.module`, and `.install` generally | — | — | — | Plan issue https://www.drupal.org/project/drupal/issues/3481555, status "Needs review" on 2026-09-14. Under review, not policy |

## Common Mistakes

- Citing "procedural hooks are removed in Drupal 13" → no committed change record says that. The committed facts are the rows above; the general plan is under review.
- Treating "11.5.0" as shipped → at verification the newest stable was 11.4.6. Say "11.5.0 (unreleased)" until it ships.
- Confusing the two `hook_requirements()` rows → the hook is 11.2.0 → 12.0.0; running the procedural function unmarked is 11.3.0 → 13.0.0.

## See Also

- ← [Migrating to OOP Hooks](migrating-to-oop-hooks.md) | [Hooks Best Practices](hooks-best-practices.md) →
- Release listing: https://www.drupal.org/project/drupal/releases
- Change record listing filtered to hooks: https://www.drupal.org/list-changes/drupal?keywords_description=hook
