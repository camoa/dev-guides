---
description: You need undo/redo functionality for user edits.
---

## 7.4 History & Undo/Redo

### When to Use
You need undo/redo functionality for user edits.

### Description
History extension tracks editor transactions and provides undo/redo commands. Included in StarterKit.

### Options
| Option | Type | Default | Notes |
|---|---|---|---|
| depth | number | 100 | Number of history steps to keep |
| newGroupDelay | number | 500 | Time (ms) to group edits into single undo step |

### Usage Example
```typescript
import History from '@tiptap/extension-history'

History.configure({
  depth: 50, // Keep last 50 undo steps
  newGroupDelay: 1000, // Group edits within 1 second
})

// Commands
editor.commands.undo()
editor.commands.redo()

// Keyboard shortcuts (built-in)
// Mod-z: Undo
// Mod-Shift-z or Mod-y: Redo
```

### Common Mistakes
- Using History with Collaboration extension → Collaboration has its own history (Y-CRDT); disable StarterKit's history
- Setting `depth` too high → Memory bloat; 100 is sufficient for most editors
- Expecting cross-session history → History is session-based; doesn't persist on page reload
- Not grouping rapid edits → Set `newGroupDelay` to avoid creating undo step per keystroke

### See Also
- → 15.1 Collaboration | Y.js history handling
- Reference: https://tiptap.dev/docs/editor/extensions/functionality/history

