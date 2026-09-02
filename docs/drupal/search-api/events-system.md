---
description: Search API events — available events, when they dispatch, and event subscriber pattern for query and indexing hooks
tldr: "Use this when hooking into Search API's query or indexing pipeline. Search API 1.x uses Symfony events, not hooks — all 18 alter hooks in search_api.api.php are deprecated and removed in 2.0.0."
drupal_version: "11.x"
---

# Events System

## When to Use

> When hooking into Search API's query or indexing pipeline without creating full custom processors.

## Decision: Events Replaced Hooks

Every alter hook Search API once documented is deprecated. All 18 hooks in `search_api.api.php` — `hook_search_api_query_alter()`, `hook_search_api_results_alter()`, `hook_search_api_index_items_alter()`, `hook_search_api_items_indexed()`, the `*_info_alter()` family, and the rest — carry the same notice: deprecated in `search_api:8.x-1.14`, removed in `search_api:2.0.0`, use the matching `search_api.*` event instead. Write event subscribers, not hook implementations. The change record is [node/3059866](https://www.drupal.org/node/3059866).

## Decision: Available Events

| Event Constant | Class | When | Use Case |
|---|---|---|---|
| `INDEXING_ITEMS` | IndexingItemsEvent | Before items indexed | Modify items pre-indexing |
| `ITEMS_INDEXED` | ItemsIndexedEvent | After items indexed | Trigger post-indexing actions |
| `REINDEX_SCHEDULED` | ReindexScheduledEvent | Reindex triggered | Notification |
| `QUERY_PRE_EXECUTE` | QueryPreExecuteEvent | Before backend executes | Modify query at last moment |
| `PROCESSING_RESULTS` | ProcessingResultsEvent | After backend returns | Modify raw results |
| `DETERMINING_SERVER_FEATURES` | DeterminingServerFeaturesEvent | Feature check | Alter backend capabilities |
| `MAPPING_FIELD_TYPES` | MappingFieldTypesEvent | Field type mapping | Custom type mapping |
| `MAPPING_VIEWS_HANDLERS` | MappingViewsHandlersEvent | Views handler mapping | Custom handler mapping |
| `GATHERING_*` | GatheringPluginInfoEvent | Plugin discovery | Alter plugin definitions |

## Pattern: Event Subscriber

```php
// my_module.services.yml
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
    return [
      SearchApiEvents::QUERY_PRE_EXECUTE => 'onQueryPreExecute',
    ];
  }

  public function onQueryPreExecute(QueryPreExecuteEvent $event): void {
    $query = $event->getQuery();
    // Modify query before execution.
    $query->addCondition('status', TRUE);
  }

}
```

## See Also

- [Query System](query-system.md) — query modification
- [Custom Plugin Development](custom-plugin-development.md) — full plugin approach
