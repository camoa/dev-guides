---
description: Security and performance implications of service design — avoiding user input in definitions, lazy services, tagged iterators, constructor dependency limits, container caching, and profiling.
---

# Security & Performance

## When to Use

When you need to understand the security and performance implications of service design and dependency injection patterns.

## Security Best Practices

### 1. Never Inject User Input Directly
**Vulnerable**:
```yaml
# DON'T dynamically set service arguments from user input
services:
  my_module.service:
    arguments: ['%user_provided_value%']  # DANGEROUS if user controls this
```

**Why**: Service definitions are configuration. User input should never influence service instantiation.

---

### 2. Validate Service Arguments
**Good**:
```php
class MyServiceFactory {
  public function create(string $type): MyServiceInterface {
    $allowed = ['foo', 'bar', 'baz'];
    if (!in_array($type, $allowed, TRUE)) {
      throw new \InvalidArgumentException('Invalid type');
    }
    return new MyService($type);
  }
}
```

**Why**: Factory methods should validate arguments before creating services.

---

### 3. Don't Expose Sensitive Services Publicly
**Bad**:
```yaml
services:
  my_module.password_hasher:
    class: Drupal\my_module\PasswordHasher
    public: true  # BAD — allows \Drupal::service() access
```

**Good**:
```yaml
services:
  my_module.password_hasher:
    class: Drupal\my_module\PasswordHasher
    public: false  # Only accessible via DI
```

**Why**: Internal security services shouldn't be accessible via global service container.

---

### 4. Use Dependency Injection for Access Checks
**Good**:
```php
class MyService {
  public function __construct(
    protected AccountProxyInterface $currentUser,
  ) {}

  public function sensitiveOperation() {
    if (!$this->currentUser->hasPermission('administer site')) {
      throw new AccessDeniedException();
    }
    // Proceed
  }
}
```

**Why**: Injecting current_user makes access checks testable and explicit.

---

### 5. Avoid Serializing Sensitive Data
**Risky**:
```php
class MyService {
  use DependencySerializationTrait;

  protected string $apiKey;  // Will be serialized if cached
}
```

**Solution**:
- Don't cache services with secrets
- Use state/config for sensitive data, fetch on-demand
- Override __sleep() to exclude sensitive properties

---

## Performance Best Practices

### 1. Use Lazy Services for Heavy Dependencies
**Performance Issue**:
```yaml
services:
  my_module.heavy_service:
    class: Drupal\my_module\HeavyService
    arguments: ['@giant_dependency']  # Instantiated even if unused
```

**Optimized**:
```yaml
services:
  my_module.heavy_service:
    class: Drupal\my_module\HeavyService
    arguments: ['@giant_dependency']
    lazy: true  # Only instantiated when first method called
```

---

### 2. Use Tagged Iterators Over service_collector
**Slow**:
```yaml
tags:
  - { name: service_collector, tag: my_handler }  # Instantiates ALL handlers
```

**Fast**:
```yaml
arguments: [!tagged_iterator my_handler]  # Lazy — only instantiate when iterated
```

**Why**: service_collector creates all instances immediately. Tagged iterators are lazy.

---

### 3. Minimize Constructor Dependencies
**Slow** (10 dependencies):
```php
public function __construct(
  Connection $db,
  EntityTypeManagerInterface $etm,
  ConfigFactoryInterface $cf,
  // ... 7 more
) {}
```

**Better**: Split into focused services or use factory for optional deps.

**Why**: Every injected service adds overhead. Keep services focused.

---

### 4. Cache Compiled Container
**Production settings.php**:
```php
$settings['container_yamls'][] = DRUPAL_ROOT . '/sites/default/services.yml';

// Ensure fast class loading
$settings['class_loader_auto_detect'] = FALSE;
```

**Why**: Compiled container is PHP code; opcache makes it very fast. Don't recompile on every request.

---

### 5. Avoid Heavy Logic in Service Providers
**Slow**:
```php
public function alter(ContainerBuilder $container) {
  // Expensive computation on every cache rebuild
  $result = $this->scanFilesystem();  // BAD
  $container->setParameter('my_param', $result);
}
```

**Fast**: Compute once, store in state, only recompute when needed.

**Why**: Service providers run on cache rebuild; keep them fast.

---

### 6. Profile Service Instantiation
Use Webprofiler or Xdebug to find services that are:
- Instantiated but never used
- Take long time to construct
- Have circular or unnecessary dependencies

---

## Performance Metrics

| Pattern | Instantiation Cost | Runtime Cost |
|---|---|---|
| Direct injection | Low (once per request) | None |
| Lazy service | Very low (deferred) | Tiny (proxy overhead) |
| service_collector | High (all handlers) | None |
| !tagged_iterator | Very low (lazy) | Tiny (iterator) |
| \Drupal::service() | Low (singleton) | Small (lookup) |

---

## Common Security Mistakes

- **Exposing internal services publicly** — Use `public: false` for internal services
- **Not validating factory inputs** — Always validate parameters passed to factories
- **Caching services with secrets** — Don't serialize sensitive data
- **Trusting user input in service definitions** — Service config must be admin-controlled
- **Not checking permissions in service methods** — Inject current_user, check permissions

## Common Performance Mistakes

- **Over-injecting** — Don't inject 15 services; split the class
- **Eager collection** — Use tagged iterators, not service_collector
- **Heavy constructors** — Keep constructors simple; defer work to methods
- **Not profiling** — Measure before optimizing; don't guess
- **Recompiling container** — Cache compiled container in production

## See Also

- [Anti-Patterns & Common Mistakes](anti-patterns-and-common-mistakes.md)
- [Code Reference Map](code-reference-map.md)
