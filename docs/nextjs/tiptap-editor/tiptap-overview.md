---
description: You need to choose a rich text editor framework for a React/Next.js application or headless CMS integration.
---

## 1.1 Tiptap Overview

### When to Use
You need to choose a rich text editor framework for a React/Next.js application or headless CMS integration.

### Decision
| If you need... | Use... | Why |
|---|---|---|
| Headless editor built on battle-tested foundation | Tiptap | Built on ProseMirror (13+ years mature), headless architecture, framework-agnostic |
| Full control with minimal dependencies | Lexical | Meta-built, React-first, no external dependencies, excellent performance |
| Maximum customization flexibility | Slate | React-first, completely customizable schema, ideal for unique use cases |
| Drop-in WYSIWYG editor | CKEditor/TinyMCE | Traditional WYSIWYG, batteries-included, lower learning curve |
| Modern decoupled Drupal | Tiptap | Best integration with JSON API, strong community, extensive extension ecosystem |

### Pattern
```typescript
import { Editor } from '@tiptap/core'
import StarterKit from '@tiptap/starter-kit'

const editor = new Editor({
  element: document.querySelector('.editor'),
  extensions: [StarterKit],
  content: '<p>Hello World</p>',
  autofocus: true,
})
```

### Common Mistakes
- Using Tiptap for simple textarea needs → Use native HTML textarea or Quill for simpler requirements
- Expecting WYSIWYG features out-of-box → Tiptap is headless; UI components are separate
- Ignoring schema validation → Schema mismatch silently breaks content sync; always enable `enableContentCheck: true` in production
- Not understanding ProseMirror foundation → Read ProseMirror docs for advanced usage; Tiptap is a wrapper, not a replacement
- Choosing based on GitHub stars alone → Lexical has 21K+ stars but lacks 1.0 release; Tiptap is production-ready now

### See Also
- → 1.2 Editor Comparison | Detailed feature matrix
- Reference: https://tiptap.dev/docs/editor/getting-started/overview

