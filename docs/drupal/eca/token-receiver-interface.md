---
description: Implement TokenReceiverInterface to preserve event tokens across workflow execution
drupal_version: "11.x"
---

# Token Receiver Interface

## When to Use

> Implement `TokenReceiverInterface` when your event plugin needs to preserve specific tokens across the entire workflow execution, ensuring token data survives even after actions complete.

## Decision

| Token Survival Need | Implement Interface | Why |
|---------------------|---------------------|-----|
| Event provides entity | Yes | Entity tokens must persist for all actions |
| Workflow-wide data | Yes | Tokens used by multiple actions |
| Ephemeral action data | No | Action creates/uses token locally |
| Global tokens | No | Already preserved by system |

## Pattern

```php
use Drupal\eca\Plugin\DataProviderInterface;
use Drupal\eca\Token\TokenReceiverTrait;
use Drupal\eca\Token\TokenInterface;

class MyEvent extends EventBase implements DataProviderInterface {

  use TokenReceiverTrait;  // Provides token preservation logic

  /**
   * {@inheritdoc}
   */
  public function getData(string $key): mixed {
    // Provide token data from event
    $event = $this->event;

    if ($key === 'entity' && method_exists($event, 'getEntity')) {
      return $event->getEntity();
    }

    if ($key === 'custom_data' && method_exists($event, 'getCustomData')) {
      return $event->getCustomData();
    }

    // Token will be preserved across workflow due to TokenReceiverInterface
    return parent::getData($key);
  }

  /**
   * {@inheritdoc}
   */
  public static function definitions(): array {
    return [
      'my_event' => [
        'label' => 'My Custom Event',
        'event_name' => MyModuleEvents::CUSTOM_EVENT,
        'event_class' => MyCustomEvent::class,
        'tags' => Tag::RUNTIME | Tag::CONTENT,
      ],
    ];
  }
}
```

## Common Mistakes

- **Wrong**: Not using TokenReceiverTrait → **Right**: Must implement all methods manually
- **Wrong**: Implementing interface without preserving tokens → **Right**: Interface has no effect
- **Wrong**: Preserving all tokens → **Right**: Memory overhead for unused data
- **Wrong**: Not documenting which tokens survive → **Right**: Other developers don't know what's available
- **Wrong**: Missing `getData()` implementation → **Right**: Tokens can't be accessed

## See Also

- [Cleanup Interface](cleanup-interface.md) for cleanup patterns
- [Token Form Integration](token-form-integration.md) for token usage
- [Event Plugin Basics](event-plugin-basics.md) for event structure

**References:**
- Core: `/modules/contrib/eca/src/Token/TokenReceiverInterface.php`
- Trait: `/modules/contrib/eca/src/Token/TokenReceiverTrait.php`
