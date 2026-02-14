---
description: Configure DeepChat API connection and request/response interceptors for dynamic context injection
---

# Connect Configuration

## When to Use

> Use `connect` property to define API endpoint and headers. Use interceptors to inject context, track threads, or modify requests/responses.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Add context to every message | Request interceptor | Injects data before sending |
| Track conversation thread | Response interceptor | Extracts thread ID from response |
| Add authentication headers | Request interceptor | Modifies headers |
| Process custom response data | Response interceptor | Handles non-standard fields |
| Log requests/responses | Both interceptors | Debugging and analytics |

## Basic Configuration

```tsx
const requestConfig = {
  url: '/api/chat',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  additionalBodyProps: {
    assistant_id: 'my_assistant',
    stream: 1,
  },
  stream: true, // Enable SSE client-side
};

<DeepChat connect={requestConfig} />
```

## Configuration Options

| Property | Type | Purpose |
|----------|------|---------|
| `url` | string | API endpoint (required) |
| `method` | string | HTTP method (default: POST) |
| `headers` | object | Request headers |
| `additionalBodyProps` | object | Extra data in request body |
| `credentials` | string | Cookie handling (default: same-origin) |
| `stream` | boolean | Enable SSE streaming |
| `websocket` | boolean/string | Use WebSocket instead |
| `handler` | function | Custom request handler |

## With Dynamic Values

```tsx
const requestConfig = useMemo(() => ({
  url: `/api/chat`,
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  additionalBodyProps: {
    assistant_id: assistantId,
    thread_id: threadId,
    stream: 1,
  },
  stream: true,
}), [assistantId, threadId]);
```

## Request Interceptor

Modify requests before sending:

```tsx
const requestInterceptor = async (request: any) => {
  // Inject context
  if (contextProvider) {
    const context = await contextProvider();
    request.body = {
      ...request.body,
      contexts: context,
    };
  }

  // Add custom headers
  request.headers['X-User-ID'] = userId;

  return request;
};
```

## Response Interceptor

Process responses after receiving:

```tsx
const responseInterceptor = (response: any) => {
  // Track thread ID
  if (response.thread_id) {
    setThreadId(response.thread_id);
    onThreadIdChange?.(response.thread_id);
  }

  // Extract custom data
  if (response.custom) {
    handleCustomData(response.custom);
  }

  return response;
};
```

## Pattern

```tsx
// Context injection pattern
const requestInterceptor = async (request: any) => {
  const context = {
    page: window.location.pathname,
    user_role: userRole,
    timestamp: Date.now(),
  };

  request.body.contexts = [JSON.stringify(context)];
  return request;
};

// Full setup
<DeepChat
  connect={requestConfig}
  requestInterceptor={requestInterceptor}
  responseInterceptor={responseInterceptor}
/>
```

## Common Mistakes

- **Wrong**: Mutating request without returning it → **Right**: Interceptor must return the modified request object
- **Wrong**: Blocking async operations → **Right**: Use `async`/`await` properly or return will be undefined
- **Wrong**: Throwing errors in interceptor → **Right**: Catch and log errors gracefully instead. Throwing breaks the request
- **Wrong**: Not handling missing properties → **Right**: Check `if (request.body)` before spreading
- **Wrong**: Forgetting to set `Content-Type` header → **Right**: Set to `application/json` so backend can parse correctly

## See Also

- [Next.js API Routes](nextjs-api-routes.md)
- [Message Formats](message-formats.md)
- Reference: https://deepchat.dev/docs/interceptors/
