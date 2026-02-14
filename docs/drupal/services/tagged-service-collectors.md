---
description: Building extensible systems with tagged service collectors — service_collector tag, addHandler pattern, tagged_iterator for lazy loading, and named arguments.
---

# Tagged Service Collectors

## When to Use

When you need to build an extensible system where multiple services can register themselves to be used by a manager service — plugin-like architecture without the plugin API overhead.

## Steps

1. **Define the collector service**
   ```yaml
   services:
     my_module.handler_manager:
       class: Drupal\my_module\HandlerManager
       tags:
         - { name: service_collector, tag: my_handler, call: addHandler }
   ```

2. **Implement the collector class with addHandler() method**
   ```php
   namespace Drupal\my_module;

   class HandlerManager {

     protected array $handlers = [];

     public function addHandler(HandlerInterface $handler, int $priority = 0) {
       $this->handlers[$priority][] = $handler;
     }

     public function getHandlers(): array {
       krsort($this->handlers);
       return array_merge(...$this->handlers);
     }
   }
   ```

3. **Define handler services with the tag**
   ```yaml
   services:
     my_module.handler_foo:
       class: Drupal\my_module\Handler\FooHandler
       tags:
         - { name: my_handler, priority: 100 }

     my_module.handler_bar:
       class: Drupal\my_module\Handler\BarHandler
       tags:
         - { name: my_handler, priority: 50 }
   ```

4. **Alternative: Use !tagged_iterator (Drupal 11+ / Symfony 7+)**
   ```yaml
   services:
     my_module.handler_manager:
       class: Drupal\my_module\HandlerManager
       arguments:
         - !tagged_iterator my_handler
   ```

   ```php
   namespace Drupal\my_module;

   class HandlerManager {

     public function __construct(
       protected iterable $handlers,
     ) {}

     public function getHandlers(): array {
       return iterator_to_array($this->handlers);
     }
   }
   ```

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Choosing collection method | Drupal 10.x | Use `service_collector` tag |
| Choosing collection method | Drupal 11+ | Prefer `!tagged_iterator` for lazy loading |
| Naming the tag | Tag is public API | Document tag name and required interface |
| Naming the tag | Tag is internal | Use module-prefixed name |
| Handling priority | Order matters | Accept `$priority` param in addHandler(), sort in getter |

## Pattern

**Named Arguments in addHandler() (Drupal 11+)**:
```php
// Compiler pass injects tag attributes as named parameters
public function addHandler(
  HandlerInterface $handler,
  string $id,  // Service ID
  int $priority = 0,
  string $custom_attribute = '',
) {
  $this->handlers[$priority][$id] = [
    'handler' => $handler,
    'custom' => $custom_attribute,
  ];
}
```

```yaml
services:
  my_module.handler_foo:
    tags:
      - { name: my_handler, priority: 100, custom_attribute: 'foo_value' }
```

Reference: `/core/lib/Drupal/Core/DependencyInjection/Compiler/TaggedHandlersPass.php`, [Service collectors deep dive](https://tech.sparkfabrik.com/en/blog/drupal-service-container-deep-dive-part-3/)

## Common Mistakes

- **Eagerly instantiating all handlers** — `service_collector` creates all instances at manager creation; use `!tagged_iterator` for lazy loading
- **Not sorting by priority** — Handlers are passed in random order; sort them yourself if order matters
- **Missing type hint on $handler parameter** — TaggedHandlersPass requires type hint to validate handlers
- **Using service locator pattern** — Don't inject the container to fetch handlers; collect them via tags
- **Forgetting to document the tag** — Other developers won't know to use your tag without documentation

## See Also

- [Service Tags](service-tags.md)
- [Event Subscribers](event-subscribers.md)
- [Practical Use Cases of Tagged Services in Drupal](https://drupal.com.ua/135/practical-use-cases-tagged-services-drupal)
- [Services can now use tagged iterators](https://www.drupal.org/node/3436859)
