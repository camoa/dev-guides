---
description: You need to save/load Tiptap content via Next.js API routes.
---

## 13.2 Next.js API Routes & Content Persistence

### When to Use
You need to save/load Tiptap content via Next.js API routes.

### Pattern
```typescript
// app/api/content/route.ts (App Router)
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const content = await db.getContent() // Your database logic
  return NextResponse.json({ content })
}

export async function POST(request: NextRequest) {
  const { content } = await request.json()
  await db.saveContent(content) // Your database logic
  return NextResponse.json({ success: true })
}

// components/Editor.tsx
'use client'

import { useEditor, EditorContent } from '@tiptap/react'
import { useEffect } from 'react'
import { debounce } from 'lodash'

export default function Editor() {
  const editor = useEditor({
    extensions: [StarterKit],
    immediatelyRender: false,
  })

  // Load content on mount
  useEffect(() => {
    fetch('/api/content')
      .then(res => res.json())
      .then(({ content }) => {
        editor?.commands.setContent(content)
      })
  }, [editor])

  // Auto-save on update (debounced)
  useEffect(() => {
    if (!editor) return

    const saveContent = debounce((content) => {
      fetch('/api/content', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content }),
      })
    }, 1000)

    editor.on('update', ({ editor }) => {
      saveContent(editor.getJSON())
    })

    return () => {
      saveContent.cancel()
    }
  }, [editor])

  return <EditorContent editor={editor} />
}
```

### Common Mistakes
- Saving on every keystroke → Debounce auto-save (1000ms)
- Storing HTML instead of JSON → Use `getJSON()`, not `getHTML()`
- Not handling save errors → Add error handling and retry logic
- Loading content before editor ready → Check `editor` exists before `setContent()`
- Not canceling debounced saves on unmount → Memory leak; call `.cancel()`

### See Also
- ← 13.1 Next.js Setup
- → 14.1 Drupal JSON API Integration
- Reference: https://nextjs.org/docs/app/building-your-application/routing/route-handlers

