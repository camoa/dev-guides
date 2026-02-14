---
description: Understanding Drupal's three-layer access control architecture for routes, entities, and fields.
---

# Access System Architecture

## When to Use
When designing routes, controllers, or entities that require access control -- understanding the architecture prevents security gaps.

## Decision
Drupal's access system has three main layers:

| Access Type | Scope | When to Use |
|---|---|---|
| Route Access | HTTP endpoints | Controlling URL access before controller execution |
| Entity Access | Content/config entities | Controlling create/read/update/delete operations on entities |
| Field Access | Entity fields | Hiding/protecting individual fields (rare, usually use entity) |

**Access Check Flow:**
1. Request arrives at routing system
2. `AccessManager` collects all applicable access checks for the route
3. Each check returns `AccessResult` (allowed/forbidden/neutral)
4. Results combine: ANY forbidden = denied, ALL must allow = granted
5. If granted, route controller executes

## Pattern
Route access checks specified in `*.routing.yml`:
```yaml
mymodule.admin_page:
  path: '/admin/mymodule'
  defaults:
    _controller: '\Drupal\mymodule\Controller\AdminController::build'
  requirements:
    _permission: 'administer site configuration'
    # OR custom access check
    _custom_access: '\Drupal\mymodule\Access\CustomCheck::access'
```
Reference: `/core/lib/Drupal/Core/Access/AccessManager.php`

## Common Mistakes
- No access check on route -- Anyone can access, including anonymous users
- Using neutral when forbidden needed -- Neutral means "no opinion", forbidden actively denies
- Checking access only in controller -- Route-level checks prevent execution entirely
- Not caching access results -- Adds cache contexts/tags or page performance suffers
- Using `AccessResult::allowed()` unconditionally -- This is always wrong; condition it

## See Also
- [Route Access Checks](route-access-checks.md) for implementation details
- [AccessResult Patterns](accessresult-patterns.md) for return values
- Reference: https://www.drupal.org/docs/8/api/routing-system/access-checking-on-routes
