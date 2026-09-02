---
description: Build custom block plugins with programmatic logic and service integration
tldr: "Use a block plugin when you need programmatic logic, external data, or service integration. Use content blocks when editors need to manage content without code changes."
drupal_version: "11.x"
---

# Creating Block Plugins

## When to Use

> Building a block that requires programmatic logic, external data, or service integration.

## Steps

1. **Create the block plugin file**
   - Location: `{module}/src/Plugin/Block/MyBlock.php`
   - Namespace: `Drupal\{module}\Plugin\Block`

2. **Define the class with #[Block] attribute**
   ```php
   #[Block(
     id: "my_custom_block",
     admin_label: new TranslatableMarkup("My Custom Block"),
     category: new TranslatableMarkup("Custom"),
   )]
   ```

3. **Extend BlockBase and implement build()**
   ```php
   class MyBlock extends BlockBase {
     public function build() {
       return [
         '#markup' => $this->t('Block content'),
       ];
     }
   }
   ```

4. **Clear cache** to discover the plugin
   - `drush cr` or `/admin/config/development/performance`

5. **Place the block** via UI (`/admin/structure/block`) or config

## Decision Points

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

**Reference:** `core/lib/Drupal/Core/Block/Plugin/Block/PageTitleBlock.php`, `core/modules/system/src/Plugin/Block/SystemMessagesBlock.php`

## Common Mistakes

- Forgetting `new TranslatableMarkup()` in attribute → Causes errors; all text in attributes must be TranslatableMarkup
- Returning raw HTML strings → Use render arrays with `#markup` or theme functions
- Not clearing cache after creating plugin → Drupal won't discover the plugin until cache clear
- Using `echo` or `print` in `build()` → Return render arrays only
- Hardcoding text without `$this->t()` → Breaks translations

## See Also

- [Block Configuration Forms](block-configuration.md) (adding settings)
- [Dependency Injection in Blocks](dependency-injection.md) (injecting services)
- [Block Caching Strategies](block-caching.md) (performance)
- Reference: https://www.drupal.org/docs/creating-modules/creating-custom-blocks/create-a-custom-block-plugin
