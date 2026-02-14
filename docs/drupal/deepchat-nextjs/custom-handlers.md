---
description: Implement custom request handlers, transform requests/responses, and add retry logic with DeepChat
---

# Custom Request/Response Handlers

## When to Use

> Use custom handler for complex request flow or retry logic. Use interceptors for simple transforms. Always call `signals.onResponse()`.

## Decision

| Scenario | Pattern |
|----------|---------|
| Custom auth logic | Request interceptor |
| Provider-specific format | Response interceptor |
| Complex request flow | Custom handler |
| Retry logic | Custom handler with loop |
| Multiple backends | Custom handler with routing |

## The handler Property

Instead of using `connect.url`, you can define a custom function to handle requests entirely:

```tsx
const customHandler = async (body: any, signals: Signals) => {
  try {
    // Custom request logic
    const response = await fetch('/api/custom-chat', {
      method: 'POST',
      body: JSON.stringify(body),
    });

    const data = await response.json();

    // Notify DeepChat of response
    signals.onResponse({ html: data.html });
  } catch (error) {
    signals.onResponse({ error: 'Request failed' });
  }
};

<DeepChat
  connect={{ handler: customHandler }}
/>
```

## Signals Object

| Signal | Purpose |
|--------|---------|
| `onResponse` | Display response message |
| `onOpen` | Notify connection opened |
| `onClose` | Notify connection closed |
| `stopClicked` | Listen for stop button |
| `newUserMessage` | Listen for new messages |

## Streaming with Handler

```tsx
const streamingHandler = async (body: any, signals: Signals) => {
  const response = await fetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify(body),
  });

  const reader = response.body!.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split('\n').filter(line => line.trim());

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6));
        signals.onResponse(data);
      }
    }
  }
};
```

## Transform Request

```tsx
const requestInterceptor = (request: any) => {
  // Add auth token
  request.headers['Authorization'] = `Bearer ${getToken()}`;

  // Transform message format
  request.body.messages = request.body.messages.map(m => ({
    role: m.role === 'ai' ? 'assistant' : 'user',
    content: m.text,
  }));

  return request;
};
```

## Transform Response

```tsx
const responseInterceptor = (response: any) => {
  // Transform provider format to DeepChat format
  if (response.choices) {
    return {
      html: response.choices[0].message.content,
    };
  }

  // Handle errors
  if (response.error) {
    return {
      error: response.error.message,
    };
  }

  return response;
};
```

## Error Handling

```tsx
const customHandler = async (body: any, signals: Signals) => {
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const error = await response.json();
      signals.onResponse({
        error: error.message || 'Request failed',
      });
      return;
    }

    const data = await response.json();
    signals.onResponse(data);
  } catch (error) {
    signals.onResponse({
      error: 'Network error. Please try again.',
    });
  }
};
```

## Pattern

```tsx
// Retry logic with exponential backoff
const retryHandler = async (body: any, signals: Signals) => {
  let attempt = 0;
  const maxAttempts = 3;

  while (attempt < maxAttempts) {
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        body: JSON.stringify(body),
      });

      if (response.ok) {
        const data = await response.json();
        signals.onResponse(data);
        return;
      }

      if (response.status === 429) {
        // Rate limited - wait and retry
        const wait = Math.pow(2, attempt) * 1000;
        await new Promise(resolve => setTimeout(resolve, wait));
        attempt++;
        continue;
      }

      throw new Error(`Request failed: ${response.status}`);
    } catch (error) {
      if (attempt === maxAttempts - 1) {
        signals.onResponse({ error: 'Failed after 3 attempts' });
      }
      attempt++;
    }
  }
};
```

## Common Mistakes

- **Wrong**: Not returning modified request from interceptor → **Right**: Changes are lost. Always return the request object
- **Wrong**: Throwing errors in interceptor → **Right**: Breaks request flow. Return `{ error: '...' }` instead
- **Wrong**: Not calling `signals.onResponse()` → **Right**: DeepChat waits forever. Always call it, even on error
- **Wrong**: Mutating original request object → **Right**: Create copy if shared. Use `{...request}` spread
- **Wrong**: Not handling async interceptors → **Right**: Use `async`/`await` properly or return Promise
- **Wrong**: Forgetting to decode stream chunks → **Right**: Streaming responses need `TextDecoder`

## See Also

- [Streaming Responses](streaming-responses.md)
- [Authentication & Sessions](authentication-sessions.md)
- Reference: https://deepchat.dev/docs/interceptors/
