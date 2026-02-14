---
description: You need to decide how to store, retrieve, or transfer editor content.
---

## 4.2 Content Formats & Serialization

### When to Use
You need to decide how to store, retrieve, or transfer editor content.

### Decision
| Format | Use When... | Pros | Cons |
|---|---|---|---|
| JSON | Storing in database, API transfers, version control | Structured, type-safe, lossless, diff-friendly | Larger payload |
| HTML | Rendering to end users, email, legacy systems | Human-readable, portable, SEO-friendly | Lossy, XSS risk |
| Markdown | Git workflows, plain text editing | Simple, portable, readable | Limited features |
| Plain Text | Search indexing, character count, previews | Universal, fast | No formatting |

### Pattern
```typescript
// Get content in different formats
const json = editor.getJSON() // Recommended for storage
const html = editor.getHTML() // Recommended for display
const text = editor.getText({ blockSeparator: '\n\n' })

// Set content
editor.commands.setContent('<p>HTML content</p>')
editor.commands.setContent({
  type: 'doc',
  content: [
    { type: 'paragraph', content: [{ type: 'text', text: 'JSON content' }] }
  ]
})

// Example JSON structure
{
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "attrs": { "textAlign": "center" },
      "content": [
        { "type": "text", "text": "Hello, " },
        { "type": "text", "text": "world", "marks": [{ "type": "bold" }] }
      ]
    }
  ]
}
```

### Common Mistakes
- Storing HTML in database → JSON is safer, structured, and lossless; HTML risks XSS
- Not sanitizing HTML output → Always sanitize before rendering to users (see 18.1 Security)
- Using `getHTML()` for content comparison → HTML changes with style/class updates; use `getJSON()` for diffs
- Expecting Markdown to preserve all formatting → Tiptap JSON → Markdown is lossy (no custom attributes)
- Storing plain text for editable content → You lose all formatting; use JSON

### See Also
- → 11.1 Serialization Patterns | Advanced serialization
- → 18.1 Security Model | HTML sanitization
- Reference: https://tiptap.dev/docs/guides/output-json-html

