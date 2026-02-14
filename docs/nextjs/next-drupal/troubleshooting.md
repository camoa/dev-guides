---
description: "Diagnose and resolve common issues when integrating Next.js with Drupal."
drupal_version: "11.x"
topic: "drupal/next-drupal"
---

## Troubleshooting

### When to Use

Diagnose and resolve common issues when integrating Next.js with Drupal.

### Items

#### CORS Errors

**Symptoms:**
- "Access to fetch at ... from origin ... has been blocked by CORS policy"
- Network errors in browser console

**Solution:**

Configure CORS in Drupal `sites/default/services.yml`:

```yaml
cors:
  enabled: true
  allowedOrigins:
    - 'http://localhost:3000'
    - 'https://your-nextjs-site.com'
  allowedMethods:
    - GET
    - POST
    - PATCH
    - DELETE
  allowedHeaders:
    - '*'
```

Clear Drupal cache: `drush cr`

**Gotchas:**
- Must include both dev and production URLs
- Wildcard `*` not recommended for allowedOrigins in production

#### Authentication Failures (401/403)

**Symptoms:**
- 401 Unauthorized errors
- 403 Forbidden on preview/draft requests
- Token invalid errors

**Solution:**

1. Verify OAuth credentials match:

```bash
# Check .env.local matches Drupal OAuth consumer
DRUPAL_CLIENT_ID=exact-uuid-from-drupal
DRUPAL_CLIENT_SECRET=exact-secret-from-drupal
```

2. Check OAuth scope permissions:
- Visit `/admin/people/permissions`
- Scope role must have "Bypass content access control"

3. Verify OAuth token URL:

```typescript
// Default is /oauth/token
// If using different URL:
auth: {
  clientId,
  clientSecret,
  url: "/custom/oauth/path",
}
```

4. Check token expiration (tokens expire, client should auto-refresh)

**Gotchas:**
- OAuth consumer must have "Client Credentials" grant type
- Encryption keys must be generated at `/admin/config/people/simple_oauth`

#### Path Resolution Issues

**Symptoms:**
- 404 errors for valid Drupal content
- "Resource not found" errors
- translatePath returns null

**Solution:**

1. Verify path aliases configured:
- Visit `/admin/config/search/path/patterns`
- Each content type needs a pattern

2. Check Decoupled Router enabled:
- Visit `/admin/modules`
- Ensure "Decoupled Router" is enabled

3. For multilingual sites, apply patch:
- See Multilingual Support section

4. Debug with translatePath:

```typescript
const path = await drupal.translatePath("/blog/my-article")
console.log(path) // Should return entity info, not null
```

**Gotchas:**
- Path must start with `/`
- Multilingual sites need patch and locale parameter

#### 50 Resource Limit

**Symptoms:**
- getResourceCollection returns max 50 items
- Missing pages in generateStaticParams

**Solution:**

1. Configure Drupal services.yml:

```yaml
parameters:
  next_jsonapi.size_max: 100
```

2. Use sparse fieldsets with `path` field:

```typescript
const pages = await drupal.getResourceCollection("node--page", {
  params: {
    "fields[node--page]": "path,title,nid", // path field required
    "page[limit]": 100,
  },
})
```

3. Or use pagination:

```typescript
const page1 = await drupal.getResourceCollection("node--page", {
  params: { "page[limit]": 50, "page[offset]": 0 },
})
const page2 = await drupal.getResourceCollection("node--page", {
  params: { "page[limit]": 50, "page[offset]": 50 },
})
```

**Gotchas:**
- Override only works with `path` as first field
- Clear Drupal cache after services.yml changes

#### Draft Mode Not Working

**Symptoms:**
- Preview shows published content, not draft
- 403 errors in iframe preview

**Solution:**

1. Verify OAuth authentication configured (see Authentication Failures)

2. Check preview secret matches:

```bash
# .env.local
DRUPAL_PREVIEW_SECRET=exact-match-from-drupal

# Drupal: /admin/config/services/next (edit site)
# Secret key must match exactly
```

3. Verify draft URL configured:
- Drupal Next.js site: `http://localhost:3000/api/draft`
- Must be accessible from Drupal server

4. Check entity type configuration:
- `/admin/config/services/next/entity-types`
- Content type must have Draft Mode configured

**Gotchas:**
- Requires authenticated requests (OAuth)
- Preview secret different from revalidate secret

#### On-Demand Revalidation Not Triggering

**Symptoms:**
- Drupal content updates don't appear in Next.js
- No requests to revalidate endpoint

**Solution:**

1. Verify revalidate URL reachable:
- Test: `curl http://localhost:3000/api/revalidate?secret=YOUR_SECRET&path=/blog/test`
- Should return "Revalidated"

2. Check secret matches:

```bash
# .env.local
DRUPAL_REVALIDATE_SECRET=match-drupal

# Drupal: /admin/config/services/next (edit site)
# Revalidate secret must match
```

3. Verify entity type configuration:
- `/admin/config/services/next/entity-types`
- Revalidator plugin must be configured (Path or Cache Tag)

4. Check Drupal logs:
- `/admin/reports/dblog`
- Look for revalidation errors

**Gotchas:**
- Revalidate route must handle both GET and POST
- Must use `cache: 'force-cache'` in Next.js

#### Build Timeouts / Memory Issues

**Symptoms:**
- Builds exceed time limits
- Out of memory errors
- Vercel/Netlify build failures

**Solution:**

1. Use ISR instead of full SSG:

```typescript
export async function generateStaticParams() {
  // Generate only top 100 pages
  const topPages = await getTopPages(100)
  return topPages
}

export const dynamicParams = true // Enable on-demand generation
```

2. Implement caching for global resources

3. Use sparse fieldsets to reduce memory:

```typescript
params: {
  "fields[node--article]": "title,path,nid",
}
```

4. Increase build timeout (Vercel):

```json
// vercel.json
{
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next",
      "config": {
        "maxDuration": 300
      }
    }
  ]
}
```

**Gotchas:**
- Sites with >1000 pages should use ISR with fallback: 'blocking'
- Build timeouts vary by platform (Vercel: 300s, Netlify: 900s)

### Common Mistakes

- **Not checking Drupal logs** — Errors logged server-side. WHY: Next.js only sees HTTP status codes.
- **Testing with cache enabled** — Stale data confuses debugging. WHY: Disable cache during troubleshooting.
- **Mixing development and production URLs** — Environment mismatch. WHY: Ensure .env.local matches current environment.

### See Also

- Security Best Practices
- Performance Optimization
- Drupal Setup
