---
description: Every media source plugin must implement security measures to prevent common vulnerabilities.
---

# Security Best Practices

### When to Use

Every media source plugin must implement security measures to prevent common vulnerabilities.

### Decision

| Vulnerability | Prevention Strategy | Implementation |
|---------------|---------------------|----------------|
| **XSS (Cross-Site Scripting)** | Sanitize all metadata, validate URLs | Use `\Drupal\Component\Utility\UrlHelper::isValid()`, filter HTML |
| **SSRF (Server-Side Request Forgery)** | Validate remote URLs, whitelist domains | Check URL scheme (http/https only), validate domain |
| **Arbitrary file access** | Validate file URIs, check file ownership | Use file entity API, check file_managed table |
| **SQL Injection** | Use entity API, avoid raw queries | Use `$media->set()`, not db_query() |
| **Unvalidated redirects** | Validate oEmbed redirect URLs | Check redirect targets match provider |

### Pattern

Secure URL validation and fetching (8 lines):
```php
use Drupal\Component\Utility\UrlHelper;

protected function fetchFromApi(string $url): mixed {
  // 1. Validate URL format
  if (!UrlHelper::isValid($url, TRUE)) {
    $this->logger->warning('Invalid URL: @url', ['@url' => $url]);
    return NULL;
  }

  // 2. Whitelist allowed domains
  $allowed_domains = ['api.example.com', 'cdn.example.com'];
  $host = parse_url($url, PHP_URL_HOST);
  if (!in_array($host, $allowed_domains, TRUE)) {
    $this->logger->warning('Disallowed domain: @host', ['@host' => $host]);
    return NULL;
  }

  // 3. Use HTTPS only
  if (parse_url($url, PHP_URL_SCHEME) !== 'https') {
    $this->logger->warning('Non-HTTPS URL rejected: @url', ['@url' => $url]);
    return NULL;
  }

  try {
    $response = $this->httpClient->get($url, ['timeout' => 5]);
    return json_decode($response->getBody(), TRUE);
  } catch (\Exception $e) {
    $this->logger->error('API fetch failed: @msg', ['@msg' => $e->getMessage()]);
    return NULL;
  }
}
```

Sanitizing metadata for display (3 lines):
```php
use Drupal\Component\Utility\Xss;

public function getMetadata(MediaInterface $media, $attribute_name): mixed {
  $raw_value = $this->fetchFromApi($id, $attribute_name);
  return is_string($raw_value) ? Xss::filter($raw_value) : $raw_value;
}
```

### Common Mistakes

- Trusting user-supplied URLs → SSRF attacks, internal network scanning
- Not sanitizing API responses → XSS when metadata displayed
- Allowing HTTP URLs → Man-in-the-middle attacks, credential theft
- No timeout on HTTP requests → DoS via slow APIs, hanging requests
- Storing credentials in code → Exposed in version control, leaked in logs

**WHY these matter (the security reasoning):**
- **SSRF is critical**: Accepting arbitrary URLs allows attackers to scan internal networks, access cloud metadata endpoints (AWS EC2 metadata), or probe internal services
- **XSS in metadata**: Metadata displayed in HTML; unsanitized content allows JavaScript injection, session hijacking, and credential theft
- **HTTP vs HTTPS**: HTTP traffic is readable by network eavesdroppers; API keys and tokens transmitted in plain text
- **Timeouts prevent DoS**: Attackers can provide URLs to slow endpoints, tying up PHP workers and causing site-wide outages
- **Credential exposure**: Hardcoded credentials in code are visible in Git history, deployment logs, and error messages

### See Also

- Next: [Performance Optimization](index.md)
- Reference: https://www.getastra.com/blog/cms/drupal-security/drupal-security-guide/
- Reference: https://metadesignsolutions.com/drupal-security-best-practices-protecting-enterprise-websites-in-2026/
- Reference: https://www.drupal.org/docs/security-in-drupal