---
description: "Build statically generated (SSG), server-rendered (SSR), or incrementally static regenerated (ISR) pages from Drupal content. App Router uses native fetch with Next.js cache options."
drupal_version: "11.x"
topic: "drupal/next-drupal"
---

## Building Pages

### When to Use

Build statically generated (SSG), server-rendered (SSR), or incrementally static regenerated (ISR) pages from Drupal content. App Router uses native fetch with Next.js cache options.

### Decision

| Rendering | Use Case | Revalidation | App Router Function |
|-----------|----------|--------------|---------------------|
| **SSG** | Marketing pages, blogs | Time-based or on-demand | generateStaticParams |
| **SSR** | Personalized content, real-time data | Every request | Server Component (default) |
| **ISR** | Frequently updated content | On-demand or time-based | generateStaticParams + revalidate |

### Pattern

**Static Generation with Dynamic Routes:**

```typescript
// app/[...slug]/page.tsx
export async function generateStaticParams() {
  const resources = await drupal.getResourceCollectionPathSegments([
    "node--page",
    "node--article",
  ])
  return resources.map((resource) => ({ slug: resource.segments }))
}

export default async function Page({ params }) {
  const path = await drupal.translatePath(params.slug)
  const type = path.jsonapi.resourceName
  const uuid = path.entity.uuid

  const node = await drupal.getResource(type, uuid, {
    params: {
      include: type === "node--article" ? "field_image,uid" : "",
    },
    next: { revalidate: 3600 }, // ISR: revalidate every hour
  })

  return <article><h1>{node.title}</h1></article>
}
```

**Tag-based Revalidation:**

```typescript
const tag = `${path.entity.type}:${path.entity.id}`

const node = await drupal.getResource(type, uuid, {
  cache: "force-cache",
  next: { tags: [tag] }, // Revalidate when Drupal sends tag
})
```

**Server-side Rendering:**

```typescript
// Omit generateStaticParams for SSR
export default async function Page({ params }) {
  const node = await drupal.getResourceByPath(`/${params.slug.join("/")}`, {
    cache: "no-store", // No caching, always fresh
  })

  return <article>{node.title}</article>
}
```

### Common Mistakes

- **Pre-generating all paths for large sites** — Build times exceed limits. WHY: Use `fallback: 'blocking'` or SSR for 1000+ pages.
- **Mixing revalidate and tags** — Conflicting strategies. WHY: Choose one: time-based (revalidate) or tag-based (tags).
- **Not configuring revalidate API route** — On-demand ISR fails. WHY: Requires `/api/revalidate` endpoint.
- **Using cache: 'no-store' for static content** — Defeats purpose of ISR. WHY: Use 'force-cache' with revalidation instead.

### See Also

- On-Demand Revalidation
- Fetching Content
- Performance Optimization
