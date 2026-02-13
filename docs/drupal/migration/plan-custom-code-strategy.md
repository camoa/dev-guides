---
description: Rewrite vs retrofit vs retire strategy for D7 custom modules in D11
drupal_version: "11.x"
---

# Plan Custom Code Strategy

## When to Use

D7 custom modules use hooks, procedural code, and deprecated APIs. D11 requires object-oriented plugins, services, event subscribers. Decide: rewrite, retrofit, or retire each custom module.

## Decision

| If the module... | Strategy | Timeline impact |
|---|---|---|
| Provides core-equivalent functionality | Retire, use D11 core | Eliminates maintenance burden |
| Has contrib D11 replacement | Retire, use contrib | Faster than custom rewrite |
| Business-critical, complex logic | Rewrite using D11 patterns | 4-8 weeks per module |
| Temporary need, deprecated soon | Retrofit, plan replacement | Bridge solution only |
| Simple form/block functionality | Rewrite quickly | 1-2 weeks per module |

## Pattern

**D7 hook to D11 event subscriber:**

```php
// D7: hook_node_presave in custom.module
function custom_node_presave($node) {
  if ($node->type == 'article') {
    $node->field_updated[LANGUAGE_NONE][0]['value'] = time();
  }
}

// D11: Event subscriber in src/EventSubscriber/NodeEventSubscriber.php
namespace Drupal\custom\EventSubscriber;

use Drupal\Core\Entity\EntityInterface;
use Drupal\hook_event_dispatcher\HookEventDispatcherInterface;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class NodeEventSubscriber implements EventSubscriberInterface {

  public static function getSubscribedEvents() {
    return [
      HookEventDispatcherInterface::ENTITY_PRE_SAVE => 'onEntityPresave',
    ];
  }

  public function onEntityPresave(Event $event) {
    $entity = $event->getEntity();
    if ($entity->getEntityTypeId() === 'node' && $entity->bundle() === 'article') {
      $entity->set('field_updated', \Drupal::time()->getRequestTime());
    }
  }
}
```

**Reference**: `/core/lib/Drupal/Core/EventSubscriber/` for core event subscribers

## Common Mistakes

- **Wrong**: Attempting to run D7 code in D11 without Retrofit → **Right**: PHP/API incompatibilities cause fatal errors
- **Wrong**: Rewriting modules no longer needed → **Right**: Check if D11 core or contrib provides functionality
- **Wrong**: Not using dependency injection → **Right**: Static calls make code untestable, violates D11 standards
- **Wrong**: Copying D7 architecture patterns → **Right**: Embrace D11's plugin system, service layer

## See Also

- Reference: [Drupal 11 coding standards](https://www.drupal.org/docs/develop/standards)
- Reference: [Plugin API](https://www.drupal.org/docs/drupal-apis/plugin-api)
- Reference: [Services and dependency injection](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection)
