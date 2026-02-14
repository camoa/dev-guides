---
description: "Implement search functionality using Drupal Search API exposed via JSON:API."
drupal_version: "11.x"
topic: "drupal/next-drupal"
---

## Search Integration

### When to Use

Implement search functionality using Drupal Search API exposed via JSON:API.

### Steps

**1. Install required modules**

```bash
composer require drupal/search_api drupal/jsonapi_search_api
# Optional for faceted search
composer require drupal/facets drupal/jsonapi_search_api_facets
```

Enable: Search API, Database Search, JSON:API Search API (and Facets modules if needed).

**2. Create search index in Drupal**

Visit `/admin/config/search/search-api`:
- Add Server (Database)
- Add Index (e.g., "content_index")
- Select datasources (Content, Users, etc.)
- Add fields to index (title, body, etc.)
- Configure processors
- Save and index content

**3. Create facets (optional)**

Visit `/admin/config/search/facets`:
- Click "Add facet"
- Facet source: Select your search index
- Field: Select field to facet on
- Widget: JSON:API Search API
- Save

**4. Create search API route in Next.js**

```typescript
// app/api/search/[index]/route.ts
import { NextRequest, NextResponse } from "next/server"
import { drupal } from "@/lib/drupal"

export async function POST(
  request: NextRequest,
  { params }: { params: { index: string } }
) {
  try {
    const body = await request.json()

    const results = await drupal.getSearchIndex(params.index, {
      params: body.params,
      locale: body.locale,
      defaultLocale: body.defaultLocale,
    })

    return NextResponse.json(results)
  } catch (error) {
    return NextResponse.json(
      { error: (error as Error).message },
      { status: 400 }
    )
  }
}
```

**5. Query from frontend**

```typescript
// In a client component
const handleSearch = async (term: string) => {
  const response = await fetch("/api/search/content_index", {
    method: "POST",
    body: JSON.stringify({
      params: {
        filter: { title: term },
      },
      locale: router.locale,
      defaultLocale: router.defaultLocale,
    }),
  })

  const results = await response.json()
}
```

### Decision Points

| Decision | When | Impact |
|----------|------|--------|
| Index fields | Setup | Query performance vs flexibility |
| Facet configuration | Filtered search | User experience vs complexity |
| API route vs direct | Architecture | Security vs simplicity |

### Common Mistakes

- **Querying search index directly from client** — Exposes Drupal URL. WHY: Use API route to abstract backend.
- **Not passing locale to API route** — Incorrect language results. WHY: Search API needs locale context.
- **Missing rate limiting** — DoS vulnerability. WHY: Search is expensive, add rate limiting middleware.
- **Not indexing content** — Empty results. WHY: Must run indexing cron or manual index after setup.

### See Also

- Fetching Content
- Security Best Practices
- drupal-jsonapi.md
