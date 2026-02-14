---
description: You need to export editor content to different formats, transform content, or integrate with external systems.
---

## 11.1 Content Serialization & Export Patterns

### When to Use
You need to export editor content to different formats, transform content, or integrate with external systems.

### Pattern
```typescript
// JSON (recommended for storage)
const json = editor.getJSON()
localStorage.setItem('content', JSON.stringify(json))

// HTML (for display)
const html = editor.getHTML()
document.querySelector('.preview').innerHTML = html

// Plain text (for search indexing)
const text = editor.getText({ blockSeparator: '\n\n' })
indexForSearch(text)

// Custom serialization
import { getHTMLFromFragment } from '@tiptap/core'

const customHTML = getHTMLFromFragment(
  editor.state.doc.content,
  editor.schema
)

// Server-side rendering (Node.js)
import { generateHTML, generateJSON } from '@tiptap/html'
import StarterKit from '@tiptap/starter-kit'

const html = generateHTML(jsonContent, [StarterKit])
const json = generateJSON(htmlContent, [StarterKit])
```

### Decision
| Format | Store? | Display? | Transfer? | Why |
|---|---|---|---|---|
| JSON | ✓ Best | ✗ No | ✓ Best | Lossless, structured, versioned |
| HTML | ✗ Avoid | ✓ Best | △ OK | XSS risk, lossy on re-parse |
| Text | ✗ No | ✗ No | ✗ No | Search index only |
| Markdown | △ Maybe | ✗ No | △ OK | Limited features, portable |

### Common Mistakes
- Storing HTML in database → Use JSON; HTML is lossy and risks XSS
- Not sanitizing HTML output → XSS vulnerability; sanitize before rendering
- Comparing HTML for change detection → HTML changes with class/style; use JSON
- Serializing on every update → Expensive; debounce serialization
- Not handling serialization errors → Invalid content throws errors; wrap in try/catch

### See Also
- → 4.2 Content Formats | Format comparison
- → 18.1 Security Model | HTML sanitization
- Reference: https://tiptap.dev/docs/guides/output-json-html

