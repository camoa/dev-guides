---
description: Debug ECA workflows with logging, token inspection, and drush watchdog commands
drupal_version: "11.x"
---

# Debugging Workflows

## When to Use

> Debug ECA workflows when actions don't execute as expected, tokens have unexpected values, or conditions evaluate incorrectly. Use logging, watchdog, and token inspection.

## Decision

| Debug Need | Tool | Command/Method |
|------------|------|----------------|
| View workflow logs | Drush watchdog | `drush watchdog:show --filter=eca` |
| Inspect token values | Logger in action | `$this->logger->debug('Token: @value', ['@value' => $token])` |
| Check action execution | Logger in execute() | `$this->logger->info('Action started')` |
| Verify configuration | Logger in access() | `$this->logger->debug('Config: @config', ['@config' => json_encode($this->configuration)])` |
| Trace workflow path | ECA UI | View execution history in ECA admin |

## Pattern

```php
class MyDebuggableAction extends ConfigurableActionBase {

  /**
   * Add comprehensive logging for debugging.
   */
  public function execute(): void {
    // Log entry point
    $this->logger->info('Starting @action for configuration: @config', [
      '@action' => $this->getPluginId(),
      '@config' => json_encode($this->configuration),
    ]);

    // Log token values
    $input = $this->tokenService->getOrReplace($this->configuration['input_field']);
    $this->logger->debug('Input value after token replacement: @value', [
      '@value' => $input,
    ]);

    // Log all available tokens (debug mode only)
    if ($this->configFactory->get('eca.settings')->get('debug_mode')) {
      $all_tokens = $this->getAllTokens();
      $this->logger->debug('All available tokens: @tokens', [
        '@tokens' => json_encode($all_tokens, JSON_PRETTY_PRINT),
      ]);
    }

    try {
      $result = $this->performOperation($input);

      // Log success
      $this->logger->info('Action @action completed successfully: @result', [
        '@action' => $this->getPluginId(),
        '@result' => json_encode($result),
      ]);

      $this->tokenService->addTokenData($this->configuration['result_token'], $result);

    } catch (\Exception $e) {
      // Log detailed error context
      $this->logger->error('Action @action failed: @error | Stack trace: @trace', [
        '@action' => $this->getPluginId(),
        '@error' => $e->getMessage(),
        '@trace' => $e->getTraceAsString(),
      ]);

      // Store error in token for inspection
      $this->tokenService->addTokenData($this->configuration['result_token'], [
        'success' => 0,
        'error' => $e->getMessage(),
        'debug_trace' => $e->getTraceAsString(),
      ]);
    }
  }

  /**
   * Get all available token data for debugging.
   */
  protected function getAllTokens(): array {
    $tokens = [];

    // This is implementation-specific to your token service
    // Check ECA's token service for exact method
    if (method_exists($this->tokenService, 'getAllTokenData')) {
      $tokens = $this->tokenService->getAllTokenData();
    }

    return $tokens;
  }
}
```

**Viewing Logs:**
```bash
# View recent ECA logs
drush watchdog:show --filter=eca

# View logs with severity
drush watchdog:show --severity=Error --filter=eca

# Tail logs in real-time
drush watchdog:tail --filter=eca

# Clear old logs
drush watchdog:delete all
```

## Common Mistakes

- **Wrong**: Not logging at all → **Right**: Impossible to debug production issues
- **Wrong**: Logging sensitive data → **Right**: API keys, passwords in logs
- **Wrong**: Too much logging → **Right**: Performance impact, log bloat
- **Wrong**: Wrong log level → **Right**: Info should be debug, or debug should be error
- **Wrong**: Not checking logs → **Right**: Logging without reading them
- **Wrong**: Missing context in log messages → **Right**: Can't understand what failed

## See Also

- [Kernel Testing](kernel-testing.md) for testing approaches
- [Advanced Action Patterns](advanced-action-patterns.md) for error handling
- [Complex Token Structures](complex-token-structures.md) for token inspection

**References:**
- Drupal Logging: https://api.drupal.org/api/drupal/core!core.api.php/group/logging
- Drush: https://www.drush.org/latest/commands/watchdog_show/
