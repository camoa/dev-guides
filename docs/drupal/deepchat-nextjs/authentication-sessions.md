---
description: NextAuth Bearer token authentication, Drupal OAuth + CSRF flow, session management, and thread persistence
---

# Authentication & Sessions

## When to Use

> Use NextAuth + Bearer token for user-specific chat. Use OAuth + CSRF flow for Drupal backend. Store threadId in localStorage for persistence.

## Decision

| Scenario | Pattern |
|----------|---------|
| User-specific chat | NextAuth + Bearer token |
| Drupal backend | OAuth + CSRF flow |
| Anonymous chat | No auth (public endpoint) |
| Thread persistence | localStorage + threadId |
| Multi-user app | Session per user |

## Bearer Token Authentication

**NextAuth.js Pattern:**

```typescript
// app/api/chat/route.ts
import { auth } from '@/lib/auth';

export async function POST(request: NextRequest) {
  // Get session
  const session = await auth();

  if (!session?.user) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  const accessToken = session.accessToken;

  // Use token for backend requests
  const response = await fetch(`${backendUrl}/api/chat`, {
    headers: {
      'Authorization': `Bearer ${accessToken}`,
    },
  });

  // ...
}
```

## Drupal OAuth Flow

```typescript
// 1. Get CSRF token
async function getCsrfToken(accessToken: string): Promise<string> {
  const response = await fetch(`${drupalUrl}/api/deepchat/session`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
    },
  });
  return response.text();
}

// 2. Use token in chat request
export async function POST(request: NextRequest) {
  const session = await auth();
  const csrfToken = await getCsrfToken(session.accessToken);

  const chatResponse = await fetch(
    `${drupalUrl}/api/deepchat?token=${csrfToken}`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${session.accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(await request.json()),
    }
  );

  return NextResponse.json(await chatResponse.json());
}
```

## Session Management

**Client-Side Session Hook:**

```tsx
function useChatSession(assistantId: string) {
  const [csrfToken, setCsrfToken] = useState<string | null>(null);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    const fetchSession = async () => {
      const response = await fetch('/api/chat/session', {
        method: 'POST',
      });

      if (response.ok) {
        const token = await response.text();
        setCsrfToken(token);
        setIsReady(true);
      }
    };

    fetchSession();
  }, []);

  return { csrfToken, isReady };
}

// Usage
function ChatWidget({ assistantId }) {
  const { csrfToken, isReady } = useChatSession(assistantId);

  if (!isReady) {
    return <div>Loading session...</div>;
  }

  return <DeepChat connect={requestConfig} />;
}
```

## Thread Persistence

```tsx
function useChatThread(assistantId: string) {
  const [threadId, setThreadId] = useState<string | null>(() => {
    // Load from localStorage
    return localStorage.getItem(`chat_thread_${assistantId}`);
  });

  const updateThreadId = (newThreadId: string) => {
    setThreadId(newThreadId);
    localStorage.setItem(`chat_thread_${assistantId}`, newThreadId);
  };

  const resetThread = () => {
    setThreadId(null);
    localStorage.removeItem(`chat_thread_${assistantId}`);
  };

  return { threadId, updateThreadId, resetThread };
}
```

## Pattern

```typescript
// Complete authenticated chat setup
// app/api/chat/route.ts
import { auth } from '@/lib/auth';

let csrfCache: Map<string, { token: string; expires: number }> = new Map();

async function getCachedCsrfToken(userId: string, accessToken: string) {
  const cached = csrfCache.get(userId);
  if (cached && cached.expires > Date.now()) {
    return cached.token;
  }

  const response = await fetch(`${drupalUrl}/api/deepchat/session`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${accessToken}` },
  });

  const token = await response.text();

  csrfCache.set(userId, {
    token,
    expires: Date.now() + 20 * 60 * 1000, // 20 min
  });

  return token;
}

export async function POST(request: NextRequest) {
  const session = await auth();

  if (!session?.user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const csrfToken = await getCachedCsrfToken(
    session.user.id,
    session.accessToken
  );

  const body = await request.json();

  const drupalResponse = await fetch(
    `${drupalUrl}/api/deepchat?token=${csrfToken}`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${session.accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    }
  );

  return NextResponse.json(await drupalResponse.json());
}
```

## Common Mistakes

- **Wrong**: Not validating session server-side → **Right**: Client can fake session. Always check on server
- **Wrong**: Caching CSRF token across users → **Right**: User-specific. Use Map keyed by userId
- **Wrong**: Storing access tokens in localStorage → **Right**: XSS risk. Use httpOnly cookies or server session
- **Wrong**: Not handling token expiration → **Right**: Tokens expire. Implement refresh logic
- **Wrong**: Exposing session endpoint without auth → **Right**: Public CSRF endpoint is security risk
- **Wrong**: Not clearing cache on logout → **Right**: Old tokens persist. Clear on logout

## See Also

- [Next.js API Routes](nextjs-api-routes.md)
- [Drupal Backend Integration](drupal-backend.md)
- [Security](security.md)
- Reference: https://next-auth.js.org/getting-started/introduction
