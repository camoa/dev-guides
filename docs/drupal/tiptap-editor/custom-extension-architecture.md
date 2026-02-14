---
description: You need to create a new extension type (node, mark, or functionality) not provided by built-in extensions.
---

## 8.1 Custom Extension Architecture

### When to Use
You need to create a new extension type (node, mark, or functionality) not provided by built-in extensions.

### Decision
| If you need... | Create... | Why |
|---|---|---|
| Block-level content (card, callout, accordion) | Node extension | Structural content with children |
| Inline formatting (tooltip, annotation) | Mark extension | Apply to text ranges |
| Editor behavior (auto-save, mentions, AI) | Extension | No document structure, just functionality |
| Interactive content with React | Node extension + NodeView | Custom rendering with React components |

### Pattern
```typescript
import { Node, Mark, Extension } from '@tiptap/core'

// Node extension example
const CustomNode = Node.create({
  name: 'customNode',
  group: 'block',
  content: 'inline*',

  addAttributes() {
    return {
      customAttr: { default: null },
    }
  },

  parseHTML() {
    return [{ tag: 'div[data-type="custom"]' }]
  },

  renderHTML({ HTMLAttributes }) {
    return ['div', { 'data-type': 'custom', ...HTMLAttributes }, 0]
  },

  addCommands() {
    return {
      setCustomNode: (attrs) => ({ commands }) => {
        return commands.setNode(this.name, attrs)
      },
    }
  },
})

// Mark extension example
const CustomMark = Mark.create({
  name: 'customMark',

  addAttributes() {
    return {
      color: { default: 'red' },
    }
  },

  parseHTML() {
    return [{ tag: 'span[data-custom]' }]
  },

  renderHTML({ HTMLAttributes }) {
    return ['span', { 'data-custom': true, ...HTMLAttributes }, 0]
  },
})

// Extension example (functionality only)
const CustomExtension = Extension.create({
  name: 'customExtension',

  addOptions() {
    return { enabled: true }
  },

  addKeyboardShortcuts() {
    return {
      'Mod-Alt-x': () => {
        console.log('Custom shortcut')
        return true
      },
    }
  },

  onUpdate() {
    // React to editor updates
  },
})
```

### Common Mistakes
- Creating Mark when you need Node → Marks are inline-only; use Node for block-level content
- Not defining `parseHTML()` and `renderHTML()` → Extension can't serialize/deserialize
- Forgetting to add commands → Users can't interact with your extension via API
- Not extending TypeScript types → No autocomplete for custom commands
- Returning wrong value from commands → Commands must return `true` (success) or `false` (failure)

### See Also
- → 8.2 Input Rules & Paste Rules | Markdown-style shortcuts
- → 8.3 Node Views | Custom rendering
- Reference: https://tiptap.dev/docs/editor/extensions/custom-extensions

