---
description: "Stopping the procedural hook scan at container build with skip_procedural_hook_scan or #[ProceduralHookScanStop]."
tldr: "Stopping the procedural hook scan at container build once a module has converted to #[Hook] classes, via skip_procedural_hook_scan or #[ProceduralHookScanStop]."
drupal_version: "11.x"
---

# Procedural Scan Performance

## When to Use

> Your module has converted to `#[Hook]` classes and you want to stop the backwards-compatibility layer from parsing every `.module`, `.inc`, `.install`, and `.profile` file at container build (change record 3490771, 11.1.0).

## Decision

| If the module... | Use... | Why |
|---|---|---|
| Has no procedural hooks left | `parameters: my_module.skip_procedural_hook_scan: true` in `my_module.services.yml` | The collector skips the procedural branch for that module entirely. `src/Hook/` is still scanned |
| Still has some procedural hooks, in `.module` or `.inc` | `#[ProceduralHookScanStop]` on the first non-hook function in each file | Everything above the marked function is parsed; parsing stops there |
| Implements `hook_hook_info()` | Neither the parameter nor a stop before that function | The parameter prevents `hook_hook_info()` from being discovered (change record 3490771). The stop attribute scans everything above it, so `hook_hook_info()` must sit above the marker |
| Supports 11.1 | The 11.1 names: `hook_converted` parameter, `#[StopProceduralHookScan]` attribute | Both renamed in 11.2 (change record 3490771) |

This is a `services.yml` parameter, not an `.info.yml` key. Core's own shape, `core/modules/dblog/dblog.services.yml`:

```yaml
parameters:
  dblog.skip_procedural_hook_scan: true
```

Core sets it `true` in `history`, `menu_ui`, `serialization`, `dblog`, `page_cache`, `content_moderation`, `path_alias`, `help`, `field`, and more; `comment.services.yml` sets it `false`. `HookCollectorKeyValueWritePass` strips all `*.skip_procedural_hook_scan` parameters after use, so they never reach the runtime container.

## Pattern

```php
// my_module.module
use Drupal\Core\Hook\Attribute\ProceduralHookScanStop;

function my_module_cron(): void {}

/**
 * Helper. Nothing below this line is a hook.
 */
#[ProceduralHookScanStop]
function _my_module_format_label(string $label): string {
  return trim($label);
}
```

What still gets scanned regardless of either mechanism: every `.php` file under `src/Hook/` (`HookCollectorPass::collectModuleHookImplementations()`, the OOP branch is not gated by `$skip_procedural`).

## Common Mistakes

- Putting `skip_procedural_hook_scan: true` in `.info.yml` → ignored. It is a container parameter in `services.yml`.
- Setting the parameter while a plain procedural hook remains → the hook silently stops firing. Confirm with `hasImplementations()` first (see [Migrating to OOP Hooks](migrating-to-oop-hooks.md)).
- Placing `#[ProceduralHookScanStop]` above a real hook → that hook is never collected. The attribute's docblock lists what the scan above it still finds: `hook_hook_info()`, `hook_module_implements_alter()`, `hook_requirements()`, `hook_preprocess()`, `hook_preprocess_HOOK()`.
- Expecting the parameter to speed up runtime → it only shortens container build. Runtime reads compiled data from the `hook_data` key-value store.

## See Also

- ← [Theme Hooks (OOP)](theme-hooks-oop.md) | [Migrating to OOP Hooks](migrating-to-oop-hooks.md) →
- Change record: https://www.drupal.org/node/3490771
- Reference: `core/lib/Drupal/Core/Hook/Attribute/ProceduralHookScanStop.php`, `core/lib/Drupal/Core/Hook/HookCollectorPass.php`, `core/lib/Drupal/Core/Hook/HookCollectorKeyValueWritePass.php`, `core/modules/dblog/dblog.services.yml`
