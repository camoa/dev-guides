---
description: Control block visibility based on pages, roles, content types, or custom condition plugins
drupal_version: "11.x"
---

# Visibility Conditions

## When to Use

> Use visibility conditions for UI-configurable placement rules (pages, roles, node type). Use `blockAccess()` for programmatic logic that can't be expressed in conditions.

## Decision

| Condition | Use when... | Plugin ID |
|-----------|-------------|-----------|
| request_path | Show/hide based on URL patterns | `request_path` |
| user_role | Show/hide based on user's roles | `user_role` |
| entity_bundle:node | Show/hide based on node content type | `entity_bundle:node` |
| current_theme | Show/hide based on active theme | `current_theme` |
| response_status | Show/hide based on HTTP status (404, 403) | `response_status` |
| Custom condition | Complex logic needed | Create `#[Condition]` plugin |

## Pattern

**Core visibility conditions:**

```php
'visibility' => [
  'request_path' => [
    'id' => 'request_path',
    'pages' => "/admin/*\n/user/*/edit",
    'negate' => TRUE, // Hide on these pages
  ],
  'user_role' => [
    'id' => 'user_role',
    'roles' => [
      'authenticated' => 'authenticated',
      'premium' => 'premium',
    ],
    'negate' => FALSE,
  ],
  'entity_bundle:node' => [
    'id' => 'entity_bundle:node',
    'bundles' => ['article' => 'article'],
    'negate' => FALSE,
    'context_mapping' => [
      'node' => '@node.node_route_context:node',
    ],
  ],
],
```

**Custom visibility condition:**

```php
namespace Drupal\mymodule\Plugin\Condition;

use Drupal\Core\Condition\Attribute\Condition;
use Drupal\Core\Condition\ConditionPluginBase;
use Drupal\Core\StringTranslation\TranslatableMarkup;

#[Condition(
  id: "time_of_day",
  label: new TranslatableMarkup("Time of Day"),
)]
class TimeOfDay extends ConditionPluginBase {

  public function evaluate() {
    $hour = (int) date('H');
    return $hour >= 9 && $hour <= 17; // Business hours
  }

  public function summary() {
    return $this->t('Visible during business hours (9am-5pm)');
  }
}
```

**Reference:** `core/modules/user/src/Plugin/Condition/UserRole.php`, `core/modules/system/src/Plugin/Condition/RequestPath.php`

## Common Mistakes

- **Wrong**: Using `request_path` without leading slash → **Right**: Condition never matches; paths must start with `/`
- **Wrong**: Forgetting context mapping for entity-based conditions → **Right**: Plugin can't access entity; condition fails
- **Wrong**: Not considering cache implications → **Right**: Add appropriate cache contexts in condition
- **Wrong**: Using complex logic in `request_path` → **Right**: Create custom condition plugin for complex rules
- **Wrong**: Negating conditions when positive logic is clearer → **Right**: Use `negate => FALSE` and adjust condition instead

## See Also

- [Block Access Control](block-access-control.md)
- [Block Placement & Configuration](block-placement.md)
- Reference: https://www.drupal.org/docs/drupal-apis/plugin-api/plugin-api-overview
- Reference: https://www.jaypan.com/tutorial/custom-drupal-block-visibility-plugins-and-condition-plugin-api
