---
description: "Automatically update Next.js cached pages when content is created, updated, or deleted in Drupal. Supports path-based and tag-based revalidation."
drupal_version: "11.x"
topic: "drupal/next-drupal"
---

## On-Demand Revalidation

### When to Use

Automatically update Next.js cached pages when content is created, updated, or deleted in Drupal. Supports path-based and tag-based revalidation.

### Steps

**1. Configure Next.js site revalidation in Drupal**

Visit `/admin/config/services/next`, edit your site:
- On-demand Revalidation tab
- Revalidate URL: `http://localhost:3000/api/revalidate`
- Revalidate secret: Generate secure token
- Save

**2. Create revalidate API route**

```typescript
// app/api/revalidate/route.ts
import { revalidatePath, revalidateTag } from "next/cache"
import type { NextRequest } from "next/server"

async function handler(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const path = searchParams.get("path")
  const tags = searchParams.get("tags")
  const secret = searchParams.get("secret")

  if (secret !== process.env.DRUPAL_REVALIDATE_SECRET) {
    return new Response("Invalid secret.", { status: 401 })
  }

  if (!path && !tags) {
    return new Response("Missing path or tags.", { status: 400 })
  }

  try {
    path && revalidatePath(path)
    tags?.split(",").forEach((tag) => revalidateTag(tag))
    return new Response("Revalidated.")
  } catch (error) {
    return new Response((error as Error).message, { status: 500 })
  }
}

export { handler as GET, handler as POST }
```

**3. Configure environment variable**

```bash
DRUPAL_REVALIDATE_SECRET=your-revalidate-secret
```

**4. Configure entity types for revalidation**

Visit `/admin/config/services/next/entity-types`:

**For tag-based revalidation:**
- Click "Configure entity type" or edit existing
- On-demand Revalidation tab
- Plugin: Cache Tag
- Save

**For path-based revalidation:**
- Plugin: Path
- Check "Revalidate page"
- Optional: Add additional paths (e.g., `/blog` for article listings)
- Save

**5. Set revalidation strategy in Next.js**

**Path-based:**

```typescript
const node = await drupal.getResource(type, uuid, {
  cache: "force-cache",
  next: { revalidate: 3600 }, // Also set time-based fallback
})
```

**Tag-based (recommended):**

```typescript
const tag = `${path.entity.type}:${path.entity.id}`

const node = await drupal.getResource(type, uuid, {
  cache: "force-cache",
  next: { tags: [tag] },
})
```

### Decision Points

| Strategy | Pros | Cons |
|----------|------|------|
| **Path-based** | Simple, explicit | Must configure all paths, limited to URLs |
| **Tag-based** | Flexible, Drupal cache tag system | Requires tag extraction from translatePath |

### Common Mistakes

- **Not setting cache: 'force-cache'** — ISR doesn't work. WHY: Next.js needs to cache responses to revalidate them.
- **Exposing revalidate endpoint without secret** — Security hole. WHY: Anyone could trigger expensive rebuilds.
- **Using revalidate without tags for related content** — Stale related content. WHY: Updating article doesn't update taxonomy term pages.
- **Forgetting additional paths** — Listing pages not updated. WHY: Must explicitly configure `/blog` when article changes.

### See Also

- Building Pages
- Security Best Practices
- Performance Optimization
