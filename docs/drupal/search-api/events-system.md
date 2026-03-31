---
description: Search API events — available events, when they dispatch, and event subscriber pattern for query and indexing hooks
drupal_version: "11.x"
---

# Events System

## When to Use

> Use this when hooking into Search API's query or indexing pipeline without creating full custom processors.

## Decision

| Event Constant | Class | When | Use Case |
|---|---|---|---|
| `INDEXING_ITEMS` | IndexingItemsEvent | Before items indexed | Modify items pre-indexing |
| `ITEMS_INDEXED` | ItemsIndexedEvent | After items indexed | Trigger post-indexing actions |
| `REINDEX_SCHEDULED` | ReindexScheduledEvent | Reindex triggered | Notification |
| `QUERY_PRE_EXECUTE` | QueryPreExecuteEvent | Before backend executes | Modify query at last moment |
| `PROCESSING_RESULTS` | ProcessingResultsEvent | After backend returns | Modify raw results |

## Pattern

```yaml
# my_module.services.yml
services:
  my_module.search_api_subscriber:
    class: Drupal\my_module\EventSubscriber\SearchApiSubscriber
    tags:
      - { name: event_subscriber }
```

```php
namespace Drupal\my_module\EventSubscriber;

use Drupal\search_api\Event\QueryPreExecuteEvent;
use Drupal\search_api\Event\SearchApiEvents;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class SearchApiSubscriber implements EventSubscriberInterface {

  public static function getSubscribedEvents(): array {
    return [SearchApiEvents::QUERY_PRE_EXECUTE => 'onQueryPreExecute'];
  }

  public function onQueryPreExecute(QueryPreExecuteEvent $event): void {
    $query = $event->getQuery();
    $query->addCondition('status', TRUE);
  }
}
```

## Common Mistakes

- **Wrong**: Using hooks instead of events → **Right**: Search API 1.x uses Symfony events. Use event subscribers, not hook implementations.

## See Also

- [Query System](query-system.md)
- [Custom Plugin Development](custom-plugin-development.md)
- Reference: `web/modules/contrib/search_api/src/Event/SearchApiEvents.php`
