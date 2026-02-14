---
description: "Support multiple languages in your Next.js site backed by multilingual Drupal content."
drupal_version: "11.x"
topic: "drupal/next-drupal"
---

## Multilingual Support

### When to Use

Support multiple languages in your Next.js site backed by multilingual Drupal content.

### Steps

**1. Apply Decoupled Router patch**

See Drupal Setup section for patch details. Required for language resolution.

**2. Configure locales in Next.js**

```typescript
// next.config.js
module.exports = {
  i18n: {
    locales: ['en', 'es', 'fr'],
    defaultLocale: 'en',
  },
}
```

**3. Use locale parameter when fetching**

```typescript
const article = await drupal.getResource(
  "node--article",
  uuid,
  {
    locale: "es",
    defaultLocale: "en",
  }
)
```

**4. Configure path aliases per language**

In Drupal, configure path patterns for each language at `/admin/config/search/path/patterns`.

**5. Translate path for dynamic routes**

```typescript
// app/[...slug]/page.tsx
export default async function Page({ params }) {
  const path = await drupal.translatePath(params.slug, {
    locale: params.locale,
  })

  const node = await drupal.getResource(
    path.jsonapi.resourceName,
    path.entity.uuid,
    {
      locale: params.locale,
      defaultLocale: "en",
    }
  )
}
```

### Decision Points

| Decision | When | Impact |
|----------|------|--------|
| Path prefix strategy | Setup | `/es/about` vs `/about?lang=es` |
| Language fallback | Content gaps | Show default language vs 404 |
| Translation workflow | Content strategy | Sync vs independent translation |

### Common Mistakes

- **Not applying Decoupled Router patch** — Language resolution fails. WHY: Drupal can't resolve paths in non-default languages.
- **Forgetting locale in translatePath** — Always returns default language. WHY: Drupal needs explicit locale for routing.
- **Inconsistent locale parameter** — Mixed language content. WHY: Must pass locale to all drupal.getResource calls.
- **Missing path aliases per language** — 404 errors. WHY: Each language needs its own path configuration.

### See Also

- Drupal Setup
- Building Pages
- Troubleshooting
