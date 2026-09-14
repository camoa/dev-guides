---
description: "The hooks that must stay procedural — install, update, schema, meta hooks — and what replaces hook_requirements()."
tldr: "Which hooks (install, update, schema, meta hooks) must stay procedural when converting a module, and what replaces hook_requirements()."
drupal_version: "11.x"
---

# Procedural-Only Hooks

## When to Use

> You are converting a module and need the list of hooks that cannot become `#[Hook]` methods, where each one lives, and what replaces `hook_requirements()`.

## Items

### Install and update hooks

Called by `core/lib/Drupal/Core/Extension/ModuleInstaller.php` with `function_exists("{$module}_{$hook}")`. The hook collector never touches them, and `#[Hook]` on any of these names throws a `LogicException` at container build (`HookCollectorPass::checkForProceduralOnlyHooks()`).

| Hook | Lives in |
|---|---|
| `hook_install()`, `hook_uninstall()` | `<module>.install` |
| `hook_schema()` | `<module>.install` |
| `hook_update_N()`, `hook_update_last_removed()`, `hook_update_dependencies()` | `<module>.install` |
| `hook_post_update_NAME()`, `hook_removed_post_updates()` | `<module>.post_update.php` |
| `hook_install_tasks()`, `hook_install_tasks_alter()` | `<profile>.profile` |

**Gotchas:**
- These stay procedural in core's own modules too. The question of deprecating them is open in plan issue 3481555, which is at "Needs review" and is not policy.
- `hook_install()`, `hook_uninstall()` receive `$is_syncing` (8.9.0, change record 3098920).

### Legacy meta hooks

| Hook | Lives in | Status |
|---|---|---|
| `hook_hook_info()` | `<module>.module` | Include groups (`$module.$group.inc`) deprecated 11.2.0, removed 12.0.0 (change record 3489765). The hook itself is intentionally not deprecated; support ends in 12.0.0 (`core/lib/Drupal/Core/Extension/module.api.php` docblock) |
| `hook_module_implements_alter()` | `<module>.module` | Without `#[LegacyModuleImplementsAlter]`: deprecated 11.2.0, removed 12.0.0 (change record 3496788). See [Hook Ordering](hook-ordering.md) |

**Gotchas:**
- Both are still collected and executed in 11.4.5. `hook_hook_info()` runs at container build to compute group includes; `hook_module_implements_alter()` is invoked through the normal alter machinery in `ModuleHandler::reOrderModulesForAlter()`.
- A module with `hook_hook_info()` must not set `skip_procedural_hook_scan`; the hook would never be found (change record 3490771).

### `hook_requirements()` and its replacements

`hook_requirements()` is deprecated 11.2.0, removed 12.0.0 (change record 3512364). Its three phases split into three mechanisms, all available since 11.2.0 (change record 3549685):

| Phase | Replacement | OOP? | Core example |
|---|---|---|---|
| `install` | Class implementing `InstallRequirementsInterface` in `src/Install/Requirements/<Module>Requirements.php`, `public static function getRequirements(): array` | Static class, not a hook | `core/modules/system/src/Install/Requirements/SystemRequirements.php`, `core/modules/media/...`, `core/modules/workspaces/...`, `core/modules/package_manager/...`, `core/modules/pgsql/...` |
| `runtime` | `hook_runtime_requirements()` + `hook_runtime_requirements_alter()` | Yes, `#[Hook('runtime_requirements')]` | `core/modules/node/src/Hook/NodeRequirements.php` |
| `update` | `hook_update_requirements()` + `hook_update_requirements_alter()` | Yes, `#[Hook('update_requirements')]` | `core/modules/system/src/Hook/SystemRequirementsHooks.php` |

```php
namespace Drupal\my_module\Install\Requirements;

use Drupal\Core\Extension\InstallRequirementsInterface;
use Drupal\Core\Extension\Requirement\RequirementSeverity;

class MyModuleRequirements implements InstallRequirementsInterface {

  public static function getRequirements(): array {
    return ['my_module_ext' => [
      'title' => t('Required PHP extension'),
      'severity' => extension_loaded('intl') ? RequirementSeverity::OK : RequirementSeverity::Error,
    ]];
  }

}
```

`core/includes/install.inc` (`install_check_class_requirements()`) scans `src/Install/Requirements/*.php`, requires each file, and calls `getRequirements()` on any class implementing the interface. The class runs before the module's container exists, so it has no injection.

Severity is the `RequirementSeverity` enum (`Info`, `OK`, `Warning`, `Error`). Integer constants are deprecated 11.2.0 and the enum is required in 12.0.0 (change record 3410939).

**Gotchas:**
- Two separate deprecations exist. The hook itself: 11.2.0 → 12.0.0. Running a procedural `hook_requirements()` without `#[LegacyRequirementsHook]`: 11.3.0 → 13.0.0 (change record 3549685, `HookCollectorPass::addProceduralImplementation()`).
- `#[LegacyRequirementsHook]` stops the procedural function on 11.3.0+ and silences the deprecation. 11.2 does not know the attribute and invokes both the legacy and the new hooks. Use it only while you still support core older than 11.2.
- `#[Hook('requirements')]` is on the deny list; the container throws.

## Common Mistakes

- Moving `hook_schema()` or `hook_update_N()` into a hook class → container build fails with "does not support attributes and must remain procedural."
- Keeping `hook_requirements()` with a `$phase` switch after your minimum is 11.2 → a deprecation notice at every container rebuild since 11.3.0. Split it.
- Injecting services into the `InstallRequirementsInterface` class → it is instantiated by a static call during install; nothing is injected.
- Returning `REQUIREMENT_ERROR` integers → deprecated since 11.2.0. Return `RequirementSeverity::Error`.

## See Also

- ← [Hook Ordering](hook-ordering.md) | [Theme Hooks (OOP)](theme-hooks-oop.md) →
- Reference: `core/lib/Drupal/Core/Extension/ModuleInstaller.php`, `core/lib/Drupal/Core/Extension/InstallRequirementsInterface.php`, `core/lib/Drupal/Core/Extension/Requirement/RequirementSeverity.php`, `core/lib/Drupal/Core/Extension/module.api.php`, `core/includes/install.inc`
- Change records: https://www.drupal.org/node/3512364, https://www.drupal.org/node/3549685, https://www.drupal.org/node/3410939, https://www.drupal.org/node/3489765, https://www.drupal.org/node/3496788
