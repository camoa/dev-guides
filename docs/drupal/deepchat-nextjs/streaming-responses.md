---
description: Implement Server-Sent Events streaming with ReadableStream for AI chat responses in Next.js
---

# Streaming Responses

## When to Use

> Use SSE streaming for AI chat responses. Use ReadableStream with transform for OpenAI/Anthropic. Use direct proxy for Drupal backend streaming.

## Decision

| Scenario | Pattern |
|----------|---------|
| OpenAI/Anthropic streaming | ReadableStream with transform |
| Drupal backend streaming | Direct proxy |
| Custom AI backend | ReadableStream |
| Non-streaming fallback | JSON response |

## SSE vs WebSocket

| Feature | SSE | WebSocket |
|---------|-----|-----------|
| Direction | Server → Client | Bidirectional |
| Protocol | HTTP | Custom (ws://) |
| Reconnection | Automatic | Manual |
| Complexity | Low | Medium |
| Use Case | AI streaming | Real-time chat |

## Client Configuration

```tsx
const requestConfig = {
  url: '/api/chat',
  method: 'POST',
  additionalBodyProps: {
    stream: 1, // Tell backend to stream
  },
  stream: true, // Enable SSE client-side
};
```

## Server Response Format

```
data: {"html": "Hello"}\n\n
data: {"html": " world"}\n\n
data: {"html": "!"}\n\n
```

Each event:
- Starts with `data: `
- Contains JSON payload
- Ends with `\n\n` (two newlines)

## ReadableStream Implementation

**Next.js App Router Pattern:**

```typescript
export async function POST(request: NextRequest) {
  const body = await request.json();

  // Call AI provider with streaming
  const aiResponse = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'gpt-4',
      messages: body.messages,
      stream: true,
    }),
  });

  // Create transform stream
  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    async start(controller) {
      const reader = aiResponse.body!.getReader();
      const decoder = new TextDecoder();

      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          const lines = chunk.split('\n').filter(line => line.trim());

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6);
              if (data === '[DONE]') continue;

              const parsed = JSON.parse(data);
              const content = parsed.choices[0]?.delta?.content;

              if (content) {
                // Send SSE format
                const sseMessage = `data: ${JSON.stringify({ html: content })}\n\n`;
                controller.enqueue(encoder.encode(sseMessage));
              }
            }
          }
        }
      } finally {
        controller.close();
      }
    },
  });

  return new NextResponse(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache, no-transform',
      'Connection': 'keep-alive',
    },
  });
}
```

## Proxy Streaming (Drupal)

```typescript
export async function POST(request: NextRequest) {
  const body = await request.json();
  const isStreaming = body.stream === 1;

  const drupalResponse = await fetch(
    `${baseUrl}/api/deepchat?token=${csrfToken}`,
    {
      headers: {
        'Accept': 'text/event-stream',
        'Authorization': `Bearer ${accessToken}`,
      },
      body: JSON.stringify(body),
    }
  );

  // Proxy stream directly
  return new NextResponse(drupalResponse.body, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
```

## Pattern

```typescript
// Reusable streaming helper
async function streamAIResponse(
  provider: 'openai' | 'anthropic',
  messages: any[]
) {
  const encoder = new TextEncoder();

  return new ReadableStream({
    async start(controller) {
      const response = await callAIProvider(provider, messages);
      const reader = response.body!.getReader();
      const decoder = new TextDecoder();

      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          const content = extractContent(provider, chunk);

          if (content) {
            controller.enqueue(
              encoder.encode(`data: ${JSON.stringify({ html: content })}\n\n`)
            );
          }
        }
      } catch (error) {
        controller.enqueue(
          encoder.encode(`data: ${JSON.stringify({ error: error.message })}\n\n`)
        );
      } finally {
        controller.close();
      }
    },
  });
}
```

## Common Mistakes

- **Wrong**: Not setting `Content-Type: text/event-stream` → **Right**: Set header so browser recognizes as SSE
- **Wrong**: Missing `\n\n` after each event → **Right**: DeepChat requires double newline to parse events correctly
- **Wrong**: Not encoding text before enqueuing → **Right**: Use `TextEncoder().encode()` to avoid `TypeError`
- **Wrong**: Forgetting to close controller → **Right**: Always call `controller.close()` in finally block
- **Wrong**: Not handling stream errors → **Right**: Client waits forever. Always close on error
- **Wrong**: Using `cache: 'force-cache'` → **Right**: Streaming won't work. Set `Cache-Control: no-cache`
- **Wrong**: Not checking `stream: true` in request → **Right**: Backend may send JSON instead of SSE

## See Also

- [AI Provider Integration](ai-provider-integration.md)
- [Best Practices](best-practices.md)
- Reference: https://upstash.com/blog/sse-streaming-llm-responses
- Reference: https://www.eaures.online/streaming-llm-responses-in-next-js
- Reference: https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream
