---
description: AI Chatbot module — DeepChat frontend, REST API endpoints, streaming, ChatProcessor plugins, and authentication flow
tldr: "Integrate DeepChat as a Drupal block or call its REST API from decoupled frontends; always fetch CSRF token first. New in 1.4: ChatProcessorInterface is the stable contract for any chat UI; extend ChatProcessorBase."
drupal_version: "11.x"
---

# AI Chatbot (DeepChat)

## When to Use

> Use this guide when integrating the DeepChat chatbot frontend with Drupal. Use [AI Assistant API](ai-assistant-api.md) when building the backend assistant logic or custom actions.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Embed chatbot in Drupal page | `ai_deepchat_block` block | No custom code; configure in block UI |
| Call from decoupled frontend | REST API with CSRF flow | Session-based; requires `credentials: 'include'` |
| Toolbar chatbot button | Set `placement: toolbar` on block | `hook_toolbar()` registers automatically |
| Reset conversation | `/ajax/chatbot/reset-session/{id}/{thread}` | Flood-protected: 3 resets per session |
| Custom chat front-end (Slack bot, etc.) | Implement `ChatProcessorInterface` | Stable API contract for any UI to back-end |

## Pattern

```javascript
// 1. Get CSRF token.
const sessionRes = await fetch('/api/deepchat/session', {
  method: 'POST',
  credentials: 'include',
});
const csrfToken = await sessionRes.text();

// 2. Send message with token.
const chatRes = await fetch(`/api/deepchat?token=${csrfToken}`, {
  method: 'POST',
  credentials: 'include',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    assistant_id: 'my_assistant',
    stream: 0,
    messages: [{ role: 'user', text: 'Hello' }],
  }),
});
const data = await chatRes.json();
// data.html contains sanitized response.
```

## REST API Endpoints

| Endpoint | Method | Permission |
|----------|--------|------------|
| `/api/deepchat/session` | POST | `access deepchat api` |
| `/api/deepchat` | POST | `access deepchat api` + CSRF |
| `/ajax/chatbot/reset-session/{id}/{thread}` | POST | `access deepchat api` |

## API Request Format

```json
{
  "assistant_id": "my_assistant",
  "thread_id": "optional-uuid",
  "stream": 1,
  "messages": [{"role": "user", "text": "Hello"}],
  "contexts": {"current_route": "/node/1"},
  "structured_results": false,
  "show_copy_icon": true,
  "verbose_mode": false
}
```

**Streamed response (SSE):** Each chunk is `data: {"html": "...", "overwrite": true}`. Final chunk includes `"should_continue"`. When `should_continue: true`, the agent called a tool and the frontend automatically re-requests.

## Block Settings

| Setting | Type | Description |
|---------|------|-------------|
| `ai_assistant` | string | Assistant entity ID |
| `stream` | integer | Enable SSE streaming |
| `placement` | string | `sticky`, `toolbar`, or inline |
| `toggle_state` | string | `remember`, `open`, `close` |
| `verbose_mode` | boolean | Show intermediate agent steps |
| `show_structured_results` | boolean | Show action results under messages |
| `style_file` | string | Custom DeepChat YAML theme path |

## XSS Sanitization

All LLM output is sanitized with `Xss::filter()`. Allowed tags: `<a>`, `<b>`, `<br>`, `<code>`, `<em>`, headings, `<li>`, `<ol>`, `<p>`, `<pre>`, `<span>`, `<strong>`, `<table>` elements, `<ul>`, `<img>`, `<details>`, `<summary>`.

## ChatProcessor Plugins (New in 1.4)

`ChatProcessorInterface` (`#[ChatProcessor]` attribute, manager `plugin.manager.ai.chat_processor`) is the stable contract between any chat UI and the Drupal-side generation logic. It lets contrib ship alternative chat frontends (e.g., Slack bot, CLI) against a consistent API without coupling to the DeepChat block.

Key methods: `setInput(ChatInput)` / `getInput()`, `setOutput(ChatOutput)` / `getOutput()`, `doExecute(): ChatOutput` (custom processing logic), `execute(): ChatOutput` (validates input, calls `doExecute()`, stores output). Extend `ChatProcessorBase` (`Drupal\ai\Base\ChatProcessorBase`) rather than implementing the interface directly.

## Hooks

```php
hook_deepchat_settings(array &$deepchat_settings)  // Alter DeepChat component attributes
hook_deepchat_buttons_alter(array &$buttons)        // Add/alter per-message buttons
hook_deepchat_prepend_message($message, $type, $assistant_id, $thread_id)
```

## Common Mistakes

- **Wrong**: Calling API without `credentials: 'include'` → **Right**: Session-based history requires cookies
- **Wrong**: Missing CSRF token in request → **Right**: Fetch token from `/api/deepchat/session` first
- **Wrong**: Building infinite retry on reset → **Right**: Flood protection allows only 3 resets per session

## See Also

- [AI Assistant API](ai-assistant-api.md)
- [Security](security.md)
- Reference: `web/modules/contrib/ai/modules/ai_chatbot/`
