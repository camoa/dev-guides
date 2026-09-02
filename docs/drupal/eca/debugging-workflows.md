---
description: "Debug ECA workflows with logging, token inspection, drush watchdog, and the ECA 3.1 built-in Process Debugger"
tldr: "Debug ECA workflows when actions don't execute as expected, tokens have unexpected values, or conditions evaluate incorrectly. Use logging, watchdog, and token inspection."
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
| Trace a full model run (events, conditions, actions, recursion) | ECA Process Debugger (3.1) | Enable debug mode; inspect the recorded trace / replay it in the modeller |

## ECA 3.1: Built-in Process Debugger

ECA 3.1 ships a **Process Debugger** (`Drupal\eca\ProcessDebugger`) with a **Replay Mode**. When debug mode is enabled, ECA records a detailed execution trace for every model run — event start, each successor evaluation (including the condition IDs that were checked), every action execution, access denials, exceptions, and recursion detection. The Modeler API's **Test Mode** lets you trigger and replay these traces directly in the modeller UI. For diagnosing *why a workflow behaved as it did*, this is now the first tool to reach for — ahead of hand-placed logger statements. The manual logging patterns below remain valuable inside custom plugin code, for production observability, and for data the trace does not capture.

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

- Not logging at all → Impossible to debug production issues
- Logging sensitive data → API keys, passwords in logs
- Too much logging → Performance impact, log bloat
- Wrong log level → Info should be debug, or debug should be error
- Not checking logs → Logging without reading them
- Missing context in log messages → Can't understand what failed

## See Also

- [Kernel Testing](kernel-testing.md) for testing approaches
- [Advanced Action Patterns](advanced-action-patterns.md) for error handling
- [Complex Token Structures](complex-token-structures.md) for token inspection

**References:**
- Drupal Logging: `https://api.drupal.org/api/drupal/core!core.api.php/group/logging`
- Drush: `https://www.drush.org/latest/commands/watchdog_show/`
