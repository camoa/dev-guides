---
description: You're integrating Tiptap into a React or Next.js application.
---

## 2.2 React Integration & SSR Handling

### When to Use
You're integrating Tiptap into a React or Next.js application.

### Pattern
```typescript
'use client' // Next.js App Router

import { useEditor, EditorContent } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'

function Editor() {
  const editor = useEditor({
    extensions: [StarterKit],
    content: '<p>Hello World</p>',
    immediatelyRender: false, // CRITICAL for SSR
    shouldRerenderOnTransaction: false, // Performance optimization
  })

  return <EditorContent editor={editor} />
}
```

### Common Mistakes
- Omitting `'use client'` directive → SSR error in Next.js App Router
- Not setting `immediatelyRender: false` → Hydration mismatch errors
- Using EditorProvider AND useEditor together → They're mutually exclusive; EditorProvider wraps useEditor
- Rendering editor in same component as unrelated state → Every state change re-renders editor; isolate in separate component
- Re-creating editor on every render → useEditor already memoizes; don't wrap in useMemo
- Setting `shouldRerenderOnTransaction: true` → Editor re-renders on every keystroke; use `useEditorState` instead

### Decision Points
| Scenario | Pattern | Why |
|---|---|---|
| Next.js App Router | `'use client'` + `immediatelyRender: false` | Prevents SSR execution |
| Next.js Pages Router | Dynamic import with `ssr: false` | Ensures client-only rendering |
| Performance-critical UI | `shouldRerenderOnTransaction: false` + `useEditorState` | Prevents unnecessary re-renders |
| Multi-editor instances | Separate components per editor | Prevents state interference |

### See Also
- → 13.1 Next.js Setup | App Router patterns
- → 17.1 React Performance | Optimization techniques
- Reference: https://tiptap.dev/docs/editor/getting-started/install/react

