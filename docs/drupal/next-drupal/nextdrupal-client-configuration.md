---
description: "Configure the NextDrupal client to customize API prefix, authentication, caching, deserialization, and other client behaviors."
drupal_version: "11.x"
topic: "drupal/next-drupal"
---

## NextDrupal Client Configuration

### When to Use

Configure the NextDrupal client to customize API prefix, authentication, caching, deserialization, and other client behaviors.

### Items

#### apiPrefix

**Description:** Custom JSON:API prefix (if using jsonapi_extras module).

**Props:**

| Property | Type | Default | Required |
|----------|------|---------|----------|
| apiPrefix | string | `/jsonapi` | No |

**Usage Example:**

```typescript
new NextDrupal(baseUrl, {
  apiPrefix: "/api",
})
```

**Gotchas:**
- Must match Drupal JSON:API Extras configuration
- Requires jsonapi_extras module enabled

#### frontPage

**Description:** Path for your front page (resolves to `/` in Next.js).

**Props:**

| Property | Type | Default | Required |
|----------|------|---------|----------|
| frontPage | string | `/home` | No |

**Usage Example:**

```typescript
new NextDrupal(baseUrl, {
  frontPage: "/front",
})
```

#### auth

**Description:** Default authentication configuration for all requests.

**Props:**

| Property | Type | Options | Required |
|----------|------|---------|----------|
| auth | object or function | Bearer, Basic, Callback, AccessToken | No |

**Usage Example:**

```typescript
new NextDrupal(baseUrl, {
  auth: {
    clientId: process.env.DRUPAL_CLIENT_ID,
    clientSecret: process.env.DRUPAL_CLIENT_SECRET,
  },
})
```

**Gotchas:**
- OAuth tokens are auto-refreshed
- See Authentication Patterns for full options

#### deserializer

**Description:** Custom JSON:API deserializer to transform response data structure.

**Props:**

| Property | Type | Default | Required |
|----------|------|---------|----------|
| deserializer | function | jsona | No |

**Usage Example:**

```typescript
import { Deserializer } from "jsonapi-serializer"

const customDeserializer = new Deserializer({
  keyForAttribute: "camelCase",
}).deserialize.bind(jsonDeserializer)

new NextDrupal(baseUrl, {
  deserializer: customDeserializer,
})
```

**Gotchas:**
- Must return same structure as default deserializer
- Pages Router uses `serializer` option instead

#### fetcher

**Description:** Custom fetch implementation for logging, proxying, or custom headers.

**Props:**

| Property | Type | Default | Required |
|----------|------|---------|----------|
| fetcher | function | fetch | No |

**Usage Example:**

```typescript
import crossFetch from "cross-fetch"

const customFetcher = (url, options) => {
  return crossFetch(url, {
    ...options,
    // Add custom agent, headers, etc.
  })
}

new NextDrupal(baseUrl, { fetcher: customFetcher })
```

#### cache

**Description:** Cache implementation for storing resources during builds.

**Props:**

| Property | Type | Interface | Required |
|----------|------|-----------|----------|
| cache | object | DataCache (set, get) | No |

**Usage Example:**

```typescript
import { DataCache } from "next-drupal"
import Redis from "ioredis"

const redis = new Redis(process.env.REDIS_URL)

const redisCache: DataCache = {
  async set(key, value) {
    return await redis.set(key, value)
  },
  async get(key) {
    return await redis.get(key)
  },
}

new NextDrupal(baseUrl, { cache: redisCache })
```

#### withAuth

**Description:** Enable authenticated requests by default for all client methods.

**Props:**

| Property | Type | Default | Required |
|----------|------|---------|----------|
| withAuth | boolean | false | No |

**Usage Example:**

```typescript
new NextDrupal(baseUrl, {
  auth: { clientId, clientSecret },
  withAuth: true, // All requests now authenticated
})
```

#### headers

**Description:** Custom default headers for all requests.

**Props:**

| Property | Type | Default | Required |
|----------|------|---------|----------|
| headers | object | JSON:API headers | No |

**Usage Example:**

```typescript
new NextDrupal(baseUrl, {
  headers: {
    "Content-Type": "application/json",
    "Custom-Header": "value",
  },
})
```

#### debug

**Description:** Enable built-in logging for debugging requests.

**Props:**

| Property | Type | Default | Required |
|----------|------|---------|----------|
| debug | boolean | false | No |

**Usage Example:**

```typescript
new NextDrupal(baseUrl, { debug: true })
```

### Common Mistakes

- **Not using cache for global data** — Refetches menus/blocks on every page. WHY: Performance waste during builds.
- **Overriding default headers incorrectly** — Breaks JSON:API format. WHY: Must include `application/vnd.api+json` headers.
- **Using custom fetcher without handling withAuth** — Authentication breaks. WHY: Custom fetcher must implement auth logic.

### See Also

- Authentication Patterns
- Performance Optimization
- drupal-jsonapi.md
