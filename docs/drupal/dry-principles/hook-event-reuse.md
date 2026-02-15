---
description: Share logic across Drupal hooks and event subscribers by delegating to services instead of duplicating code in each hook.
---

# Hook and Event Reuse

## When to Use

When you need to respond to system events (entity operations, form alterations, request processing) without duplicating logic across similar hooks or event subscribers.

## Hooks vs Events (Drupal 11+)

| Mechanism | Use When | Example |
|-----------|----------|---------|
| **Hook classes (attributes)** | Standard Drupal operations (form alter, entity presave, theme) | `#[Hook('form_alter')]`, `#[Hook('entity_presave')]` |
| **Event subscribers** | Symfony events, custom events | `KernelEvents::REQUEST`, custom domain events |
| **Legacy .module hooks** | Legacy code (being phased out) | `hook_form_alter()`, `hook_preprocess_HOOK()` |

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Alter forms | Hook class with `#[Hook('form_alter')]` | Modern, OOP, supports DI and autowiring |
| React to entity save | Hook class with `#[Hook('entity_presave')]` | Standard Drupal pattern |
| Custom application event | Event dispatcher + subscribers | Decoupled, reusable across modules |
| Shared hook logic across forms | Base hook class or service method | Avoid duplicating logic in each hook |

## Pattern

```php
// Modern hook class (Drupal 11+)
namespace Drupal\mymodule\Hook;

use Drupal\Core\Hook\Attribute\Hook;
use Drupal\Core\Form\FormStateInterface;

class MyModuleHooks {

  public function __construct(
    protected MyService $myService,
  ) {}

  #[Hook('form_alter')]
  public function formAlter(array &$form, FormStateInterface $form_state, string $form_id): void {
    // Shared validation logic via service
    if (str_starts_with($form_id, 'node_')) {
      $this->myService->addCustomValidation($form, $form_state);
    }
  }

  #[Hook('entity_presave')]
  public function entityPresave($entity): void {
    if ($entity->getEntityTypeId() === 'node') {
      // Shared presave logic
      $this->myService->processNode($entity);
    }
  }
}
```

```php
// Extract shared logic to service
class MyService {

  public function addCustomValidation(array &$form, FormStateInterface $form_state): void {
    // Logic used by multiple form_alter implementations
    $form['#validate'][] = [$this, 'validateCustomField'];
  }

  public function processNode($node): void {
    // Logic used by multiple entity hooks
    if (!$node->get('field_custom')->isEmpty()) {
      // Process custom field
    }
  }
}
```

Reference: `core/lib/Drupal/Core/Hook/`, `core/modules/system/src/Hook/SystemHooks.php`, `core/lib/Drupal/Component/EventDispatcher/`

## Event Subscribers (When Needed)

```php
namespace Drupal\mymodule\EventSubscriber;

use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\HttpKernel\KernelEvents;

class MyEventSubscriber implements EventSubscriberInterface {

  public static function getSubscribedEvents() {
    return [
      KernelEvents::REQUEST => ['onRequest', 100],
    ];
  }

  public function onRequest($event): void {
    // Event logic
  }
}
```

## Common Mistakes

- **Duplicating logic across similar hooks** — Extract to service method, call from multiple hooks
- **Using event subscribers for standard Drupal operations** — Use hook classes (modern) for form_alter, entity hooks, theme hooks
- **Complex logic directly in hook** — Keep hooks thin, delegate to services
- **Not checking entity type/bundle in generic hooks** — Always filter in entity_presave, entity_insert, etc.
- **Multiple event subscribers doing similar things** — Consolidate into one subscriber or extract shared logic to service

## See Also

- [Render Array Patterns](render-array-patterns.md)
- [Config Split and Environments](config-split-environments.md)
- Reference: [Subscribe to and dispatch events | Drupal.org](https://www.drupal.org/docs/develop/creating-modules/subscribe-to-and-dispatch-events)
- Reference: [Hooks Vs Events in Drupal | Specbee](https://www.specbee.com/blogs/hooks-vs-events-in-drupal-making-informed-choice)
