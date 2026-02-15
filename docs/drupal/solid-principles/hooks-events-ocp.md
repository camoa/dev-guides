---
description: Use hooks and event subscribers to extend Drupal behavior without modifying existing code
drupal_version: "11.x"
---

# Hooks & Events - Open for Extension (OCP)

## When to Use

Hooks and event subscribers let you extend behavior without modifying existing code. Use `hook_alter()` for data modification, events for architectural extension points.

## Decision

| To extend... | Use... | Pattern |
|---|---|---|
| Entity data before save | hook_ENTITY_TYPE_presave() | Alter entity in hook |
| Form structure | hook_form_alter() | Modify $form array |
| Render arrays | hook_preprocess_HOOK() | Add template variables |
| Access decisions | hook_ENTITY_TYPE_access() | Return AccessResult |
| Routing decisions | RouteSubscriber event | Alter route collection |
| Kernel/HTTP events | Symfony events | Event subscriber |

## Pattern

**GOOD: Extending via hook_alter (OCP)**

```php
// src/Hook/MyModuleEntityHooks.php
class MyModuleEntityHooks {
  #[Hook('node_presave')]
  public function nodePresave(NodeInterface $node): void {
    // Extend node save behavior without modifying NodeStorage
    if ($node->bundle() === 'article') {
      $node->set('field_custom', 'value');
    }
  }
}
```

**GOOD: Event subscriber (OCP)**

```php
// src/EventSubscriber/RouteSubscriber.php
class RouteSubscriber extends RouteSubscriberBase {
  protected function alterRoutes(RouteCollection $collection) {
    // Extend routing without modifying core router
    if ($route = $collection->get('node.add')) {
      $route->setRequirement('_permission', 'create content');
    }
  }
}
```

Reference:

- `/core/modules/node/src/Hook/NodeEntityHooks.php` -- OOP hook implementations
- `/core/lib/Drupal/Core/Routing/RouteSubscriberBase.php` -- event subscriber base

## Common Mistakes

- Copying and modifying core functions -- use hooks to alter behavior. **WHY:** Duplicate code breaks when core updates; impossible to maintain
- Returning incorrect type from hooks -- follow hook signature exactly. **WHY:** `hook_alter()` returns void, `hook_access()` returns AccessResult; wrong type breaks system
- Doing heavy processing in every hook invocation -- add conditions early, cache results. **WHY:** Hooks run on every request; slow hooks destroy site performance
- Not checking if event listener should act -- check context before processing. **WHY:** Running on wrong entity/form/route causes bugs, performance issues

## See Also

- [Plugin System](plugin-system-ocp.md) for plugin-based extension
- [Access Results](access-results-lsp.md) for access hook patterns
- Reference: [Drupal Hook API](https://api.drupal.org/api/drupal/core!core.api.php/group/hooks/11.x)
