---
description: You need the foundational nodes required for any Tiptap document: Document, Paragraph, Text.
---

## 5.1 Document Structure Nodes

### When to Use
You need the foundational nodes required for any Tiptap document: Document, Paragraph, Text.

### Items

#### Document
**Description:** Root node that wraps all content. Required in every Tiptap editor.
**Schema:**
```typescript
content: 'block+' // Must contain one or more block nodes
topNode: true // Identifies this as the root
```
**Usage Example:**
```typescript
import Document from '@tiptap/extension-document'

new Editor({
  extensions: [Document, Paragraph, Text],
})
```
**Gotchas:**
- Can't be removed or replaced (required by ProseMirror)
- Custom document nodes must set `topNode: true`

#### Paragraph
**Description:** Basic block-level node for text content. Default block in most editors.
**Schema:**
```typescript
content: 'inline*' // Zero or more inline nodes (text, marks)
group: 'block' // Part of the block group
```
**Usage Example:**
```typescript
import Paragraph from '@tiptap/extension-paragraph'

// Configure default paragraph
Paragraph.configure({
  HTMLAttributes: {
    class: 'my-paragraph',
  },
})
```
**Gotchas:**
- Paragraphs can't contain other blocks (only text and inline nodes)
- Empty paragraphs are valid (zero content)

#### Text
**Description:** Leaf node representing actual text content. Required for any text editing.
**Schema:**
```typescript
group: 'inline' // Part of the inline group
```
**Usage Example:**
```typescript
import Text from '@tiptap/extension-text'

// Text node is always required, no configuration needed
new Editor({
  extensions: [Document, Paragraph, Text],
})
```
**Gotchas:**
- Cannot be configured or extended (simplest node)
- Only node type that can contain actual text

### Common Mistakes
- Forgetting to include Document, Paragraph, or Text → Editor won't initialize
- Trying to nest paragraphs inside paragraphs → Invalid schema; use list items for nesting
- Expecting text outside inline context → Text must be inside a node with `content: 'inline*'`

### See Also
- → 5.2 Content Nodes | Heading, blockquote, code block
- → 3.2 Schema Architecture | Content expression rules
- Reference: https://tiptap.dev/docs/editor/extensions/nodes

