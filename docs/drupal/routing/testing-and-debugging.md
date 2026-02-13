---
description: Testing and debugging Drupal routes - validate YAML syntax and troubleshoot routing issues
drupal_version: "11.x"
---

# Testing and Debugging

## When to Use

> Always test routes after creation or modification. Routing errors can crash sites, so validation is critical before deployment.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Validate YAML syntax | `drush cr` or `yamllint` | Catches syntax errors before they break site |
| List all routes | `drush route:list` | See registered routes and their properties |
| Debug specific route | `drush route:debug ROUTE_NAME` | View full route definition and requirements |
| Test access control | Browser testing + permission changes | Real-world access validation |
| Find route by path | `drush route:list --path=/admin/config` | Match routes to URLs |
| Validate routing file | Manual grep for double backslashes | Find the critical escaping error |

## Pattern

```bash
# Critical: Test cache rebuild after routing changes
drush cr
# If this fails, your routing YAML has errors

# List all routes from a module
drush route:list | grep my_module

# Debug specific route
drush route:debug my_module.admin

# Check for double backslash errors
grep -n '\\\\\\\\' *.routing.yml

# Validate YAML syntax (if yamllint installed)
yamllint my_module.routing.yml

# Find routes by path pattern
drush route:list --path=/admin
```

## Common Mistakes

- **Wrong**: Not running `drush cr` after routing changes → **Right**: Always rebuild cache to see changes
- **Wrong**: Deploying routing changes without testing → **Right**: Test cache rebuild before deployment
- **Wrong**: Missing grep check for double backslashes → **Right**: Validate no `\\\\` in routing files
- **Wrong**: Not testing access control with different roles → **Right**: Test with multiple user roles
- **Wrong**: Assuming YAML is valid without validation → **Right**: Run `drush cr` or yamllint
- **Wrong**: Not checking route conflicts → **Right**: Use `drush route:list` to verify no path collisions

## See Also

- [Custom Access Checking](custom-access-checking.md)
- [Common Pitfalls](common-pitfalls.md)
- Reference: Drush routing commands documentation
