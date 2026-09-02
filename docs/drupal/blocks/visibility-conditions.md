---
description: Control block visibility based on pages, roles, content types, or custom condition plugins
tldr: "Use visibility conditions for UI-configurable placement rules (pages, roles, node type). Use `blockAccess()` for programmatic logic that can't be expressed in conditions."
drupal_version: "11.x"
---

# Visibility Conditions

## When to Use

> Controlling block visibility based on pages, user roles, content types, or custom logic.

## Items

#### request_path
**Description:** Show/hide block based on URL patterns
**Plugin ID:** `request_path`
**Configuration:**
| Setting | Type | Description |
|---------|------|-------------|
| pages | string | One path per line, wildcards supported (`/user/*`, `<front>`) |
| negate | boolean | Reverse the condition |

**Usage Example:**
```php
'visibility' => [
  'request_path' => [
    'id' => 'request_path',
    'pages' => "/admin/*\n/user/*/edit",
    'negate' => TRUE, // Hide on these pages
  ],
],
```
**Gotchas:** Paths must start with `/`; `<front>` is special keyword for homepage; comparison is case-insensitive

#### user_role
**Description:** Show/hide block based on user's roles
**Plugin ID:** `user_role`
**Configuration:**
| Setting | Type | Description |
|---------|------|-------------|
| roles | array | Machine names of roles (e.g., `['authenticated', 'administrator']`) |
| negate | boolean | Reverse the condition |

**Usage Example:**
```php
'visibility' => [
  'user_role' => [
    'id' => 'user_role',
    'roles' => [
      'authenticated' => 'authenticated',
      'premium' => 'premium',
    ],
    'negate' => FALSE,
  ],
],
```
**Gotchas:** Empty roles array shows to all users; cache context `user.roles` automatically added

#### entity_bundle:node
**Description:** Show/hide block based on node content type
**Plugin ID:** `entity_bundle:node`
**Configuration:**
| Setting | Type | Description |
|---------|------|-------------|
| bundles | array | Node type machine names (e.g., `['article', 'page']`) |
| negate | boolean | Reverse the condition |

**Usage Example:**
```php
'visibility' => [
  'entity_bundle:node' => [
    'id' => 'entity_bundle:node',
    'bundles' => [
      'article' => 'article',
    ],
    'negate' => FALSE,
    'context_mapping' => [
      'node' => '@node.node_route_context:node',
    ],
  ],
],
```
**Gotchas:** Requires node context; only works on node pages; check context mapping

#### current_theme
**Description:** Show/hide block based on active theme
**Plugin ID:** `current_theme`
**Configuration:**
| Setting | Type | Description |
|---------|------|-------------|
| theme | string | Theme machine name |
| negate | boolean | Reverse the condition |

**Gotchas:** Rarely needed; blocks already theme-specific via placement

#### response_status
**Description:** Show/hide block based on HTTP response status
**Plugin ID:** `response_status`
**Configuration:**
| Setting | Type | Description |
|---------|------|-------------|
| status_codes | array | HTTP status codes (e.g., `[403, 404]`) |
| negate | boolean | Reverse the condition |

**Gotchas:** Useful for error pages; ensure cache contexts set properly

## Creating Custom Visibility Conditions

**Steps:**
1. Create condition plugin in `{module}/src/Plugin/Condition/`
2. Extend `ConditionPluginBase`
3. Use `#[Condition]` attribute
4. Implement `evaluate()` method

**Pattern:**
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

- Using `request_path` without leading slash → Condition never matches; paths must start with `/`
- Forgetting context mapping for entity-based conditions → Plugin can't access entity; condition fails
- Not considering cache implications → Add appropriate cache contexts in condition
- Using complex logic in `request_path` → Create custom condition plugin for complex rules
- Negating conditions when positive logic is clearer → Use `negate => FALSE` and adjust condition instead

## See Also

- [Block Access Control](block-access-control.md) (programmatic access)
- [Block Placement & Configuration](block-placement.md)
- Reference: https://www.drupal.org/docs/drupal-apis/plugin-api/plugin-api-overview
- Reference: https://www.jaypan.com/tutorial/custom-drupal-block-visibility-plugins-and-condition-plugin-api
