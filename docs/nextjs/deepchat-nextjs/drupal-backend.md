---
description: Drupal AI module integration with DeepChat including session management, CSRF flow, and assistant configuration
---

# Drupal Backend Integration

## When to Use

> Use Drupal AI module endpoints when ai_chatbot and ai_assistant_api modules are installed. Use CSRF token in query parameter, not header.

## Decision

| Scenario | Pattern |
|----------|---------|
| Drupal AI module installed | Use Drupal endpoints |
| Custom Drupal backend | Implement compatible API |
| Non-Drupal backend | Skip CSRF, use direct auth |
| Multiple AI providers | Configure per assistant |

## Architecture

```
DeepChat (frontend)
    ↓
Next.js API Route (/api/chat)
    ↓
Drupal /api/deepchat?token=<csrf>
    ↓
ai_chatbot module (DeepChatApi controller)
    ↓
ai_assistant_api module (AiAssistantApiRunner service)
    ↓
AI Provider (OpenAI, Anthropic, etc.)
```

## Drupal Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/deepchat/session` | POST | Create session, return CSRF token |
| `/api/deepchat?token=<csrf>` | POST | Process chat message |
| `/ajax/chatbot/reset-session/{assistant_id}/{thread_id}` | POST | Reset conversation |

## Required Permission

```php
// User must have this permission
'access deepchat api'
```

## Session Flow

**1. Initialize Session:**

```typescript
// Next.js calls Drupal session endpoint
const response = await fetch(`${drupalUrl}/api/deepchat/session`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
  },
});

const csrfToken = await response.text(); // Plain text!
```

**2. Send Message:**

```typescript
const chatResponse = await fetch(
  `${drupalUrl}/api/deepchat?token=${csrfToken}`,
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
    },
    body: JSON.stringify({
      assistant_id: 'site_helper',
      messages: [{ role: 'user', text: 'Hello' }],
      stream: 1,
    }),
  }
);
```

## Backend Storage

All conversation history stored in Drupal's PrivateTempStore:

```php
// Backend storage structure
PrivateTempStore: 'ai_assistant_api'
├── {thread_id}
│   ├── messages: [
│   │   {role: 'user', message: '...', timestamp: 123456},
│   │   {role: 'assistant', message: '...', timestamp: 123457}
│   │ ]
│   ├── created: 1234567890
```

**History expires with PHP session (~24 hours).**

## AI Assistant Configuration

**AI Assistant Entity Fields:**

| Field | Purpose |
|-------|---------|
| `id` | Machine name (e.g., 'site_helper') |
| `label` | Display name |
| `provider` | AI provider (openai, anthropic, etc.) |
| `model_id` | Model (gpt-4, claude-3-opus, etc.) |
| `system_prompt` | Base instructions |
| `temperature` | Randomness (0-2) |
| `max_tokens` | Response length limit |
| `history_context_length` | Messages to send (pairs) |
| `allow_history` | none, session_one_thread, session |

**Example Configuration:**

```yaml
# Assistant: site_helper
provider: openai
model_id: gpt-4
system_prompt: "You are a helpful assistant..."
temperature: 0.7
max_tokens: 1000
history_context_length: 5  # Send 11 messages (5 pairs + current)
allow_history: session      # Persist per session
```

## Pattern

```typescript
// Reusable Drupal chat client
class DrupalChatClient {
  private baseUrl: string;
  private csrfToken: string | null = null;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  async initialize(accessToken: string) {
    const response = await fetch(`${this.baseUrl}/api/deepchat/session`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${accessToken}` },
    });
    this.csrfToken = await response.text();
  }

  async sendMessage(
    assistantId: string,
    message: string,
    threadId?: string,
    options: { stream?: boolean; contexts?: string[] } = {}
  ) {
    const response = await fetch(
      `${this.baseUrl}/api/deepchat?token=${this.csrfToken}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          assistant_id: assistantId,
          messages: [{ role: 'user', text: message }],
          thread_id: threadId,
          stream: options.stream ? 1 : 0,
          contexts: options.contexts,
        }),
      }
    );

    return options.stream ? response.body : response.json();
  }
}
```

## Common Mistakes

- **Wrong**: Using different Bearer tokens for session and chat → **Right**: Token must be identical to avoid session mismatch
- **Wrong**: Expecting JSON from session endpoint → **Right**: Returns plain text. Use `response.text()`, not `response.json()`
- **Wrong**: Not URL-encoding CSRF token → **Right**: Use `encodeURIComponent()` as token may contain special characters
- **Wrong**: Sending CSRF in header → **Right**: Drupal expects query parameter: `?token=<csrf>`
- **Wrong**: Not starting PHP session → **Right**: OAuth doesn't auto-create session. Backend must call `$session->start()`
- **Wrong**: Caching CSRF token across users → **Right**: Token is user-specific. Never share

## See Also

- [Next.js API Routes](nextjs-api-routes.md)
- [Authentication & Sessions](authentication-sessions.md)
- Reference: `/home/camoa/workspace/claude_memory/skills/drupal-ai/references/deepchat-backend.md`
- Reference: Drupal AI module at `~/workspace/contrib/web/modules/contrib/ai/`
