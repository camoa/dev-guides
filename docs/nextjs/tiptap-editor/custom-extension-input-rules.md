---
description: You need Markdown-style shortcuts (e.g., `**bold**` converts to bold) or custom paste handling.
---

## 8.2 Input Rules & Paste Rules

### When to Use
You need Markdown-style shortcuts (e.g., `**bold**` converts to bold) or custom paste handling.

### Input Rules
Trigger transformations as user types.

```typescript
import { Node } from '@tiptap/core'
import { textblockTypeInputRule } from '@tiptap/core'

const Heading = Node.create({
  addInputRules() {
    return [
      textblockTypeInputRule({
        find: /^(#{1,6})\s$/, // Match # to ######
        type: this.type,
        getAttributes: (match) => ({ level: match[1].length }),
      }),
    ]
  },
})

// Mark input rule example
import { markInputRule } from '@tiptap/core'

const Bold = Mark.create({
  addInputRules() {
    return [
      markInputRule({
        find: /(?:\*\*|__)([^*_]+)(?:\*\*|__)$/, // **text** or __text__
        type: this.type,
      }),
    ]
  },
})
```

### Paste Rules
Trigger transformations on paste.

```typescript
import { markPasteRule } from '@tiptap/core'

const Link = Mark.create({
  addPasteRules() {
    return [
      markPasteRule({
        find: /https?:\/\/[^\s]+/g, // Match URLs
        type: this.type,
        getAttributes: (match) => ({ href: match[0] }),
      }),
    ]
  },
})
```

### Common Mistakes
- Input rules triggering mid-word → Use `$` anchor and space requirement (e.g., `/^#\s$/`)
- Paste rules not matching entire pattern → Use `g` flag for global matching
- Not escaping regex special characters → `*` needs `\*` in regex
- Input rules conflicting with each other → Order matters; first match wins
- Forgetting to enable/disable rules → Use `enableInputRules: false` to disable globally

### See Also
- → 8.1 Custom Extension Architecture
- Reference: https://tiptap.dev/docs/editor/api/input-rules

