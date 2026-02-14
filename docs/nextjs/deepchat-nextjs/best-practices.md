---
description: Component architecture, performance optimization, lazy loading, error handling, and production patterns for DeepChat
---

# Best Practices & Patterns

## When to Use

> Lazy load when chat not immediately visible. Use error boundaries in production. Memoize config objects to prevent re-renders.

## Decision

| Pattern | When |
|---------|------|
| Lazy loading | Chat not immediately visible |
| Virtualization | >100 messages |
| Debouncing | Real-time features (typing indicators) |
| Error boundaries | Production apps |
| Retry logic | Unreliable networks |

## Component Architecture

**Separation of Concerns:**

```
components/
  chat/
    ChatWidget.tsx          # Main component
    ChatContainer.tsx       # Layout wrapper
    hooks/
      useChatSession.ts     # Session management
      useChatThread.ts      # Thread persistence
      useChatContext.ts     # Context injection
    types/
      chat.types.ts         # TypeScript types
```

## Reusable Chat Component

```tsx
// components/chat/ChatWidget.tsx
'use client';

import dynamic from 'next/dynamic';
import { useChatSession } from './hooks/useChatSession';
import { useChatThread } from './hooks/useChatThread';

const DeepChat = dynamic(
  () => import('deep-chat-react').then((mod) => mod.DeepChat),
  { ssr: false }
);

interface ChatWidgetProps {
  assistantId: string;
  contextProvider?: () => Promise<any>;
  onThreadChange?: (threadId: string) => void;
}

export function ChatWidget({
  assistantId,
  contextProvider,
  onThreadChange,
}: ChatWidgetProps) {
  const { isReady } = useChatSession(assistantId);
  const { threadId, updateThreadId } = useChatThread(assistantId);

  const requestConfig = {
    url: '/api/chat',
    method: 'POST',
    additionalBodyProps: {
      assistant_id: assistantId,
      thread_id: threadId,
      stream: 1,
    },
    stream: true,
  };

  const requestInterceptor = async (request: any) => {
    if (contextProvider) {
      const context = await contextProvider();
      request.body.contexts = context;
    }
    return request;
  };

  const responseInterceptor = (response: any) => {
    if (response.thread_id && response.thread_id !== threadId) {
      updateThreadId(response.thread_id);
      onThreadChange?.(response.thread_id);
    }
    return response;
  };

  if (!isReady) {
    return <div>Loading chat...</div>;
  }

  return (
    <DeepChat
      connect={requestConfig}
      requestInterceptor={requestInterceptor}
      responseInterceptor={responseInterceptor}
      style={{ borderRadius: '8px', height: '600px' }}
    />
  );
}
```

## Performance Optimization

**Lazy Loading:**

```tsx
// Only load chat when user opens it
function ChatPage() {
  const [showChat, setShowChat] = useState(false);

  return (
    <div>
      <button onClick={() => setShowChat(true)}>Open Chat</button>
      {showChat && <ChatWidget assistantId="site_helper" />}
    </div>
  );
}
```

**Request Debouncing:**

```tsx
// Prevent rapid-fire requests
const debouncedSend = useCallback(
  debounce(async (message: string) => {
    // Send message
  }, 500),
  []
);
```

**Streaming Backpressure:**

```typescript
// Handle slow clients
const stream = new ReadableStream({
  async start(controller) {
    for (const chunk of chunks) {
      controller.enqueue(chunk);

      // Wait if queue is full
      if (controller.desiredSize !== null && controller.desiredSize <= 0) {
        await new Promise(resolve => setTimeout(resolve, 100));
      }
    }
  },
});
```

## Error Handling

**Graceful Degradation:**

```tsx
const requestInterceptor = async (request: any) => {
  try {
    const context = await contextProvider();
    request.body.contexts = context;
  } catch (error) {
    console.warn('Context provider failed:', error);
    // Continue without context
  }
  return request;
};
```

**Error Boundaries:**

```tsx
import { ErrorBoundary } from 'react-error-boundary';

function ChatPage() {
  return (
    <ErrorBoundary
      fallback={<div>Chat failed to load. Please refresh.</div>}
      onError={(error) => console.error('Chat error:', error)}
    >
      <ChatWidget assistantId="site_helper" />
    </ErrorBoundary>
  );
}
```

**Retry Logic:**

```typescript
async function fetchWithRetry(url: string, options: any, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url, options);
      if (response.ok) return response;

      if (response.status === 429) {
        const wait = Math.pow(2, i) * 1000;
        await new Promise(resolve => setTimeout(resolve, wait));
        continue;
      }

      throw new Error(`HTTP ${response.status}`);
    } catch (error) {
      if (i === retries - 1) throw error;
    }
  }
}
```

## Common Mistakes

- **Wrong**: Loading chat on every page → **Right**: Lazy load when needed to reduce bundle size impact
- **Wrong**: Not memoizing config objects → **Right**: Use `useMemo` to prevent re-renders
- **Wrong**: Rendering all messages → **Right**: Use virtualization for long conversations (>100 messages)
- **Wrong**: No error handling → **Right**: Chat breaks silently. Always handle errors
- **Wrong**: Not cleaning up streams → **Right**: Close controllers in `finally` to prevent memory leaks
- **Wrong**: Blocking UI during requests → **Right**: Show loading states. Use optimistic updates

## See Also

- [Streaming Responses](streaming-responses.md)
- [Security](security.md)
- Reference: https://nextjs.org/docs/app/building-your-application/optimizing/lazy-loading
