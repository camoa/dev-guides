---
description: DeepChat + Next.js integration guides covering setup, API routes, streaming, Drupal backend, and security
tracks:
  - project: deep-chat
    registry: npm
    channel: stable
    declared: "2.3.0"
    verified: 2026-02-14
guide-meta:
  concepts:
    - DeepChat web component
    - DeepChat connect property
    - Next.js API routes
    - SSE streaming
    - DeepChat message formats
    - AI provider integration
    - DeepChat file upload
  not:
    - Drupal AI module (see drupal/ai-content)
    - Tiptap editor (see nextjs/tiptap-editor)
  requires: []
  complements:
    - nextjs/deepchat-drupal-auth
    - nextjs/next-drupal
    - drupal/ai-content
  specializes: ""
  category: nextjs
---

# DeepChat + Next.js

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what DeepChat is and when to use it | [DeepChat Overview](deepchat-overview.md) | Use DeepChat when you need a drop-in chat widget with minimal configuration. Use Chatbot UI or Vercel AI Chat when you need full control over UI/UX. |
| Install and configure DeepChat in Next.js | [Installation & Setup](installation.md) | Use dynamic import with `ssr: false` for all DeepChat instances in Next.js. DeepChat is a web component that requires browser APIs. |
| Configure the connect property and interceptors | [Connect Configuration](connect-configuration.md) | Use `connect` property to define API endpoint and headers. Use interceptors to inject context, track threads, or modify requests/responses. |
| Create Next.js API route handlers | [Next.js API Routes](nextjs-api-routes.md) | Use proxy pattern for Drupal/external backends. Use CSRF flow for Drupal with OAuth + CSRF. |
| Handle CSRF tokens and authentication | [Next.js API Routes](nextjs-api-routes.md) | Use proxy pattern for Drupal/external backends. Use CSRF flow for Drupal with OAuth + CSRF. |
| Implement SSE streaming responses | [Streaming Responses](streaming-responses.md) | Use SSE streaming for AI chat responses. Use ReadableStream with transform for OpenAI/Anthropic. |
| Structure messages and handle history | [Message Formats & History](message-formats.md) | Send only current message + thread_id for Drupal/session backends. Send full history for stateless backends. |
| Integrate with Drupal AI module | [Drupal Backend Integration](drupal-backend.md) | Use Drupal AI module endpoints when ai_chatbot and ai_assistant_api modules are installed. Use CSRF token in query parameter, not header. |
| Connect directly to OpenAI or Anthropic | [AI Provider Integration](ai-provider-integration.md) | Use Drupal AI module when available. Use direct provider integration for simple Next.js apps. |
| Style and theme DeepChat | [Styling & Theming](styling-theming.md) | Use CSS variables for brand colors. Use messageStyles for message bubbles. |
| Upload files and images | [File Upload & Attachments](file-upload.md) | Use `images` for image upload/analysis. Use `mixedFiles` for any file type (PDFs, docs). |
| Add custom request handlers | [Custom Handlers](custom-handlers.md) | Use custom handler for complex request flow or retry logic. Use interceptors for simple transforms. |
| Implement authentication and sessions | [Authentication & Sessions](authentication-sessions.md) | Use NextAuth + Bearer token for user-specific chat. Use OAuth + CSRF flow for Drupal backend. |
| Follow architecture best practices | [Best Practices & Patterns](best-practices.md) | Lazy load when chat not immediately visible. Use error boundaries in production. |
| Prevent XSS attacks and secure the app | [Security](security.md) | Always sanitize AI output on server. Never expose API keys client-side. |
| Avoid common mistakes | [Anti-Patterns & Common Mistakes](anti-patterns.md) | Common mistakes and anti-patterns to avoid in DeepChat + Next.js integration |
