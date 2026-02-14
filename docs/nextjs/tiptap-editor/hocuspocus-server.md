---
description: You're self-hosting collaborative editing with Y.js and need a WebSocket server.
---

## 15.2 Hocuspocus Server Setup

### When to Use
You're self-hosting collaborative editing with Y.js and need a WebSocket server.

### Pattern
```typescript
// server.ts
import { Server } from '@hocuspocus/server'
import { Database } from '@hocuspocus/extension-database'

const server = Server.configure({
  port: 1234,

  extensions: [
    new Database({
      // Fetch document from database on connect
      fetch: async ({ documentName }) => {
        const doc = await db.getDocument(documentName)
        return doc ? Buffer.from(doc) : null
      },

      // Store document updates
      store: async ({ documentName, state }) => {
        await db.saveDocument(documentName, state)
      },
    }),
  ],

  onAuthenticate: async ({ token }) => {
    // Validate user token
    const user = await validateToken(token)
    if (!user) throw new Error('Unauthorized')
    return { user }
  },

  onConnect: ({ documentName, context }) => {
    console.log(`User ${context.user.name} connected to ${documentName}`)
  },

  onDisconnect: ({ documentName, context }) => {
    console.log(`User ${context.user.name} disconnected`)
  },
})

server.listen()
```

### Common Mistakes
- Not implementing database persistence → Documents lost on server restart
- Missing authentication → Anyone can connect and edit
- Not handling concurrent updates → Use database's `fetch` to merge state
- Storing entire document on every update → Store incremental updates (Y.js does this)
- Not monitoring server load → Collaboration is resource-intensive; scale horizontally

### See Also
- ← 15.1 Collaboration Architecture
- Reference: https://tiptap.dev/hocuspocus/introduction

