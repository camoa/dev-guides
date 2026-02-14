---
description: You need to understand Tiptap's underlying architecture to build custom extensions or debug complex issues.
---

## 3.1 ProseMirror Foundation & Concepts

### When to Use
You need to understand Tiptap's underlying architecture to build custom extensions or debug complex issues.

### Core Concepts
| Concept | Description | Tiptap Equivalent |
|---|---|---|
| Schema | Defines allowed document structure (nodes, marks, attributes) | Derived from registered extensions |
| Document | Tree of nodes representing content | `editor.state.doc` |
| State | Immutable snapshot (document + selection + plugins) | `editor.state` |
| Transaction | State change operation (insert, delete, format) | `editor.commands.*` |
| Node | Content block (paragraph, heading, image) | Node extensions |
| Mark | Inline formatting (bold, link) | Mark extensions |
| Command | Function that creates a transaction | `editor.chain().*` |
| Plugin | Custom behavior (decorations, key bindings) | Extension hooks |

### Pattern
```typescript
// Accessing ProseMirror internals
const schema = editor.schema // ProseMirror schema
const state = editor.state // Current EditorState
const view = editor.view // EditorView instance

// Transaction inspection
editor.on('transaction', ({ editor, transaction }) => {
  console.log('Steps:', transaction.steps)
  console.log('Selection:', transaction.selection)
  console.log('Updated:', transaction.docChanged)
})
```

### Common Mistakes
- Mutating editor state directly → State is immutable; use commands/transactions
- Bypassing Tiptap API to call ProseMirror directly → Breaks Tiptap's event system; always use `editor.commands`
- Not understanding content expressions → `'block+'` means "one or more block nodes"; learn ProseMirror schema syntax
- Ignoring transaction batching → Multiple `editor.commands.*` calls create separate transactions; use `editor.chain()` to batch
- Expecting DOM synchronization → ProseMirror updates state first, then DOM; don't query DOM mid-transaction

### See Also
- → 3.2 Schema Architecture | Document structure rules
- → 9.1 Commands API | Transaction execution
- Reference: https://prosemirror.net/docs/guide/

