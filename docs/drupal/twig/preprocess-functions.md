---
topic: drupal/twig
guide: preprocess-functions
---

## Preprocess Functions

### When to Use
When you need to prepare data for templates, pass custom variables, modify existing variables, or manipulate the rendering pipeline before a template renders.

### Decision
| Level | Format | When to use |
|---|---|---|
| Theme-specific hook | `THEME_preprocess_HOOK(&$vars)` | In `.theme` file — most common for theme work |
| Theme-generic | `THEME_preprocess(&$vars, $hook)` | All templates — use sparingly |
| Module-specific hook | OOP with `#[Hook('preprocess_HOOK')]` | In module `src/Hook/` class |
| Module-generic | OOP with `#[Hook('preprocess')]` | All templates from a module — rare |
| Initial preprocess | Registered in `hook_theme()` | Runs first, sets base variables (core pattern) |

### Preprocess Execution Order
Drupal calls preprocess functions in this order for each template render:
1. **Initial preprocess** — registered in `hook_theme()` `'initial preprocess'` key (core only)
2. **Module preprocess** — `MODULE_preprocess_HOOK()` or `#[Hook('preprocess_HOOK')]`
3. **Theme base preprocess** — parent theme's `THEME_preprocess_HOOK()`
4. **Theme preprocess** — active theme's `THEME_preprocess_HOOK()`

Later preprocessors can override earlier ones. Theme always wins over modules.

**Drupal 11.2+ note:** `template_preprocess()` and `template_preprocess_HOOK()` procedural functions in `theme.inc` are deprecated and delegate to OOP service classes. New code should never call or override these.

### Pattern

**Procedural (in `.theme` file — still the norm for themes):**
```php
// mytheme.theme
function mytheme_preprocess_node(&$variables) {
  $node = $variables['node'];
  // Only for article nodes in full view mode
  if ($node->bundle() === 'article' && $variables['view_mode'] === 'full') {
    $variables['reading_time'] = ceil(str_word_count(
      strip_tags($node->body->processed ?? '')
    ) / 200);
  }
}
```

**OOP (Drupal 11.2+ modules; Drupal 11.3+ themes):**
```php
// src/Hook/NodeHooks.php
namespace Drupal\mymodule\Hook;
use Drupal\Core\Hook\Attribute\Hook;

class NodeHooks {
  #[Hook('preprocess_node')]
  public function preprocessNode(array &$variables): void {
    $variables['my_custom_var'] = 'value';
  }
}
```

**Theme OOP hooks (Drupal 11.3+):**
```php
// themes/custom/mytheme/src/Hook/ThemeHooks.php
namespace Drupal\mytheme\Hook;
use Drupal\Core\Hook\Attribute\Hook;

class ThemeHooks {
  #[Hook('preprocess_node')]
  public function preprocessNode(array &$variables): void {
    // Same as mytheme_preprocess_node()
  }
}
```

### Common Mistakes
- Adding complex business logic or DB queries in preprocess → performance problem; preprocess runs on every render
- Calling `\Drupal::service()` statically in preprocess when using OOP hooks → inject dependencies via constructor
- Overriding `template_preprocess_node()` in a module → that function is deprecated in 11.2; implement `#[Hook('preprocess_node')]` instead
- Forgetting `&$variables` — pass by reference or your changes are lost
- Using procedural `THEME_preprocess_HOOK()` in themes when they need to support Drupal < 11.3 → stick with procedural for now if supporting older core

### See Also
- Adding variables → [Adding Variables in Preprocess](adding-variables-preprocess.md)
- Core source: `core/lib/Drupal/Core/Theme/ThemeManager.php`
- Node theme hooks: `core/modules/node/src/Hook/NodeThemeHooks.php`
