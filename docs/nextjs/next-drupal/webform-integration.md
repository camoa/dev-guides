---
description: "Submit webforms from Next.js to Drupal using the Webform REST module. Supports client-side and server-side (API route) submission."
drupal_version: "11.x"
topic: "drupal/next-drupal"
---

## Webform Integration

### When to Use

Submit webforms from Next.js to Drupal using the Webform REST module. Supports client-side and server-side (API route) submission.

### Steps

**1. Install Webform REST module**

```bash
composer require drupal/webform_rest
```

Enable: Webform, Webform REST, REST UI

**2. Configure REST resource**

Visit `/admin/config/services/rest`:
- Enable "Webform Submit" resource
- Methods: POST
- Accepted request formats: json
- Authentication providers: cookie (or oauth2 if needed)
- Save

**3. Set permissions**

Visit `/admin/people/permissions`:
- Grant anonymous users: "Access POST on Webform Submit resource"

**4. Server-side submission (recommended)**

```typescript
// app/api/contact/route.ts
import { NextRequest, NextResponse } from "next/server"
import { drupal } from "@/lib/drupal"

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    const url = drupal.buildUrl("/webform_rest/submit")
    const result = await drupal.fetch(url.toString(), {
      method: "POST",
      body: JSON.stringify({
        webform_id: "contact",
        name: body.name,
        email: body.email,
        message: body.message,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    })

    if (!result.ok) {
      throw new Error("Submission failed")
    }

    return NextResponse.json({ success: true })
  } catch (error) {
    return NextResponse.json(
      { error: (error as Error).message },
      { status: 400 }
    )
  }
}
```

**5. Frontend form submission**

```typescript
const handleSubmit = async (event: FormEvent) => {
  event.preventDefault()

  const response = await fetch("/api/contact", {
    method: "POST",
    body: JSON.stringify({
      name: formData.name,
      email: formData.email,
      message: formData.message,
    }),
  })

  if (response.ok) {
    // Show success message
  }
}
```

**6. Client-side submission (not recommended)**

```typescript
// Exposes Drupal URL and webform_id
const response = await fetch(
  `${process.env.NEXT_PUBLIC_DRUPAL_BASE_URL}/webform_rest/submit`,
  {
    method: "POST",
    body: JSON.stringify({
      webform_id: "contact",
      name: formData.name,
      email: formData.email,
    }),
    headers: { "Content-Type": "application/json" },
  }
)
```

### Decision Points

| Approach | Pros | Cons |
|----------|------|------|
| **Server-side (API route)** | Hides Drupal URL, adds validation layer | Extra route to maintain |
| **Client-side** | Simpler, direct | Exposes Drupal URL and form IDs |

### Common Mistakes

- **Client-side submission in production** — Security exposure. WHY: Drupal URL and webform IDs are visible.
- **Missing CORS configuration** — Client-side submission fails. WHY: Drupal needs CORS headers for cross-origin requests.
- **Not validating server-side** — Accept invalid data. WHY: Client validation can be bypassed.
- **Hardcoding webform_id** — Brittle integration. WHY: Use environment variables or Drupal JSON:API to fetch form config.

### See Also

- Security Best Practices
- Fetching Content (for dynamic form fetching)
- Environment Variables
