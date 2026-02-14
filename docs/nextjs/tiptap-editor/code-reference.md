---
description: You need quick reference to key Tiptap packages, classes, and imports.
---

## 20.1 Code Reference Map

### When to Use
You need quick reference to key Tiptap packages, classes, and imports.

### Core Packages
| Package | Purpose | Install |
|---|---|---|
| @tiptap/core | Core editor, extension API | `npm install @tiptap/core` |
| @tiptap/react | React integration (hooks, components) | `npm install @tiptap/react` |
| @tiptap/starter-kit | Common extensions bundle | `npm install @tiptap/starter-kit` |
| @tiptap/extension-* | Individual extensions | `npm install @tiptap/extension-link` |
| @tiptap/pm | ProseMirror re-exports | Included with core |

### Key Classes
```typescript
import { Editor } from '@tiptap/core'
import { Node, Mark, Extension } from '@tiptap/core'
import { useEditor, EditorContent, BubbleMenu, FloatingMenu } from '@tiptap/react'
import { ReactNodeViewRenderer, NodeViewWrapper } from '@tiptap/react'
```

### Extension Imports
```typescript
// Nodes
import Document from '@tiptap/extension-document'
import Paragraph from '@tiptap/extension-paragraph'
import Text from '@tiptap/extension-text'
import Heading from '@tiptap/extension-heading'
import Blockquote from '@tiptap/extension-blockquote'
import CodeBlock from '@tiptap/extension-code-block'
import Image from '@tiptap/extension-image'
import Table from '@tiptap/extension-table'
import TableRow from '@tiptap/extension-table-row'
import TableCell from '@tiptap/extension-table-cell'

// Marks
import Bold from '@tiptap/extension-bold'
import Italic from '@tiptap/extension-italic'
import Strike from '@tiptap/extension-strike'
import Link from '@tiptap/extension-link'
import Code from '@tiptap/extension-code'
import Highlight from '@tiptap/extension-highlight'

// Functionality
import History from '@tiptap/extension-history'
import Placeholder from '@tiptap/extension-placeholder'
import CharacterCount from '@tiptap/extension-character-count'
import Collaboration from '@tiptap/extension-collaboration'
import CollaborationCursor from '@tiptap/extension-collaboration-cursor'
```

### TypeScript Declarations
```typescript
// Custom commands
declare module '@tiptap/core' {
  interface Commands<ReturnType> {
    customExtension: {
      customCommand: () => ReturnType
    }
  }
}

// Custom storage
declare module '@tiptap/core' {
  interface Storage {
    customExtension: CustomStorageType
  }
}

// Extension types
Extension.create<OptionsType, StorageType>({ /* ... */ })
Node.create<OptionsType, StorageType>({ /* ... */ })
Mark.create<OptionsType, StorageType>({ /* ... */ })
```

### See Also
- Reference: https://tiptap.dev/docs/editor/api/editor
- GitHub: https://github.com/ueberdosis/tiptap

