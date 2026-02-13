---
description: Create custom ECA Event plugins with EventBase and derivers for business logic triggers
drupal_version: "11.x"
---

# Event Plugin Basics

## When to Use

> Create custom Event plugins when you need to trigger ECA workflows based on custom application logic, third-party integrations, or domain-specific business events that core Drupal events don't cover.

## Decision

| If you need... | Event Type | Files Required |
|----------------|------------|----------------|
| Custom business event | EventBase + Deriver | Event class, Constants, Plugin, Deriver (4 files) |
| Entity operation event | Extend content entity events | Reuse existing entity event infrastructure |
| Field-specific event | FieldSelectionBase | Event class with field filtering |
| Cron-triggered event | BaseEvent with custom definition | Single plugin with cron integration |

## Pattern

**Event Constants (src/MyModuleEvents.php):**
```php
final class MyModuleEvents {
  const CUSTOM_EVENT = 'my_module.custom_event';
}
```

**Event Class (src/Event/CustomEvent.php):**
```php
namespace Drupal\my_module\Event;

use Drupal\eca\Event\Tag;
use Symfony\Contracts\EventDispatcher\Event;

class CustomEvent extends Event {

  const TAGS = Tag::RUNTIME | Tag::CONTENT;

  protected string $eventId;
  protected mixed $data;

  public function __construct(string $event_id, mixed $data) {
    $this->eventId = $event_id;
    $this->data = $data;
  }

  public function getEventId(): string {
    return $this->eventId;
  }

  public function getData(): mixed {
    return $this->data;
  }
}
```

**Event Plugin (src/Plugin/ECA/Event/MyEvent.php):**
```php
#[EcaEvent(
  id: 'my_module_events',
  deriver: 'Drupal\my_module\Plugin\ECA\Event\MyEventDeriver',
)]
class MyEvent extends EventBase {

  public static function definitions(): array {
    return [
      'custom' => [
        'label' => 'Custom Event',
        'event_name' => MyModuleEvents::CUSTOM_EVENT,
        'event_class' => CustomEvent::class,
        'tags' => Tag::RUNTIME | Tag::CONTENT,
      ],
    ];
  }
}
```

## Common Mistakes

- **Wrong**: Missing event deriver → **Right**: Plugin won't discover event definitions
- **Wrong**: Wrong event tags → **Right**: Events show in wrong admin UI categories
- **Wrong**: Not implementing `getData()` for tokens → **Right**: Event data unavailable to actions
- **Wrong**: Missing `appliesForWildcard()` → **Right**: Event filtering doesn't work
- **Wrong**: Forgetting to dispatch event in code → **Right**: Events defined but never triggered

## See Also

- [Entity-Aware Events](entity-aware-events.md) for entity filtering
- [Cleanup Interface](cleanup-interface.md) for post-execution cleanup
- [Plugin Derivers](plugin-derivers.md) for dynamic event generation

**References:**
- Core: `/modules/contrib/eca/src/Plugin/ECA/Event/EventBase.php`
- Example: `/modules/contrib/eca/modules/base/src/Plugin/ECA/Event/BaseEvent.php`
