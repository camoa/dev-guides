---
description: Using factories for complex service instantiation — factory classes, static factory methods, YAML factory configuration, and the core logger factory pattern.
---

# Factory Services

## When to Use

When a service requires complex instantiation logic, runtime parameters, or conditional creation — factories encapsulate creation logic.

## Steps

1. **Create a factory service**
   ```php
   namespace Drupal\my_module;

   use Drupal\Core\Database\Connection;
   use Psr\Log\LoggerInterface;

   class MyServiceFactory {

     public function __construct(
       protected Connection $database,
       protected LoggerInterface $logger,
     ) {}

     public function create(string $type): MyServiceInterface {
       return match ($type) {
         'foo' => new FooService($this->database, $this->logger),
         'bar' => new BarService($this->database),
         default => throw new \InvalidArgumentException("Unknown type: $type"),
       };
     }
   }
   ```

2. **Register factory and services in YAML**
   ```yaml
   services:
     my_module.factory:
       class: Drupal\my_module\MyServiceFactory
       arguments: ['@database', '@logger.channel.my_module']

     my_module.service_foo:
       class: Drupal\my_module\FooService
       factory: ['@my_module.factory', 'create']
       arguments: ['foo']

     my_module.service_bar:
       class: Drupal\my_module\BarService
       factory: ['@my_module.factory', 'create']
       arguments: ['bar']
   ```

3. **Use the factory directly in code**
   ```php
   public function __construct(
     protected MyServiceFactory $factory,
   ) {}

   public function doSomething() {
     $service = $this->factory->create('foo');
     $service->execute();
   }
   ```

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Choosing factory vs direct | Service needs runtime parameters | Use factory |
| Choosing factory vs direct | Service creation is complex (5+ lines) | Use factory |
| Choosing factory vs direct | Service is simple dependency injection | Direct instantiation via YAML |
| Factory location | Factory is reusable across services | Separate factory class |
| Factory location | Factory is single-purpose | Static factory method on service class |

## Pattern

**Static Factory Method**:
```php
namespace Drupal\my_module;

class MyService {

  public static function create(Connection $database, string $type): self {
    $instance = new static($database);
    $instance->setType($type);
    return $instance;
  }

  protected function __construct(
    protected Connection $database,
  ) {}
}
```

```yaml
services:
  my_module.service:
    class: Drupal\my_module\MyService
    factory: ['Drupal\my_module\MyService', 'create']
    arguments: ['@database', 'foo']
```

**Logger Factory Pattern (Core Example)**:
```yaml
# From core.services.yml
logger.factory:
  class: Drupal\Core\Logger\LoggerChannelFactory

logger.channel.default:
  class: Drupal\Core\Logger\LoggerChannel
  factory: ['@logger.factory', 'get']
  arguments: ['default']
```

Reference: `/core/lib/Drupal/Core/Logger/LoggerChannelFactory.php`, `/core/core.services.yml` (search for `factory:`)

## Common Mistakes

- **Using factory when not needed** — Simple DI doesn't need factory; use direct class + arguments
- **Factory with too much logic** — Keep factories focused on instantiation, not business logic
- **Not injecting factory dependencies** — Factory should receive its own dependencies via DI
- **Returning different interfaces** — Factory should return consistent interface/base class
- **Forgetting cache rebuild** — Adding factory methods requires container rebuild

## See Also

- [Core Services Reference](core-services-reference.md)
- [DependencySerializationTrait](dependency-serialization-trait.md)
