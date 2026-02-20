---
description: Architectural guidance for maintainable, performant, testable block plugins
drupal_version: "11.x"
---

# Best Practices

## When to Use

> Apply these patterns when building any block plugin. These are the architectural decisions that keep blocks maintainable, testable, and performant.

## Decision

| Area | Best Practice | Why |
|------|---------------|-----|
| **Architecture** | Use block plugins for logic, content blocks for content | Separation of concerns, right tool for the job |
| **Dependency Injection** | Always inject services via DI, never use `\Drupal::service()` | Testable, follows Symfony best practices |
| **Caching** | Add granular cache contexts, not `max-age = 0` | Performance; vary cache by actual conditions |
| **Access Control** | Use `blockAccess()` with proper cache metadata | Security + performance; leverages Drupal's access system |
| **Configuration** | Validate in `blockValidate()`, transform in `blockSubmit()` | Data integrity, separation of concerns |
| **Naming** | Use descriptive plugin IDs: `{module}_{purpose}` | Avoid conflicts, clear purpose |
| **Return Values** | Return render arrays from `build()`, never echo/print | Proper render pipeline, themeable, cacheable |
| **Empty Blocks** | Return `[]` (empty array) when block should hide | Drupal won't render wrapper; better than conditional in template |
| **Cache Tags** | Tag with entities/config your block depends on | Auto-invalidation when dependencies change |
| **Translations** | Wrap all user-facing text in `$this->t()` | i18n support, translatable UI |

## Pattern

**Ideal block plugin structure:**

```php
namespace Drupal\mymodule\Plugin\Block;

use Drupal\Core\Block\Attribute\Block;
use Drupal\Core\Block\BlockBase;
use Drupal\Core\Cache\Cache;
use Drupal\Core\Entity\EntityTypeManagerInterface;
use Drupal\Core\Form\FormStateInterface;
use Drupal\Core\Plugin\ContainerFactoryPluginInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;

#[Block(
  id: "mymodule_recent_content",
  admin_label: new TranslatableMarkup("Recent Content"),
  category: new TranslatableMarkup("Content"),
)]
class RecentContentBlock extends BlockBase implements ContainerFactoryPluginInterface {

  public function __construct(
    array $configuration,
    $plugin_id,
    $plugin_definition,
    protected EntityTypeManagerInterface $entityTypeManager,
  ) {
    parent::__construct($configuration, $plugin_id, $plugin_definition);
  }

  public static function create(ContainerInterface $container, array $configuration, $plugin_id, $plugin_definition) {
    return new static($configuration, $plugin_id, $plugin_definition, $container->get('entity_type.manager'));
  }

  public function defaultConfiguration() {
    return ['items_count' => 5, 'content_type' => 'article'] + parent::defaultConfiguration();
  }

  public function blockForm($form, FormStateInterface $form_state) {
    $form['items_count'] = [
      '#type' => 'number',
      '#title' => $this->t('Number of items'),
      '#default_value' => $this->configuration['items_count'],
      '#min' => 1, '#max' => 20,
    ];
    return $form;
  }

  public function blockValidate($form, FormStateInterface $form_state) {
    $count = $form_state->getValue('items_count');
    if ($count < 1 || $count > 20) {
      $form_state->setErrorByName('items_count', $this->t('Count must be 1-20'));
    }
  }

  public function blockSubmit($form, FormStateInterface $form_state) {
    $this->configuration['items_count'] = (int) $form_state->getValue('items_count');
  }

  public function build() {
    $storage = $this->entityTypeManager->getStorage('node');
    $nids = $storage->getQuery()
      ->condition('type', $this->configuration['content_type'])
      ->condition('status', 1)
      ->sort('created', 'DESC')
      ->range(0, $this->configuration['items_count'])
      ->accessCheck(TRUE)
      ->execute();

    if (empty($nids)) {
      return []; // No render when empty
    }

    $nodes = $storage->loadMultiple($nids);
    $view_builder = $this->entityTypeManager->getViewBuilder('node');
    return array_map(fn($n) => $view_builder->view($n, 'teaser'), $nodes);
  }

  public function getCacheTags() {
    return Cache::mergeTags(parent::getCacheTags(), ['node_list:' . $this->configuration['content_type']]);
  }

  public function getCacheContexts() {
    return Cache::mergeContexts(parent::getCacheContexts(), ['user.permissions']);
  }
}
```

**Code organization:**
- One block plugin per file: `{module}/src/Plugin/Block/{ClassName}.php`
- Use typed properties (PHP 8.0+)
- Test: Unit (mock services), Kernel (real services), Functional (UI placement)

## Common Mistakes

- **Wrong**: Not calling `parent::defaultConfiguration()` → **Right**: Loses base block settings
- **Wrong**: Using global functions (`\Drupal::`, `node_load()`) → **Right**: Not testable, tight coupling
- **Wrong**: Complex logic in `build()` without service extraction → **Right**: Hard to test, reuse
- **Wrong**: Not handling empty results → **Right**: Block wrapper renders even when empty
- **Wrong**: Hardcoding translatable strings → **Right**: Breaks multilingual sites
- **Wrong**: Over-configuring simple blocks → **Right**: Keep UI simple; expose only necessary settings

## See Also

- [Creating Block Plugins](creating-block-plugins.md)
- [Dependency Injection in Blocks](dependency-injection.md)
- [Block Caching Strategies](block-caching.md)
- [Security & Performance](security-performance.md)
- Reference: https://www.drupal.org/docs/develop/coding-standards
