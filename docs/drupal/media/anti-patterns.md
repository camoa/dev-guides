---
description: Common mistakes and anti-patterns to avoid in media source plugins
drupal_version: "11.x"
---

# Anti-Patterns

## When to Use

> Use this guide to avoid common mistakes that lead to maintenance problems, security issues, or performance degradation.

## Decision

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| `\Drupal::service()` in plugins | Breaks testability, static dependency | Inject via constructor |
| No default_name implementation | Media items show "Unsaved media" | Always implement default_name |
| Skipping caching | API rate limits, slow pages | Cache with tags |
| Weak URL validation | SSRF attacks, security breach | Whitelist domains, validate scheme |
| Synchronous thumbnail downloads | Page timeouts, poor UX | Queue-based generation |

## Pattern

**WRONG - Static service calls:**
```php
class CustomApi extends MediaSourceBase {
  protected function fetchFromApi($id) {
    $client = \Drupal::httpClient(); // ❌ Static dependency
    return $client->get("https://api.example.com/{$id}");
  }
}
```

**RIGHT - Dependency injection:**
```php
class CustomApi extends MediaSourceBase {
  protected ClientInterface $httpClient;

  public function __construct(..., ClientInterface $http_client) {
    parent::__construct(...);
    $this->httpClient = $http_client; // ✅ Injected dependency
  }

  protected function fetchFromApi($id) {
    return $this->httpClient->get("https://api.example.com/{$id}");
  }
}
```

**WRONG - No caching:**
```php
public function getMetadata(MediaInterface $media, $attribute_name): mixed {
  $data = $this->httpClient->get($url)->getBody(); // ❌ Every call hits API
  return json_decode($data, TRUE)[$attribute_name];
}
```

**RIGHT - Cached responses:**
```php
public function getMetadata(MediaInterface $media, $attribute_name): mixed {
  $cache_key = "module:meta:{$id}:{$attribute_name}";
  if ($cached = $this->cache->get($cache_key)) {
    return $cached->data; // ✅ Cached result
  }

  $data = $this->httpClient->get($url)->getBody();
  $value = json_decode($data, TRUE)[$attribute_name];
  $this->cache->set($cache_key, $value, time() + 3600);
  return $value;
}
```

**WRONG - Weak validation:**
```php
if (strpos($url, 'example.com') !== FALSE) { // ❌ Accepts http://evil.com/example.com
  return $this->httpClient->get($url);
}
```

**RIGHT - Strong validation:**
```php
if (!UrlHelper::isValid($url, TRUE)) return NULL;
$host = parse_url($url, PHP_URL_HOST);
if ($host !== 'api.example.com') return NULL; // ✅ Exact domain match
if (parse_url($url, PHP_URL_SCHEME) !== 'https') return NULL; // ✅ HTTPS only
```

## Common Mistakes

- **Wrong**: Not implementing default_name → **Right**: Return title/name for automatic naming
- **Wrong**: No error handling on HTTP requests → **Right**: Catch exceptions, return NULL
- **Wrong**: Caching without tags → **Right**: Tag with media ID for targeted invalidation
- **Wrong**: Hardcoding API credentials → **Right**: Use config or key module
- **Wrong**: Not calling parent methods → **Right**: Call parent for core functionality

## See Also

- Security: [Security Best Practices](security-best-practices.md)
- Performance: [Performance Optimization](performance-optimization.md)
- Reference: All previous sections for correct patterns
