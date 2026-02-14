---
description: "Follow these practices for all Next.js + Drupal implementations to prevent common security vulnerabilities."
drupal_version: "11.x"
topic: "drupal/next-drupal"
---

## Security Best Practices

### When to Use

Follow these practices for all Next.js + Drupal implementations to prevent common security vulnerabilities.

### Decision

| Practice | Why | Implementation |
|----------|-----|----------------|
| **Use OAuth over Basic Auth** | Basic auth is base64 encoded, not encrypted | simple_oauth module with client credentials |
| **Validate secrets in API routes** | Prevent unauthorized access | Check against environment variables |
| **Never commit secrets** | Prevent credential leaks | Use .env.local, add to .gitignore |
| **Separate preview and revalidate secrets** | Principle of least privilege | Different secrets for different endpoints |
| **Configure CORS properly** | Prevent unauthorized API access | Drupal services.yml configuration |
| **Use HTTPS in production** | Encrypt data in transit | SSL certificates, secure cookies |
| **Implement rate limiting** | Prevent DoS attacks | Middleware on search/form endpoints |
| **Validate input server-side** | Prevent injection attacks | Never trust client input |

### Pattern

**Secure API route with secret validation:**

```typescript
// app/api/revalidate/route.ts
export async function POST(request: NextRequest) {
  const secret = request.nextUrl.searchParams.get("secret")

  // Always validate secret first
  if (secret !== process.env.DRUPAL_REVALIDATE_SECRET) {
    return new Response("Unauthorized", { status: 401 })
  }

  // Process request
}
```

**OAuth scope with minimal permissions:**

```php
// Drupal: Create role with only necessary permissions
// For preview: "Bypass content access control", "Issue subrequests"
// Avoid: "Administer site", "Access administration pages"
```

**CORS configuration in Drupal:**

```yaml
# sites/default/services.yml
cors:
  enabled: true
  allowedOrigins:
    - 'https://your-nextjs-site.com'
  allowedMethods:
    - GET
    - POST
  allowedHeaders:
    - '*'
```

**Environment variable security:**

```bash
# .env.local (never commit)
DRUPAL_CLIENT_SECRET=secure-random-string
DRUPAL_REVALIDATE_SECRET=different-secure-string

# .env.example (commit template only)
DRUPAL_CLIENT_SECRET=
DRUPAL_REVALIDATE_SECRET=
```

### Common Mistakes

- **Using NEXT_PUBLIC_ prefix for secrets** — Exposed in client bundle. WHY: All NEXT_PUBLIC_ vars are bundled into JavaScript.
- **Same OAuth consumer for all environments** — Shared credentials. WHY: Separate dev/staging/prod consumers.
- **No rate limiting on public API routes** — DoS vulnerability. WHY: Search and form endpoints are expensive.
- **Basic auth in production** — Unencrypted credentials. WHY: Base64 is encoding, not encryption.
- **Broad OAuth scope permissions** — Privilege escalation. WHY: Scope should have minimal necessary permissions.
- **Ignoring JSON:API write permission** — Unauthorized writes. WHY: Disable write operations if not needed at `/admin/config/services/jsonapi`.

### See Also

- Authentication Patterns
- Environment Variables
- Webform Integration
- Search Integration
