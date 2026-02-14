---
description: Inject Drupal services into block plugins
drupal_version: "11.x"
---

# Dependency Injection in Blocks

## When to Use

Your block plugin needs access to Drupal services (database, config, entity manager, custom services).

## Decision

| At this step... | If... | Then... |
|-----------------|-------|---------|
| Step 1 (interface) | Need any services | Always implement `ContainerFactoryPluginInterface` |
| Step 2 (create) | Many services | Use promoted properties (PHP 8.0+) for brevity |
| Step 3 (constructor) | Parent constructor needed | Always call `parent::__construct()` first |
| Step 4 (usage) | Service might not exist | Handle exceptions or check service exists |

## Pattern

Complete dependency injection example:

```php
namespace Drupal\mymodule\Plugin\Block;

use Drupal\Core\Block\Attribute\Block;
use Drupal\Core\Block\BlockBase;
use Drupal\Core\Config\ConfigFactoryInterface;
use Drupal\Core\Entity\EntityTypeManagerInterface;
use Drupal\Core\Plugin\ContainerFactoryPluginInterface;
use Drupal\Core\Session\AccountInterface;
use Drupal\Core\StringTranslation\TranslatableMarkup;
use Symfony\Component\DependencyInjection\ContainerInterface;

#[Block(
  id: "recent_articles",
  admin_label: new TranslatableMarkup("Recent Articles"),
)]
class RecentArticlesBlock extends BlockBase implements ContainerFactoryPluginInterface {

  public function __construct(
    array $configuration,
    $plugin_id,
    $plugin_definition,
    protected EntityTypeManagerInterface $entityTypeManager,
    protected AccountInterface $currentUser,
    protected ConfigFactoryInterface $configFactory,
  ) {
    parent::__construct($configuration, $plugin_id, $plugin_definition);
  }

  public static function create(
    ContainerInterface $container,
    array $configuration,
    $plugin_id,
    $plugin_definition
  ) {
    return new static(
      $configuration,
      $plugin_id,
      $plugin_definition,
      $container->get('entity_type.manager'),
      $container->get('current_user'),
      $container->get('config.factory')
    );
  }

  public function build() {
    $limit = $this->configFactory->get('mymodule.settings')->get('article_limit');

    $storage = $this->entityTypeManager->getStorage('node');
    $query = $storage->getQuery()
      ->condition('type', 'article')
      ->condition('status', 1)
      ->sort('created', 'DESC')
      ->range(0, $limit)
      ->accessCheck(TRUE);

    $nids = $query->execute();
    $nodes = $storage->loadMultiple($nids);

    $view_builder = $this->entityTypeManager->getViewBuilder('node');
    $build = [];
    foreach ($nodes as $node) {
      $build[] = $view_builder->view($node, 'teaser');
    }

    return $build;
  }

  public function getCacheTags() {
    return ['node_list'];
  }
}
```

**Reference:** `core/modules/system/src/Plugin/Block/SystemBrandingBlock.php` (lines 28-55), `core/modules/user/src/Plugin/Block/UserLoginBlock.php` (lines 41-80)

## Common Mistakes

- **Wrong**: Using `\Drupal::service()` in block plugins → **Right**: Use dependency injection; it's testable and follows best practices
- **Wrong**: Not implementing `ContainerFactoryPluginInterface` → **Right**: Required for DI; without it services can't be injected
- **Wrong**: Wrong parameter order in `__construct()` → **Right**: Must match parent: `($configuration, $plugin_id, $plugin_definition, ...services)`
- **Wrong**: Forgetting to call `parent::__construct()` → **Right**: BlockBase needs to initialize; always call parent
- **Wrong**: Injecting too many services → **Right**: If you need >5 services, consider refactoring logic into a custom service
- **Wrong**: Not type-hinting services → **Right**: Use interfaces (e.g., `EntityTypeManagerInterface`) not classes for flexibility

## See Also

- [Creating Block Plugins](creating-block-plugins.md)
- [Best Practices](best-practices.md)
- Reference: https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/dependency-injection-in-plugin-block
