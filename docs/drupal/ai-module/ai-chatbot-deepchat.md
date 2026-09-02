---
description: AI Chatbot module — DeepChat frontend, REST API endpoints, streaming, ChatProcessor plugins, and authentication flow
tldr: "Integrate DeepChat as a Drupal block or call its REST API from decoupled frontends; always fetch CSRF token first. New in 1.4: ChatProcessorInterface is the stable contract for any chat UI; extend ChatProcessorBase."
drupal_version: "11.x"
---

# AI Chatbot (DeepChat)

## When to Use

> Use this guide when integrating the DeepChat chatbot frontend with Drupal. Use [AI Assistant API](ai-assistant-api.md) when building the backend assistant logic or custom actions.

The `ai_chatbot` module provides the frontend for AI assistants: blocks, a REST API, and toolbar integration. It uses the [DeepChat](https://deepchat.dev/) web component.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Embed chatbot in Drupal page | `ai_deepchat_block` block | No custom code; configure in block UI |
| Call from decoupled frontend | REST API with CSRF flow | Session-based; requires `credentials: 'include'` |
| Toolbar chatbot button | Set `placement: toolbar` on block | `hook_toolbar()` registers automatically |
| Reset conversation | `/ajax/chatbot/reset-session/{id}/{thread}` | Flood-protected: 3 resets per session |
| Custom chat front-end (Slack bot, etc.) | Implement `ChatProcessorInterface` | Stable API contract for any UI to back-end |

## Dependencies

- `ai_assistant_api` (required)
- `league/commonmark` (optional, for Markdown rendering)

## REST API Endpoints

| Endpoint | Method | Purpose | Permission |
|----------|--------|---------|------------|
| `/api/deepchat/session` | POST | Get CSRF token (plain text) | `access deepchat api` |
| `/api/deepchat` | POST | Send/receive messages | `access deepchat api` + CSRF |
| `/ajax/chatbot/reset-session/{assistant_id}/{thread_id}` | POST | Reset conversation (flood-protected: 3/session) | `access deepchat api` |
| `/ajax/chatbot/message-skeleton/{assistant_id}/{thread_id}/{user}` | GET | Get message HTML skeleton | `access deepchat api` |

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

## API Response Format

**Non-streamed:**

```json
{"html": "<p>Response</p>", "should_continue": false}
```

**Streamed (SSE):**

```
data: {"html": "<p>partial</p>", "overwrite": true}\n\n
```

Each SSE chunk is a `data:` line with JSON containing `html` (the accumulated HTML so far) and `overwrite: true` (the client replaces the previous content rather than appending). The final chunk includes `should_continue`.

`should_continue: true` means the assistant called a tool and needs another round-trip — the frontend automatically re-requests.

## Authentication Flow (for decoupled frontends)

```javascript
// 1. Get CSRF token
const sessionRes = await fetch('/api/deepchat/session', {
  method: 'POST',
  credentials: 'include',
});
const csrfToken = await sessionRes.text();

// 2. Send message with token
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
// data.html contains sanitized response
```

## Block Configuration (`ai_deepchat_block`)

| Setting | Type | Description |
|---------|------|-------------|
| `ai_assistant` | string | Assistant entity ID |
| `bot_name` | string | Display name |
| `bot_image` | text | Avatar URL |
| `first_message` | text | Initial bot greeting |
| `stream` | integer | Enable SSE streaming |
| `placement` | string | `sticky`, `toolbar`, or inline |
| `toggle_state` | string | `remember`, `open`, `close` |
| `width` / `height` | string | CSS dimensions |
| `style_file` | string | Custom DeepChat YAML theme path |
| `show_structured_results` | boolean | Show action results under messages |
| `show_copy_icon` | boolean | Copy button per message |
| `verbose_mode` | boolean | Show intermediate agent steps |

## XSS Sanitization

The `DeepChatApi` controller sanitizes all LLM output with `Xss::filter()`, allowing only safe HTML tags: `<a>`, `<b>`, `<br>`, `<code>`, `<em>`, `<h1>`-`<h6>`, `<hr>`, `<i>`, `<li>`, `<ol>`, `<p>`, `<pre>`, `<span>`, `<strong>`, `<table>`, `<td>`, `<th>`, `<tr>`, `<ul>`, `<img>`, `<details>`, `<summary>`. All other HTML is stripped.

## Toolbar Integration

When a DeepChat block is placed with `placement: toolbar`, the module implements `hook_toolbar()` to add a toolbar tray. The `ChatbotHooks` service handles toolbar, topbar, and theme suggestions. The toolbar variant uses the `ai-deepchat--toolbar.html.twig` template and the `toolbar.yml` style file.

## DeepChat Theme Files

Place `.yml` files in `{theme}/deepchat_styles/` or `{module}/deepchat_styles/`. Bundled: `bard.yml`, `bing.yaml`, `chatgpt.yml`, `toolbar.yml`.

## Hooks

```php
hook_deepchat_settings(array &$deepchat_settings)  // Alter DeepChat component attributes
hook_deepchat_buttons_alter(array &$buttons)        // Add/alter per-message buttons
hook_deepchat_prepend_message($message, $type, $assistant_id, $thread_id) // Prepend to responses
```

## Setup Steps

1. Enable `ai_chatbot` (enables `ai_assistant_api` automatically)
2. Install `league/commonmark` for Markdown rendering
3. Create an assistant at `/admin/config/ai/ai-assistant`
4. Place the "AI DeepChat Chatbot" block; select assistant, configure placement
5. Grant `access deepchat api` to relevant roles
6. Toolbar button appears automatically when block is placed

## ChatProcessor Plugins (New in 1.4)

`ChatProcessorInterface` (`#[ChatProcessor]` plugin type, manager `plugin.manager.ai.chat_processor`) is the contract between a conversational UI and whatever generates the reply — usually an AI assistant/agent, but it can be any custom logic (naive RAG, an ECA flow, a remote command). It lets contrib ship alternative chat front-ends (e.g. a Slack bot) against a stable Drupal-side API.

Key methods: `setInput(ChatInput)` / `getInput()`, `setOutput(ChatOutput)` / `getOutput()`, `doExecute(): ChatOutput` (the processing logic), `execute(): ChatOutput` (validates input, calls `doExecute()`, stores the output), plus thread-ID management. Extend `ChatProcessorBase` (`Drupal\ai\Base\ChatProcessorBase`) rather than implementing the interface directly.

## Common Mistakes

| Mistake | Why it's wrong |
|---------|---------------|
| Using WebFetch from frontend | Must use proper REST API with CSRF token |
| Not including `credentials: 'include'` | Session-based history requires cookies |
| Forgetting flood protection on reset | 3 attempts per session — design UI accordingly |

## See Also

- [AI Assistant API](ai-assistant-api.md)
- [Security](security.md)
- Reference: `web/modules/contrib/ai/modules/ai_chatbot/`
