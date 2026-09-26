---
description: "Writing OOP theme hooks since core 11.3.0, and the .theme file deprecation."
tldr: "Writing theme hooks as #[Hook] classes since core 11.3.0; the .theme file is deprecated in 11.5.0 (unreleased at verification)."
drupal_version: "11.x"
---

# Theme Hooks (OOP)

## When to Use

> You are writing `hook_preprocess_HOOK()`, `hook_theme_suggestions_HOOK_alter()`, `hook_form_alter()` or `hook_page_attachments_alter()` in a theme, and your minimum core is 11.3.0 or later. Themes support `#[Hook]` classes since 11.3.0 (change record 3551652); the `.theme` file is deprecated in 11.5.0 (unreleased at verification, change record 3581222).

## Decision

| If your theme supports... | Put hooks in... | Why |
|---|---|---|
| 11.3.0 or later only | `src/Hook/*.php` classes, no `.theme` file | Claro ships no `.theme` file in 11.4.5. Change record 3581222: "Drupal supports themes without a .theme file on all versions greater than Drupal 11.3.0" |
| 11.2 or earlier as well | `.theme` file, procedural. If you also ship the class, add a `#[LegacyHook]` shim that calls `\Drupal::classResolver(MyThemeHooks::class)->method(...)`; the class then needs no constructor arguments, or implements `ContainerInjectionInterface` with `create()`: 11.2 and earlier register no service for it | The theme collector landed in 11.3.0; older cores never see `src/Hook/` in a theme, and a theme cannot ship a `services.yml`, so `\Drupal::service()` throws there. `ClassResolver::getInstanceFromDefinition()` returns the container service when one exists, else calls `create()` on a `ContainerInjectionInterface` class, else `new` with no arguments. On 11.3.0 and later the collector skips the shim and autowires the class through its constructor, never `create()`, so constructor arguments must be autowirable |
| Anything, after 11.5.0 ships | Classes, and `#[ExtensionFileIsConverted]` on the first function of `.theme` only if it must remain for cores below 11.3.0 | Change record 3581222: the attribute only silences the deprecation; `.theme` files are no longer auto-loaded in Drupal 13. The attribute is not present in 11.4.5 |

Rules that differ from modules, from `core/lib/Drupal/Core/Hook/ThemeHookCollectorPass.php` and change record 3551652:

| Rule | Detail |
|---|---|
| Namespace | `Drupal\<theme>\Hook`, files under `src/Hook/`, `.php` only |
| `module:` parameter | Forbidden. `LogicException("The 'module' parameter on the #[Hook] attribute is not allowed in themes. Found in $class.")` |
| `order:` parameter | Forbidden. `LogicException("The 'order' parameter on the #[Hook] attribute is not allowed in themes. Found in $class.")` |
| `#[ReorderHook]`, `#[RemoveHook]` | Forbidden, each with its own `LogicException` |
| Execution order | Base theme hooks run before the active theme. Cannot be changed |
| Inactive themes | Their hooks do not execute |
| Autowiring | Same as modules: the class is registered as an autowired service named after itself |
| Services | Themes cannot define services. Helper classes that are not hook classes must use `\Drupal::service()` or `\Drupal::classResolver()` (change record 3581222) |
| Procedural scan | `.theme`, `.inc`, and `theme-settings.php` are still scanned. `templates/` is skipped |

## Pattern

Preprocess with injected services, the shape of `core/themes/olivero/src/Hook/OliveroPagePreprocessHooks.php`:

```php
namespace Drupal\my_theme\Hook;

use Drupal\Core\Extension\ThemeSettingsProvider;
use Drupal\Core\Hook\Attribute\Hook;

class MyThemePreprocessHooks {

  public function __construct(
    protected ThemeSettingsProvider $themeSettingsProvider,
  ) {}

  #[Hook('preprocess_html')]
  public function preprocessHtml(array &$variables): void {
    if ($this->themeSettingsProvider->getSetting('mobile_menu_all_widths') === 1) {
      $variables['attributes']['class'][] = 'is-always-mobile-nav';
    }
  }

}
```

Suggestion alter, from `core/themes/claro/src/Hook/ClaroHooks.php`:

```php
#[Hook('theme_suggestions_form_element_alter')]
public function themeSuggestionsFormElementAlter(array &$suggestions, array $variables): void {
  if (!empty($variables['element']['#type'])) {
    $suggestions[] = 'form_element__' . $variables['element']['#type'];
  }
}
```

## The stale core docblock

`core/core.api.php` and `core/lib/Drupal/Core/Hook/Attribute/Hook.php` both still say "Hooks implemented by themes must remain procedural." That sentence predates 11.3.0. `ThemeHookCollectorPass` and the `src/Hook/` classes in Claro and Olivero are the working behavior; the docblock is stale.

## Common Mistakes

- Adding `order:` to a theme hook to run after the base theme → `LogicException` at container build. Base-before-active is fixed.
- Expecting a sub-theme's `src/Hook/` class to run when the parent is active → hooks in inactive themes do not execute.
- Leaving helper functions in `.theme` after converting hooks → the file is deprecated in 11.5.0 and not auto-loaded in 13. Move helpers to a method on the hook class or a utility class.
- Declaring services in a `my_theme.services.yml` → themes cannot define services. Only the hook classes themselves get autowired.

## See Also

- ← [Procedural-Only Hooks](procedural-only-hooks.md) | [Procedural Scan Performance](procedural-scan-performance.md) →
- Preprocess mechanics and variables: https://camoa.github.io/dev-guides/drupal/twig/preprocess-functions/, https://camoa.github.io/dev-guides/drupal/twig/adding-variables-preprocess/
- Theme hook registration and suggestions: https://camoa.github.io/dev-guides/drupal/twig/theme-hooks-registration/, https://camoa.github.io/dev-guides/drupal/twig/template-suggestions/, https://camoa.github.io/dev-guides/drupal/render-api/theme-hooks-suggestions/
- Change records: https://www.drupal.org/node/3551652, https://www.drupal.org/node/3581222
- Reference: `core/lib/Drupal/Core/Hook/ThemeHookCollectorPass.php`, `core/themes/claro/src/Hook/`, `core/themes/olivero/src/Hook/`
