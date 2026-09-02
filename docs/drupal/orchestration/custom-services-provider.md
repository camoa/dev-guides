---
description: Write a custom Orchestration services provider to expose custom Drupal capabilities as callable services for external platforms
tldr: "Implement `ServicesProviderInterface` and register the class as a Symfony service tagged `orchestration_services_provider`. No plugin annotation needed. Provider ID must not contain colons — the UUID is `{provider_id}::{service_id}`. `execute()` must return `array|string`."
drupal_version: "11.x"
---

# Custom Services Provider

## When to Use

> Use this when you want to expose a custom Drupal capability — one not covered by the four built-in submodules — as an Orchestration service callable by external platforms.

## How Discovery Works

Any Drupal service tagged `orchestration_services_provider` is automatically collected by `ServicesProviderManager` via Symfony's service collector pattern — no plugin manager, no annotation, no hook needed. The manager calls `addServicesProvider()` for each tagged service at container compile time.

## Steps

**1. Implement `ServicesProviderInterface`**

```php
namespace Drupal\my_module;

use Drupal\orchestration\Service;
use Drupal\orchestration\ServiceConfig;
use Drupal\orchestration\ServicesProviderInterface;

class MyServicesProvider implements ServicesProviderInterface {

  public function getId(): string {
    return 'my_module'; // Use your module machine name; no colons
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
    // The manager verifies the service exists before calling execute().
    // $config keys match the ServiceConfig keys you defined in getAll().
    $targetId = (string) ($config['target_id'] ?? '');
    // ... your logic ...
    return ['success' => TRUE, 'target_id' => $targetId];
  }

}
```

**2. Register as a tagged Drupal service**

```yaml
# my_module.services.yml
services:
  my_module.orchestration_services_provider:
    class: Drupal\my_module\MyServicesProvider
    arguments:
      - '@some_dependency'
    tags:
      - { name: 'orchestration_services_provider' }
```

**3. Verify it appears in the catalog**

```bash
drush cache-rebuild
curl -u admin:password https://your-site.example.com/orchestration/services
# Look for {"id": "my_module::my_action", ...}
```

## `Service` and `ServiceConfig` Details

**`Service` constructor**: `new Service($provider, $id, $label, $description)`. The UUID (used as the `id` field in the API) is `{provider->getId()}::{id}` (double colon, from `Service::uuid()`). Call `$service->addConfig(ServiceConfig $config)` for each parameter; it is fluent and returns `$this`.

**`ServiceConfig` constructor** (all positional or named):

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `key` | string | — | Config field key; matches what the external caller sends in `config` |
| `label` | string | — | Human-readable label |
| `description` | string | — | Field description |
| `required` | bool | — | Whether this config is required |
| `type` | string | `'string'` | Data type hint (e.g., `string`, `integer`, `boolean`) |
| `isEditable` | bool | `TRUE` | If false, the field appears in the catalog but cannot be set by the caller |
| `defaultValue` | mixed | `''` | Default value |
| `weight` | int | `0` | Display order (lower = earlier in sorted list) |
| `constraints` | array | `[]` | Symfony constraints; `Choice` constraint populates `options` in API response |

**Choice constraint example** (creates a dropdown in the external platform):

```php
new ServiceConfig(
  key: 'status',
  label: 'Status',
  description: 'Target status.',
  required: TRUE,
  type: 'string',
  constraints: ['Choice' => ['choices' => ['draft' => 'Draft', 'published' => 'Published']]],
)
```

API response `options`: `[{"key": "draft", "name": "Draft"}, {"key": "published", "name": "Published"}]`

## Common Mistakes

- **Using a colon in `getId()`** — the UUID is `getId() . '::' . $service_id`; a colon in the provider ID would create a malformed triple-colon UUID
- **Returning objects from `execute()`** — the contract is `array|string`; serialize to array before returning
- **Forgetting `drush cache-rebuild` after changing the service tag** — the service collector is resolved at container build time
- **Throwing exceptions from `getAll()`** — an exception in one provider breaks the entire `/orchestration/services` endpoint for all callers; catch internally and log
- **Doing expensive work (entity loads, external API calls) in `getAll()`** — this method is called on every `/orchestration/services` request; cache if needed

## See Also

- [Architecture](architecture.md) → for how `ServicesProviderManager` collects providers
- [Orchestration API Reference](orchestration-api-reference.md) → for what the external caller sends in `execute`
- Reference: `src/ServicesProviderInterface.php`, `src/Service.php`, `src/ServiceConfig.php`, `docs/develop/plugin.md`
