---
description: You need real-time collaborative editing (multiple users editing simultaneously, like Google Docs).
---

## 15.1 Collaborative Editing Architecture

### When to Use
You need real-time collaborative editing (multiple users editing simultaneously, like Google Docs).

### Decision
| If you need... | Use... | Why |
|---|---|---|
| Official Tiptap solution | Tiptap Collaboration (paid) | Managed infrastructure, enterprise support |
| Open-source self-hosted | Y.js + Hocuspocus | Free, full control, proven stack |
| Third-party managed | Liveblocks | Turnkey solution, generous free tier |
| Simple presence only | Custom WebSocket | No CRDT needed for cursors-only |

### Y.js + Hocuspocus Pattern
```typescript
import { useEditor, EditorContent } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'
import Collaboration from '@tiptap/extension-collaboration'
import CollaborationCursor from '@tiptap/extension-collaboration-cursor'
import * as Y from 'yjs'
import { HocuspocusProvider } from '@hocuspocus/provider'

export default function CollaborativeEditor({ documentId, user }) {
  const editor = useEditor({
    extensions: [
      StarterKit.configure({
        history: false, // CRITICAL: Disable StarterKit history
      }),
      Collaboration.configure({
        document: new Y.Doc(),
      }),
      CollaborationCursor.configure({
        provider: new HocuspocusProvider({
          url: 'ws://localhost:1234',
          name: documentId,
        }),
        user: {
          name: user.name,
          color: user.color,
        },
      }),
    ],
    immediatelyRender: false,
  })

  return <EditorContent editor={editor} />
}
```

### Common Mistakes
- Not disabling StarterKit History → Conflicts with Y.js history; must disable
- Forgetting CollaborationCursor → Users can't see each other's cursors
- Not handling WebSocket reconnection → Network drops break sync; implement retry logic
- Storing Y.Doc state in localStorage → Can cause conflicts on reload; use server persistence
- Using Collaboration without understanding CRDTs → Read Y.js docs for conflict resolution model

### See Also
- → 15.2 Hocuspocus Server Setup
- Reference: https://tiptap.dev/docs/editor/extensions/functionality/collaboration
- Y.js: https://docs.yjs.dev/

