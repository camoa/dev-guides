---
description: You need a complete set of common extensions without installing each individually.
---

## 7.1 StarterKit Bundle & Core Functionality

### When to Use
You need a complete set of common extensions without installing each individually.

### Description
StarterKit is a pre-configured bundle of the most common Tiptap extensions. It's the fastest way to get a functional editor.

### Included Extensions
| Extension | Type | Purpose |
|---|---|---|
| Document | Node | Root document node |
| Paragraph | Node | Basic text blocks |
| Text | Node | Text content |
| Heading | Node | Headings (h1-h6) |
| Bold | Mark | Bold formatting |
| Italic | Mark | Italic formatting |
| Strike | Mark | Strikethrough |
| Code | Mark | Inline code |
| BulletList | Node | Unordered lists |
| OrderedList | Node | Numbered lists |
| ListItem | Node | List item container |
| Blockquote | Node | Block quotes |
| CodeBlock | Node | Code blocks |
| HorizontalRule | Node | Horizontal rules |
| HardBreak | Node | Line breaks (Shift+Enter) |
| Dropcursor | Functionality | Drop cursor indicator |
| Gapcursor | Functionality | Navigate to empty blocks |
| History | Functionality | Undo/redo |

### Usage Example
```typescript
import StarterKit from '@tiptap/starter-kit'

// Use with defaults
new Editor({
  extensions: [StarterKit],
})

// Configure specific extensions
new Editor({
  extensions: [
    StarterKit.configure({
      heading: {
        levels: [1, 2, 3], // Only h1-h3
      },
      history: false, // Disable if using Collaboration
      codeBlock: {
        HTMLAttributes: {
          class: 'code-block',
        },
      },
    }),
  ],
})

// Exclude specific extensions
new Editor({
  extensions: [
    StarterKit.configure({
      strike: false, // Disable strikethrough
      codeBlock: false, // Disable code blocks
    }),
  ],
})
```

### Common Mistakes
- Registering StarterKit AND individual base extensions → Document/Paragraph/Text are duplicated; causes conflicts
- Not disabling History when using Collaboration → Collaboration has its own history; conflicts with StarterKit's
- Expecting StarterKit to include Link, Image, Table → It doesn't; install separately
- Configuring extensions not in StarterKit → No effect; configure them outside StarterKit
- Using StarterKit for minimal editors → Overkill; install only needed extensions for smaller bundle

### See Also
- → 7.2 Utility Extensions | Placeholder, character count
- → 15.1 Collaboration | Disabling History
- Reference: https://tiptap.dev/docs/editor/extensions/functionality/starterkit

