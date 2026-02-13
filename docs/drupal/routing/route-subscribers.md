---
description: Route subscribers - alter existing core or contrib routes without patching
drupal_version: "11.x"
---

# Route Subscribers

## When to Use

> Use when you need to alter existing routes from core or contrib modules. Do NOT use to create routes - use `route_callbacks` or static YAML instead.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Alter existing route properties | `RouteSubscriber` with `alterRoutes()` | Modify path, requirements, defaults, options |
| Change route access control | Alter `requirements` in `alterRoutes()` | Add/remove/modify access checks |
| Redirect route to different controller | Alter `_controller` default | Override behavior without patching |
| Adjust route weight/priority | `getSubscribedEvents()` with priority | Control order of route processing |

## Pattern

```php
// src/Routing/RouteSubscriber.php
namespace Drupal\my_module\Routing;

use Drupal\Core\Routing\RouteSubscriberBase;
use Symfony\Component\Routing\RouteCollection;

class RouteSubscriber extends RouteSubscriberBase {

  protected function alterRoutes(RouteCollection $collection) {
    // Alter user login route
    if ($route = $collection->get('user.login')) {
      $route->setPath('/custom-login');
      $route->setDefault('_title', 'Custom Login');
    }

    // Change access requirements
    if ($route = $collection->get('my_module.page')) {
      $route->setRequirement('_permission', 'new permission');
    }
  }

  // Control subscriber weight/priority
  public static function getSubscribedEvents(): array {
    $events = parent::getSubscribedEvents();
    // Run after other subscribers (higher number = later)
    $events[RoutingEvents::ALTER] = ['onAlterRoutes', -200];
    return $events;
  }
}
```

```yaml
# my_module.services.yml
services:
  my_module.route_subscriber:
    class: Drupal\my_module\Routing\RouteSubscriber
    tags:
      - { name: event_subscriber }
```

Reference: `core/lib/Drupal/Core/Routing/RouteSubscriberBase.php`

## Common Mistakes

- **Wrong**: Using RouteSubscriber to create routes → **Right**: Use `route_callbacks` for new routes
- **Wrong**: Not checking if route exists before altering → **Right**: Always check `if ($route = $collection->get(...))`
- **Wrong**: Forgetting to register service with tag → **Right**: Add `event_subscriber` tag in services.yml
- **Wrong**: Wrong event priority causing conflicts → **Right**: Adjust priority number to control order
- **Wrong**: Altering routes without clearing cache → **Right**: Run `drush cr` after changes

## See Also

- [Dynamic Routes](dynamic-routes.md)
- [Custom Access Checking](custom-access-checking.md)
- Reference: [Altering existing routes - Drupal.org](https://www.drupal.org/docs/drupal-apis/routing-system/altering-existing-routes-and-adding-new-routes-based-on-dynamic-ones)
- Reference: [Route Subscriber service - Drupal Sun](https://drupalsun.com/philipnorton42/2022/10/16/drupal-9-altering-routes-route-subscriber-service)
- Reference: [Overwriting routes - Stefan Van Looveren](https://stefvanlooveren.me/blog/overwriting-routes-drupal-9-10-using-route-subscriber-and-custom-controller)
