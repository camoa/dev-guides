---
description: Security best practices organized by domain covering access control, code security, input/output, authentication, and infrastructure hardening.
---

# Best Practices and Patterns

## When to Use
When establishing security standards for a project or conducting code reviews.

## Decision
Security best practices organized by domain:

### Access Control Best Practices
| Practice | Why |
|---|---|
| Always check access at route level | Prevents controller execution for unauthorized users |
| Use `->accessCheck(TRUE)` on entity queries | Filters results to what user can see |
| Return `forbidden()` not `neutral()` for denied | Explicitly blocks access |
| Add cache metadata to access results | Performance; prevents stale access decisions |
| Use permissions, not roles, in code | Roles are configurable; permissions are API |

### Code Security Best Practices
| Practice | Why |
|---|---|
| Dependency injection over `\Drupal::` | Testable, follows architecture |
| Use Database API, never raw SQL | Parameterized queries prevent SQL injection |
| Use Form API for all forms | Automatic CSRF, validation, theming |
| Implement `TrustedCallbackInterface` | Prevents arbitrary callback execution |
| Type-hint parameters | Catches injection at PHP level |

### Input/Output Best Practices
| Practice | Why |
|---|---|
| Validate input, sanitize output | Input validation ensures integrity; output sanitization prevents XSS |
| Use Twig templates, not PHP in themes | Autoescape prevents XSS |
| Never use `|raw` filter without justification | Disables XSS protection |
| Use `Markup::create()` only for trusted content | Bypasses autoescape |
| Validate file uploads strictly | Unrestricted upload = RCE |

### Authentication/Session Best Practices
| Practice | Why |
|---|---|
| Enforce HTTPS in production | Protects credentials in transit |
| Set `trusted_host_patterns` | Prevents cache poisoning, session hijacking |
| Use flood control on login | Prevents brute force |
| Regenerate session on privilege escalation | Prevents session fixation |
| Implement rate limiting | Prevents abuse |

### Infrastructure Best Practices
| Practice | Why |
|---|---|
| Keep Drupal core and contrib updated | Security patches |
| Disable unused modules | Reduces attack surface |
| Use private file system for sensitive files | Access-controlled |
| Set appropriate file permissions (755/644) | Prevents unauthorized modification |
| Configure CSP headers | Defense-in-depth against XSS |
| Enable error logging, disable display | Log attacks, don't expose internals |

## Pattern
Security-first development checklist:
```php
// 1. Access control
AccessResult::allowedIfHasPermission($account, 'my permission')
  ->addCacheContexts(['user.permissions']);

// 2. Input validation
$form['#validate'][] = '::validateForm';

// 3. Database query
$database->query('SELECT * FROM {table} WHERE id = :id', [':id' => $id]);

// 4. Output sanitization
{{ user_input }}  {# Twig autoescape #}
// OR
$build['#markup'] = Xss::filter($content);

// 5. CSRF protection
// Route: _csrf_token: 'TRUE'
// Form: automatic

// 6. Session security
// settings.php: trusted_host_patterns, HTTPS
```

## Common Mistakes
- Security through obscurity -- Attackers will find it; use proven defenses
- Assuming Drupal is "secure by default" -- Must be configured and used correctly
- Ignoring contrib security advisories -- Compromises happen through contrib
- Not threat modeling -- Identify assets and attack vectors first
- Over-relying on WAF -- Application layer must be secure
- Not testing negative cases -- Test what happens when access denied, input invalid

## See Also
- Reference: https://www.drupal.org/docs/administering-a-drupal-site/security-in-drupal
