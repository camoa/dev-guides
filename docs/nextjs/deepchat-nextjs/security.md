---
description: XSS prevention, API key management, file upload validation, rate limiting, and CSP for secure DeepChat implementation
---

# Security

## When to Use

> Always sanitize AI output on server. Never expose API keys client-side. Validate file uploads server-side with magic bytes. Implement rate limiting.

## XSS Prevention

**The Problem:**

AI responses can contain malicious HTML/JavaScript. DeepChat renders `html` responses directly in the DOM.

**Backend Sanitization (Required):**

```php
// Drupal example
use Drupal\Component\Utility\Xss;

$allowedTags = [
  'a', 'b', 'blockquote', 'br', 'code', 'del', 'em',
  'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img',
  'li', 'ol', 'p', 'pre', 'strong', 'ul',
];

$sanitizedResponse = Xss::filter($aiResponse, $allowedTags);
```

**Next.js/Node.js:**

```typescript
import sanitizeHtml from 'sanitize-html';

const allowedTags = [
  'a', 'b', 'blockquote', 'br', 'code', 'del', 'em',
  'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img',
  'li', 'ol', 'p', 'pre', 'strong', 'ul',
];

export async function POST(request: NextRequest) {
  const aiResponse = await callAI();

  const sanitized = sanitizeHtml(aiResponse, {
    allowedTags,
    allowedAttributes: {
      'a': ['href', 'target'],
      'img': ['src', 'alt'],
    },
  });

  return NextResponse.json({ html: sanitized });
}
```

**Content Security Policy:**

```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  const response = NextResponse.next();

  response.headers.set(
    'Content-Security-Policy',
    [
      "default-src 'self'",
      "script-src 'self' 'unsafe-inline'", // DeepChat needs inline
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: https:",
      "connect-src 'self' https://api.openai.com",
    ].join('; ')
  );

  return response;
}
```

## API Key Management

**Never Expose Keys:**

```tsx
// ❌ WRONG - API key exposed
<DeepChat
  directConnection={{
    openai: {
      key: 'sk-...',
    },
  }}
/>

// ✅ CORRECT - Key on server
// app/api/chat/route.ts
const response = await fetch('https://api.openai.com/v1/chat/completions', {
  headers: {
    'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
  },
});
```

**Environment Variables:**

```bash
# .env.local (NEVER commit)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
DRUPAL_BASE_URL=https://drupal.example.com
```

**Runtime Validation:**

```typescript
// lib/config.ts
const config = {
  openaiApiKey: process.env.OPENAI_API_KEY,
  drupalBaseUrl: process.env.DRUPAL_BASE_URL,
};

// Validate on startup
if (!config.openaiApiKey) {
  throw new Error('OPENAI_API_KEY is required');
}

export default config;
```

## File Upload Security

**Validate File Type:**

```typescript
export async function POST(request: NextRequest) {
  const formData = await request.formData();
  const files = formData.getAll('files') as File[];

  for (const file of files) {
    // Check MIME type
    if (!file.type.startsWith('image/')) {
      return NextResponse.json(
        { error: 'Only images allowed' },
        { status: 400 }
      );
    }

    // Check size (5MB limit)
    if (file.size > 5 * 1024 * 1024) {
      return NextResponse.json(
        { error: 'File too large' },
        { status: 400 }
      );
    }

    // Check magic bytes (real validation)
    const buffer = Buffer.from(await file.arrayBuffer());
    const isPNG = buffer[0] === 0x89 && buffer[1] === 0x50;
    const isJPG = buffer[0] === 0xFF && buffer[1] === 0xD8;

    if (!isPNG && !isJPG) {
      return NextResponse.json(
        { error: 'Invalid file format' },
        { status: 400 }
      );
    }
  }

  // Process files...
}
```

**Scan for Malware:**

```typescript
import { scan } from 'clamav.js';

const result = await scan(buffer);
if (result.isInfected) {
  return NextResponse.json(
    { error: 'File contains malware' },
    { status: 400 }
  );
}
```

## Rate Limiting

**API Route Protection:**

```typescript
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '1 m'), // 10 requests per minute
});

export async function POST(request: NextRequest) {
  const ip = request.ip ?? '127.0.0.1';
  const { success } = await ratelimit.limit(ip);

  if (!success) {
    return NextResponse.json(
      { error: 'Rate limit exceeded' },
      { status: 429 }
    );
  }

  // Process request...
}
```

**User-Based Limits:**

```typescript
const session = await auth();
const userId = session?.user?.id ?? 'anonymous';

const { success, remaining } = await ratelimit.limit(userId);

if (!success) {
  return NextResponse.json(
    { error: `Rate limit exceeded. ${remaining} requests remaining.` },
    { status: 429 }
  );
}
```

## Common Mistakes

- **Wrong**: Trusting AI output is safe → **Right**: AI can output malicious HTML. Always sanitize
- **Wrong**: Sanitizing on client side → **Right**: Client can bypass. Sanitize on server
- **Wrong**: Using `dangerouslySetInnerHTML` → **Right**: XSS risk. Let DeepChat handle rendering
- **Wrong**: Not validating file uploads → **Right**: Users can upload executables. Check magic bytes
- **Wrong**: Storing API keys in frontend → **Right**: Exposed in bundle. Always use server routes
- **Wrong**: No rate limiting → **Right**: API abuse and cost explosion. Implement limits
- **Wrong**: Weak CSP → **Right**: XSS still possible. Use strict CSP

## See Also

- [Best Practices](best-practices.md)
- [Anti-Patterns](anti-patterns.md)
- Reference: https://web.dev/articles/strict-csp
- Reference: https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html
- Reference: https://owasp.org/www-community/attacks/xss/
