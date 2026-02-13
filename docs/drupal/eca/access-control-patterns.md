---
description: Validate plugin config in access() before execution with AccessResult patterns
drupal_version: "11.x"
---

# Access Control Patterns

## When to Use

> Implement `access()` to validate plugin configuration before execution. This prevents workflows from running with invalid settings, provides clear error messages, and catches problems early.

## Decision

| Validation Type | Check In `access()` | Why |
|-----------------|---------------------|-----|
| Required fields | Empty/null checks | Prevent execution with missing config |
| YAML syntax | Parse attempt | Catch syntax errors before execution |
| External API state | API validation call | Ensure API credentials/model exists |
| Token existence | Token lookup | Verify dependent tokens available |
| Field names | Entity/form field check | Prevent invalid field access |

## Pattern

```php
use Drupal\Core\Access\AccessResult;
use Drupal\Core\Access\AccessResultInterface;
use Drupal\Core\Session\AccountInterface;

public function access($object, ?AccountInterface $account = NULL, $return_as_object = FALSE): bool|AccessResultInterface {
  // Validate required configuration
  $field_name = $this->tokenService->replace($this->configuration['field_name']);

  if (empty($field_name)) {
    $result = AccessResult::forbidden('Field name is required.');
    return $return_as_object ? $result : FALSE;
  }

  // Validate YAML syntax if configured
  if (!empty($this->configuration['yaml_config'])) {
    try {
      $this->yamlParser->parse($this->configuration['yaml_config']);
    } catch (ParseException $e) {
      $result = AccessResult::forbidden('Invalid YAML: ' . $e->getMessage());
      return $return_as_object ? $result : FALSE;
    }
  }

  // Validate external API state
  if (!empty($this->configuration['model_id'])) {
    $provider = $this->loadModelProvider();
    $violations = $this->validator->validate($provider, $this->configuration['model_id']);

    if ($violations->count() > 0) {
      $messages = array_map(fn($v) => (string) $v->getMessage(), (array) $violations->getIterator());
      $result = AccessResult::forbidden(implode(' | ', $messages));
      return $return_as_object ? $result : FALSE;
    }
  }

  // Validate context (for events)
  if (isset($this->event) && method_exists($this->event, 'hasRequiredData')) {
    if (!$this->event->hasRequiredData($field_name)) {
      $result = AccessResult::forbidden('Event does not provide required data.');
      return $return_as_object ? $result : FALSE;
    }
  }

  // Always call parent at the end
  return parent::access($object, $account, $return_as_object);
}
```

## Common Mistakes

- **Wrong**: Not calling `parent::access()` → **Right**: Bypasses base class validation
- **Wrong**: Throwing exceptions instead of returning AccessResult → **Right**: Breaks access checking
- **Wrong**: Not respecting `$return_as_object` parameter → **Right**: Type errors in some contexts
- **Wrong**: Missing clear error messages → **Right**: Users can't diagnose problems
- **Wrong**: Expensive operations in `access()` → **Right**: Slows down all workflow evaluations
- **Wrong**: Validating in `execute()` instead → **Right**: Errors occur during execution, not during config

## See Also

- [YAML Configuration](yaml-configuration.md) for YAML validation
- [Advanced Action Patterns](advanced-action-patterns.md) for API validation
- [Mandatory Rules](mandatory-rules.md) for access() requirements

**References:**
- Core: `/modules/contrib/eca/src/Plugin/ECA/EcaPluginBase.php`
- Example: `/modules/contrib/eca_base/src/Plugin/Action/EcaStateWrite.php`
