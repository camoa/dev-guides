---
description: "Facets event subscribers for hooking into URL building, active filter parsing, and cache metadata without a full custom processor"
tldr: "Use this guide when you need to hook into the facets processing pipeline without creating a full custom processor — modifying URL formats, overriding active filter detection, or adjusting cache metadata."
drupal_version: "11.x"
---

# Events

## When to Use

> When you need to hook into the facets processing pipeline without creating a full custom processor.

## Decision

| Event Constant | Class | When Dispatched | Use Case |
|---|---|---|---|
| `QUERY_STRING_CREATED` | QueryStringCreated | After building URL query string | Modify URL parameter format |
| `ACTIVE_FILTERS_PARSED` | ActiveFiltersParsed | After parsing URL parameters | Override active filter detection |
| `URL_CREATED` | UrlCreated | After building facet link URL | Modify individual link destinations |
| `POST_BUILD_FACET` | PostBuildFacet | After complete BUILD stage | Final modifications to rendered facet |
| `GET_FACET_CACHE_CONTEXTS` | GetFacetCacheContexts | During cache metadata collection | Add/override cache contexts |
| `GET_FACET_CACHE_MAX_AGE` | GetFacetCacheMaxAge | During cache metadata collection | Override cache max age |
| `GET_FACET_CACHE_TAGS` | GetFacetCacheTags | During cache metadata collection | Add/override cache tags |

## Pattern

```yaml
# my_module.services.yml
services:
  my_module.facets_subscriber:
    class: Drupal\my_module\EventSubscriber\FacetsSubscriber
    tags:
      - { name: event_subscriber }
```

```php
namespace Drupal\my_module\EventSubscriber;

use Drupal\facets\Event\FacetsEvents;
use Drupal\facets\Event\QueryStringCreated;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class FacetsSubscriber implements EventSubscriberInterface {

  public static function getSubscribedEvents(): array {
    return [
      FacetsEvents::QUERY_STRING_CREATED => 'onQueryStringCreated',
    ];
  }

  public function onQueryStringCreated(QueryStringCreated $event): void {
    // Modify the query string parameters.
    $filter_params = $event->getFilterParameters();
    // ... modify $filter_params
    $event->setFilterParameters($filter_params);
  }

}
```

## Common Mistakes

- **Wrong**: Writing a custom processor just to tweak a URL format → **Right**: Subscribe to `QUERY_STRING_CREATED` or `URL_CREATED` instead — no plugin boilerplate needed.

## See Also

- [URL Processors](url-processors.md) — URL events in context
- [Caching](caching.md) — cache events
- Reference: `src/Event/`
