---
description: Complete reference of all properties available in service definitions — class, arguments, tags, calls, factory, autowire, autoconfigure, shared, lazy, deprecated, and more.
---

# Service Definition Properties

## When to Use

When defining a service in *.services.yml — this reference catalog covers all available properties and their purposes.

## Properties

### class
**Description**: Fully-qualified class name for the service
**Required**: Yes (unless using `parent:` or `alias:`)
**Example**:
```yaml
services:
  my_module.manager:
    class: Drupal\my_module\MyManager
```

---

### arguments
**Description**: Constructor arguments passed when instantiating the service
**Type**: Array (ordered list)
**Syntax**:
- `@service_id` — Inject another service
- `%parameter_name%` — Inject a parameter value
- Scalar values — String, integer, boolean, null
- `@?optional_service` — Optional service (null if not available)

**Example**:
```yaml
services:
  my_module.manager:
    class: Drupal\my_module\MyManager
    arguments:
      - '@database'
      - '@logger.factory'
      - '%site.path%'
      - 'scalar string value'
```

---

### tags
**Description**: Mark the service for special handling by compiler passes
**Type**: Array of associative arrays
**Syntax**:
```yaml
tags:
  - { name: tag_name }
  - { name: tag_name, priority: 100, custom_attr: value }
```
**Common Tags**: `event_subscriber`, `cache.context`, `access_check`, `breadcrumb_builder`, `service_collector`

See [Service Tags](service-tags.md) for complete catalog.

---

### calls
**Description**: Method calls to execute after instantiation (setter injection)
**Type**: Array of method calls
**Example**:
```yaml
calls:
  - [setLogger, ['@logger.factory']]
  - [setContainer, ['@service_container']]
```

---

### factory
**Description**: Factory service and method to create the service instance
**Syntax**: `['@factory_service', 'createMethod']`
**Example**:
```yaml
factory: ['@my_module.factory', 'create']
```

See [Factory Services](factory-services.md) for details.

---

### parent
**Description**: Inherit from another service definition
**Type**: Service ID string
**Example**:
```yaml
services:
  default_plugin_manager:
    abstract: true
    class: Drupal\Core\Plugin\DefaultPluginManager

  plugin.manager.my_plugin:
    parent: default_plugin_manager
    arguments: ['@container.namespaces', '@cache.discovery', '@module_handler']
```

---

### abstract
**Description**: Mark service as a template (not instantiable)
**Type**: Boolean
**Use**: With `parent:` to create service templates
**Example**:
```yaml
abstract: true
```

---

### public
**Description**: Whether service is accessible via `\Drupal::service()`
**Type**: Boolean
**Default**: `true` in Drupal (Symfony 6/7 default is `false`)
**Example**:
```yaml
public: false  # Only accessible via dependency injection
```

---

### autowire
**Description**: Enable autowiring for constructor arguments
**Type**: Boolean
**Default**: `false`
**Example**:
```yaml
autowire: true
```

See [Autowiring](autowiring.md) for details.

---

### autoconfigure
**Description**: Automatically tag services based on interfaces they implement
**Type**: Boolean
**Default**: `false` (set to `true` in `_defaults` in Drupal 11+)
**Behavior**: If a service implements `EventSubscriberInterface`, automatically add `event_subscriber` tag
**Example**:
```yaml
autoconfigure: true
```

---

### shared
**Description**: Whether service is singleton or creates new instance each time
**Type**: Boolean
**Default**: `true` (singleton)
**Example**:
```yaml
shared: false  # New instance on each request
```

---

### synthetic
**Description**: Service is injected into container externally (not created by container)
**Type**: Boolean
**Use**: For services set via `$container->set()` (rare in Drupal)
**Example**:
```yaml
synthetic: true
```

---

### lazy
**Description**: Wrap service in a lazy-loading proxy
**Type**: Boolean
**Performance**: Delays instantiation until first method call
**Example**:
```yaml
lazy: true
```

---

### deprecated
**Description**: Mark service as deprecated
**Type**: String (deprecation message)
**Example**:
```yaml
deprecated: 'The "%service_id%" service is deprecated. Use "new_service" instead.'
```

Reference: `/core/core.services.yml` (examples throughout), Symfony DependencyInjection component documentation

## Common Mistakes

- **Wrong argument order** — Arguments must match constructor parameter order
- **Missing @ prefix** — `database` is a string, `@database` is the database service
- **Using calls for required dependencies** — Use constructor injection for required deps, setter injection for optional
- **Setting public: false without understanding implications** — Service won't be accessible via \Drupal::service()
- **Enabling autowire without type hints** — Autowiring requires typed constructor parameters

## See Also

- [services.yml Schema](services-yml-schema.md)
- [Defining Services](defining-services.md)
- [Structure of a service file](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/structure-of-a-service-file)
