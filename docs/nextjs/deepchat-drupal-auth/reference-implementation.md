---
description: Complete working implementation — Next.js proxy route handler, React ChatWorkspace component, and Drupal setSession controller
drupal_version: "11.x"
---

# Reference Implementation

## When to Use

> Use this guide as the canonical working example for DeepChat + Drupal OAuth integration. Start here when building from scratch or verifying your implementation against a known-good pattern.

## Decision

| File | Role |
|------|------|
| `/frontend/app/api/deepchat/route.ts` | Proxy: fetches CSRF token, forwards to Drupal, streams SSE back |
| `/frontend/src/components/chat/ChatWorkspace.tsx` | Component: initializes session, renders `<DeepChat>` when ready |
| `DeepChatApi::setSession()` | Drupal: starts PHP session, generates CSRF token, returns as plain text |

**Critical rule**: Same `accessToken` used for session fetch AND API call within every request to the proxy.

## Pattern

**Next.js proxy (`/frontend/app/api/deepchat/route.ts`):**

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/auth';

const baseUrl = process.env.NEXT_PUBLIC_DRUPAL_BASE_URL!;

async function getCsrfTokenFromDrupal(accessToken: string): Promise<string> {
  const response = await fetch(`${baseUrl}/api/deepchat/session`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
  });
  if (!response.ok) throw new Error(`Failed to get CSRF token: ${response.status}`);
  return response.text();
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const isStreaming = body.stream === 1 || body.stream === true;
  const session = await auth();
  if (!session?.accessToken) {
    return NextResponse.json({ error: 'Authentication required' }, { status: 401 });
  }

  const csrfToken = await getCsrfTokenFromDrupal(session.accessToken);

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${session.accessToken}`,
    ...(isStreaming && { 'Accept': 'text/event-stream' }),
  };

  const drupalResponse = await fetch(
    `${baseUrl}/api/deepchat?token=${encodeURIComponent(csrfToken)}`,
    { method: 'POST', headers, body: JSON.stringify(body) }
  );

  if (!drupalResponse.ok) {
    return NextResponse.json({ error: 'Chat request failed' }, { status: drupalResponse.status });
  }

  if (isStreaming && drupalResponse.body) {
    return new NextResponse(drupalResponse.body, {
      status: 200,
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    });
  }
  return NextResponse.json(await drupalResponse.json());
}
```

**React component (`/frontend/src/components/chat/ChatWorkspace.tsx`):**

```typescript
'use client';
import dynamic from 'next/dynamic';
import { useMemo, useCallback } from 'react';
import { useChatSession } from './hooks/useChatSession';

const DeepChat = dynamic(
  () => import('deep-chat-react').then((mod) => mod.DeepChat),
  { ssr: false }
);

export function ChatWorkspace({ assistantId, threadId, onThreadIdChange }) {
  const { csrfToken, isReady, error } = useChatSession({ assistantId });
  if (!isReady) return <div>Initializing chat session...</div>;
  if (error) return <div>Error: {error.message}</div>;

  const requestConfig = useMemo(() => ({
    url: `/api/deepchat`,
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    additionalBodyProps: { assistant_id: assistantId, thread_id: threadId, stream: 1 },
    stream: true,
  }), [assistantId, threadId]);

  const responseInterceptor = useCallback((response: any) => {
    if (response.thread_id) onThreadIdChange?.(response.thread_id);
    return response;
  }, [onThreadIdChange]);

  return <DeepChat connect={requestConfig} responseInterceptor={responseInterceptor} />;
}
```

**Drupal controller (`DeepChatApi::setSession()`):**

```php
public function setSession(Request $request): Response {
  $session = $request->getSession();
  if (!$session->isStarted()) {
    $session->start();  // CRITICAL: OAuth does not create sessions automatically
  }
  $session->set('deepchat', 'true');
  return new Response($this->csrfTokenGenerator->get("api/deepchat"));
}
```

## Common Mistakes

- **Wrong**: `dynamic()` import without `{ ssr: false }` → **Right**: DeepChat is a browser-only web component; SSR will fail
- **Wrong**: Caching CSRF token across requests at module level → **Right**: Fetch a fresh token per proxy request (token is tied to session seed)

## See Also

- [Architecture Overview](oauth-csrf-overview.md)
- [Authentication Flow](dual-authentication-flow.md)
- [DeepChat Configuration](deepchat-configuration.md)
- [Common Pitfalls](common-pitfalls.md)
- Reference: `/web/modules/contrib/ai/modules/ai_chatbot/src/Controller/DeepChatApi.php`
- Drupal docs: [CSRF Access Checking](https://www.drupal.org/docs/8/api/routing-system/access-checking-on-routes/csrf-access-checking)
