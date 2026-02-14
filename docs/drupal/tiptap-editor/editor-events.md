---
description: You need to react to editor state changes: content updates, selection changes, focus/blur, etc.
---

## 10.1 Editor Events & Lifecycle Hooks

### When to Use
You need to react to editor state changes: content updates, selection changes, focus/blur, etc.

### Available Events
| Event | When Triggered | Use Case |
|---|---|---|
| beforeCreate | Before editor view creation | Initialize dependencies |
| create | Editor fully initialized | Auto-save setup, analytics |
| update | Content changed | Save draft, character count |
| selectionUpdate | Selection/cursor moved | Update toolbar state |
| transaction | Any state change | Debug, logging |
| focus | Editor gains focus | Show toolbar, analytics |
| blur | Editor loses focus | Hide toolbar, validate |
| destroy | Editor being destroyed | Cleanup, save final state |
| paste | Content pasted | Transform pasted content |
| drop | Content dropped | Handle file uploads |
| contentError | Invalid schema content | Disable collaboration |

### Pattern
```typescript
// Option 1: Configuration
const editor = new Editor({
  onCreate({ editor }) {
    console.log('Editor created')
  },
  onUpdate({ editor }) {
    const json = editor.getJSON()
    localStorage.setItem('draft', JSON.stringify(json))
  },
  onSelectionUpdate({ editor }) {
    updateToolbarState(editor)
  },
  onFocus({ editor, event }) {
    console.log('Focused')
  },
  onBlur({ editor, event }) {
    console.log('Blurred')
  },
  onContentError({ editor, error, disableCollaboration }) {
    console.error('Schema error:', error)
    disableCollaboration()
    editor.setEditable(false)
  },
})

// Option 2: Binding
editor.on('update', ({ editor }) => {
  saveDraft(editor.getJSON())
})

// Unbinding
const onUpdate = ({ editor }) => { /* ... */ }
editor.on('update', onUpdate)
editor.off('update', onUpdate)

// Option 3: Extension hooks
const AutoSave = Extension.create({
  name: 'autoSave',

  onUpdate() {
    this.editor.storage.autoSave.lastSaved = Date.now()
  },
})
```

### Common Mistakes
- Using `onUpdate` for every keystroke → Debounce for auto-save (use 500-1000ms delay)
- Not cleaning up event listeners → Memory leak; use `.off()` when component unmounts
- Confusing `update` with `transaction` → `transaction` fires on ALL state changes (selection, focus, etc.); `update` only on content changes
- Mutating editor state in event handlers → Causes infinite loops; use commands instead
- Not handling `contentError` in production → Invalid content silently breaks collaboration

### See Also
- → 10.2 Debouncing & Throttling Events
- Reference: https://tiptap.dev/docs/editor/api/events

