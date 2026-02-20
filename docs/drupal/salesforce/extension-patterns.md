---
description: Salesforce extension patterns — custom auth provider, custom queue processor, custom pull worker
drupal_version: "11.x"
---

# Extension Patterns

## When to Use

> Use these extension points when built-in auth providers, queue processors, or pull workers cannot meet your requirements — for example, custom SSO auth, bulk API processing, or complex pull transformations not achievable via events.

## Decision

| Extension Point | Base Class / Interface | Use When |
|---|---|---|
| Custom auth provider | `SalesforceAuthProviderPluginBase` + `SalesforceAuthProviderInterface` | Non-standard auth flow (custom SSO, custom token) |
| Custom queue processor | `PushQueueProcessorInterface` | Alternative API calls, bulk/external system integration |
| Custom pull worker | QueueWorker plugin + `@QueueWorker` annotation | Complex pull processing, external API calls during pull |
| Custom field mapping | `PropertiesBase` | Reusable custom field logic — see [Custom Field Mapping Plugin](custom-field-mapping-plugin.md) |

## Pattern

**Custom auth provider:**
```php
/**
 * @SalesforceAuthProvider(
 *   id = "my_custom_auth",
 *   label = @Translation("My Custom Auth"),
 * )
 */
class MyCustomAuthPlugin extends SalesforceAuthProviderPluginBase
  implements SalesforceAuthProviderInterface {
  // Implement auth flow methods
}
```

**Custom queue processor:**
```php
/**
 * @Plugin(
 *   id = "my_bulk_processor",
 * )
 */
class MyBulkProcessor implements PushQueueProcessorInterface {
  public function process(array $items, SalesforceMappingInterface $mapping): void {
    // Alternative API calls, bulk processing, external system integration
  }
}
// Register with: plugin.manager.salesforce_push_queue_processor
```

**Custom pull worker:**
```php
/**
 * @QueueWorker(
 *   id = "custom_pull_worker",
 *   title = @Translation("Custom Pull Worker"),
 *   cron = {"time" = 60},
 * )
 */
class CustomPullWorker extends QueueWorkerBase {
  public function processItem($data): void {
    // Custom pull logic, external API calls, complex transformations
  }
}
```

## Common Mistakes

- **Wrong**: Extending `SalesforceAuthProviderPluginBase` without implementing all required interface methods → **Right**: Implement the full `SalesforceAuthProviderInterface`; use the OAuth plugin as reference
- **Wrong**: Creating a custom pull worker that bypasses `MappedObject` creation → **Right**: Custom pull workers still need to create or update `MappedObject` entities to maintain sync tracking

## See Also

- [Custom Field Mapping Plugin](custom-field-mapping-plugin.md)
- [Event System](event-system.md)
- [Decision Framework](decision-framework.md)
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_oauth/src/Plugin/SalesforceAuthProvider/SalesforceOAuthPlugin.php`
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_push/src/PushQueueProcessorPluginManager.php`
