---
description: Catalog of core service tags — event_subscriber, cache.context, cache.bin, access_check, breadcrumb_builder, service_collector, theme_negotiator, path processors, and more.
---

# Service Tags

## When to Use

When you need to mark a service for special processing by compiler passes — tags group services by purpose and enable extensible architectures.

## Core Service Tags

### event_subscriber
**Description**: Register service as an event subscriber
**Required Interface**: `EventSubscriberInterface`
**Attributes**: None
**Usage**:
```yaml
services:
  my_module.subscriber:
    class: Drupal\my_module\EventSubscriber\MySubscriber
    tags:
      - { name: event_subscriber }
```
**Gotchas**: Must implement `getSubscribedEvents()` static method

---

### cache.context
**Description**: Register a custom cache context
**Required Interface**: `CacheContextInterface`
**Attributes**: None
**Usage**:
```yaml
services:
  cache_context.my_context:
    class: Drupal\my_module\Cache\MyContext
    tags:
      - { name: cache.context }
```
**Gotchas**: Service ID must start with `cache_context.`

---

### cache.bin
**Description**: Register a custom cache bin
**Attributes**: `default_backend` (optional)
**Usage**:
```yaml
services:
  cache.my_bin:
    class: Drupal\Core\Cache\CacheBackendInterface
    tags:
      - { name: cache.bin }
    factory: ['@cache_factory', 'get']
    arguments: ['my_bin']
```

---

### access_check
**Description**: Register an access checker for routes
**Required Interface**: `AccessInterface`
**Attributes**: `applies_to` (routing requirement key)
**Usage**:
```yaml
services:
  my_module.access_check:
    class: Drupal\my_module\Access\MyAccessCheck
    tags:
      - { name: access_check, applies_to: _my_custom_access }
```

---

### breadcrumb_builder
**Description**: Register a breadcrumb builder
**Required Interface**: `BreadcrumbBuilderInterface`
**Attributes**: `priority` (higher = earlier)
**Usage**:
```yaml
services:
  my_module.breadcrumb:
    class: Drupal\my_module\Breadcrumb\MyBreadcrumb
    tags:
      - { name: breadcrumb_builder, priority: 100 }
```

---

### service_collector
**Description**: Collect other tagged services
**Attributes**: `tag` (tag to collect), `call` (method to call), `required` (boolean)
**Usage**:
```yaml
services:
  my_module.manager:
    class: Drupal\my_module\MyManager
    tags:
      - { name: service_collector, tag: my_handler, call: addHandler }
```
**Gotchas**: Eagerly instantiates all collected services

---

### service_id_collector
**Description**: Collect service IDs (not instances) of tagged services
**Attributes**: `tag` (tag to collect)
**Usage**:
```yaml
services:
  my_module.manager:
    class: Drupal\my_module\MyManager
    arguments: [!tagged_iterator my_handler]
    tags:
      - { name: service_id_collector, tag: my_handler }
```
**Gotchas**: Lazy loading — services instantiated when iterated

---

### theme_negotiator
**Description**: Register a theme negotiator
**Required Interface**: `ThemeNegotiatorInterface`
**Attributes**: `priority` (higher = earlier)
**Usage**:
```yaml
tags:
  - { name: theme_negotiator, priority: 50 }
```

---

### path_processor_inbound
**Description**: Process inbound URL paths
**Required Interface**: `InboundPathProcessorInterface`
**Attributes**: `priority`

---

### path_processor_outbound
**Description**: Process outbound URL paths
**Required Interface**: `OutboundPathProcessorInterface`
**Attributes**: `priority`

---

### route_subscriber
**Description**: Alter route definitions (deprecated — use event_subscriber instead)
**Required Interface**: `EventSubscriberInterface`
**Deprecated**: Use `event_subscriber` tag and listen to `RoutingEvents::ALTER`

Reference: `/core/core.api.php` (Service Tags API group), `/core/core.services.yml` (examples)

## Common Mistakes

- **Tagging without implementing required interface** — Compiler pass expects interface; will throw exception
- **Wrong tag name** — Tags are case-sensitive; `event_Subscriber` won't work
- **Missing tag attributes** — Some tags require attributes like `applies_to` for `access_check`
- **Using deprecated tags** — Check Drupal version change records for deprecated tags
- **Forgetting priority** — Services without priority default to 0; explicitly set priority to control order

## See Also

- [Tagged Service Collectors](tagged-service-collectors.md)
- [Service Tags](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/service-tags)
