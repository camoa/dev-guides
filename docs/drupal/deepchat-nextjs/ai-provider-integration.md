---
description: Direct OpenAI and Anthropic API integration with streaming support for DeepChat
---

# AI Provider Integration

## When to Use

> Use Drupal AI module when available. Use direct provider integration for simple Next.js apps. Abstract with provider interface for multiple providers.

## Decision

| Scenario | Pattern |
|----------|---------|
| Drupal AI module | Let Drupal handle provider integration |
| Simple Next.js app | Direct provider integration |
| Multiple providers | Abstract with provider interface |
| Custom models | Implement compatible API wrapper |

## OpenAI Integration

**Direct OpenAI (No Drupal):**

```typescript
// app/api/chat/route.ts
export async function POST(request: NextRequest) {
  const body = await request.json();
  const lastMessage = body.messages[body.messages.length - 1];

  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'gpt-4',
      messages: body.messages.map(m => ({
        role: m.role === 'ai' ? 'assistant' : 'user',
        content: m.text,
      })),
      stream: body.stream === 1,
    }),
  });

  if (body.stream === 1) {
    // Stream response (see streaming guide)
    return streamOpenAIResponse(response);
  }

  const data = await response.json();
  return NextResponse.json({
    html: data.choices[0].message.content,
  });
}
```

**OpenAI Streaming:**

```typescript
async function streamOpenAIResponse(response: Response) {
  const encoder = new TextEncoder();
  const decoder = new TextDecoder();

  const stream = new ReadableStream({
    async start(controller) {
      const reader = response.body!.getReader();

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

              try {
                const parsed = JSON.parse(data);
                const content = parsed.choices[0]?.delta?.content;

                if (content) {
                  const sseMessage = `data: ${JSON.stringify({ html: content })}\n\n`;
                  controller.enqueue(encoder.encode(sseMessage));
                }
              } catch (e) {
                // Skip invalid JSON
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
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
```

## Anthropic Integration

**Direct Anthropic:**

```typescript
export async function POST(request: NextRequest) {
  const body = await request.json();

  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'x-api-key': process.env.ANTHROPIC_API_KEY!,
      'anthropic-version': '2023-06-01',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 1024,
      messages: body.messages.map(m => ({
        role: m.role === 'ai' ? 'assistant' : 'user',
        content: m.text,
      })),
      stream: body.stream === 1,
    }),
  });

  if (body.stream === 1) {
    return streamAnthropicResponse(response);
  }

  const data = await response.json();
  return NextResponse.json({
    html: data.content[0].text,
  });
}
```

**Anthropic Streaming:**

```typescript
async function streamAnthropicResponse(response: Response) {
  const encoder = new TextEncoder();
  const decoder = new TextDecoder();

  const stream = new ReadableStream({
    async start(controller) {
      const reader = response.body!.getReader();

      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          const lines = chunk.split('\n').filter(line => line.trim());

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6);

              try {
                const parsed = JSON.parse(data);

                if (parsed.type === 'content_block_delta') {
                  const content = parsed.delta?.text;
                  if (content) {
                    const sseMessage = `data: ${JSON.stringify({ html: content })}\n\n`;
                    controller.enqueue(encoder.encode(sseMessage));
                  }
                }
              } catch (e) {
                // Skip invalid JSON
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
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
```

## Pattern

```typescript
// Provider abstraction
interface AIProvider {
  sendMessage(messages: any[], stream: boolean): Promise<Response>;
}

class OpenAIProvider implements AIProvider {
  async sendMessage(messages: any[], stream: boolean) {
    return fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'gpt-4',
        messages,
        stream,
      }),
    });
  }
}

class AnthropicProvider implements AIProvider {
  async sendMessage(messages: any[], stream: boolean) {
    return fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'x-api-key': process.env.ANTHROPIC_API_KEY!,
        'anthropic-version': '2023-06-01',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'claude-3-5-sonnet-20241022',
        max_tokens: 1024,
        messages,
        stream,
      }),
    });
  }
}
```

## Common Mistakes

- **Wrong**: Exposing API keys client-side → **Right**: **NEVER** put API keys in frontend code. Always use server routes
- **Wrong**: Not handling rate limits → **Right**: Implement exponential backoff and error handling
- **Wrong**: Forgetting to transform message roles → **Right**: OpenAI uses 'assistant', DeepChat uses 'ai'. Map correctly
- **Wrong**: Not validating API key presence → **Right**: Check `process.env.OPENAI_API_KEY` exists before calling
- **Wrong**: Mixing streaming formats → **Right**: OpenAI and Anthropic have different SSE formats. Parse correctly
- **Wrong**: Not handling stream errors → **Right**: Streams can fail mid-response. Always close gracefully

## See Also

- [Streaming Responses](streaming-responses.md)
- [Security](security.md)
- Reference: https://platform.openai.com/docs/guides/streaming-responses
- Reference: https://docs.anthropic.com/en/api/messages-streaming
