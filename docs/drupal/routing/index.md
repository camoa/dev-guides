---
description: Drupal Routing - YAML route definitions, access control, dynamic routes, and security best practices
guide-meta:
  concepts:
    - routing.yml
    - route definitions
    - route parameters
    - access control
    - custom access checkers
    - dynamic routes
    - route subscribers
    - admin routes
  not:
    - menu links
    - breadcrumbs (see drupal/breadcrumbs)
  requires: []
  complements:
    - drupal/security
    - drupal/forms
    - drupal/services
  specializes: ""
  category: drupal
tracks:
  - project: drupal
    channel: stable
    verified: 2026-02-12
---

# Drupal Routing

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Fix a routing error causing site crashes | [YAML Escaping Rules](yaml-escaping-rules.md) | Use single backslashes in single quotes for controller/form class references. This is CRITICAL - incorrect escaping causes fatal site crashes during cache rebuild. |
| Write a basic route definition | [Basic Route Structure](basic-route-structure.md) | Use when defining any new route in a `*.routing.yml` file. This is the foundation for all routing definitions. |
| Add access control to a route | [Access Control Patterns](access-control-patterns.md) | Use when restricting route access to specific users, roles, or custom conditions. Always define access requirements - never leave routes open. |
| Create routes with parameters | [Route Parameters](route-parameters.md) | Use when routes need dynamic segments (e.g., node IDs, user IDs, custom identifiers). Parameters enable reusable routes for multiple entities or contexts. |
| Configure admin routes with proper theme | [Admin Route Configuration](admin-route-configuration.md) | Use when creating administrative interfaces that should use the admin theme and integrate with Drupal's admin UI patterns. |
| Build dynamic routes programmatically | [Dynamic Routes](dynamic-routes.md) | Use when routes need to be generated programmatically based on configuration, content, or runtime conditions. Prefer static YAML routes when possible - use dynamic routes only when necessary. |
| Alter existing routes | [Route Subscribers](route-subscribers.md) | Use when you need to alter existing routes from core or contrib modules. Do NOT use to create routes - use `route_callbacks` or static YAML instead. |
| Create custom access checkers | [Custom Access Checking](custom-access-checking.md) | Use when built-in access checks (`_permission`, `_role`, `_entity_access`) are insufficient. Complex business logic, multi-factor checks, or context-dependent access require custom checkers. |
| Debug routing issues | [Testing and Debugging](testing-and-debugging.md) | Always test routes after creation or modification. Routing errors can crash sites, so validation is critical before deployment. |
| Avoid common routing mistakes | [Common Pitfalls](common-pitfalls.md) | Reference this before committing routing YAML or when debugging routing issues. These are real-world errors that crash sites or create security vulnerabilities. |
| Ensure routing security | [Security Best Practices](security-best-practices.md) | Use when designing any route - security must be considered from the start, not added later. Every route is a potential attack vector. |
| Optimize routing performance | [Performance Best Practices](performance-best-practices.md) | Use when routes are high-traffic, when using dynamic routes or custom access checkers, or when routes load significant data. Performance issues in routing affect every page load. |
