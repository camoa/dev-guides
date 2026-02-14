---
description: "Authentication is required for draft mode, creating/updating content, and accessing unpublished resources. Choose the pattern based on your security requirements and Drupal configuration."
drupal_version: "11.x"
topic: "drupal/next-drupal"
---

## Authentication Patterns

### When to Use

Authentication is required for draft mode, creating/updating content, and accessing unpublished resources. Choose the pattern based on your security requirements and Drupal configuration.

### Decision

| Pattern | Use Case | Drupal Requirements | Security Level |
|---------|----------|---------------------|----------------|
| **OAuth (Bearer)** | Draft mode, authenticated API requests | simple_oauth module | High (encrypted tokens) |
| **Basic Auth** | Development only | basic_auth core module | Low (base64 encoded) |
| **Access Token** | NextAuth.js integration | OAuth consumer | High (delegated) |
| **Callback** | Custom auth logic | Your implementation | Varies |

### Pattern

**OAuth (Bearer) - Recommended:**

```typescript
// Drupal: Enable simple_oauth, create OAuth consumer
export const drupal = new NextDrupal(baseUrl, {
  auth: {
    clientId: process.env.DRUPAL_CLIENT_ID,
    clientSecret: process.env.DRUPAL_CLIENT_SECRET,
    url: "/oauth/token", // Optional, default URL
  },
})
```

**Basic Auth - Development Only:**

```typescript
// Drupal: Enable basic_auth module
export const drupal = new NextDrupal(baseUrl, {
  auth: {
    username: process.env.DRUPAL_USERNAME,
    password: process.env.DRUPAL_PASSWORD,
  },
})
```

**Access Token:**

```typescript
// Use with NextAuth.js or direct token
export const drupal = new NextDrupal(baseUrl, {
  auth: {
    access_token: "ECYM594IlARGc3S8...",
    token_type: "Bearer",
    expires_in: 3600,
  },
})
```

**Callback:**

```typescript
export const drupal = new NextDrupal(baseUrl, {
  auth: async () => {
    // Custom logic to fetch token
    return `Bearer ${token}`
  },
})
```

### Common Mistakes

- **Using Basic Auth in production** — Credentials sent in plain base64. WHY: Not secure, use OAuth instead.
- **Hardcoding OAuth secrets** — Exposed in version control. WHY: Use environment variables only.
- **Not setting OAuth scope permissions** — Preview access denied. WHY: Scope must have "Bypass content access control" permission.
- **Forgetting to generate OAuth encryption keys** — Token generation fails. WHY: simple_oauth requires public/private keypair.

### See Also

- Draft Mode
- Security Best Practices
- Drupal Setup
