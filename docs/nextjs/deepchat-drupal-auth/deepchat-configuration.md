---
description: Configure deep-chat-react for Next.js proxy — connect, requestInterceptor, responseInterceptor, SSE streaming, and useChatSession hook
drupal_version: "11.x"
---

# DeepChat Configuration

## When to Use

> Use this guide to configure `deep-chat-react` in Next.js with the proxy pattern. Use [Reference Implementation](reference-implementation.md) for the complete working example including the Next.js route handler.

## Decision

| Config Area | Choice | Why |
|------------|--------|-----|
| `connect.url` | `/api/deepchat` (Next.js route) | Centralizes CSRF token management in the proxy |
| `stream` | `true` + `additionalBodyProps.stream: 1` | Client enables SSE; `1` tells Drupal to use `StreamedResponse` |
| CSRF token | Fetched per-request by Next.js proxy | Browser never handles CSRF token directly |
| Session init | `useChatSession` hook on component mount | Ensures session is ready before first message |

## Pattern

**Component setup:**

```typescript
import { DeepChat } from 'deep-chat-react';

const requestConfig = {
  url: `/api/deepchat`,
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  additionalBodyProps: {
    assistant_id: assistantId,
    thread_id: threadId,
    stream: 1,
  },
  stream: true,
};

<DeepChat
  connect={requestConfig}
  requestInterceptor={requestInterceptor}
  responseInterceptor={responseInterceptor}
/>
```

**Request interceptor (inject context):**

```typescript
const requestInterceptor = async (request: any) => {
  if (contextProvider) {
    const context = await contextProvider();
    request.body = { ...request.body, contexts: context };
  }
  return request;
};
```

**Response interceptor (track thread):**

```typescript
const responseInterceptor = (response: any) => {
  if (response.thread_id) setThreadId(response.thread_id);
  return response;
};
```

**`useChatSession` hook (session init):**

```typescript
const { csrfToken, isReady } = useChatSession({ assistantId });
if (!isReady) return <LoadingSpinner />;
```

## Common Mistakes

- **Wrong**: Setting `connect.url` to Drupal's base URL directly → **Right**: Always use the Next.js proxy route (`/api/deepchat`)
- **Wrong**: Omitting `stream: true` on `requestConfig` → **Right**: Both client (`stream: true`) and body (`stream: 1`) flags are required for SSE
- **Wrong**: Rendering `<DeepChat>` before session is ready → **Right**: Gate on `isReady` from `useChatSession`

## See Also

- [Reference Implementation](reference-implementation.md)
- [Authentication Flow](dual-authentication-flow.md)
- deep-chat docs: [Connect](https://deepchat.dev/docs/connect/)
- deep-chat docs: [Interceptors](https://deepchat.dev/docs/interceptors/)
- Package: [deep-chat-react on npm](https://www.npmjs.com/package/deep-chat-react)
- Reference: `/frontend/src/components/chat/ChatWorkspace.tsx`
- Reference: `/frontend/src/components/chat/hooks/useChatSession.ts`
