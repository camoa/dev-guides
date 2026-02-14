---
description: Install DeepChat in Next.js and configure dynamic import to avoid SSR errors
---

# Installation & Setup

## When to Use

> Use dynamic import with `ssr: false` for all DeepChat instances in Next.js. DeepChat is a web component that requires browser APIs.

## Decision

| Scenario | Pattern |
|----------|---------|
| Chat in app layout | Dynamic import in page component |
| Chat as widget | Dynamic import in widget component |
| Multiple chat instances | Reusable dynamic component |
| Custom chat wrapper | Dynamic import + forwarded ref |

## Installation

**Install DeepChat:**

```bash
npm install deep-chat-react
```

**For vanilla JS/other frameworks:**

```bash
npm install deep-chat
```

**Via CDN (not recommended for production):**

```html
<script src="https://unpkg.com/deep-chat@2.3.0/dist/deepChat.bundle.js"></script>
```

## Next.js Dynamic Import

**The Problem:**

DeepChat is a web component that relies on browser APIs. Next.js SSR will fail because `customElements` is undefined on the server.

**The Solution:**

Use `next/dynamic` with `ssr: false`:

```tsx
// components/chat/ChatWidget.tsx
'use client';

import dynamic from 'next/dynamic';

const DeepChat = dynamic(
  () => import('deep-chat-react').then((mod) => mod.DeepChat),
  { ssr: false }
);

export function ChatWidget() {
  return (
    <DeepChat
      connect={{ url: '/api/chat', method: 'POST' }}
    />
  );
}
```

**Why this works:**

- `dynamic` delays import until client-side
- `ssr: false` skips server rendering
- `then((mod) => mod.DeepChat)` extracts named export

## Pattern

```tsx
// app/page.tsx
import { ChatWidget } from '@/components/chat/ChatWidget';

export default function Page() {
  return (
    <div>
      <h1>My App</h1>
      <ChatWidget />
    </div>
  );
}
```

## Common Mistakes

- **Wrong**: Importing DeepChat directly in server component → **Right**: Use dynamic import with `ssr: false` to avoid `ReferenceError: customElements is not defined`
- **Wrong**: Forgetting `'use client'` directive → **Right**: Add `'use client'` at top of component file
- **Wrong**: Using static import in page → **Right**: Use dynamic import even with dynamic component wrapper
- **Wrong**: Not extracting named export → **Right**: Use `.then((mod) => mod.DeepChat)` to extract the component
- **Wrong**: Using `loading` component that changes layout → **Right**: Keep loading minimal to avoid flash when hydrating

## See Also

- [Connect Configuration](connect-configuration.md)
- Reference: https://nextjs.org/docs/app/building-your-application/optimizing/lazy-loading
