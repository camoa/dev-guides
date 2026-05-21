---
description: "Use when creating a new Next.js frontend for an existing Drupal backend. App Router (Next.js 13+) is recommended over Pages Router."
tldr: "Use when creating a new Next.js frontend for an existing Drupal backend. App Router (Next.js 13+) is recommended over Pages Router."
drupal_version: "11.x"
topic: "drupal/next-drupal"
---

## Next.js Project Setup

### When to Use

Use when creating a new Next.js frontend for an existing Drupal backend. App Router (Next.js 13+) is recommended over Pages Router.

### Steps

**1. Create project from starter**

The official starters live in the `next-drupal` monorepo under `starters/`:

```bash
# Basic starter (App Router, JSON:API)
npx create-next-app -e https://github.com/chapter-three/next-drupal/tree/main/starters/basic-starter

# GraphQL starter (App Router)
npx create-next-app -e https://github.com/chapter-three/next-drupal/tree/main/starters/graphql-starter

# Pages Router starter (legacy)
npx create-next-app -e https://github.com/chapter-three/next-drupal/tree/main/starters/pages-starter
```

All starters pin Next.js 15 / React 19 / `next-drupal` 2.x. Do not bump Next.js to 16 — see Project Status in the Decoupled Architecture Decision section.

**2. Configure environment variables**

Copy `.env.example` to `.env.local`:

```bash
# Required
NEXT_PUBLIC_DRUPAL_BASE_URL=http://localhost:8080
NEXT_IMAGE_DOMAIN=localhost

# OAuth (if using authentication)
DRUPAL_CLIENT_ID=your-client-id
DRUPAL_CLIENT_SECRET=your-client-secret

# Revalidation (if using ISR)
DRUPAL_REVALIDATE_SECRET=your-revalidate-secret

# Preview (if using draft mode)
DRUPAL_PREVIEW_SECRET=your-preview-secret
```

**3. Initialize NextDrupal client**

Create `lib/drupal.ts`:

```typescript
import { NextDrupal } from "next-drupal"

export const drupal = new NextDrupal(
  process.env.NEXT_PUBLIC_DRUPAL_BASE_URL,
  {
    auth: {
      clientId: process.env.DRUPAL_CLIENT_ID,
      clientSecret: process.env.DRUPAL_CLIENT_SECRET,
    },
  }
)
```

**4. Start development server**

```bash
npm run dev
# or
yarn dev
```

Visit `http://localhost:3000`

### Decision Points

| Choice | When | Impact |
|--------|------|--------|
| App Router vs Pages Router | Next.js 13+ | App Router is modern, Pages Router is legacy |
| TypeScript vs JavaScript | Team preference | TypeScript offers better type safety |
| Basic vs GraphQL starter | API choice | Match your Drupal API configuration |

### Common Mistakes

- **Committing .env.local to version control** — Security risk. WHY: Exposes secrets.
- **Using NEXT_PUBLIC_ prefix for secrets** — Client-side exposure. WHY: Public prefix makes vars accessible in browser.
- **Mismatching Next.js and next-drupal versions** — Compatibility issues. WHY: Breaking changes between major versions.

### See Also

- NextDrupal Client Configuration
- Environment Variables
- Security Best Practices
