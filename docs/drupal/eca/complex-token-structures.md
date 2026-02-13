---
description: Store structured data in tokens with success/error indicators for downstream actions
drupal_version: "11.x"
---

# Complex Token Structures

## When to Use

> Store complex data structures in tokens when actions need to pass multiple related values, structured results, or collections to downstream actions and conditions. Tokens can hold arrays, objects, and nested data.

## Decision

| Data Type | Token Structure | Access Pattern |
|-----------|----------------|----------------|
| Simple value | String/number | `$tokenService->getTokenData('name')` |
| Structured data | Array/object | `$tokenService->getTokenData('result')['field']` |
| Success/failure | Array with status | `$result['success'] === 1` |
| Entity collection | Array of entities | `foreach ($tokenService->getTokenData('entities') as $entity)` |
| DataTransferObject | DTO instance | `$dto->getData()`, `$dto->push()`, `$dto->pop()` |

## Pattern

```php
public function execute(): void {
  try {
    // Perform operation
    $api_response = $this->callExternalApi();

    // Store structured success result
    $result = [
      'success' => 1,
      'data' => $api_response['items'],
      'metadata' => [
        'timestamp' => time(),
        'total_count' => count($api_response['items']),
        'source' => $this->getPluginId(),
      ],
      'statistics' => [
        'processed' => $api_response['processed'],
        'failed' => $api_response['failed'],
      ],
    ];

    $this->tokenService->addTokenData($this->configuration['result_token'], $result);

  } catch (\Exception $e) {
    // Store structured error result
    $error_result = [
      'success' => 0,
      'error' => $e->getMessage(),
      'error_code' => $e->getCode(),
      'data' => NULL,
    ];

    $this->tokenService->addTokenData($this->configuration['result_token'], $error_result);
    $this->logger->error('Operation failed: @error', ['@error' => $e->getMessage()]);
  }
}

// Downstream condition can check success
public function evaluate(): bool {
  $result = $this->tokenService->getTokenData($this->configuration['result_token']);
  return $this->negationCheck($result['success'] === 1);
}

// Downstream action can access nested data
public function execute(): void {
  $result = $this->tokenService->getTokenData('api_result');
  $items = $result['data'] ?? [];
  $total = $result['metadata']['total_count'] ?? 0;

  foreach ($items as $item) {
    $this->processItem($item);
  }
}
```

## Common Mistakes

- **Wrong**: Storing objects without serialization → **Right**: Can't be saved to database
- **Wrong**: No success/error indicator → **Right**: Downstream actions can't detect failures
- **Wrong**: Flat structure for related data → **Right**: Hard to organize and access
- **Wrong**: Missing NULL checks on nested access → **Right**: Fatal errors when structure differs
- **Wrong**: Not documenting token structure → **Right**: Other developers don't know what fields exist

## See Also

- [Token Form Integration](token-form-integration.md) for token basics
- [Advanced Action Patterns](advanced-action-patterns.md) for API integration example
- [Debugging Workflows](debugging-workflows.md) for inspecting token data

**References:**
- Core: `/modules/contrib/eca/src/Service/Tokens.php`
- Data type: `/modules/contrib/eca/src/Plugin/DataType/DataTransferObject.php`
