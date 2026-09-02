---
description: Security and performance considerations specific to recipes including permission audits and optimization
tldr: "Apply security and performance best practices when creating recipes to ensure safe and efficient recipe application."
drupal_version: "11.x"
---

# Security & Performance

## When to Use

> Apply security and performance best practices when creating recipes to ensure safe and efficient recipe application.

Security and performance considerations specific to recipes.

## Decision: Security and Performance Risks

### Security Concerns

| Risk | Mitigation | Why |
|------|------------|-----|
| Permission grants | Audit all grantPermission actions | Recipes can grant admin permissions; review carefully |
| Default content access | Content imports as admin user | Imported content bypasses access control; validate ownership |
| Input validation | Use constraints on all inputs | Unvalidated input can inject malicious config values |
| Secrets in recipes | Never commit secrets | Use inputs with env source for API keys, passwords |
| XSS in default content | Sanitize imported content | Text format filters apply on render, not import; validate HTML |

**Pattern** — Safe permission granting:
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

**Pattern** — Input validation:
```yaml
input:
  admin_email:
    data_type: string
    constraints:
      Email: ~  # Validates email format
      NotBlank: ~
    default: { source: env, env: ADMIN_EMAIL }
  site_url:
    data_type: string
    constraints:
      Url: ~  # Validates URL format
    default: { source: value, value: 'https://example.com' }
```

### Performance Concerns

| Issue | Solution | Why |
|-------|----------|-----|
| Large default content | Use migration instead | Default content loads all at once; memory intensive |
| Recursive recipe dependencies | Keep dependency depth shallow | Each level adds processing time |
| Config action wildcards | Target specific entities when possible | `user.role.*` processes all roles; slow with many entities |
| Batch vs direct application | Use batches for large recipes | Prevents timeouts on web-based application |

**Pattern** — Batch application for large recipes:
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

**Pattern** — Targeted config actions:
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

- Granting broad permissions to authenticated role → Security risk; create dedicated roles
- Not validating inputs → Allows injection of malicious values into config
- Committing API keys → Use environment variables via input system
- Importing large content datasets → Use migration for datasets >100 entities
- Not considering OWASP top 10 → SQL injection (no risk in recipes), XSS (validate text formats), CSRF (no user-triggered actions in recipes)
- Assuming recipes run as admin → They do (AdminAccountSwitcher) but validate permissions anyway
- Not testing recipe performance → Large recipes can timeout on web application; test with realistic data

## See Also

- Previous: ← [Anti-Patterns & Common Mistakes](anti-patterns-mistakes.md)
- Next: [Code Reference Map](code-reference-map.md) →
- Reference: https://owasp.org/www-project-top-ten/
