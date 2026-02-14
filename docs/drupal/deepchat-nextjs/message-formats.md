---
description: Message structure, request/response formats, history management, and agent continuation patterns for DeepChat
---

# Message Formats & History

## When to Use

> Send only current message + thread_id for Drupal/session backends. Send full history for stateless backends. Handle `should_continue` loop for agent workflows.

## Decision

| Scenario | Pattern |
|----------|---------|
| Stateless backend | Send full history in `messages` |
| Drupal/session backend | Send only current message + thread_id |
| Agent with tools | Handle `should_continue` loop |
| Persistent history | Use `browserStorage` + backend storage |

## Request Format

```json
{
  "messages": [
    {
      "role": "user",
      "text": "Hello, how are you?"
    }
  ],
  "assistant_id": "my_assistant",
  "thread_id": "uuid-1234",
  "stream": 1,
  "contexts": ["Page: /products/widget"],
  "verbose_mode": false
}
```

## Request Properties

| Property | Type | Required | Purpose |
|----------|------|----------|---------|
| `messages` | array | Yes | Message history (only last is processed) |
| `assistant_id` | string | Backend-specific | AI assistant identifier |
| `thread_id` | string | No | Conversation thread UUID |
| `stream` | number | No | 1 for streaming, 0 for JSON |
| `contexts` | array | No | Additional context data |
| `verbose_mode` | boolean | No | Show agent step messages |

**Important:** Only the **last message** is processed. Previous messages are for display only. Backend stores full history server-side.

## Response Format (JSON)

```json
{
  "html": "<p>I'm doing well, thank you!</p>",
  "thread_id": "uuid-1234",
  "should_continue": false
}
```

## Response Format (SSE)

```
data: {"html": "I'm "}\n\n
data: {"html": "doing "}\n\n
data: {"html": "well!"}\n\n
```

## Response Properties

| Property | Type | Purpose |
|----------|------|---------|
| `html` | string | Rendered response (markdown → HTML) |
| `text` | string | Plain text (alternative to html) |
| `thread_id` | string | Conversation thread UUID |
| `should_continue` | boolean | Agent needs continuation |
| `error` | string | Error message |

## Message with Files

```typescript
// Request (FormData)
const formData = new FormData();
formData.append('message0', JSON.stringify({
  role: 'user',
  text: 'Analyze this image',
}));
formData.append('files', file1);
formData.append('files', file2);

// Response
{
  "html": "I see two images...",
  "files": [
    {
      "name": "analysis.pdf",
      "src": "data:application/pdf;base64,...",
      "type": "any"
    }
  ]
}
```

## History Management

**Client-Side History (Browser Storage):**

```tsx
<DeepChat
  history={[
    { role: 'ai', html: '<p>Hello! How can I help?</p>' },
  ]}
  browserStorage={true} // Auto-save to localStorage
/>
```

**Server-Side History (Recommended for Drupal):**

Backend stores full conversation in session. Frontend only sends current message.

```typescript
// First message
{
  "messages": [{ "role": "user", "text": "Hello" }]
}

// Second message (backend has full history)
{
  "messages": [{ "role": "user", "text": "What's the weather?" }],
  "thread_id": "uuid-1234"
}
```

## Agent Continuation Pattern

```json
// Initial response
{
  "html": "Calling Search Content...<div class='loading'>Processing...</div>",
  "should_continue": true
}

// Frontend continues with dummy message
{
  "messages": [{ "role": "user", "text": "dummy_loading" }],
  "thread_id": "uuid-1234"
}

// Final response
{
  "html": "<p>Here are the search results...</p>",
  "should_continue": false
}
```

**Why "dummy_loading"?**

- Message text is required but ignored during continuation
- Backend recognizes continuation by thread context
- Prevents storing duplicate messages in history

## Pattern

```tsx
// Handling agent continuation
const sendMessage = async (text: string) => {
  let response = await fetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({
      messages: [{ role: 'user', text }],
      thread_id: threadId,
    }),
  }).then(r => r.json());

  // Continue until agent completes
  while (response.should_continue) {
    response = await fetch('/api/chat', {
      method: 'POST',
      body: JSON.stringify({
        messages: [{ role: 'user', text: 'dummy_loading' }],
        thread_id: response.thread_id,
      }),
    }).then(r => r.json());
  }

  return response;
};
```

## Common Mistakes

- **Wrong**: Sending full message history to Drupal backend → **Right**: Backend ignores all but last message. Send only current message to save bandwidth
- **Wrong**: Not tracking thread_id → **Right**: Track thread_id to maintain conversation context
- **Wrong**: Storing thread_id in component state only → **Right**: Use localStorage or URL param so it persists on page refresh
- **Wrong**: Not handling `should_continue` → **Right**: Agent workflow breaks. Frontend must loop until false
- **Wrong**: Using `text` and `html` in same response → **Right**: DeepChat prioritizes `html`. Use one or the other
- **Wrong**: Not sanitizing HTML in `html` field → **Right**: Backend must sanitize to prevent XSS vulnerability

## See Also

- [Drupal Backend Integration](drupal-backend.md)
- [Custom Handlers](custom-handlers.md)
- Reference: `/home/camoa/workspace/claude_memory/skills/drupal-ai/references/deepchat-frontend-integration.md`
