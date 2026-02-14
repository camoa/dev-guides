---
description: You need a menu that appears in empty blocks or triggered by `/` (slash commands).
---

## 12.2 Floating Menu & Slash Commands

### When to Use
You need a menu that appears in empty blocks or triggered by `/` (slash commands).

### Floating Menu Pattern
```typescript
import { FloatingMenu } from '@tiptap/react'

<FloatingMenu
  editor={editor}
  tippyOptions={{ placement: 'left' }}
  shouldShow={({ state }) => {
    const { $anchor } = state.selection
    const isRootDepth = $anchor.depth === 1
    const isEmptyTextBlock =
      $anchor.parent.isTextblock &&
      !$anchor.parent.textContent
    return isRootDepth && isEmptyTextBlock
  }}
>
  <button onClick={() => editor.chain().focus().toggleHeading({ level: 1 }).run()}>
    H1
  </button>
  <button onClick={() => editor.chain().focus().toggleBulletList().run()}>
    List
  </button>
  <button onClick={() => editor.chain().focus().insertTable({ rows: 3, cols: 3 }).run()}>
    Table
  </button>
</FloatingMenu>
```

### Slash Commands Pattern
```typescript
import { Extension } from '@tiptap/core'
import Suggestion from '@tiptap/suggestion'

const SlashCommands = Extension.create({
  name: 'slashCommands',

  addOptions() {
    return {
      suggestion: {
        char: '/',
        items: ({ query }) => {
          return [
            { title: 'Heading 1', command: ({ editor, range }) => {
              editor.chain().focus().deleteRange(range).setHeading({ level: 1 }).run()
            }},
            { title: 'Bullet List', command: ({ editor, range }) => {
              editor.chain().focus().deleteRange(range).toggleBulletList().run()
            }},
          ].filter(item => item.title.toLowerCase().startsWith(query.toLowerCase()))
        },
        render: () => {
          // Render custom suggestion dropdown
        },
      },
    }
  },

  addProseMirrorPlugins() {
    return [Suggestion(this.options.suggestion)]
  },
})
```

### Common Mistakes
- FloatingMenu showing in nested blocks → Check `$anchor.depth === 1` for root-level only
- Slash commands not deleting trigger character → Use `deleteRange(range)` in command
- Not filtering slash command suggestions → Show all items regardless of query
- Menu conflicts with Placeholder extension → Both trigger on empty blocks; coordinate visibility

### See Also
- ← 12.1 Bubble Menu
- Reference: https://tiptap.dev/docs/editor/extensions/functionality/floating-menu

