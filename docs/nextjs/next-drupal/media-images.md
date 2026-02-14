---
description: "Handle Drupal media entities, image fields, and inline images in body fields using Next.js Image component for optimization."
drupal_version: "11.x"
topic: "drupal/next-drupal"
---

## Media and Images

### When to Use

Handle Drupal media entities, image fields, and inline images in body fields using Next.js Image component for optimization.

### Decision

| Approach | Use Case | Implementation |
|----------|----------|----------------|
| **Media entity fields** | Structured image fields | Include relationship, use field_media_image |
| **Inline images in body** | WYSIWYG editor images | Parse HTML, replace with Image component |
| **File fields (deprecated)** | Legacy implementations | Use media entities instead |

### Pattern

**Media entity field:**

```typescript
const article = await drupal.getResource("node--article", uuid, {
  params: {
    include: "field_image.field_media_image",
  },
})

// In component
import Image from "next/image"

<Image
  src={`${process.env.NEXT_PUBLIC_DRUPAL_BASE_URL}${article.field_image.field_media_image.uri.url}`}
  alt={article.field_image.field_media_image.resourceIdObjMeta.alt || ""}
  width={article.field_image.field_media_image.resourceIdObjMeta.width}
  height={article.field_image.field_media_image.resourceIdObjMeta.height}
/>
```

**Inline images in body:**

```typescript
// components/body.tsx
import parse, { HTMLReactParserOptions, Element } from "html-react-parser"
import Image from "next/image"

const options: HTMLReactParserOptions = {
  replace: (domNode) => {
    if (domNode instanceof Element && domNode.name === "img") {
      const { src, alt, width, height } = domNode.attribs
      return (
        <Image
          src={`${process.env.NEXT_PUBLIC_DRUPAL_BASE_URL}${src}`}
          width={parseInt(width)}
          height={parseInt(height)}
          alt={alt}
        />
      )
    }
  },
}

export function Body({ value }: { value: string }) {
  return <>{parse(value, options)}</>
}
```

**Image derivatives (responsive images):**

```typescript
// Drupal image styles are accessible via JSON:API
const article = await drupal.getResource("node--article", uuid, {
  params: {
    include: "field_image.field_media_image",
  },
})

// Access image styles
const imageUrl = article.field_image.field_media_image.image_style_uri?.large
```

### Common Mistakes

- **Not including media relationships** — Image data missing. WHY: Media is a relationship, requires explicit include.
- **Missing alt text** — Accessibility violation. WHY: Always provide alt from resourceIdObjMeta.alt or fallback.
- **Not configuring NEXT_IMAGE_DOMAIN** — Image optimization fails. WHY: Next.js requires domain allowlist.
- **Inline images without width/height** — Layout shift. WHY: Next.js Image requires dimensions for optimization.

### See Also

- Fetching Content
- drupal-jsonapi.md (for includes syntax)
- Performance Optimization
