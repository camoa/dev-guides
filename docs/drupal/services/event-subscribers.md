---
description: Creating event subscribers — implementing EventSubscriberInterface, registering with tags or autoconfigure, kernel events, entity events, and priority ordering.
---

# Event Subscribers

## When to Use

When you need to react to events in Drupal — kernel events (request, response, exception), entity events (CRUD operations), or custom events.

## Steps

1. **Create the event subscriber class**
   ```php
   namespace Drupal\my_module\EventSubscriber;

   use Symfony\Component\EventDispatcher\EventSubscriberInterface;
   use Symfony\Component\HttpKernel\Event\RequestEvent;
   use Symfony\Component\HttpKernel\KernelEvents;

   class MySubscriber implements EventSubscriberInterface {

     public static function getSubscribedEvents(): array {
       return [
         KernelEvents::REQUEST => ['onRequest', 100],
         KernelEvents::RESPONSE => 'onResponse',
       ];
     }

     public function onRequest(RequestEvent $event): void {
       // React to request
     }

     public function onResponse($event): void {
       // React to response
     }
   }
   ```

2. **Register as a service with event_subscriber tag**
   ```yaml
   services:
     my_module.subscriber:
       class: Drupal\my_module\EventSubscriber\MySubscriber
       tags:
         - { name: event_subscriber }
   ```

3. **Alternative: Use autoconfigure (Drupal 11+)**
   ```yaml
   services:
     _defaults:
       autoconfigure: true

     my_module.subscriber:
       class: Drupal\my_module\EventSubscriber\MySubscriber
       # No tags needed — autoconfigure detects EventSubscriberInterface
   ```

4. **Inject dependencies if needed**
   ```php
   class MySubscriber implements EventSubscriberInterface {

     public function __construct(
       protected LoggerInterface $logger,
     ) {}

     public function onRequest(RequestEvent $event): void {
       $this->logger->info('Request received');
     }
   }
   ```

   ```yaml
   services:
     my_module.subscriber:
       class: Drupal\my_module\EventSubscriber\MySubscriber
       arguments: ['@logger.channel.my_module']
       tags:
         - { name: event_subscriber }
   ```

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Choosing event | Need to modify request | Listen to `KernelEvents::REQUEST` |
| Choosing event | Need to modify response | Listen to `KernelEvents::RESPONSE` |
| Choosing event | Need entity CRUD hooks | Listen to entity events (see entity.events service) |
| Setting priority | Need to run before other subscribers | Higher priority (positive number, e.g., 100) |
| Setting priority | Need to run after other subscribers | Lower priority (negative number, e.g., -100) |

## Pattern

**Common Kernel Events**:
```php
use Symfony\Component\HttpKernel\KernelEvents;

KernelEvents::REQUEST     // Before routing, controller execution
KernelEvents::CONTROLLER  // After controller resolver, before controller execution
KernelEvents::VIEW        // When controller returns non-Response
KernelEvents::RESPONSE    // Before sending response
KernelEvents::TERMINATE   // After sending response
KernelEvents::EXCEPTION   // When exception is thrown
```

**Entity Events**:
```php
use Drupal\Core\Entity\EntityTypeEvents;

EntityTypeEvents::CREATE   // New entity type created
EntityTypeEvents::UPDATE   // Entity type updated
EntityTypeEvents::DELETE   // Entity type deleted
```

For entity CRUD, use hooks (hook_entity_insert, hook_entity_update) or entity event subscribers via entity.events service.

Reference: `/core/lib/Drupal/Core/EventSubscriber/` (core examples), [Subscribe to and dispatch events](https://www.drupal.org/docs/develop/creating-modules/subscribe-to-and-dispatch-events)

## Common Mistakes

- **Returning array keys without event name** — `return [100 => 'onRequest']` is wrong; must be `['event.name' => ...]`
- **Wrong priority order** — Higher number = earlier execution (100 runs before 50)
- **Not stopping propagation when needed** — Call `$event->stopPropagation()` if your subscriber should prevent others from running
- **Heavy processing in high-frequency events** — KernelEvents::REQUEST runs on every request; keep it fast
- **Assuming event objects are mutable** — Some events are immutable; check event class documentation
- **Forgetting to clear cache** — New subscribers require cache rebuild

## See Also

- [Tagged Service Collectors](tagged-service-collectors.md)
- [Service Providers and Altering](service-providers-and-altering.md)
- [Events (Drupal at your Fingertips)](https://www.drupalatyourfingertips.com/events)
- [Subscribe to and dispatch events](https://www.drupal.org/docs/develop/creating-modules/subscribe-to-and-dispatch-events)
