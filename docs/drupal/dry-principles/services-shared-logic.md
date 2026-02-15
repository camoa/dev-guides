---
description: Extract shared business logic into Drupal services with dependency injection for testable, reusable code.
---

# Services for Shared Logic

## When to Use

When you have business logic, API integrations, calculations, or data transformations that are used in multiple places (controllers, forms, event subscribers, Drush commands).

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Logic used in 2+ places | Extract to service | Single source of truth, testable, reusable |
| API integration | Service with HTTP client injected | Centralized, mockable for testing |
| Complex calculations | Service method | Avoids duplication, easier to test |
| One-off controller logic | Keep in controller | Don't abstract prematurely (Rule of Three) |
| Utility functions | Static utility class OR service | Service preferred for DI benefits |

## Pattern

```php
// mymodule/src/MyApiService.php
namespace Drupal\mymodule;

use Drupal\Core\Config\ConfigFactoryInterface;
use GuzzleHttp\ClientInterface;

class MyApiService {

  public function __construct(
    protected ClientInterface $httpClient,
    protected ConfigFactoryInterface $configFactory,
  ) {}

  public function fetchData(string $endpoint): array {
    $config = $this->configFactory->get('mymodule.settings');
    $base_url = $config->get('api.endpoint');
    $response = $this->httpClient->get($base_url . $endpoint);
    return json_decode($response->getBody(), TRUE);
  }
}
```

```yaml
# mymodule/mymodule.services.yml
services:
  mymodule.api:
    class: Drupal\mymodule\MyApiService
    arguments: ['@http_client', '@config.factory']
```

```php
// Use in multiple places (controller, form, Drush command)
$data = $this->apiService->fetchData('/users');
```

Reference: `core/core.services.yml`, `core/lib/Drupal/Core/DependencyInjection/ContainerInjectionInterface.php`

## Common Mistakes

- **Static \Drupal:: calls instead of dependency injection** — Hides dependencies, untestable, violates DRY by duplicating container access
- **God services with too many responsibilities** — Keep services focused (Single Responsibility Principle); if your service does "everything", split it
- **Premature service creation** — Wait until you have 2-3 consumers before extracting (Rule of Three)
- **Constructor logic beyond property assignment** — Constructors should only assign injected dependencies to properties, not perform operations
- **Not using factories when needed** — For cache bins, loggers, HTTP clients, use factory services (e.g., `logger.factory`, not `logger.channel.default`)

## See Also

- [Config as Single Source of Truth](config-single-source-truth.md)
- [Base Classes and Inheritance](base-classes-inheritance.md)
- Reference: [Services and dependency injection | Drupal.org](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection)
- Reference: [Dependency injection anti-patterns in Drupal](https://mglaman.dev/blog/dependency-injection-anti-patterns-drupal)
