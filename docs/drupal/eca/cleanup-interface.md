---
description: Implement CleanupInterface to restore state after event actions complete (account switching, locks)
drupal_version: "11.x"
---

# Cleanup Interface

## When to Use

> Implement `CleanupInterface` when your event plugin needs to perform cleanup operations after all successor actions complete, such as restoring switched user accounts, releasing resources, or processing accumulated state.

## Decision

| Cleanup Need | Implement `CleanupInterface` | Why |
|--------------|------------------------------|-----|
| Account switching | Yes | Must restore original user context |
| Resource locks | Yes | Release file handles, database locks |
| Accumulated state | Yes | Process batched data after all actions |
| Token processing | Yes | Apply collected tokens back to event object |
| Temporary changes | Yes | Revert temporary system state |

## Pattern

```php
use Drupal\eca\Plugin\CleanupInterface;

class MyEvent extends EventBase implements CleanupInterface {

  /**
   * Static storage for event state during execution.
   */
  protected static array $eventStates = [];

  /**
   * {@inheritdoc}
   */
  public function cleanupAfterSuccessors(): void {
    switch ($this->getDerivativeId()) {

      case 'account_switch':
        // Restore original user account
        if ($original_account = array_pop(self::$eventStates)) {
          $this->accountSwitcher->switchBack();
        }
        break;

      case 'token_collection':
        // Process accumulated tokens
        if (!($event_data = array_pop(self::$eventStates))) {
          return;
        }

        $token_name = $this->configuration['token_name'] ?? NULL;
        if ($token_name && $this->tokenService->hasTokenData($token_name)) {
          $collected_data = $this->tokenService->getTokenData($token_name);
          $this->applyCollectedData($event_data['event'], $collected_data);
        }
        break;

      case 'resource_lock':
        // Release locked resources
        if ($lock_id = array_pop(self::$eventStates)) {
          $this->lockBackend->release($lock_id);
        }
        break;
    }
  }

  /**
   * Store state for cleanup (call this in your event dispatcher).
   */
  public static function storeEventState($event, array $data): void {
    self::$eventStates[] = [
      'event' => $event,
      'data' => $data,
      'timestamp' => time(),
    ];
  }
}
```

## Common Mistakes

- **Wrong**: Not using static storage → **Right**: State lost between registration and cleanup
- **Wrong**: Missing cleanup → **Right**: Resources remain locked, accounts not restored
- **Wrong**: Complex logic in cleanup → **Right**: Should be simple state restoration
- **Wrong**: Not checking if state exists → **Right**: Errors when cleanup called without setup
- **Wrong**: Forgetting to pop from stack → **Right**: Memory leak over time

## See Also

- [Token Receiver Interface](token-receiver-interface.md) for token preservation
- [Event Plugin Basics](event-plugin-basics.md) for event structure
- [Service Injection](service-injection.md) for cleanup services

**References:**
- Core: `/modules/contrib/eca/src/Plugin/CleanupInterface.php`
- Example: `/modules/contrib/eca/modules/content/src/Plugin/ECA/Event/ContentEntityEvent.php`
