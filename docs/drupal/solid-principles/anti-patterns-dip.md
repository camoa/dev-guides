---
description: Recognize and fix dependency injection anti-patterns that violate DIP in Drupal
drupal_version: "11.x"
---

# Dependency Injection Anti-Patterns - DIP

## When to Use

Recognize these patterns as violations of DIP. They create tight coupling, prevent testability, and make code fragile.

## Decision

| Anti-pattern | Why it's bad | Fix |
|---|---|---|
| `\Drupal::service()` in classes | Untestable, hides dependencies | Constructor injection |
| `\Drupal::entityTypeManager()` | Static coupling to global | Inject EntityTypeManagerInterface |
| `\Drupal::database()` | Bypasses entity API, tight coupling | Use entity storage or inject connection |
| `new ClassName()` in business logic | Can't inject dependencies into created object | Factory service or dependency |
| Global $user | Untestable, deprecated | Inject CurrentUserInterface |

## Pattern

**BAD: Static service calls (violates DIP)**

```php
class ArticleManager {
  public function publish($nid) {
    // All static calls - untestable, tightly coupled
    $storage = \Drupal::entityTypeManager()->getStorage('node');
    $node = $storage->load($nid);
    $node->setPublished(TRUE);
    $node->save();

    \Drupal::logger('mymodule')->notice('Published');
    \Drupal::cache('data')->set('last_published', $nid);
    \Drupal::messenger()->addStatus('Published');
  }
}
```

**GOOD: Proper dependency injection (follows DIP)**

```php
class ArticleManager {
  public function __construct(
    private EntityTypeManagerInterface $entityTypeManager,
    private LoggerInterface $logger,
    private CacheBackendInterface $cache,
    private MessengerInterface $messenger,
  ) {}

  public function publish($nid) {
    // All dependencies injected - testable, swappable
    $storage = $this->entityTypeManager->getStorage('node');
    $node = $storage->load($nid);
    $node->setPublished(TRUE);
    $node->save();

    $this->logger->notice('Published');
    $this->cache->set('last_published', $nid);
    $this->messenger->addStatus('Published');
  }
}
```

Reference: [Drupal API Best Practices](https://api.drupal.org/api/drupal/core!core.api.php/group/best_practices/11.x)

## Common Mistakes

- Using `\Drupal::` in services "because it's easier" -- invest in proper DI. **WHY:** "Easy" now = impossible to test, impossible to reuse in CLI/batch/API contexts
- Mixing injected dependencies and static calls in same class -- be consistent. **WHY:** Inconsistency confuses developers; partial testing gives false confidence
- Using static calls in .module files -- extract to service. **WHY:** .module files always load; services use PSR-4 autoloading (performance)
- Not mocking dependencies in tests -- mock injected services. **WHY:** Tests without mocks are slow, fragile integration tests; not unit tests
- Creating "hybrid" classes with both patterns -- choose one: static OR injection. **WHY:** Hybrid pattern is worst of both worlds; can't fully test, can't fully refactor

## See Also

- [Dependency Injection Patterns](dependency-injection-patterns-dip.md) for correct patterns
- [Service Container](service-container-dip.md) for DI architecture
- [Common Mistakes](common-mistakes.md) for more anti-patterns
