---
description: "Development, troubleshooting, and quality assurance of JSON:API implementations."
drupal_version: "11.x"
topic: "drupal/jsonapi"
---

## Testing & Debugging

### When to Use

Development, troubleshooting, and quality assurance of JSON:API implementations.

### Steps

**1. Enable verbose errors (development only):**
```php
// settings.php
$config['system.logging']['error_level'] = 'verbose';
```

**2. Check resource discovery:**
```bash
# List all available resources
curl -X GET https://example.com/jsonapi | json_pp
```

**3. Test with curl:**
```bash
# Verbose output shows headers and response
curl -v https://example.com/jsonapi/node/article

# Pretty print JSON
curl https://example.com/jsonapi/node/article | json_pp

# Save response to file
curl https://example.com/jsonapi/node/article -o response.json

# Test authentication
curl -u username:password https://example.com/jsonapi/node/article
```

**4. Validate responses:**
- Use JSON:API validator: https://jsonapi-validator.herokuapp.com/
- Paste response JSON to check spec compliance

**5. Debug normalization (development only):**
```bash
# Enable debug mode (if available)
GET /jsonapi/node/article?_normalization_debug=1
```

**6. Check Drupal logs:**
```bash
drush watchdog:show --type=jsonapi
```

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| 403 Forbidden | No permission | Check user permissions, entity access |
| 404 Not Found | Wrong UUID or resource disabled | Verify UUID, check JSON:API Extras config |
| 422 Unprocessable | Validation failed | Check `errors` array for field issues |
| Empty response | No matching results | Verify filter syntax and values |
| CORS error | Cross-origin blocked | Configure CORS in `services.yml` |
| Wrong MIME type | Missing Accept header | Add `Accept: application/vnd.api+json` |

### Testing Tools

**Postman collection:**
```json
{
  "info": { "name": "Drupal JSON:API Tests" },
  "item": [{
    "name": "Get Articles",
    "request": {
      "method": "GET",
      "header": [{"key": "Accept", "value": "application/vnd.api+json"}],
      "url": "{{base_url}}/jsonapi/node/article"
    }
  }]
}
```

**PHPUnit test example:**
```php
namespace Drupal\Tests\mymodule\Functional;

use Drupal\Tests\jsonapi\Functional\JsonApiFunctionalTestBase;

class ArticleApiTest extends JsonApiFunctionalTestBase {

  public function testGetCollection() {
    $url = Url::fromRoute('jsonapi.node--article.collection');
    $request_options = [
      RequestOptions::HEADERS => ['Accept' => 'application/vnd.api+json'],
    ];
    $response = $this->request('GET', $url, $request_options);
    $this->assertSame(200, $response->getStatusCode());

    $data = Json::decode((string) $response->getBody());
    $this->assertArrayHasKey('data', $data);
  }
}
```

### Debugging Techniques

**Check cache:**
```bash
# Clear cache if changes not appearing
drush cache:rebuild
```

**Inspect query parameters:**
```javascript
// Log constructed URL before fetching
const url = `/jsonapi/node/article?filter[status]=1&include=uid`;
console.log('Fetching:', url);
fetch(url).then(/* ... */);
```

**Check response headers:**
```bash
curl -I https://example.com/jsonapi/node/article

# Look for:
# Content-Type: application/vnd.api+json
# Cache-Control: max-age=...
# X-Drupal-Cache: HIT/MISS
```

**Enable Drupal debug:**
```php
// settings.local.php
$config['system.performance']['css']['preprocess'] = FALSE;
$config['system.performance']['js']['preprocess'] = FALSE;
$settings['cache']['bins']['render'] = 'cache.backend.null';
$settings['cache']['bins']['dynamic_page_cache'] = 'cache.backend.null';
$settings['cache']['bins']['page'] = 'cache.backend.null';
```

### Common Mistakes

**Testing with cached responses:** Not realizing response is cached from previous request. WHY: Drupal caches aggressively. Clear cache or disable caching during development.

**Not checking actual HTTP status codes:** Assuming 200 OK without verifying. WHY: Error responses often return 200 with error payload in some clients. Always check `response.status`.

**Ignoring error response details:** Only looking at status code, not error array. WHY: JSON:API error responses include detailed field-level errors. Check `errors[].detail` and `errors[].source.pointer`.

**Testing as admin user only:** Permissions issues only appear for non-admin. WHY: UID 1 bypasses access checks. Test as authenticated and anonymous users.

**Not validating against JSON:API spec:** Custom normalizers might break spec compliance. WHY: Spec violations cause client library failures. Use validator tool regularly.

### See Also
- [Core Architecture](core-architecture.md)
- [Security Best Practices](security-best-practices.md)
- [Performance Optimization](performance-optimization.md)
- JSON:API Specification: https://jsonapi.org/
