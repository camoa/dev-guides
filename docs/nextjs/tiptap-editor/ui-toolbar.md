---
description: You need a persistent toolbar (always visible, not context-dependent).
---

## 12.3 Fixed Toolbar Patterns

### When to Use
You need a persistent toolbar (always visible, not context-dependent).

### Pattern
```typescript
function Toolbar({ editor }) {
  if (!editor) return null

  return (
    <div className="toolbar">
      <button
        onClick={() => editor.chain().focus().toggleBold().run()}
        className={editor.isActive('bold') ? 'active' : ''}
        disabled={!editor.can().toggleBold()}
      >
        Bold
      </button>

      <button
        onClick={() => editor.chain().focus().toggleItalic().run()}
        className={editor.isActive('italic') ? 'active' : ''}
      >
        Italic
      </button>

      <select
        onChange={(e) => {
          const level = parseInt(e.target.value)
          if (level) {
            editor.chain().focus().toggleHeading({ level }).run()
          } else {
            editor.chain().focus().setParagraph().run()
          }
        }}
        value={
          editor.isActive('heading', { level: 1 }) ? 1 :
          editor.isActive('heading', { level: 2 }) ? 2 :
          editor.isActive('heading', { level: 3 }) ? 3 : 0
        }
      >
        <option value="0">Paragraph</option>
        <option value="1">Heading 1</option>
        <option value="2">Heading 2</option>
        <option value="3">Heading 3</option>
      </select>

      <button
        onClick={() => editor.chain().focus().undo().run()}
        disabled={!editor.can().undo()}
      >
        Undo
      </button>

      <button
        onClick={() => editor.chain().focus().redo().run()}
        disabled={!editor.can().redo()}
      >
        Redo
      </button>
    </div>
  )
}
```

### Common Mistakes
- Not using `editor.isActive()` for button states → Buttons don't reflect current selection
- Forgetting `editor.can()` for disabled states → Buttons enabled when commands can't execute
- Not calling `.focus()` in commands → Editor loses focus on button click
- Re-rendering toolbar on every editor update → Use `useEditorState` to optimize (see 17.1)

### See Also
- ← 12.1 Bubble Menu | Selection-based menus
- → 17.1 React Performance | Toolbar optimization

