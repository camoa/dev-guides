---
description: Your editor re-renders too frequently, causing lag or poor UX.
---

## 17.1 React Performance Optimization

### When to Use
Your editor re-renders too frequently, causing lag or poor UX.

### Patterns

#### Isolate Editor Component
```typescript
// ❌ BAD: Editor in same component as unrelated state
function App() {
  const [sidebar, setSidebar] = useState(false)
  const editor = useEditor({ extensions: [StarterKit] })

  return (
    <>
      <Sidebar open={sidebar} onChange={setSidebar} /> {/* Re-renders editor */}
      <EditorContent editor={editor} />
    </>
  )
}

// ✓ GOOD: Isolate editor
function EditorComponent() {
  const editor = useEditor({ extensions: [StarterKit] })
  return <EditorContent editor={editor} />
}

function App() {
  const [sidebar, setSidebar] = useState(false)
  return (
    <>
      <Sidebar open={sidebar} onChange={setSidebar} />
      <EditorComponent /> {/* Doesn't re-render when sidebar changes */}
    </>
  )
}
```

#### Use `useEditorState` for Toolbar
```typescript
// ❌ BAD: Toolbar re-renders on every editor update
function Toolbar({ editor }) {
  return (
    <button className={editor.isActive('bold') ? 'active' : ''}>
      Bold
    </button>
  )
}

// ✓ GOOD: Subscribe to specific state
import { useEditorState } from '@tiptap/react'

function Toolbar({ editor }) {
  const { isBold } = useEditorState({
    editor,
    selector: ({ editor }) => ({
      isBold: editor.isActive('bold'),
    }),
  })

  return <button className={isBold ? 'active' : ''}>Bold</button>
}
```

#### Disable Unnecessary Re-renders
```typescript
const editor = useEditor({
  extensions: [StarterKit],
  shouldRerenderOnTransaction: false, // Don't re-render on every transaction
  immediatelyRender: false, // SSR optimization
})
```

### Common Mistakes
- Not isolating editor in separate component → Parent re-renders cause editor re-renders
- Using `onUpdate` without debouncing → Auto-save fires on every keystroke
- Re-creating editor instance on re-render → useEditor already memoizes
- Not using `useEditorState` for toolbar → Entire toolbar re-renders on every change
- Setting `shouldRerenderOnTransaction: true` → Editor re-renders on selection change

### See Also
- → 17.2 Node View Performance | React node view costs
- Reference: https://tiptap.dev/docs/guides/performance

