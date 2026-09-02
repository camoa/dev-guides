---
description: "Security considerations for AI-assisted Drupal contributions — AI-specific risks (hallucinated APIs, missing sanitization, access bypass, CSRF), the security review sequence, and sanitization APIs"
tldr: "Use this when reviewing AI-generated code for security issues, or when you want to understand the security risks specific to AI-assisted Drupal development."
drupal_version: "11.x"
---

# Security Considerations

## When to Use

> When reviewing AI-generated code for security issues, or when you want to understand the security risks specific to AI-assisted Drupal development.

## Decision: AI-Specific Security Risks

| Risk | Description | Detection | Prevention |
|---|---|---|---|
| Hallucinated APIs | AI invents function names that look real, may bypass security layers | Check API docs for every unfamiliar function | Verify all function calls exist in target Drupal version |
| Missing sanitization | AI forgets `Html::escape()`, `Xss::filter()`, `#plain_text` | Search for unescaped output in templates and render arrays | Use Drupal's render system; avoid raw HTML concatenation |
| SQL injection | AI uses raw queries instead of entity queries or DBAL | Search for `db_query` with string interpolation | Use entity queries or parameterized database queries |
| Access bypass | AI skips `$entity->access('view')` checks or omits route access | Check every route has `_permission` or `_access` | Audit all routes and entity operations for access checks |
| CSRF | AI creates custom endpoints without token validation | Check non-Form-API routes for token handling | Use Form API (automatic CSRF) or add manual token validation |
| Insecure defaults | AI sets overly permissive permissions or disables security | Review all permission assignments and config | Follow least-privilege principle |
| Dependency confusion | AI suggests packages that don't exist or are malicious | Verify package names on packagist.org/drupal.org | Only install packages from trusted sources |
| Information disclosure | AI logs sensitive data or exposes it in error messages | Review all logging and error handling | Never log passwords, tokens, or PII |

## Pattern: Security Review Sequence

1. **Routes**: Does every route have proper access requirements?
2. **Forms**: Are all forms using Form API (automatic CSRF protection)?
3. **Output**: Is all user-supplied content properly escaped?
4. **Queries**: Are all database queries parameterized?
5. **Access**: Are entity access checks performed before display/modification?
6. **Permissions**: Are custom permissions following least-privilege?
7. **Files**: Are file uploads validated for type and size?
8. **Configuration**: Are sensitive values stored securely (not in code)?

## Pattern: Sanitization APIs AI Commonly Skips

```php
// Output escaping
Html::escape($user_input);           // Plain text in HTML context
Xss::filter($html_input);           // Allow safe HTML tags
Xss::filterAdmin($admin_input);     // Admin-only filtered HTML

// Render array escaping
'#plain_text' => $user_input,        // Auto-escaped in render
'#markup' => $safe_html_only,        // NOT escaped — only use with safe HTML

// URL handling
Url::fromUserInput($input);          // Validates URL input
UrlHelper::filterBadProtocol($url);  // Removes javascript: etc.

// Database
$query->condition('field', $value);  // Parameterized — safe
// NEVER: "SELECT * FROM {table} WHERE field = '$value'" — SQL injection
```

## Common Mistakes

- **Trusting AI's security claims** — AI will say "this is secure" while missing OWASP Top 10 vulnerabilities. Verify yourself.
- **Using `#markup` for user input** — `#markup` is NOT escaped. Use `#plain_text` for user-supplied content or `Xss::filter()` for HTML.
- **Missing access checks on custom routes** — AI often creates routes without `_permission` or `_access` requirements
- **Accepting AI's "this is sanitized" without checking** — Trace the data flow from input to output. Every user-supplied value must be escaped before rendering.

## See Also

- [AI Code Review Checklist](ai-code-review-checklist.md) — full pre-submission checklist
- [Coding Standards](coding-standards.md) — standards AI commonly violates
- [Human Review Requirements](human-review-requirements.md) — review depth expectations
