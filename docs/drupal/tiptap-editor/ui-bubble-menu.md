---
description: You need a selection-based menu (appears on text selection) or context menu (right-click).
---

## 12.1 Bubble Menu & Context Menus

### When to Use
You need a selection-based menu (appears on text selection) or context menu (right-click).

### Pattern
```typescript
import { BubbleMenu } from '@tiptap/react'

function Editor() {
  const editor = useEditor({ extensions: [StarterKit] })

  return (
    <>
      <EditorContent editor={editor} />
      <BubbleMenu
        editor={editor}
        tippyOptions={{
          duration: 100,
          placement: 'top',
        }}
        shouldShow={({ editor, view, state, from, to }) => {
          // Only show for non-empty text selections
          const { doc, selection } = state
          const { empty } = selection

          // Don't show in code blocks
          const isCode = editor.isActive('codeBlock')

          return !empty && !isCode && from !== to
        }}
      >
        <button
          onClick={() => editor.chain().focus().toggleBold().run()}
          className={editor.isActive('bold') ? 'active' : ''}
        >
          Bold
        </button>
        <button
          onClick={() => editor.chain().focus().toggleItalic().run()}
          className={editor.isActive('italic') ? 'active' : ''}
        >
          Italic
        </button>
        <button
          onClick={() => {
            const url = window.prompt('URL')
            editor.chain().focus().setLink({ href: url }).run()
          }}
        >
          Link
        </button>
      </BubbleMenu>
    </>
  )
}
```

### Common Mistakes
- Not implementing `shouldShow` → Menu appears in unwanted contexts (code blocks, empty selections)
- Forgetting `.focus()` in commands → Editor loses focus when button clicked
- Not checking `isActive()` for button states → Buttons don't reflect current formatting
- Using default positioning in scrollable containers → Menu appears offscreen; adjust `tippyOptions.placement`
- Making menu too large → Obscures content; keep minimal

### See Also
- → 12.2 Floating Menu | Empty block menus
- → 12.3 Slash Commands | Keyboard-driven menus
- Reference: https://tiptap.dev/docs/editor/extensions/functionality/bubble-menu

