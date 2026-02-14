---
description: Understanding Drupal's authentication providers including cookie-based auth, API keys, OAuth, and custom authentication implementation.
---

# Authentication System

## When to Use
Understanding how Drupal identifies users and when to implement custom authentication providers (OAuth, SAML, LDAP, API keys).

## Decision
| If you need... | Use... | Why |
|---|---|---|
| Standard cookie-based auth | Core user module | Built-in, secure, handles sessions |
| API authentication | HTTP Basic or custom provider | Stateless, suitable for REST/JSON API |
| OAuth/SAML/LDAP | Contrib modules | Proven implementations: `simple_oauth`, `simplesamlphp_auth`, `ldap` |
| Two-factor auth | TFA contrib module | Security layer on top of primary auth |
| Custom auth mechanism | AuthenticationProviderInterface | Full control, integrate with external systems |

## Pattern
Custom authentication provider:
```php
// src/Authentication/Provider/ApiKeyAuth.php
namespace Drupal\mymodule\Authentication\Provider;

use Drupal\Core\Authentication\AuthenticationProviderInterface;
use Symfony\Component\HttpFoundation\Request;

class ApiKeyAuth implements AuthenticationProviderInterface {

  public function applies(Request $request) {
    // Only apply if X-API-Key header present
    return $request->headers->has('X-API-Key');
  }

  public function authenticate(Request $request) {
    $api_key = $request->headers->get('X-API-Key');

    // Validate API key and load user
    $uid = $this->validateApiKey($api_key);
    if ($uid) {
      return User::load($uid);
    }

    return NULL;  // Authentication failed
  }

  protected function validateApiKey($key) {
    // Query for user with matching API key
    $query = \Drupal::entityQuery('user')
      ->accessCheck(FALSE)
      ->condition('field_api_key', $key)
      ->condition('status', 1)
      ->range(0, 1);
    $uids = $query->execute();
    return $uids ? reset($uids) : NULL;
  }
}
```

Register in `mymodule.services.yml`:
```yaml
services:
  mymodule.authentication.api_key:
    class: Drupal\mymodule\Authentication\Provider\ApiKeyAuth
    tags:
      - { name: authentication_provider, priority: 100 }
```
Reference: `/core/lib/Drupal/Core/Authentication/AuthenticationManager.php`

## Common Mistakes
- Implementing custom auth when contrib exists -- Use `simple_oauth` for OAuth, etc.
- Not using flood control -- Brute force attacks succeed
- Storing passwords in plain text -- **CRITICAL**: Use `\Drupal::service('password')->hash()`
- Weak password requirements -- Enforce complexity via `password_policy` module
- Not invalidating sessions on logout -- Session fixation vulnerability
- Authentication without authorization -- Auth identifies user; still need access checks

## See Also
- Reference: `/core/modules/user/src/Entity/User.php`
- [Session Management](session-management.md) for session security
- Reference: https://www.drupal.org/docs/8/modules/simple-oauth
