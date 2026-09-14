---
description: "Choosing between a #[Hook] class method, a procedural function, or both, based on the lowest core version supported."
tldr: "Choosing between a #[Hook] class method, a procedural function, or both when adding or converting a hook implementation; the lowest core version supported decides it."
drupal_version: "11.x"
---

# Hook Implementation Decision

## When to Use

> You are adding or converting a hook implementation and need to pick between a `#[Hook]` class method, a procedural `<module>_<hook>()` function, or both. The lowest core version you support decides it.

## Decision

| If you support... | Use... | Why |
|---|---|---|
| 11.1.0 or later only | A class in `src/Hook/` with `#[Hook]` methods, no procedural function | OOP hooks landed in 11.1.0 (change record 3442349). Core's own modules finished converting; their `.module` files hold helper functions only |
| 11.2.0 or later only | Same, plus the `order:` parameter when order matters | `order:` on `#[Hook]`, `#[ReorderHook]`, and `#[RemoveHook]` landed in 11.2.0 |
| 10.x or 11.0.x as well | The class method **and** a procedural function marked `#[LegacyHook]` that calls the class | On 11.1+ the collector skips the `#[LegacyHook]` function so the hook runs once. On versions that do not know the attribute, only the procedural function runs (`core/lib/Drupal/Core/Hook/Attribute/LegacyHook.php`) |
| Any version, for `hook_install()`, `hook_update_N()`, `hook_schema()` and the other install-time hooks | Procedural only | The collector throws a `LogicException` when it finds `#[Hook]` on those names. See [Procedural-Only Hooks](procedural-only-hooks.md) |

A hook method has the same signature as its procedural counterpart. The class and method may have any name (change record 3442349).

## Pattern

The shape core uses, from `core/modules/system/src/Hook/PageAttachmentsHook.php`:

```php
namespace Drupal\my_module\Hook;

use Drupal\Core\Hook\Attribute\Hook;
use Drupal\Core\Render\BareHtmlPageRendererInterface;

final class PageAttachmentsHook {

  public function __construct(
    private readonly BareHtmlPageRendererInterface $bareHtmlPageRenderer,
  ) {}

  /**
   * Implements hook_page_attachments().
   */
  #[Hook('page_attachments')]
  public function pageAttachments(array &$page): void {
    $this->bareHtmlPageRenderer->systemPageAttachments($page);
  }

}
```

The class is registered as an autowired service with the class name as service id. No `services.yml` entry is needed (`core/lib/Drupal/Core/Hook/HookCollectorPass.php`, `registerHookServices()`).

The legacy shim, only when you must support core older than 11.1.0, goes in `my_module.module`:

```php
use Drupal\Core\Hook\Attribute\LegacyHook;
use Drupal\my_module\Hook\PageAttachmentsHook;

#[LegacyHook]
function my_module_page_attachments(array &$page): void {
  \Drupal::service(PageAttachmentsHook::class)->pageAttachments($page);
}
```

## Common Mistakes

- Writing both a class method and a plain procedural function without `#[LegacyHook]` → the hook runs twice on 11.1+. Add the attribute or delete the function.
- Keeping the shim after dropping 10.x/11.0 support → dead code. The collector skips `#[LegacyHook]` functions, so the scan is unaffected, but the file still loads. In core the attribute survives only in `core/themes/stable9/stable9.theme` and two test fixtures.
- Putting the class outside `src/Hook/` → never discovered. Only `.php` files under `src/Hook/` are scanned for attributes.
- Reaching for `#[FormAlter]` or `#[Preprocess]` → those attributes existed in 11.2.0-alpha1 and were removed for 11.2.0-beta1 (change record 3524585). Use `#[Hook('form_alter')]` and `#[Hook('preprocess_node')]`.

## See Also

- Next: [Hook Attribute Anatomy](hook-attribute-anatomy.md) →
- Organizing hook classes by concern: https://camoa.github.io/dev-guides/drupal/solid-principles/hook-classes-srp/
- Hooks vs events: https://camoa.github.io/dev-guides/drupal/solid-principles/hooks-events-ocp/ and https://camoa.github.io/dev-guides/drupal/dry-principles/hook-event-reuse/
- Change record: https://www.drupal.org/node/3442349
- Reference: `core/lib/Drupal/Core/Hook/Attribute/Hook.php`, `core/lib/Drupal/Core/Hook/Attribute/LegacyHook.php`
