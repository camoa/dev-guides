---
description: "The #[Hook] attribute constructor, the three placement forms, discovery rules, and the install-hook exception."
tldr: "Writing or reading a #[Hook] attribute: the exact constructor, the three placement forms, discovery rules, and the two exceptions the collector enforces at container build."
drupal_version: "11.x"
---

# Hook Attribute Anatomy

## When to Use

> You are writing or reading a `#[Hook]` attribute and need the exact constructor, the three placement forms, the discovery rules, and the two exceptions the collector enforces at container build.

## Items

### `#[Hook]` constructor

`core/lib/Drupal/Core/Hook/Attribute/Hook.php`:

```php
#[\Attribute(\Attribute::TARGET_CLASS | \Attribute::TARGET_METHOD | \Attribute::IS_REPEATABLE)]
class Hook implements HookAttributeInterface {
  public function __construct(
    public string $hook,
    public string $method = '',
    public ?string $module = NULL,
    public ?OrderInterface $order = NULL,
  ) {}
}
```

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `hook` | `string` | required | Short hook name without the `hook_` prefix: `'form_alter'`, `'entity_presave'`, `'preprocess_html'`. Required since 11.2.0-beta1; the `PREFIX`/`SUFFIX` constants are gone (change record 3524585) |
| `method` | `string` | `''` | Only needed when the attribute sits on the class. Omit it and the class must define `__invoke()` |
| `module` | `?string` | `NULL` | Implement on behalf of another module. Defaults to the module that owns the class. Forbidden in themes |
| `order` | `?OrderInterface` | `NULL` | `Order::First`, `Order::Last`, `new OrderBefore(...)`, `new OrderAfter(...)`. Landed 11.2.0 (change record 3493962). Forbidden in themes |

**Gotchas:**
- Extending `Hook` to make your own shorthand attribute is no longer supported (change record 3524585).
- `HookAttributeInterface` is `@internal`; it exists only so the collector can fetch every hook-related attribute in one call.

### Three placement forms

```php
// 1. On a method. Most common.
#[Hook('entity_presave')]
public function entityPresave(EntityInterface $entity): void {}

// 2. On the class, naming the method.
#[Hook('entity_presave', method: 'entityPresave')]
final class EntityHooks { public function entityPresave(EntityInterface $entity): void {} }

// 3. On the class, with __invoke().
#[Hook('cron')]
final class CronHook { public function __invoke(): void {} }
```

The attribute is repeatable, so one method can implement several hooks:

```php
#[Hook('node_insert')]
#[Hook('node_update')]
public function nodeSave(NodeInterface $node): void {}
```

**Gotchas:**
- With form 3, `#[ReorderHook]` from another module must target `method: '__invoke'` (`core/lib/Drupal/Core/Hook/Attribute/ReorderHook.php`).

### `module:` — implementing on behalf of another module

```php
#[Hook('help', module: 'other_module')]
public function otherModuleHelp(string $route_name, RouteMatchInterface $route_match): ?string {}
```

The implementation is registered under `other_module` for ordering and for `ModuleHandler::invoke('other_module', 'help')`.

**Gotchas:**
- If `other_module` also implements the hook, and the hook allows one implementation per module, `invoke()` throws `LogicException("Module $module should not implement $hook more than once")` (`core/lib/Drupal/Core/Extension/ModuleHandler.php`, `invoke()`).

### Single-implementation hooks

Four hooks may not have more than one implementation per module (`Hook.php` docblock):

| Hook | Why one only |
|---|---|
| `hook_help()` | Called with `invoke()` for one module; result is a single string or render array |
| `hook_mail()` | Same: `invoke()` per module |
| `hook_library_info_build()` | Same |
| `hook_node_update_index()` | Same |

Two `#[Hook('help')]` methods in one module, or a `module:` collision, trigger the `invoke()` `LogicException` above.

### Discovery rules

From `core/lib/Drupal/Core/Hook/HookCollectorPass.php` (`collectModuleHookImplementations()`, `filterIterator()`, `registerHookServices()`):

| Rule | Detail |
|---|---|
| Directory | Only files under `src/Hook/` are scanned for attributes. Subdirectories are allowed |
| Extension | Only `.php` files in that directory |
| Namespace | `src/` maps to `Drupal\<module>\`, so the class lives in `Drupal\<module>\Hook` or a sub-namespace |
| Service id | The fully qualified class name. `$container->register($class, $class)->setAutowired(TRUE)` runs for every hook class not already defined |
| Existing definition | If you define the class as a service yourself in `services.yml`, the collector leaves your definition alone |
| Compile time | Discovery is a compiler pass. Adding or renaming a hook class needs a container rebuild (`drush cr`) |

Compiled results are written to the `hook_data` key-value store by `core/lib/Drupal/Core/Hook/HookCollectorKeyValueWritePass.php`, and `ModuleHandler::getHookImplementationList()` filters them to installed modules at runtime.

### The install-hook `LogicException`

`HookCollectorPass::checkForProceduralOnlyHooks()` runs for every `#[Hook]` found in `src/Hook/`:

```php
$staticDenyHooks = ['hook_info', 'install', 'install_tasks', 'install_tasks_alter',
  'module_implements_alter', 'removed_post_updates', 'requirements', 'schema',
  'uninstall', 'update_dependencies', 'update_last_removed'];
if (in_array($hookAttribute->hook, $staticDenyHooks) || preg_match('/^(post_update_|update_\d+$)/', $hookAttribute->hook)) {
  throw new \LogicException("The hook $hookAttribute->hook on class $class does not support attributes and must remain procedural.");
}
```

The container fails to build. See [Procedural-Only Hooks](procedural-only-hooks.md) for where each of these lives instead.

## Common Mistakes

- Prefixing the name: `#[Hook('hook_form_alter')]` → the hook `hook_form_alter` never fires. Drop `hook_`.
- Attribute on the class, no `method:`, no `__invoke()` → collector error. Pick one form.
- Calling `\Drupal::moduleHandler()->getImplementations()` → the method does not exist in 11.4.5. Use `hasImplementations()` or `invokeAllWith()`.
- Expecting discovery in `src/Plugin/` or `src/EventSubscriber/` → only `src/Hook/` is scanned.

## See Also

- ← [Hook Implementation Decision](hook-implementation-decision.md) | [Hook Ordering](hook-ordering.md) →
- Autowiring mechanics: https://camoa.github.io/dev-guides/drupal/services/autowiring/
- API reference: https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Hook%21Attribute%21Hook.php/class/Hook/11.x
- Change records: https://www.drupal.org/node/3442349, https://www.drupal.org/node/3524585
