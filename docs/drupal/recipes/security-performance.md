---
description: Security and performance considerations specific to recipes including permission audits and optimization
drupal_version: "11.x"
---

# Security & Performance

## When to Use

> Apply security and performance best practices when creating recipes to ensure safe and efficient recipe application.

## Decision

### Security Concerns

| Risk | Mitigation | Why |
|------|------------|-----|
| Permission grants | Audit all grantPermission actions | Recipes can grant admin permissions; review carefully |
| Default content access | Content imports as admin user | Imported content bypasses access control; validate ownership |
| Input validation | Use constraints on all inputs | Unvalidated input can inject malicious config values |
| Secrets in recipes | Never commit secrets | Use inputs with env source for API keys, passwords |
| XSS in default content | Sanitize imported content | Text format filters apply on render, not import; validate HTML |

### Performance Concerns

| Issue | Solution | Why |
|-------|----------|-----|
| Large default content | Use migration instead | Default content loads all at once; memory intensive |
| Recursive recipe dependencies | Keep dependency depth shallow | Each level adds processing time |
| Config action wildcards | Target specific entities when possible | `user.role.*` processes all roles; slow with many entities |
| Batch vs direct application | Use batches for large recipes | Prevents timeouts on web-based application |

## Pattern

Safe permission granting:

```yaml
# DANGEROUS: Grants admin permission to authenticated users
user.role.authenticated:
  grantPermission: 'administer site configuration'

# SAFE: Grants limited permission
user.role.authenticated:
  grantPermission: 'access content'

# SAFE: Creates dedicated role for admin permissions
user.role.site_admin:
  createIfNotExists:
    label: 'Site Administrator'
  grantPermissions:
    - 'administer site configuration'
```

Input validation:

```yaml
input:
  admin_email:
    data_type: string
    constraints:
      Email: ~
      NotBlank: ~
    default: { source: env, env: ADMIN_EMAIL }
  site_url:
    data_type: string
    constraints:
      Url: ~
    default: { source: value, value: 'https://example.com' }
```

Batch application for large recipes:

```php
// Direct application (fast but can timeout)
RecipeRunner::processRecipe($recipe);

// Batch application (slower but handles timeouts)
$batch = [
  'operations' => RecipeRunner::toBatchOperations($recipe),
  'finished' => 'my_recipe_batch_finished',
];
batch_set($batch);
```

Targeted config actions:

```yaml
# SLOW: Processes every role
config:
  actions:
    user.role.*:
      grantPermission: 'access content'

# FAST: Processes only specific roles
config:
  actions:
    user.role.authenticated:
      grantPermission: 'access content'
    user.role.editor:
      grantPermission: 'access content'
```

## Common Mistakes

- **Wrong**: Granting broad permissions to authenticated role → **Right**: Security risk; create dedicated roles
- **Wrong**: Not validating inputs → **Right**: Allows injection of malicious values into config
- **Wrong**: Committing API keys → **Right**: Use environment variables via input system
- **Wrong**: Importing large content datasets → **Right**: Use migration for datasets >100 entities
- **Wrong**: Assuming recipes run as admin → **Right**: They do (AdminAccountSwitcher) but validate permissions anyway
- **Wrong**: Not testing recipe performance → **Right**: Large recipes can timeout on web application; test with realistic data

## See Also

- [Anti-Patterns & Common Mistakes](anti-patterns-mistakes.md)
- [Code Reference Map](code-reference-map.md)
- Reference: https://owasp.org/www-project-top-ten/
