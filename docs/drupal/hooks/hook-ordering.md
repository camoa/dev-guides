---
description: "Ordering hook execution with order: on #[Hook], #[ReorderHook], or #[RemoveHook] since core 11.2.0."
tldr: "Ordering hook execution with order: on #[Hook], #[ReorderHook], or #[RemoveHook] since 11.2.0, replacing hook_module_implements_alter()."
drupal_version: "11.x"
---

# Hook Ordering

## When to Use

> Your implementation must run before or after another module's, or you must stop another module's implementation from running. Since 11.2.0 you declare this in attributes; `hook_module_implements_alter()` is on its way out.

## Decision

Default order, from `core/core.api.php` (`@defgroup hooks`): module weight, then alphabetical by module name. Within one module, procedural implementations run before OOP implementations of the same hook (11.2.0, change record 3515207).

| If you need... | Use... | Why |
|---|---|---|
| Your implementation first or last among all modules | `order: Order::First` or `order: Order::Last` on your `#[Hook]` | `FirstOrLast` operation moves your identifier to the array start or end |
| Yours before or after named modules | `order: new OrderBefore(modules: ['a', 'b'])` / `new OrderAfter(modules: [...])` | `BeforeOrAfter` splices yours immediately before the earliest, or after the latest, of the named modules |
| Yours before or after one specific class method | `new OrderAfter(classesAndMethods: [[Foo::class, 'method']])` | Same operation, finer target. Use `[ProceduralCall::class, 'function_name']` to target a procedural implementation |
| Another module's implementation moved, without touching that module | `#[ReorderHook(hook, class, method, order)]` on any class or method in your `src/Hook/` | Runs after every `#[Hook(order:)]` is applied (`core.api.php`, "ordering_other_module_hooks"). 11.2.0, change record 3497308 |
| Another module's implementation removed | `#[RemoveHook(hook, class, method)]` | 11.2.0, change record 3496786 |
| Support for core before 11.2.0 | Keep `hook_module_implements_alter()` and mark it `#[LegacyModuleImplementsAlter]` | On 11.2+ the attribute stops the procedural function from running so the attribute ordering wins. Without the attribute the function still runs but is deprecated 11.2.0, removed 12.0.0 (change record 3496788) |

## Pattern

`order:` on the implementation:

```php
use Drupal\Core\Hook\Attribute\Hook;
use Drupal\Core\Hook\Order\Order;
use Drupal\Core\Hook\Order\OrderAfter;

#[Hook('entity_presave', order: Order::Last)]
public function entityPresaveLast(EntityInterface $entity): void {}

#[Hook('form_alter', order: new OrderAfter(modules: ['field_group']))]
public function formAlter(array &$form, FormStateInterface $form_state, string $form_id): void {}
```

Reordering another module, the example from change record 3497308:

```php
use Drupal\Core\Hook\Attribute\ReorderHook;
use Drupal\Core\Hook\Order\OrderBefore;
use Drupal\content_moderation\Hook\ContentModerationHooks;

#[ReorderHook('entity_presave', class: ContentModerationHooks::class, method: 'entityPresave', order: new OrderBefore(modules: ['workspaces']))]
#[Hook('entity_presave')]
public function entityPresave(EntityInterface $entity): void {}
```

Removing another module's implementation:

```php
use Drupal\Core\Hook\Attribute\RemoveHook;

#[RemoveHook('form_alter', class: OtherModuleHooks::class, method: 'formAlter')]
final class MyHooks {}
```

The attributes take effect wherever they sit inside `src/Hook/`; core recommends placing `#[ReorderHook]` on the implementation that needs the other one moved (change record 3497308).

## Common Mistakes

- Looking for a `priority:` parameter → there is none. Ordering is `order:` on `#[Hook]`, `#[ReorderHook]`, `#[RemoveHook]`.
- `new OrderBefore()` with no arguments → `LogicException('Order must provide either modules or class-method pairs to order against.')` (`core/lib/Drupal/Core/Hook/Order/RelativeOrderBase.php`).
- Targeting a class-form implementation with `method: 'someName'` → the target method is `'__invoke'` when the `#[Hook]` sits on the class.
- Ordering against a module that does not implement the hook → silent no-op. `BeforeOrAfter::apply()` returns without change when the reference identifier is absent.
- Assuming `Order::First` on two modules gives a defined order → both move to the front; the last applied wins. Use `OrderBefore` against the other module instead.
- Using `order:`, `#[ReorderHook]`, or `#[RemoveHook]` in a theme → `LogicException` at container build. See [Theme Hooks (OOP)](theme-hooks-oop.md).

## See Also

- ← [Hook Attribute Anatomy](hook-attribute-anatomy.md) | [Procedural-Only Hooks](procedural-only-hooks.md) →
- Reference: `core/lib/Drupal/Core/Hook/Order/Order.php`, `OrderBefore.php`, `OrderAfter.php`, `RelativeOrderBase.php`; `core/lib/Drupal/Core/Hook/OrderOperation/BeforeOrAfter.php`, `FirstOrLast.php`; `core/lib/Drupal/Core/Hook/Attribute/ReorderHook.php`, `RemoveHook.php`, `LegacyModuleImplementsAlter.php`
- Change records: https://www.drupal.org/node/3493962, https://www.drupal.org/node/3497308, https://www.drupal.org/node/3496786, https://www.drupal.org/node/3496788, https://www.drupal.org/node/3515207
