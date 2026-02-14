---
description: "Apply these optimizations to reduce build times, improve page load speed, and minimize API requests."
drupal_version: "11.x"
topic: "drupal/next-drupal"
---

## Performance Optimization

### When to Use

Apply these optimizations to reduce build times, improve page load speed, and minimize API requests.

### Decision

| Optimization | Impact | Implementation |
|--------------|--------|----------------|
| **Sparse fieldsets** | 50-80% smaller responses | Use fields parameter |
| **Resource caching** | Faster builds, fewer requests | Cache menus/blocks during build |
| **ISR over SSG** | Faster builds for large sites | Use revalidate or tags |
| **Image optimization** | 60-80% smaller images | Next.js Image component |
| **Page limit override** | Fetch >50 resources | Configure next_jsonapi.size_max |
| **Includes vs separate requests** | Reduce HTTP requests | Use include parameter |

### Pattern

**Sparse fieldsets (only fetch needed fields):**

```typescript
const articles = await drupal.getResourceCollection("node--article", {
  params: {
    "fields[node--article]": "title,created,path",
    "fields[user--user]": "display_name",
  },
})
```

**Cache global resources during build:**

```typescript
import { PHASE_PRODUCTION_BUILD } from "next/constants"

const menu = await drupal.getMenu("main", {
  withCache: process.env.NEXT_PHASE === PHASE_PRODUCTION_BUILD,
  cacheKey: "menu:main",
})
```

**Use includes for relationships:**

```typescript
// GOOD: One request
const article = await drupal.getResource("node--article", uuid, {
  params: {
    include: "field_image,uid,field_tags",
  },
})

// BAD: Multiple requests
const article = await drupal.getResource("node--article", uuid)
const author = await drupal.getResource("user--user", article.uid.id)
const image = await drupal.getResource("media--image", article.field_image.id)
```

**ISR with fallback blocking for large sites:**

```typescript
export async function generateStaticParams() {
  // Only generate top 100 most visited pages
  const topPages = await getTopPages(100)
  return topPages.map(page => ({ slug: page.segments }))
}

export const dynamicParams = true // Enable fallback: blocking
export const revalidate = 3600 // Revalidate after 1 hour
```

**Image optimization:**

```typescript
import Image from "next/image"

<Image
  src={imageUrl}
  width={800}
  height={600}
  sizes="(max-width: 768px) 100vw, 800px"
  priority={isAboveFold} // Only for above-the-fold images
/>
```

**Page limit override:**

```yaml
# Drupal: sites/default/services.yml
parameters:
  next_jsonapi.size_max: 100
```

```typescript
// Next.js: Must use sparse fieldsets with path field
const pages = await drupal.getResourceCollection("node--page", {
  params: {
    "fields[node--page]": "path,title", // path field triggers override
    "page[limit]": 100,
  },
})
```

### Common Mistakes

- **Not using sparse fieldsets** — Fetches all fields. WHY: Body field can be massive, often unnecessary.
- **Pre-generating all paths for large sites** — Build timeout. WHY: Use fallback: 'blocking' or ISR instead.
- **Not caching menus and blocks** — Refetch on every page build. WHY: Global resources rarely change.
- **Using SSR when ISR is sufficient** — Slower page loads. WHY: ISR provides nearly same freshness with caching.
- **Loading images without dimensions** — Layout shift. WHY: Next.js needs width/height for optimization.
- **Including unused relationships** — Larger responses. WHY: Only include what you render.

### See Also

- Fetching Content
- Building Pages
- Media and Images
- drupal-jsonapi.md
