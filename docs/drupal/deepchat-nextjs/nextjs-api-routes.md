---
description: Next.js API route handlers for DeepChat with proxy pattern, authentication, and CSRF token management for Drupal
---

# Next.js API Route Handlers

## When to Use

> Use proxy pattern for Drupal/external backends. Use CSRF flow for Drupal with OAuth + CSRF. Cache CSRF tokens per user session.

## Decision

| Pattern | When |
|---------|------|
| Direct API route | Simple non-Drupal backend |
| Proxy pattern | Drupal/external API backend |
| CSRF flow | Drupal with OAuth + CSRF |
| Session caching | Multiple requests per user session |

## Basic API Route

```typescript
// app/api/chat/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { messages, assistant_id } = body;

    // Process message (call AI service)
    const response = await processMessage(messages[messages.length - 1].text);

    return NextResponse.json({
      html: response,
    });
  } catch (error) {
    console.error('Chat error:', error);
    return NextResponse.json(
      { error: 'Failed to process message' },
      { status: 500 }
    );
  }
}
```

## With Authentication

```typescript
import { auth } from '@/lib/auth';

export async function POST(request: NextRequest) {
  const session = await auth();

  if (!session?.user) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  const body = await request.json();
  // Process authenticated request...
}
```

## Proxy Pattern (Recommended)

```typescript
// app/api/chat/route.ts
export async function POST(request: NextRequest) {
  const session = await auth();
  const body = await request.json();
  const isStreaming = body.stream === 1;

  // Fetch CSRF token (for Drupal)
  const csrfToken = await getCsrfToken(session.accessToken);

  // Proxy to backend
  const backendResponse = await fetch(
    `${baseUrl}/api/deepchat?token=${csrfToken}`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${session.accessToken}`,
        ...(isStreaming && { 'Accept': 'text/event-stream' }),
      },
      body: JSON.stringify(body),
    }
  );

  if (!backendResponse.ok) {
    return NextResponse.json(
      { error: 'Backend error' },
      { status: backendResponse.status }
    );
  }

  // Stream or JSON
  if (isStreaming && backendResponse.body) {
    return new NextResponse(backendResponse.body, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    });
  }

  const data = await backendResponse.json();
  return NextResponse.json(data);
}
```

## CSRF Authentication Flow

**The Problem:**

Drupal routes with `_csrf_token: 'TRUE'` require:
1. OAuth Bearer token (user authentication)
2. CSRF token from session (request validation)

**The Solution:**

Two-step pattern:

1. **Session endpoint** creates PHP session and returns CSRF token
2. **Chat endpoint** uses token as query parameter

**Session Route:**

```typescript
// app/api/chat/session/route.ts
export async function POST(request: NextRequest) {
  const session = await auth();

  const response = await fetch(
    `${baseUrl}/api/deepchat/session`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${session.accessToken}`,
      },
    }
  );

  const token = await response.text(); // Plain text!
  return new Response(token);
}
```

**Chat Route with CSRF:**

```typescript
async function getCsrfToken(accessToken: string): Promise<string> {
  const response = await fetch(`${baseUrl}/api/deepchat/session`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${accessToken}` },
  });
  return response.text();
}

export async function POST(request: NextRequest) {
  const session = await auth();
  const csrfToken = await getCsrfToken(session.accessToken);

  // Use token in query parameter
  const drupalResponse = await fetch(
    `${baseUrl}/api/deepchat?token=${encodeURIComponent(csrfToken)}`,
    {
      headers: { 'Authorization': `Bearer ${session.accessToken}` },
      // ...
    }
  );
}
```

## Pattern

```typescript
// Reusable CSRF helper with caching
let csrfTokenCache: { token: string; expires: number } | null = null;

async function getCsrfToken(accessToken: string): Promise<string> {
  if (csrfTokenCache && csrfTokenCache.expires > Date.now()) {
    return csrfTokenCache.token;
  }

  const response = await fetch(`${baseUrl}/api/deepchat/session`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${accessToken}` },
  });

  const token = await response.text();

  // Cache for 20 minutes
  csrfTokenCache = {
    token,
    expires: Date.now() + 20 * 60 * 1000,
  };

  return token;
}
```

## Common Mistakes

- **Wrong**: Fetching CSRF token with different Bearer token → **Right**: Use same token for both requests to avoid session mismatch
- **Wrong**: Caching CSRF token across users → **Right**: Token is user-specific. Cache per session/user
- **Wrong**: Passing CSRF in header instead of query → **Right**: Drupal `_csrf_token` expects query parameter
- **Wrong**: Not URL-encoding CSRF token → **Right**: Use `encodeURIComponent()` as token may contain special characters
- **Wrong**: Using `response.json()` for session endpoint → **Right**: Drupal returns plain text, use `response.text()`
- **Wrong**: Not handling CSRF expiration → **Right**: Token expires with session (~24 hours). Implement refresh logic

## See Also

- [Authentication & Sessions](authentication-sessions.md)
- [Drupal Backend Integration](drupal-backend.md)
- Reference: `/home/camoa/workspace/claude_memory/guides/deepchat-nextjs-drupal-integration.md`
