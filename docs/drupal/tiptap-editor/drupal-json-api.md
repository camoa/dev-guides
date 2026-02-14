---
description: You're building a decoupled Drupal frontend with Next.js and need to edit Drupal content via Tiptap.
---

## 14.1 Drupal JSON API Integration

### When to Use
You're building a decoupled Drupal frontend with Next.js and need to edit Drupal content via Tiptap.

### Pattern
```typescript
'use client'

import { useEditor, EditorContent } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'
import { useEffect, useState } from 'react'

interface DrupalNode {
  id: string
  type: string
  attributes: {
    title: string
    body: {
      value: string // HTML from Drupal
      format: string
    }
  }
}

export default function DrupalEditor({ nodeId }: { nodeId: string }) {
  const [loading, setLoading] = useState(true)

  const editor = useEditor({
    extensions: [StarterKit],
    immediatelyRender: false,
  })

  // Load Drupal content
  useEffect(() => {
    if (!editor) return

    fetch(`https://drupal.example.com/jsonapi/node/article/${nodeId}`, {
      headers: {
        'Accept': 'application/vnd.api+json',
        'Authorization': `Bearer ${process.env.NEXT_PUBLIC_DRUPAL_TOKEN}`,
      },
    })
      .then(res => res.json())
      .then((response) => {
        const node: DrupalNode = response.data
        // Drupal stores HTML; Tiptap can parse it
        editor.commands.setContent(node.attributes.body.value)
        setLoading(false)
      })
  }, [editor, nodeId])

  // Save to Drupal
  const saveToDrupal = () => {
    const html = editor!.getHTML()

    fetch(`https://drupal.example.com/jsonapi/node/article/${nodeId}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/vnd.api+json',
        'Accept': 'application/vnd.api+json',
        'Authorization': `Bearer ${process.env.NEXT_PUBLIC_DRUPAL_TOKEN}`,
      },
      body: JSON.stringify({
        data: {
          type: 'node--article',
          id: nodeId,
          attributes: {
            body: {
              value: html,
              format: 'full_html',
            },
          },
        },
      }),
    })
  }

  return (
    <>
      {loading ? <p>Loading...</p> : <EditorContent editor={editor} />}
      <button onClick={saveToDrupal}>Save</button>
    </>
  )
}
```

### Common Mistakes
- Storing Tiptap JSON in Drupal → Drupal expects HTML; use `getHTML()` not `getJSON()`
- Not sanitizing HTML before saving → XSS risk; validate content on server
- Forgetting OAuth2 authentication → JSON API requires auth for PATCH requests
- Using wrong content type header → Must be `application/vnd.api+json`
- Not matching Drupal text format → Use `full_html` or `basic_html` as configured in Drupal

### See Also
- → 13.1 Next.js Setup
- → 18.1 Security Model | HTML sanitization
- Reference: https://www.drupal.org/docs/core-modules-and-themes/core-modules/jsonapi-module

