---
description: "Support multiple languages in your Next.js site backed by multilingual Drupal content."
tldr: "Support multiple languages in your Next.js site backed by multilingual Drupal content."
drupal_version: "11.x"
topic: "drupal/next-drupal"
---

## Multilingual Support

### When to Use

Support multiple languages in your Next.js site backed by multilingual Drupal content.

### Steps

**1. Apply Decoupled Router patch**

See Drupal Setup section for patch details. Required for language resolution.

**2. Configure locales (App Router)**

The Pages Router `i18n` key in `next.config.js` does **not** work with the App Router — it is silently ignored. Instead, define your locales in a shared config and route localized pages through a `[lang]` dynamic segment.

```typescript
// lib/i18n.ts
export const locales = ["en", "es", "fr"] as const
export const defaultLocale = "en"
export type Locale = (typeof locales)[number]
```

Place localized routes under an `app/[lang]/` segment (e.g. `app/[lang]/[...slug]/page.tsx`). Optionally add a `middleware.ts` that redirects `/` to `/${defaultLocale}` and negotiates the visitor's preferred language from the `Accept-Language` header.

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
// app/[lang]/[...slug]/page.tsx
import { defaultLocale } from "@/lib/i18n"

// `params` is a Promise in Next.js 15+ and includes the [lang] segment.
export default async function Page({
  params,
}: {
  params: Promise<{ lang: string; slug: string[] }>
}) {
  const { lang, slug } = await params

  const path = await drupal.translatePath(`/${slug.join("/")}`, {
    locale: lang,
    defaultLocale,
  })

  const node = await drupal.getResource(
    path.jsonapi.resourceName,
    path.entity.uuid,
    {
      locale: lang,
      defaultLocale,
    }
  )

  return <article>{node.title}</article>
}
```

### Decision Points

| Decision | When | Impact |
|----------|------|--------|
| Path prefix strategy | Setup | `/es/about` vs `/about?lang=es` |
| Language fallback | Content gaps | Show default language vs 404 |
| Translation workflow | Content strategy | Sync vs independent translation |

### Common Mistakes

- **Using the `next.config.js` `i18n` key with App Router** — It is silently ignored; you get no localized routing. WHY: `i18n` config is a Pages Router feature. Use a `[lang]` route segment instead.
- **Not applying Decoupled Router patch** — Language resolution fails. WHY: Drupal can't resolve paths in non-default languages.
- **Forgetting locale in translatePath** — Always returns default language. WHY: Drupal needs explicit locale for routing.
- **Inconsistent locale parameter** — Mixed language content. WHY: Must pass locale to all drupal.getResource calls.
- **Missing path aliases per language** — 404 errors. WHY: Each language needs its own path configuration.

### See Also

- Drupal Setup
- Building Pages
- Troubleshooting
