---
description: Drupal routing security - protect routes with access control, input validation, and CSRF protection
drupal_version: "11.x"
---

# Security Best Practices

## When to Use

> Use when designing any route - security must be considered from the start, not added later. Every route is a potential attack vector.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Restrict route access | Always define `requirements` | Never leave routes open to all users |
| Validate route parameters | Regex in `requirements` | Prevent injection attacks, unexpected input |
| Protect admin functionality | `_permission` with "administer" prefix | Clear distinction between user/admin actions |
| Check entity access | `_entity_access: 'entity_type.operation'` | Leverage entity access system |
| Complex access logic | Custom access checker with proper caching | Full control with performance |
| Form routes with CSRF | Use `_form` default | Drupal handles CSRF tokens automatically |

## Pattern

```yaml
# Secure route example
my_module.admin_action:
  path: '/admin/my-module/dangerous-action/{item_id}'
  defaults:
    _form: '\Drupal\my_module\Form\DangerousActionForm'
    _title: 'Dangerous Action'
  requirements:
    # Multiple layers of security
    _permission: 'administer my module'  # Permission check
    _entity_access: 'node.delete'  # Entity access check
    item_id: '\d+'  # Input validation
  options:
    _admin_route: TRUE
    parameters:
      item_id:
        type: entity:node  # Entity validation + access
```

## Security Principles

### 1. Access Control (CRITICAL)

- NEVER leave routes without access requirements
- Use most restrictive permission necessary
- Layer multiple checks when appropriate (`_permission` + `_entity_access`)
- Test access with different user roles

### 2. Input Validation (CRITICAL)

- ALWAYS validate route parameters with regex requirements
- Use entity type validation when loading entities
- Sanitize parameter values in controller code
- Never trust user input from URL parameters

### 3. CSRF Protection

- Use `_form` routes for state-changing operations
- Forms automatically include CSRF tokens
- Don't use `_controller` for destructive actions
- Validate form tokens in custom form processing

### 4. Admin vs. User Routes

- Admin routes MUST use "administer *" permissions
- Never grant admin permissions to untrusted roles
- Use `_admin_route: TRUE` for admin pages
- Separate admin and user functionality

### 5. Entity Access Integration

- Use `_entity_access` when routes involve entities
- Don't bypass entity access checks
- Custom access checkers should respect entity access
- Consider field-level access for sensitive data

## Common Mistakes

- **Wrong**: No access requirements → **Right**: Always define `_permission` or equivalent
- **Wrong**: No parameter validation → **Right**: Add regex requirements for all parameters
- **Wrong**: Using `_controller` for destructive actions → **Right**: Use `_form` for CSRF protection
- **Wrong**: Granting admin permissions to authenticated users → **Right**: Restrict admin permissions carefully
- **Wrong**: Not using `_entity_access` → **Right**: Leverage entity access system
- **Wrong**: Custom access checkers without proper logic → **Right**: Implement thorough access logic
- **Wrong**: Trusting URL parameters in queries → **Right**: Validate and sanitize all input

## See Also

- [Common Pitfalls](common-pitfalls.md)
- [Performance Best Practices](performance-best-practices.md)
- Reference: [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- Reference: Drupal security best practices documentation
