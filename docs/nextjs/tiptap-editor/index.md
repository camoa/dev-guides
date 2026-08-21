---
description: TipTap Editor guides for React, Next.js, and Drupal integration
tracks:
  - project: tiptap
    registry: npm
    channel: stable
    declared: "2.x"
    verified: 2026-02-14
guide-meta:
  concepts:
    - Tiptap v2
    - ProseMirror
    - rich text editor
    - Tiptap extensions
    - node extensions
    - mark extensions
    - custom commands
    - node views
    - bubble menu
    - floating menu
    - collaborative editing
  not:
    - CKEditor (Drupal core)
    - Quill.js
    - DeepChat (see nextjs/deepchat-nextjs)
  requires: []
  complements:
    - nextjs/next-drupal
    - design-systems/react-design-system
  specializes: ""
  category: nextjs
---

# TipTap Editor

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Decide if Tiptap is right for my project | [Tiptap Overview](tiptap-overview.md) | You need to choose a rich text editor framework for a React/Next.js application or headless CMS integration. |
| Compare Tiptap vs Lexical vs Slate | [Editor Comparison](editor-comparison.md) | You need to make an informed decision between Tiptap, Lexical, and Slate based on specific project requirements. |
| Install Tiptap in a Next.js project | [Installation](installation.md) | You need to install Tiptap in a JavaScript/TypeScript project. |
| Set up the editor with React | [React Integration](react-integration.md) | You're integrating Tiptap into a React or Next.js application. |
| Avoid SSR hydration errors in Next.js | [React Integration](react-integration.md), [Next.js Setup](nextjs-setup.md) | You're integrating Tiptap into a React or Next.js application. |
| Understand the ProseMirror foundation | [ProseMirror Foundation](prosemirror-foundation.md) | You need to understand Tiptap's underlying architecture to build custom extensions or debug complex issues. |
| Define custom document schemas | [Schema Architecture](schema-architecture.md) | You need to define or customize the document structure rules (which nodes can contain which children, which marks are allowed). |
| Configure the editor instance | [Editor Configuration](editor-configuration.md) | You need to configure editor instance behavior, initial content, autofocus, editability, or event handlers. |
| Choose content format (HTML vs JSON) | [Content Formats](content-formats.md) | You need to decide how to store, retrieve, or transfer editor content. |
| Add paragraph, heading, and other content nodes | [Document Structure Nodes](node-extensions-structure.md), [Content Nodes](node-extensions-content.md) | You need the foundational nodes required for any Tiptap document: Document, Paragraph, Text. |
| Add images and media nodes | [Media Nodes](node-extensions-media.md) | You need images, tables, code blocks, or other rich content types. |
| Add bold, italic, and basic marks | [Basic Mark Extensions](mark-extensions-basic.md) | You need inline text formatting: bold, italic, underline, strikethrough. |
| Add link marks | [Link Mark Extension](mark-extensions-link.md) | You need hyperlinks with URL validation and target control. |
| Add advanced marks (highlight, code) | [Advanced Mark Extensions](mark-extensions-advanced.md) | You need background highlighting, text colors, font sizes, or custom text styling. |
| Enable history, placeholder, character count | [StarterKit Extensions](functionality-extensions-starter.md), [Utility Extensions](functionality-extensions-utility.md) | You need a complete set of common extensions without installing each individually. |
| Add dropCursor, gapCursor | [UI Extensions](functionality-extensions-ui.md) | You need context-aware UI elements: selection menus, slash commands, or floating toolbars. |
| Work with history and undo/redo | [History Extension](functionality-extensions-history.md) | You need undo/redo functionality for user edits. |
| Create a custom extension | [Custom Extension Architecture](custom-extension-architecture.md) | You need to create a new extension type (node, mark, or functionality) not provided by built-in extensions. |
| Add markdown-style input rules | [Input Rules](custom-extension-input-rules.md) | You need Markdown-style shortcuts (e.g., `**bold**` converts to bold) or custom paste handling. |
| Create custom node views with React | [Node Views](custom-extension-node-views.md) | You need custom DOM rendering for a node: interactive widgets, React components, or complex layouts. |
| Execute editor commands | [Commands API](commands-api.md) | You need to programmatically modify editor content, selection, or state. |
| Create custom commands | [Custom Commands](custom-commands.md) | You need to create reusable command logic for your extensions or application. |
| Handle editor events (onUpdate, onFocus) | [Editor Events](editor-events.md) | You need to react to editor state changes: content updates, selection changes, focus/blur, etc. |
| Optimize event handling | [Event Optimization](event-optimization.md) | You need to optimize expensive operations triggered by editor events (auto-save, API calls, analytics). |
| Store content as HTML or JSON | [Serialization Patterns](serialization-patterns.md) | You need to export editor content to different formats, transform content, or integrate with external systems. |
| Build a bubble menu | [Bubble Menu](ui-bubble-menu.md) | You need a selection-based menu (appears on text selection) or context menu (right-click). |
| Build a floating menu | [Floating Menu](ui-floating-menu.md) | You need a menu that appears in empty blocks or triggered by `/` (slash commands). |
| Build a toolbar | [Toolbar](ui-toolbar.md) | You need a persistent toolbar (always visible, not context-dependent). |
| Integrate with Next.js App Router | [Next.js Setup](nextjs-setup.md) | You're integrating Tiptap into a Next.js application (App Router or Pages Router). |
| Handle Next.js API routes | [Next.js API Integration](nextjs-api-integration.md) | You need to save/load Tiptap content via Next.js API routes. |
| Connect to Drupal JSON API | [Drupal JSON API](drupal-json-api.md) | You're building a decoupled Drupal frontend with Next.js and need to edit Drupal content via Tiptap. |
| Enable collaborative editing with Y.js | [Collaboration Architecture](collaboration-architecture.md) | You need real-time collaborative editing (multiple users editing simultaneously, like Google Docs). |
| Set up Hocuspocus collaboration server | [Hocuspocus Server](hocuspocus-server.md) | You're self-hosting collaborative editing with Y.js and need a WebSocket server. |
| Style the editor with CSS | [Styling Approach](styling-approach.md) | You need to style the editor content, UI elements, or integrate with a design system. |
| Implement dark mode | [Dark Mode](dark-mode.md) | You need to support light and dark themes. |
| Optimize React performance | [React Performance](react-performance.md) | Your editor re-renders too frequently, causing lag or poor UX. |
| Optimize NodeView performance | [NodeView Performance](nodeview-performance.md) | You have React node views and experiencing performance issues. |
| Prevent XSS attacks | [Security Model](security-model.md) | You're storing or displaying user-generated content from Tiptap. |
| Test custom extensions | [Testing Strategy](testing-strategy.md) | You're building custom extensions or complex editor logic and need automated tests. |
| Avoid common mistakes | [Anti-Patterns](anti-patterns.md) | You need to avoid common pitfalls and bad practices. |
| Find code examples and references | [Code Reference](code-reference.md) | You need quick reference to key Tiptap packages, classes, and imports. |
| Access official documentation | [Sources and Maintenance](sources-maintenance.md) |  |
