---
description: You need context-aware UI elements: selection menus, slash commands, or floating toolbars.
---

## 7.3 UI Extensions (BubbleMenu, FloatingMenu)

### When to Use
You need context-aware UI elements: selection menus, slash commands, or floating toolbars.

### Items

#### BubbleMenu
**Description:** Menu that appears when text is selected.
**Options:**
| Option | Type | Default | Notes |
|---|---|---|---|
| element | HTMLElement | null | DOM element for menu |
| tippyOptions | Object | {} | Tooltip positioning options |
| shouldShow | function | null | Control menu visibility |

**Usage Example:**
```typescript
import { BubbleMenu } from '@tiptap/extension-bubble-menu'

// React example
import { BubbleMenu } from '@tiptap/react'

function Editor() {
  const editor = useEditor({ extensions: [StarterKit] })

  return (
    <>
      <EditorContent editor={editor} />
      <BubbleMenu editor={editor} shouldShow={({ state, from, to }) => {
        // Only show for text selections (not empty)
        return from !== to
      }}>
        <button onClick={() => editor.chain().focus().toggleBold().run()}>
          Bold
        </button>
        <button onClick={() => editor.chain().focus().toggleItalic().run()}>
          Italic
        </button>
      </BubbleMenu>
    </>
  )
}
```
**Gotchas:**
- Menu appears even for single-character selections (use `shouldShow` to filter)
- Positioning can break in scrollable containers (adjust `tippyOptions`)
- Menu stays visible on blur (implement `onBlur` handler if needed)

#### FloatingMenu
**Description:** Menu that appears in empty blocks.
**Options:**
| Option | Type | Default | Notes |
|---|---|---|---|
| element | HTMLElement | null | DOM element for menu |
| tippyOptions | Object | {} | Tooltip positioning options |
| shouldShow | function | null | Control menu visibility |

**Usage Example:**
```typescript
import { FloatingMenu } from '@tiptap/react'

<FloatingMenu editor={editor} shouldShow={({ state }) => {
  const { $anchor } = state.selection
  return $anchor.parent.isTextblock && !$anchor.parent.textContent
}}>
  <button onClick={() => editor.chain().focus().setHeading({ level: 1 }).run()}>
    H1
  </button>
  <button onClick={() => editor.chain().focus().toggleBulletList().run()}>
    List
  </button>
</FloatingMenu>
```
**Gotchas:**
- Shows in ALL empty blocks (can be distracting; use `shouldShow` carefully)
- Conflicts with placeholder extension (both trigger on empty blocks)

### Common Mistakes
- Not implementing `shouldShow` logic → Menu shows in unwanted places (code blocks, blockquotes)
- Forgetting to `focus()` in command chains → Menu closes but cursor isn't in editor
- Using BubbleMenu for block-level actions → Use FloatingMenu for block actions (headings, lists)
- Not handling menu outside editor viewport → Menu appears offscreen; adjust `tippyOptions.placement`

### See Also
- → 12.1 Toolbar Patterns | Building custom toolbars
- Reference: https://tiptap.dev/docs/editor/extensions/functionality/bubble-menu

