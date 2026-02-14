---
description: You need to define or customize the document structure rules (which nodes can contain which children, which marks are allowed).
---

## 3.2 Schema Architecture & Document Structure

### When to Use
You need to define or customize the document structure rules (which nodes can contain which children, which marks are allowed).

### Decision
| If you need... | Use... | Why |
|---|---|---|
| Standard rich text structure | StarterKit default schema | Covers 90% of use cases |
| Custom node nesting rules | `content` attribute in Node.create() | Defines allowed children (e.g., `'block+'`) |
| Restrict marks in specific nodes | `marks` attribute in Node.create() | Control formatting (e.g., no bold in code blocks) |
| Validate content on load | `enableContentCheck: true` | Catch schema mismatches early |
| Debug schema violations | `onContentError` event | Handle invalid content gracefully |

### Pattern
```typescript
import { Node } from '@tiptap/core'

const CustomNode = Node.create({
  name: 'customBlock',
  content: 'block+', // One or more block nodes
  group: 'block', // This IS a block node
  marks: 'bold italic', // Only allow bold and italic

  parseHTML() {
    return [{ tag: 'div[data-type="custom"]' }]
  },

  renderHTML({ HTMLAttributes }) {
    return ['div', { 'data-type': 'custom', ...HTMLAttributes }, 0]
  },
})

// Enable schema validation
const editor = new Editor({
  extensions: [CustomNode, StarterKit],
  enableContentCheck: true,
  onContentError({ editor, error, disableCollaboration }) {
    console.error('Schema violation:', error)
    editor.setEditable(false) // Prevent further edits
    disableCollaboration() // Avoid syncing bad content
  },
})
```

### Common Content Expressions
```typescript
content: 'block+' // One or more block nodes
content: 'inline*' // Zero or more inline nodes
content: 'text*' // Only text
content: '(paragraph|heading)+' // Paragraphs or headings
content: 'heading block+' // Heading followed by blocks
```

### Common Mistakes
- Not enabling `enableContentCheck` in production → Invalid content silently breaks collaboration
- Allowing all marks everywhere (`marks: '_'`) → Security risk (XSS); restrict marks explicitly
- Creating circular content dependencies → `content: 'customBlock*'` in customBlock causes infinite nesting
- Forgetting Document and Paragraph nodes → Tiptap requires top-level Doc and at least one block node
- Pasting HTML without schema match → Content is stripped; listen to `contentError` to handle

### See Also
- ← 3.1 ProseMirror Foundation | Core concepts
- → 5.1 Document Structure Nodes | Built-in nodes
- Reference: https://tiptap.dev/docs/editor/core-concepts/schema

