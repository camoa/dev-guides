---
description: Keep controllers thin and forms focused - delegate business logic to services
drupal_version: "11.x"
---

# Controllers & Forms - Single Responsibility

## When to Use

Controllers should only handle HTTP request/response. Business logic belongs in services. Forms should only handle form structure/validation.

## Decision

| If you need to... | Pattern | Why |
|---|---|---|
| Display data | Controller fetches from service -> returns render array | Thin controller |
| Process complex business logic | Service method, called from controller | Reusable, testable |
| Handle form submission | Form calls service in submitForm() | Business logic in service |
| Query entities | Service method, not in controller | Reusable across contexts |
| Send emails, log, cache | Inject services, don't do directly | DIP, testability |

## Pattern

**GOOD: Thin controller, service does work**

```php
class NodeController extends ControllerBase {
  public function __construct(
    private NodeAccessServiceInterface $accessService,
  ) {}

  public function title(NodeInterface $node) {
    // Only HTTP concerns - service does business logic
    if (!$this->accessService->userCanView($node, $this->currentUser())) {
      throw new AccessDeniedHttpException();
    }
    return ['#markup' => $this->accessService->getTitle($node)];
  }
}
```

**BAD: Fat controller (violates SRP)**

```php
class NodeController extends ControllerBase {
  public function title(NodeInterface $node) {
    // Business logic mixed with HTTP handling
    $grants = \Drupal::database()->select('node_access')->execute();
    if ($grants->fetchField() != $this->currentUser()->id()) {
      throw new AccessDeniedHttpException();
    }
    $title = $node->label();
    // Caching, logging, email all in controller
    \Drupal::cache()->set('node_title_' . $node->id(), $title);
    \Drupal::logger('node')->notice('Title accessed');
    return ['#markup' => $title];
  }
}
```

Reference: `/core/modules/node/src/Controller/` -- thin controllers delegating to services

## Common Mistakes

- Entity queries in controllers -- move to repository service. **WHY:** Can't reuse in CLI, batch jobs, or tests without HTTP context
- Business logic in validateForm()/submitForm() -- extract to service. **WHY:** Can't validate outside form context (API, imports, migrations)
- Direct database queries in controllers -- use entity API or service. **WHY:** Bypasses access control, caching, hooks; creates security holes
- `\Drupal::service()` in controller -- use dependency injection. **WHY:** Hard to test; violates DIP; hides dependencies

## See Also

- [Services & SRP](services-srp.md) for service design
- [Dependency Injection Patterns](dependency-injection-patterns-dip.md) for injection
