---
description: You need to create reusable command logic for your extensions or application.
---

## 9.2 Creating Custom Commands

### When to Use
You need to create reusable command logic for your extensions or application.

### Pattern
```typescript
import { Extension } from '@tiptap/core'

// Extend TypeScript types for autocomplete
declare module '@tiptap/core' {
  interface Commands<ReturnType> {
    customExtension: {
      /**
       * Insert a custom block at current position
       */
      insertCustomBlock: (attrs: { id: string }) => ReturnType
    }
  }
}

const CustomExtension = Extension.create({
  name: 'customExtension',

  addCommands() {
    return {
      insertCustomBlock: (attrs) => ({ chain }) => {
        return chain()
          .focus()
          .insertContent({
            type: 'customNode',
            attrs,
          })
          .run()
      },
    }
  },
})

// Use custom command
editor.commands.insertCustomBlock({ id: '123' })
```

### Common Mistakes
- Not extending TypeScript `Commands` interface → No autocomplete for custom commands
- Returning wrong value → Must return `true` or `false`, not `void`
- Accessing `this.editor` in command function → Use destructured `editor` from parameters
- Not using `chain()` for multi-step commands → Creates separate transactions
- Forgetting JSDoc comments → No documentation in autocomplete

### See Also
- ← 9.1 Commands API | Built-in commands
- Reference: https://tiptap.dev/docs/editor/api/commands

