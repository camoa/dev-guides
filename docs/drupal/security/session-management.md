---
description: Securing sessions with cookie settings, trusted host patterns, session regeneration, flood control, and proper logout implementation.
---

# Session Management

## When to Use
Understanding session security to prevent session fixation, hijacking, and ensure proper session lifecycle.

## Steps
1. **Session configuration in settings.php**
   ```php
   // Secure session cookies
   ini_set('session.cookie_httponly', 1);  // Prevent JavaScript access
   ini_set('session.cookie_secure', 1);    // HTTPS only (production)
   ini_set('session.cookie_samesite', 'Lax'); // CSRF protection

   // Session lifetime
   ini_set('session.gc_maxlifetime', 200000);  // 55 hours
   ini_set('session.cookie_lifetime', 2000000); // ~23 days
   ```

2. **Trusted host patterns (REQUIRED for security)**
   ```php
   // settings.php - Prevent host header injection
   $settings['trusted_host_patterns'] = [
     '^example\.com$',
     '^.+\.example\.com$',  // Subdomains
     '^localhost$',
   ];
   ```

3. **Session regeneration on privilege escalation**
   ```php
   // Core handles this automatically on login
   // If manually changing user roles/permissions:
   \Drupal::service('session_manager')->regenerate();
   ```

4. **Proper logout implementation**
   ```php
   // In custom logout
   user_logout();  // Destroys session, invokes hooks

   // Manual approach (not recommended)
   \Drupal::service('session_manager')->destroy();
   \Drupal::currentUser()->setAccount(new AnonymousUserSession());
   ```

5. **Flood control for authentication**
   ```php
   $flood = \Drupal::flood();

   // Check before login attempt
   if (!$flood->isAllowed('user.failed_login_ip', 5, 3600)) {
     // Too many attempts from this IP
     throw new \Exception('Too many failed login attempts.');
   }

   // Register failed attempt
   $flood->register('user.failed_login_ip', 3600);

   // Clear on successful login
   $flood->clear('user.failed_login_ip');
   ```

## Decision Points
| At this step... | If... | Then... |
|---|---|---|
| Deployment | Production site | Force HTTPS, set `cookie_secure` to 1 |
| Deployment | Development/localhost | `cookie_secure` can be 0 |
| Configuration | Multi-domain setup | Configure `trusted_host_patterns` carefully |
| Custom auth | User logs in | Let core handle session regeneration |
| Custom auth | Privilege changes | Call `->regenerate()` manually |

## Common Mistakes
- No trusted_host_patterns -- **CRITICAL**: Cache poisoning, session hijacking
- Not forcing HTTPS -- Session cookies sent in clear text
- Not setting httponly flag -- XSS can steal session cookies
- Predictable session IDs -- Use Drupal's session manager, not raw PHP sessions
- Not regenerating on login -- Session fixation vulnerability
- Sharing sessions across security boundaries -- Different apps should use different session cookies

## See Also
- Reference: `/core/lib/Drupal/Core/Session/SessionManager.php`
- [Authentication System](authentication-system.md) for related concepts
- Reference: https://www.drupal.org/docs/administering-a-drupal-site/security-in-drupal
