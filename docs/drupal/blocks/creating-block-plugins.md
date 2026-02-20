---
description: Build custom block plugins with programmatic logic and service integration
drupal_version: "11.x"
---

# Creating Block Plugins

## When to Use

> Use a block plugin when you need programmatic logic, external data, or service integration. Use content blocks when editors need to manage content without code changes.

## Decision

| At this step... | If... | Then... |
|-----------------|-------|---------|
| Step 2 (attribute) | Block needs services | Add `ContainerFactoryPluginInterface`, implement `create()` |
| Step 3 (build) | Content is user-specific | Add cache context `user` |
| Step 3 (build) | Content changes frequently | Set `#cache['max-age']` |
| Step 3 (build) | Block should sometimes hide | Return empty array `[]` when hidden |

## Pattern

Complete block plugin structure:

```php
namespace Drupal\mymodule\Plugin\Block;

use Drupal\Core\Block\Attribute\Block;
use Drupal\Core\Block\BlockBase;
use Drupal\Core\StringTranslation\TranslatableMarkup;

#[Block(
  id: "hello_world",
  admin_label: new TranslatableMarkup("Hello World"),
  category: new TranslatableMarkup("Custom"),
)]
class HelloWorldBlock extends BlockBase {

  public function build() {
    return [
      '#markup' => $this->t('Hello, World!'),
    ];
  }
}
```

**Steps:**

1. Create file: `{module}/src/Plugin/Block/MyBlock.php`
2. Add `#[Block]` attribute with `id`, `admin_label`, `category`
3. Extend `BlockBase` and implement `build()`
4. Clear cache: `drush cr`
5. Place via UI: `/admin/structure/block`

**Reference:** `core/lib/Drupal/Core/Block/Plugin/Block/PageTitleBlock.php`, `core/modules/system/src/Plugin/Block/SystemMessagesBlock.php`

## Common Mistakes

- **Wrong**: Forgetting `new TranslatableMarkup()` in attribute → **Right**: All text in attributes must be TranslatableMarkup
- **Wrong**: Returning raw HTML strings → **Right**: Use render arrays with `#markup` or theme functions
- **Wrong**: Not clearing cache after creating plugin → **Right**: Drupal won't discover the plugin until cache clear
- **Wrong**: Using `echo` or `print` in `build()` → **Right**: Return render arrays only
- **Wrong**: Hardcoding text without `$this->t()` → **Right**: Breaks translations

## See Also

- [Block Configuration Forms](block-configuration.md)
- [Dependency Injection in Blocks](dependency-injection.md)
- [Block Caching Strategies](block-caching.md)
- Reference: https://www.drupal.org/docs/creating-modules/creating-custom-blocks/create-a-custom-block-plugin
