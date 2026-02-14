---
description: You need to configure editor instance behavior, initial content, autofocus, editability, or event handlers.
---

## 4.1 Editor Configuration Options

### When to Use
You need to configure editor instance behavior, initial content, autofocus, editability, or event handlers.

### Configuration Categories

#### Core Settings
```typescript
new Editor({
  element: document.querySelector('.editor'), // Mount point (not needed in React)
  extensions: [StarterKit], // Required
  content: '<p>Initial content</p>', // HTML or JSON
  editable: true, // Read-only if false
  autofocus: 'end', // 'start' | 'end' | 'all' | number | true | false
  injectCSS: true, // Include default ProseMirror styles
  enableContentCheck: true, // Validate schema (required for production)
  immediatelyRender: false, // SSR compatibility (React/Next.js)
})
```

#### Advanced Settings
```typescript
new Editor({
  editorProps: {
    attributes: {
      class: 'prose prose-sm focus:outline-none',
      'data-testid': 'editor',
    },
    transformPastedText(text) {
      return text.trim() // Clean pasted text
    },
  },
  parseOptions: {
    preserveWhitespace: 'full', // Don't collapse whitespace
  },
  enableInputRules: true, // Allow markdown-style input (e.g., `**bold**`)
  enablePasteRules: true, // Allow markdown-style paste
  injectNonce: 'your-nonce', // CSP nonce for injected styles
})
```

### Common Mistakes
- Setting `element` in React → Use `<EditorContent editor={editor} />` instead
- Not setting `enableContentCheck: true` → Silent schema violations in production
- Using `autofocus: true` in modals → Steals focus from modal triggers; use conditional autofocus
- Disabling `injectCSS` without custom styles → Editor becomes unusable (invisible cursor, no selection)
- Overriding `editorProps` after initialization → Use `editor.setOptions()` to update
- Forgetting `parseOptions.preserveWhitespace` for code editors → Whitespace collapses in `<pre>` blocks

### See Also
- → 4.2 Content Formats | HTML vs JSON
- → 10.1 Editor Events | Event handlers
- Reference: https://tiptap.dev/docs/editor/api/editor

