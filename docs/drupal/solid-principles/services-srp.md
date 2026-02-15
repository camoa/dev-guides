---
description: Keep Drupal services focused on a single responsibility - one reason to change per service
drupal_version: "11.x"
---

# Services & Single Responsibility

## When to Use

Every service should have one reason to change. If a service handles node access grants AND email notifications, split it.

## Decision

| If your service... | Do this... | Why |
|---|---|---|
| Handles 1 clear domain concern | Keep as single service | Focused, testable, reusable |
| Mixes unrelated operations | Split into multiple services | Each has one reason to change |
| Coordinates multiple services | Acceptable if it ONLY coordinates | "Service orchestrator" pattern |
| Has >500 lines or >15 methods | Re-evaluate responsibilities | Likely doing too much |

## Pattern

**GOOD: Focused service (SRP)**

```php
// One responsibility: node access grants storage
class NodeGrantDatabaseStorage {
  public function write(NodeInterface $node, array $grants) { }
  public function delete($nid) { }
  public function access(NodeInterface $node, $op, AccountInterface $account) { }
}
```

**BAD: Fat service (violates SRP)**

```php
// Multiple responsibilities mixed
class NodeManager {
  public function write(NodeInterface $node, array $grants) { }  // Access grants
  public function sendNotification($nid) { }                     // Email
  public function generateSitemap() { }                          // SEO
  public function cacheWarmup() { }                              // Caching
}
```

Reference: `/core/modules/node/src/NodeGrantDatabaseStorage.php` -- focused on access grants only

## Common Mistakes

- Service named "Manager" or "Helper" doing 10 unrelated things -- split into domain services (NodeAccessService, NodeNotificationService, etc.). **WHY:** "Manager" is a code smell indicating lack of focus; impossible to test one feature without the other 9
- Mixing business logic and presentation in one service -- business in service, presentation in controller/form. **WHY:** Can't reuse business logic in CLI, API, or batch operations when it's tangled with HTTP responses
- Service with 30+ methods -- break into smaller focused services. **WHY:** Developers can't understand what the service does; changes to one method risk breaking others
- Constructor with >8 dependencies -- service doing too much, violates SRP. **WHY:** High coupling indicates multiple responsibilities; testing requires mocking 8+ services

## See Also

- [Controllers & SRP](controllers-srp.md) for thin controller pattern
- [Dependency Injection Patterns](dependency-injection-patterns-dip.md) for constructor injection
- Reference: [Drupal Services and Dependency Injection](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/services-and-dependency-injection-in-drupal)
