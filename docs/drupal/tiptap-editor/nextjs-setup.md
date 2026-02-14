---
description: You're integrating Tiptap into a Next.js application (App Router or Pages Router).
---

## 13.1 Next.js Integration & SSR Handling

### When to Use
You're integrating Tiptap into a Next.js application (App Router or Pages Router).

### Next.js App Router (Recommended)
```typescript
'use client' // REQUIRED: Tiptap is client-only

import { useEditor, EditorContent } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'

export default function Editor() {
  const editor = useEditor({
    extensions: [StarterKit],
    content: '<p>Hello World</p>',
    immediatelyRender: false, // CRITICAL for SSR
  })

  return <EditorContent editor={editor} />
}
```

### Next.js Pages Router
```typescript
// components/Editor.tsx
import { useEditor, EditorContent } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'

export default function Editor() {
  const editor = useEditor({
    extensions: [StarterKit],
    immediatelyRender: false,
  })

  return <EditorContent editor={editor} />
}

// pages/index.tsx
import dynamic from 'next/dynamic'

const Editor = dynamic(() => import('../components/Editor'), {
  ssr: false, // Disable SSR for editor component
})

export default function Home() {
  return <Editor />
}
```

### Common Mistakes
- Forgetting `'use client'` in App Router → Server component error
- Not setting `immediatelyRender: false` → Hydration mismatch error
- Using `ssr: false` in App Router → Not needed; use `'use client'` instead
- Importing Tiptap in server components → Must be in client component
- Not handling loading state → Editor briefly shows empty on client hydration

### See Also
- → 2.2 React Integration | useEditor hook
- → 13.2 Next.js API Routes | Save content
- Reference: https://tiptap.dev/docs/editor/getting-started/install/nextjs

