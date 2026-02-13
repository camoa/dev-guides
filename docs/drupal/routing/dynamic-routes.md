---
description: Dynamic routes in Drupal - programmatic route generation based on configuration or runtime conditions
drupal_version: "11.x"
---

# Dynamic Routes

## When to Use

> Use when routes need to be generated programmatically based on configuration, content, or runtime conditions. Prefer static YAML routes when possible - use dynamic routes only when necessary.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Standalone dynamic routes | `route_callbacks` in `*.routing.yml` | Simpler than event subscribers |
| Routes depending on other routes | `RouteSubscriber` extending `RouteSubscriberBase` | Full access to route collection |
| Routes from configuration entities | `route_callbacks` returning collection | Generated from stored config |
| Conditional route creation | Callback checks condition, returns routes | Runtime flexibility |

## Pattern

```yaml
# routing.yml with route_callbacks
route_callbacks:
  - '\Drupal\my_module\Routing\MyRoutes::routes'
```

```php
// src/Routing/MyRoutes.php
namespace Drupal\my_module\Routing;

use Symfony\Component\Routing\Route;
use Symfony\Component\Routing\RouteCollection;

class MyRoutes {
  public function routes() {
    $routes = new RouteCollection();

    // Generate routes dynamically
    foreach ($this->getItemsFromConfig() as $id => $item) {
      $route = new Route(
        "/items/{$id}",
        [
          '_controller' => '\Drupal\my_module\Controller\ItemController::view',
          '_title' => $item['title'],
        ],
        ['_permission' => 'access content']
      );
      $routes->add("my_module.item.{$id}", $route);
    }

    return $routes;
  }
}
```

Reference: `core/modules/media/media.routing.yml`, `core/lib/Drupal/Core/Routing/RouteProvider.php`

## Common Mistakes

- **Wrong**: Using dynamic routes when static routes would work → **Right**: Prefer YAML for static routes
- **Wrong**: Not implementing caching for expensive route generation → **Right**: Cache route collections
- **Wrong**: Missing access checks on dynamic routes → **Right**: Define `_permission` in Route constructor
- **Wrong**: Generating too many routes → **Right**: Limit to necessary routes, consider alternatives
- **Wrong**: Not handling route name conflicts → **Right**: Use unique prefixes for generated routes

## See Also

- [Admin Route Configuration](admin-route-configuration.md)
- [Route Subscribers](route-subscribers.md)
- Reference: [Providing dynamic routes - Drupal.org](https://www.drupal.org/docs/drupal-apis/routing-system/providing-dynamic-routes)
- Reference: [Dynamic routes - Drupal at your Fingertips](https://www.drupalatyourfingertips.com/general)
