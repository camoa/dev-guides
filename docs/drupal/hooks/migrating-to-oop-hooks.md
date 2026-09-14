---
description: "Step-by-step conversion of a module or theme's procedural hooks to #[Hook] classes, from inventory to verification."
tldr: "Converting a module or theme's procedural hooks to #[Hook] classes before Drupal 12.0.0 stops collecting legacy hooks outside the main extension file."
drupal_version: "11.x"
---

# Migrating to OOP Hooks

## When to Use

> You own a module or theme with hooks in `.module`, `.theme`, or `.inc` files and want to convert them before 12.0.0 stops collecting legacy hooks outside the main extension file (change record 3613767).

## Steps

1. **Inventory the procedural hooks** — list every `<module>_<hook>()` function across `.module`, `.inc`, `.install`, and `.profile`. Separate them into three buckets: convertible hooks, [procedural-only hooks](procedural-only-hooks.md), and plain helper functions.
   ```bash
   grep -rnE '^function (my_module)_[a-z0-9_]+\(' my_module.module my_module.*.inc
   ```

2. **Create one class per domain concern in `src/Hook/`** — core splits by concern: `NodeFormHooks`, `NodeEntityHooks`, `NodeThemeHooks`, `NodeRequirements` in `core/modules/node/src/Hook/`. Namespace `Drupal\my_module\Hook`. Inject dependencies through the constructor; the class is autowired.

3. **Move each convertible hook** — copy the body into a method, keep the signature, add `#[Hook('<name>')]`, and a docblock `Implements hook_<name>().` Replace `\Drupal::service()` calls with injected properties.

4. **Decide on the legacy shim** — if your `core_version_requirement` still admits 10.x or 11.0.x, keep a procedural function with `#[LegacyHook]` that delegates to the class. Otherwise delete the procedural function. See [Hook Implementation Decision](hook-implementation-decision.md).

5. **Split `hook_requirements()`** — install phase to `src/Install/Requirements/MyModuleRequirements.php`, runtime to `#[Hook('runtime_requirements')]`, update to `#[Hook('update_requirements')]`. See [Procedural-Only Hooks](procedural-only-hooks.md).

6. **Replace `hook_module_implements_alter()`** — with `order:` on the affected `#[Hook]` or `#[ReorderHook]`. If you must keep it for cores below 11.2, mark it `#[LegacyModuleImplementsAlter]`. See [Hook Ordering](hook-ordering.md).

7. **Move helpers out of `.module`** — into the hook class that uses them, or a service. Leave only procedural-only hooks and any `#[LegacyHook]` shims.

8. **Stop the scan** — add `parameters: my_module.skip_procedural_hook_scan: true` to `my_module.services.yml` once no plain procedural hooks remain, or `#[ProceduralHookScanStop]` if some do. See [Procedural Scan Performance](procedural-scan-performance.md).

9. **Rebuild the container** — hook discovery is a compiler pass.
   ```bash
   drush cr
   ```

10. **Verify the implementations are registered** — the compiled list is what runs. `getImplementations()` no longer exists; use `hasImplementations()` and `invokeAllWith()`:
    ```bash
    drush php:eval "var_dump(\Drupal::moduleHandler()->hasImplementations('entity_presave', 'my_module'));"
    drush php:eval "\Drupal::moduleHandler()->invokeAllWith('entity_presave', function (callable \$hook, string \$module) { echo \$module, PHP_EOL; });"
    ```
    The second command prints each implementing module in execution order, once per implementation. For a repeatable check, write a kernel test that installs the module and asserts `hasImplementations()`; since 11.3.0 kernel tests can also declare `#[Hook]` methods to exercise the invocation (change record 3553794).

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Inventory | Hooks live in `my_module.<group>.inc` loaded by `hook_hook_info()` | Convert them now. Group includes are deprecated 11.2.0, removed 12.0.0 (change record 3489765). The runtime deprecation in `ModuleHandler::getHookImplementationList()` names the file |
| Inventory | Hooks live in any `.inc` the module `include`s itself | Convert or move to `.module`. 12.0.0 collects legacy hooks only from the main `.module`, `.theme`, and `theme-settings.php` files; functions elsewhere are silently ignored (change record 3613767). Converted functions marked `#[LegacyHook]` may remain in include files |
| Move hooks | The hook is `hook_install()`, `hook_update_N()`, `hook_schema()`, `hook_uninstall()`, `hook_post_update_NAME()` | Leave it procedural in `.install` or `.post_update.php` |
| Move hooks | One module has two implementations of `hook_help()`, `hook_mail()`, `hook_library_info_build()`, or `hook_node_update_index()` | Merge them; `invoke()` throws on more than one per module |
| Legacy shim | `core_version_requirement` is `^11.1` or tighter | No shim. Delete the procedural function |
| Stop the scan | The module implements `hook_hook_info()` | Do not add the parameter; use `#[ProceduralHookScanStop]` below that function instead |
| Theme variant | The extension is a theme | Same steps with these changes: minimum core 11.3.0; no `order:`, `module:`, `#[ReorderHook]`, `#[RemoveHook]`; helpers not on the hook class use `\Drupal::service()`; a theme cannot ship a `services.yml`, but the theme collector still honors `<theme>.skip_procedural_hook_scan` when a site-level `services.yml` sets it. Change record 3581222 links a Rector rule and DDEV script: https://gitlab.com/-/snippets/5975084 |
| Theme variant | You must keep `.theme` for cores below 11.3.0 after 11.5.0 ships | Add `#[ExtensionFileIsConverted]` to the first function only after everything is converted. The attribute does not exist in 11.4.5 |

## Common Mistakes

- Converting a hook and leaving the procedural copy unmarked → it runs twice. Either `#[LegacyHook]` or delete.
- Setting `skip_procedural_hook_scan` before step 7 is done → a forgotten procedural hook silently stops firing.
- Renaming or moving a hook class after step 9 without another `drush cr` → the compiled list is keyed by class name and still names the old one. Rebuild after every rename.
- Verifying with a full page load only → the hook may run from the legacy fallback in `ModuleHandler::invoke()` (`legacyInvoke()`), masking a discovery problem. Check `hasImplementations()`.

## See Also

- ← [Procedural Scan Performance](procedural-scan-performance.md) | [Hooks Deprecation Timeline](hooks-deprecation-timeline.md) →
- Testing hook implementations: https://camoa.github.io/dev-guides/drupal/tdd/testing-events-hooks/
- Splitting classes by concern: https://camoa.github.io/dev-guides/drupal/solid-principles/hook-classes-srp/
- Change records: https://www.drupal.org/node/3613767, https://www.drupal.org/node/3489765, https://www.drupal.org/node/3553794, https://www.drupal.org/node/3581222
