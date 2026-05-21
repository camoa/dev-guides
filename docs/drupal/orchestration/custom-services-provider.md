---
description: Write a custom Orchestration services provider to expose custom Drupal capabilities as callable services for external platforms
tldr: "Implement `ServicesProviderInterface` and register the class as a Symfony service tagged `orchestration_services_provider`. No plugin annotation needed. Provider ID must not contain colons — the UUID is `{provider_id}::{service_id}`. `execute()` must return `array|string`."
drupal_version: "11.x"
---

# Custom Services Provider

## When to Use

> Use this when you want to expose a custom Drupal capability — one not covered by the four built-in submodules — as an Orchestration service callable by external platforms.

## Decision

| Question | Answer |
|---|---|
| How is a custom provider discovered? | Symfony service tag: `orchestration_services_provider` |
| Do I need a plugin annotation? | No — tagged Symfony service is sufficient |
| What must `getId()` return? | A string with no colons (UUID format: `getId() . '::' . $service_id`) |
| What must `execute()` return? | `array\|string` — serialize objects before returning |
| What must `getAll()` avoid? | Exceptions (breaks the whole `/orchestration/services` endpoint) and expensive work (called on every request) |

## Pattern

**1. Implement `ServicesProviderInterface`:**

```php
namespace Drupal\my_module;

use Drupal\orchestration\Service;
use Drupal\orchestration\ServiceConfig;
use Drupal\orchestration\ServicesProviderInterface;

class MyServicesProvider implements ServicesProviderInterface {

  public function getId(): string {
    return 'my_module'; // No colons; use module machine name
  }

  public function getAll(): array {
    $service = new Service($this, 'my_action', 'My Action', 'Does something useful.');
    $service->addConfig(new ServiceConfig(
      key: 'target_id',
      label: 'Target ID',
      description: 'The ID of the thing to act on.',
      required: TRUE,
      type: 'string',
      isEditable: TRUE,
      defaultValue: '',
      weight: 0,
      constraints: [],
    ));
    return [$service];
  }

  public function execute(Service $service, array $config): array|string {
    $targetId = (string) ($config['target_id'] ?? '');
    // ... your logic ...
    return ['success' => TRUE, 'target_id' => $targetId];
  }
}
```

**2. Register as a tagged Drupal service:**

```yaml
# my_module.services.yml
services:
  my_module.orchestration_services_provider:
    class: Drupal\my_module\MyServicesProvider
    tags:
      - { name: 'orchestration_services_provider' }
```

**3. Verify:**

```bash
drush cache-rebuild
curl -u admin:password https://your-site.example.com/orchestration/services
# Look for {"id": "my_module::my_action", ...}
```

**Choice constraint example** (creates a dropdown in the external platform):

```php
new ServiceConfig(
  key: 'status',
  label: 'Status',
  required: TRUE,
  type: 'string',
  constraints: ['Choice' => ['choices' => ['draft' => 'Draft', 'published' => 'Published']]],
)
// API response options: [{"key": "draft", "name": "Draft"}, {"key": "published", "name": "Published"}]
```

## Common Mistakes

- **Wrong**: Using a colon in `getId()` → **Right**: The UUID is `getId() . '::' . $service_id`; a colon in the provider ID creates a malformed triple-colon UUID
- **Wrong**: Returning objects from `execute()` → **Right**: The contract is `array|string`; serialize to array before returning
- **Wrong**: Forgetting `drush cache-rebuild` after adding the service tag → **Right**: The service collector is resolved at container build time
- **Wrong**: Throwing exceptions from `getAll()` → **Right**: An exception in one provider breaks the entire `/orchestration/services` endpoint for all callers; catch internally and log
- **Wrong**: Doing expensive work (entity loads, external API calls) in `getAll()` → **Right**: This method is called on every `/orchestration/services` request; cache if needed

## See Also

- [Architecture](architecture.md)
- [Orchestration API Reference](orchestration-api-reference.md)
- Reference: `src/ServicesProviderInterface.php`, `src/Service.php`, `src/ServiceConfig.php`, `docs/develop/plugin.md`
