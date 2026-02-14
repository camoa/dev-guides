---
description: Framework-agnostic web component for AI chat interfaces with built-in streaming, file upload, and voice features
---

# DeepChat Overview

## When to Use

> Use DeepChat when you need a drop-in chat widget with minimal configuration. Use Chatbot UI or Vercel AI Chat when you need full control over UI/UX.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Drop-in chat widget | DeepChat | Minimal config, framework-agnostic |
| Full control over UI/UX | Chatbot UI or Vercel AI Chat | Direct access to React components |
| Multi-provider AI SDK | Vercel AI Chat | Built on Vercel AI SDK |
| Quick prototype | DeepChat | Fastest setup |
| Complex custom UI | Custom build or Chatbot UI | No shadow DOM constraints |
| Voice features | DeepChat | Built-in TTS/STT |
| Decoupled Drupal | DeepChat | Works well with Drupal AI module |

## What is DeepChat?

DeepChat is a framework-agnostic web component for building AI chat interfaces. It's a fully customizable chat UI that can connect to any API with minimal configuration.

**Core Features:**

- Web component (works with any framework)
- Built-in streaming support (SSE, WebSocket)
- File upload/drag-and-drop
- Markdown rendering
- Speech-to-text/text-to-speech
- Customizable styling (shadow DOM with CSS variables)
- Direct AI provider connections (OpenAI, Anthropic, Azure)
- Focus mode, history management, avatars
- TypeScript support

## Comparison with Alternatives

| Feature | DeepChat | Chatbot UI | Vercel AI Chat |
|---------|----------|------------|----------------|
| **Framework** | Web component (any) | Next.js | Next.js |
| **Installation** | npm package | Clone/fork | Template |
| **Styling** | Shadow DOM + CSS vars | Full control | Full control |
| **Streaming** | Built-in SSE/WebSocket | Manual | AI SDK |
| **API Integration** | Any API | Any API | AI SDK providers |
| **File Upload** | Built-in | Manual | Manual |
| **Voice** | Built-in TTS/STT | Manual | Manual |
| **Customization** | Props/CSS vars | Full codebase | Full codebase |
| **Learning Curve** | Low (props) | Medium (React) | Medium (AI SDK) |
| **Use Case** | Drop-in widget | Full app | Full app |

## Pattern

```tsx
// Minimal DeepChat setup (5 lines)
import { DeepChat } from 'deep-chat-react';

<DeepChat
  connect={{ url: '/api/chat', method: 'POST' }}
  style={{ borderRadius: '8px' }}
/>
```

## Common Mistakes

- **Wrong**: Using DeepChat when you need pixel-perfect custom UI → **Right**: Use custom React components instead. Shadow DOM limits styling
- **Wrong**: Not using dynamic import in Next.js → **Right**: Always use `next/dynamic` with `ssr: false` to avoid SSR errors
- **Wrong**: Expecting same flexibility as headless libraries → **Right**: DeepChat is opinionated. Use Vercel AI SDK for full control
- **Wrong**: Ignoring web component lifecycle → **Right**: DeepChat is a custom element, not a React component. Use refs and methods, not props for everything
- **Wrong**: Assuming DeepChat handles auth → **Right**: It doesn't. You must implement auth in your API routes

## See Also

- [Installation](installation.md)
- [Connect Configuration](connect-configuration.md)
- Reference: https://github.com/OvidijusParsiunas/deep-chat
- Reference: https://deepchat.dev/docs/connect/
