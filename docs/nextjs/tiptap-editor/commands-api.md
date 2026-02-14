---
description: You need to programmatically modify editor content, selection, or state.
---

## 9.1 Commands API & Command Chaining

### When to Use
You need to programmatically modify editor content, selection, or state.

### Core Concepts
Commands are functions that return `true` (success) or `false` (failure). Use `editor.commands.*` for single commands or `editor.chain()` for chaining.

### Pattern
```typescript
// Single command
editor.commands.setContent('<p>New content</p>')

// Command chaining (all-or-nothing transaction)
editor
  .chain()
  .focus() // Focus editor
  .clearContent() // Remove all content
  .insertContent('<p>Fresh start</p>') // Add new content
  .setTextSelection(10) // Set cursor position
  .run() // Execute chain

// Conditional execution
if (editor.can().toggleBold()) {
  editor.commands.toggleBold()
}

// Get return value
const success = editor.commands.setHeading({ level: 2 })
if (!success) {
  console.error('Failed to set heading')
}
```

### Common Command Categories
| Category | Examples | Usage |
|---|---|---|
| Content | setContent, insertContent, clearContent | Modify document |
| Formatting | toggleBold, setHeading, setTextAlign | Apply formatting |
| Selection | focus, blur, setTextSelection, selectAll | Manage cursor |
| Blocks | setNode, setBlockType, splitBlock | Transform blocks |
| Lists | toggleBulletList, sinkListItem, liftListItem | Manipulate lists |
| Marks | setMark, toggleMark, unsetMark | Apply/remove marks |

### Common Mistakes
- Forgetting `.run()` on command chains → Chain doesn't execute without `.run()`
- Not checking `.can()` before execution → Command fails silently; check first
- Chaining focus-dependent commands without `focus()` → Selection-based commands need focus first
- Mixing single commands with chains mid-transaction → Creates multiple transactions; use chains consistently
- Not handling command failures → Commands return false on failure; check return value

### See Also
- → 9.2 Custom Commands | Extending the API
- Reference: https://tiptap.dev/docs/editor/api/commands

