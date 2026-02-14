---
description: Understanding Drupal's defense-in-depth security model with multiple layers of protection against different attack vectors.
---

# Security Overview

## When to Use
Understanding Drupal's defense-in-depth security model when architecting applications, evaluating modules, or responding to security advisories.

## Decision
Drupal security operates on multiple layers — each provides defense against different attack vectors:

| Security Layer | Purpose | Primary Components |
|---|---|---|
| Access Control | Who can do what | Permissions, roles, access checks, entity access |
| Input Validation | What data is acceptable | Form API validation, typed data, sanitization |
| Output Encoding | Prevent XSS | Twig autoescape, render system, Xss::filter() |
| CSRF Protection | Prevent unauthorized actions | Token validation, session binding |
| SQL Injection Prevention | Prevent database compromise | Database API, parameterized queries |
| Authentication | Verify user identity | Session management, authentication providers |
| Infrastructure | Server-level hardening | HTTPS, security headers, file permissions |

## Pattern
Security decision flow when processing a request:
```php
// 1. Authentication: Who is this?
$account = \Drupal::currentUser();

// 2. Access Control: Can they access this?
$access = AccessResult::allowedIfHasPermission($account, 'view content');

// 3. Input Validation: Is the data safe?
$form['#validate'][] = '::validateForm';

// 4. Output Encoding: Render safely
return ['#markup' => $safe_markup]; // Twig autoescapes
```
Reference: `/core/lib/Drupal/Core/Access/AccessResult.php`

## Common Mistakes
- Relying on single security layer -- Use defense-in-depth with multiple layers
- Trusting user input -- Always validate and sanitize, even from authenticated users
- Implementing custom security -- Use Drupal's built-in systems (they're peer-reviewed)
- Ignoring contrib security advisories -- Subscribe to https://www.drupal.org/security and update promptly
- Assuming HTTPS is enough -- HTTPS protects transport, not application logic

## See Also
- [OWASP Top 10 in Drupal](owasp-top-10-in-drupal.md) for vulnerability mapping
- Reference: https://www.drupal.org/docs/develop/security
