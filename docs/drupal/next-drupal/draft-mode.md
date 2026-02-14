---
description: "Enable content editors to preview unpublished content and revisions in an iframe within Drupal before publishing."
drupal_version: "11.x"
topic: "drupal/next-drupal"
---

## Draft Mode

### When to Use

Enable content editors to preview unpublished content and revisions in an iframe within Drupal before publishing.

### Steps

**1. Create OAuth consumer in Drupal**

Follow Authentication Patterns to create an OAuth consumer with:
- Scope: Role with "Bypass content access control" permission
- Grant type: Client Credentials

**2. Create Next.js site in Drupal**

Visit `/admin/config/services/next`:
- Label: Next.js
- Base URL: `http://localhost:3000`
- Draft URL: `http://localhost:3000/api/draft`
- Preview secret: Generate a secure token

**3. Create draft API route**

```typescript
// app/api/draft/route.ts
import { drupal } from "@/lib/drupal"
import { enableDraftMode } from "next-drupal/draft"
import type { NextRequest } from "next/server"

export async function GET(request: NextRequest) {
  return enableDraftMode(request, drupal)
}
```

**4. Create disable-draft API route**

```typescript
// app/api/disable-draft/route.ts
import { disableDraftMode } from "next-drupal/draft"
import type { NextRequest } from "next/server"

export async function GET(request: NextRequest) {
  return disableDraftMode()
}
```

**5. Configure environment variables**

```bash
DRUPAL_CLIENT_ID=your-oauth-client-id
DRUPAL_CLIENT_SECRET=your-oauth-secret
DRUPAL_PREVIEW_SECRET=your-preview-secret
```

**6. Update NextDrupal client for auth**

```typescript
export const drupal = new NextDrupal(baseUrl, {
  auth: {
    clientId: process.env.DRUPAL_CLIENT_ID,
    clientSecret: process.env.DRUPAL_CLIENT_SECRET,
  },
})
```

**7. Configure content types for preview**

Visit `/admin/config/services/next/entity-types`:
- Click "Configure entity type"
- Select content type (e.g., Article)
- Draft Mode tab: Select "Site selector" plugin
- Select your Next.js site
- Save

### Decision Points

| Decision | When | Impact |
|----------|------|--------|
| Secret generation | Setup | Use cryptographically secure random string |
| OAuth scope permissions | Setup | Must include "Bypass content access control" |
| Preview plugin | Per content type | Site selector vs custom resolver |

### Common Mistakes

- **Using same secret for preview and revalidation** — Security issue. WHY: Separate concerns, different access levels.
- **Not validating preview secret** — Security hole. WHY: enableDraftMode validates automatically, don't skip it.
- **Missing auth configuration** — Preview shows 403 errors. WHY: Draft mode requires authenticated requests to fetch unpublished content.
- **Not testing with unpublished content** — Doesn't verify auth works. WHY: Test with status = 0 content.

### See Also

- Authentication Patterns
- On-Demand Revalidation
- Security Best Practices
