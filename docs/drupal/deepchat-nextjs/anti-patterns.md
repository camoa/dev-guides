---
description: Common mistakes and anti-patterns to avoid in DeepChat + Next.js integration
---

# Anti-Patterns & Common Mistakes

## Not Using Dynamic Import

❌ **Wrong:**

```tsx
import { DeepChat } from 'deep-chat-react';

export default function Page() {
  return <DeepChat connect={{ url: '/api/chat' }} />;
}
```

**Why it's bad:** SSR fails with `ReferenceError: customElements is not defined`. DeepChat relies on browser APIs.

✅ **Correct:**

```tsx
import dynamic from 'next/dynamic';

const DeepChat = dynamic(
  () => import('deep-chat-react').then(mod => mod.DeepChat),
  { ssr: false }
);
```

## Exposing API Keys Client-Side

❌ **Wrong:**

```tsx
<DeepChat
  directConnection={{
    openai: { key: 'sk-...' }
  }}
/>
```

**Why it's bad:** API key visible in browser. Anyone can steal it and rack up charges.

✅ **Correct:**

```typescript
// app/api/chat/route.ts
const response = await fetch('https://api.openai.com/v1/chat/completions', {
  headers: { 'Authorization': `Bearer ${process.env.OPENAI_API_KEY}` },
});
```

## Not Sanitizing HTML Responses

❌ **Wrong:**

```typescript
return NextResponse.json({
  html: aiResponse, // Raw AI output
});
```

**Why it's bad:** AI can be manipulated to output `<script>alert('XSS')</script>`. Major security vulnerability.

✅ **Correct:**

```typescript
import sanitizeHtml from 'sanitize-html';

const sanitized = sanitizeHtml(aiResponse, {
  allowedTags: ['p', 'b', 'i', 'a', 'ul', 'ol', 'li'],
});
return NextResponse.json({ html: sanitized });
```

## Sending Full History to Drupal

❌ **Wrong:**

```typescript
{
  messages: allMessages, // 100+ messages
  thread_id: threadId,
}
```

**Why it's bad:** Drupal stores history server-side. Sending full history wastes bandwidth and is ignored by backend.

✅ **Correct:**

```typescript
{
  messages: [currentMessage], // Only new message
  thread_id: threadId, // Backend retrieves history
}
```

## Not Handling Stream Errors

❌ **Wrong:**

```typescript
const stream = new ReadableStream({
  async start(controller) {
    const reader = response.body.getReader();
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      controller.enqueue(value);
    }
    controller.close();
  },
});
```

**Why it's bad:** If `reader.read()` throws, controller never closes. Client waits forever.

✅ **Correct:**

```typescript
const stream = new ReadableStream({
  async start(controller) {
    try {
      const reader = response.body.getReader();
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        controller.enqueue(value);
      }
    } catch (error) {
      controller.error(error);
    } finally {
      controller.close();
    }
  },
});
```

## Caching CSRF Tokens Across Users

❌ **Wrong:**

```typescript
let csrfToken: string | null = null;

async function getCsrfToken() {
  if (csrfToken) return csrfToken;
  csrfToken = await fetchToken();
  return csrfToken;
}
```

**Why it's bad:** CSRF tokens are user-specific. Sharing across users causes auth failures and security issues.

✅ **Correct:**

```typescript
const csrfCache = new Map<string, { token: string; expires: number }>();

async function getCsrfToken(userId: string) {
  const cached = csrfCache.get(userId);
  if (cached && cached.expires > Date.now()) {
    return cached.token;
  }
  const token = await fetchToken(userId);
  csrfCache.set(userId, { token, expires: Date.now() + 1200000 });
  return token;
}
```

## Using response.json() on Session Endpoint

❌ **Wrong:**

```typescript
const response = await fetch('/api/deepchat/session', { method: 'POST' });
const data = await response.json(); // Error!
```

**Why it's bad:** Drupal session endpoint returns **plain text**, not JSON. Parsing fails.

✅ **Correct:**

```typescript
const response = await fetch('/api/deepchat/session', { method: 'POST' });
const csrfToken = await response.text(); // Plain text
```

## Not Validating File Uploads Server-Side

❌ **Wrong:**

```tsx
<DeepChat
  images={{
    files: { acceptedFormats: '.jpg,.png' }
  }}
/>
```

**Why it's bad:** `acceptedFormats` is client-side only. Users can bypass by modifying requests.

✅ **Correct:**

```typescript
export async function POST(request: NextRequest) {
  const formData = await request.formData();
  const files = formData.getAll('files') as File[];

  for (const file of files) {
    if (!file.type.startsWith('image/')) {
      return NextResponse.json({ error: 'Invalid type' }, { status: 400 });
    }

    // Check magic bytes
    const buffer = Buffer.from(await file.arrayBuffer());
    const isValid = buffer[0] === 0xFF && buffer[1] === 0xD8; // JPEG
    if (!isValid) {
      return NextResponse.json({ error: 'Invalid file' }, { status: 400 });
    }
  }
}
```

## No Rate Limiting

❌ **Wrong:**

```typescript
export async function POST(request: NextRequest) {
  const response = await callOpenAI(); // No limits
  return NextResponse.json(response);
}
```

**Why it's bad:** Users can spam requests, costing $$$. Bots can abuse your API.

✅ **Correct:**

```typescript
import { Ratelimit } from '@upstash/ratelimit';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '1 m'),
});

export async function POST(request: NextRequest) {
  const { success } = await ratelimit.limit(request.ip);
  if (!success) {
    return NextResponse.json({ error: 'Rate limit' }, { status: 429 });
  }
  // Process...
}
```

## Not Memoizing Config Objects

❌ **Wrong:**

```tsx
function ChatWidget() {
  return (
    <DeepChat
      connect={{ url: '/api/chat', method: 'POST' }} // New object every render
    />
  );
}
```

**Why it's bad:** New object on every render causes DeepChat to reinitialize, breaking state.

✅ **Correct:**

```tsx
function ChatWidget() {
  const config = useMemo(() => ({
    url: '/api/chat',
    method: 'POST',
  }), []);

  return <DeepChat connect={config} />;
}
```

## See Also

- [Security](security.md)
- [Best Practices](best-practices.md)
- Reference: https://owasp.org/www-project-top-ten/
