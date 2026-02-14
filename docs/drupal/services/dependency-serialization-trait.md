---
description: Handling service serialization with DependencySerializationTrait — how it replaces service objects with IDs during serialize and restores them on wakeup.
---

# DependencySerializationTrait

## When to Use

When your service or class is serialized (stored in cache, queued, etc.) and contains injected service dependencies — this trait prevents serializing the entire service object graph.

## Steps

1. **Use the trait in your class**
   ```php
   namespace Drupal\my_module;

   use Drupal\Core\DependencyInjection\DependencySerializationTrait;
   use Drupal\Core\Database\Connection;
   use Psr\Log\LoggerInterface;

   class MyService {

     use DependencySerializationTrait;

     public function __construct(
       protected Connection $database,
       protected LoggerInterface $logger,
     ) {}

     public function doSomething() {
       // Service is now serialization-safe
     }
   }
   ```

2. **The trait handles serialization automatically**
   - **On serialize (`__sleep`)**: Replaces service objects with service IDs
   - **On unserialize (`__wakeup`)**: Reloads services from container by ID

3. **No additional code needed** — trait is fully automatic

## How It Works

**Before serialization**:
```php
$service->database     // Instance of Connection
$service->logger       // Instance of LoggerChannel
```

**After serialize + unserialize**:
```php
// Trait detected these were services and:
// 1. Stored their service IDs ('database', 'logger.channel.my_module')
// 2. Removed the objects during serialization
// 3. Re-fetched fresh instances from container on wakeup

$service->database     // Fresh instance of Connection from container
$service->logger       // Fresh instance of LoggerChannel from container
```

## Pattern

**Entity Storage Handling**:
```php
// The trait has special handling for EntityStorageInterface
protected EntityStorageInterface $nodeStorage;

// On serialize: stores entity type ID ('node')
// On unserialize: calls $entityTypeManager->getStorage('node')
// This prevents serializing static entity caches
```

**What Gets Serialized**:
- Services — replaced with IDs, re-fetched on wakeup
- Entity storages — replaced with entity type ID, re-fetched on wakeup
- Scalar values — serialized normally
- Arrays/objects that aren't services — serialized normally

Reference: `/core/lib/Drupal/Core/DependencyInjection/DependencySerializationTrait.php`

## Common Mistakes

- **Not using trait when serializing classes with services** — Entire service dependency graph gets serialized (huge cache entries)
- **Using trait when class is never serialized** — Unnecessary overhead if class won't be cached/queued
- **Expecting private properties to work** — Trait uses property names to restore; follow Drupal's property naming conventions
- **Mixing __sleep/__wakeup implementations** — If you override __sleep, call parent::__sleep() to preserve trait behavior
- **Assuming services are identical after unserialize** — Services are re-fetched; may have different state if container was rebuilt

## See Also

- [Factory Services](factory-services.md)
- [Best Practices & Patterns](best-practices-and-patterns.md)
- [DependencySerializationTrait](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!DependencyInjection!DependencySerializationTrait.php/)
