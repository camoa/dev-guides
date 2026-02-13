---
description: Sanitize input, check access, validate API responses, and secure credentials in ECA plugins
drupal_version: "11.x"
---

# Security Best Practices

## When to Use

> Apply security patterns to all plugins that handle user input, external data, API credentials, or entity access. Security is mandatory, not optional.

## Decision

| Security Risk | Mitigation | Apply When |
|---------------|------------|------------|
| XSS injection | `Html::escape()`, `Xss::filter()` | Displaying user input |
| SQL injection | Entity API, query builders | Database access |
| CSRF attacks | Form API tokens | Form submissions |
| API credential exposure | Key module, environment variables | Storing API keys |
| Unauthorized access | Permission checks | Entity operations |
| Code injection | Input validation, no `eval()` | Processing user code/config |

## Pattern

```php
use Drupal\Component\Utility\Html;
use Drupal\Component\Utility\Xss;

class MySecureAction extends ConfigurableActionBase {

  public function execute(): void {
    // SECURITY: Validate and sanitize all user input
    $user_input = $this->tokenService->getOrReplace($this->configuration['input']);

    // Filter XSS for display
    $safe_input = Xss::filter($user_input);

    // Escape for HTML output
    $escaped = Html::escape($user_input);

    // SECURITY: Check entity access before operations
    $entity = $this->loadEntity();
    if (!$entity->access('update', $this->currentUser)) {
      $this->logger->warning('Access denied for entity @id', ['@id' => $entity->id()]);
      return;
    }

    // SECURITY: Use entity API, never raw SQL
    // Bad: db_query("SELECT * FROM node WHERE title = '$user_input'")
    // Good:
    $query = $this->entityTypeManager->getStorage('node')->getQuery()
      ->accessCheck(TRUE)  // CRITICAL: Always add access check
      ->condition('title', $user_input)
      ->range(0, 10);
    $ids = $query->execute();

    // SECURITY: Validate external API responses
    try {
      $response = $this->httpClient->request('GET', $url, [
        'timeout' => 10,  // Prevent hanging
        'verify' => TRUE, // Verify SSL certificates
      ]);

      $data = json_decode($response->getBody()->getContents(), TRUE);

      // Validate response structure
      if (!isset($data['expected_field'])) {
        throw new \Exception('Invalid API response structure');
      }

    } catch (\Exception $e) {
      $this->logger->error('API call failed: @error', ['@error' => $e->getMessage()]);
      // Don't expose error details to user
      return;
    }
  }

  /**
   * SECURITY: Never store API keys in code.
   */
  protected function getApiKey(): string {
    // Good: Use key module or environment variables
    return $this->keyRepository->getKey('my_api_key')->getKeyValue();

    // Bad: Hardcoded key
    // return 'sk-1234567890abcdef';
  }

  /**
   * SECURITY: Rate limit expensive operations.
   */
  protected function checkRateLimit(): bool {
    $key = 'rate_limit:' . $this->currentUser->id();
    $count = $this->state->get($key, 0);

    if ($count >= 100) {  // Max 100 calls per hour
      $this->logger->warning('Rate limit exceeded for user @uid', [
        '@uid' => $this->currentUser->id()
      ]);
      return FALSE;
    }

    $this->state->set($key, $count + 1);
    return TRUE;
  }
}
```

## Common Mistakes

- **Wrong**: Trusting user input → **Right**: XSS, SQL injection vulnerabilities
- **Wrong**: Missing access checks on queries → **Right**: Data leaks
- **Wrong**: Hardcoding API credentials → **Right**: Credentials exposed in version control
- **Wrong**: Not validating external data → **Right**: Malicious payloads processed
- **Wrong**: Using `eval()` or `unserialize()` on user data → **Right**: Remote code execution
- **Wrong**: Missing rate limiting → **Right**: DoS attacks possible
- **Wrong**: Exposing detailed errors to users → **Right**: Information disclosure
- **Wrong**: Not using HTTPS for API calls → **Right**: Man-in-the-middle attacks

## See Also

- [Access Control Patterns](access-control-patterns.md) for validation
- [Advanced Action Patterns](advanced-action-patterns.md) for API security
- [Performance Patterns](performance-patterns.md) for rate limiting

**References:**
- OWASP: https://owasp.org/www-project-top-ten/
- Drupal Security: https://www.drupal.org/security
