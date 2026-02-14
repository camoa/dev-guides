---
description: You need to install Tiptap in a JavaScript/TypeScript project.
---

## 2.1 Installation & Package Structure

### When to Use
You need to install Tiptap in a JavaScript/TypeScript project.

### Steps
1. **Install core packages**
   ```bash
   npm install @tiptap/core @tiptap/starter-kit
   ```
   Core is required; StarterKit bundles common extensions (Document, Paragraph, Text, Bold, Italic, etc.)

2. **Install framework integration** (React example)
   ```bash
   npm install @tiptap/react
   ```
   Use `@tiptap/vue-3` for Vue, or vanilla `@tiptap/core` for plain JS

3. **Install additional extensions** (optional)
   ```bash
   npm install @tiptap/extension-link @tiptap/extension-image
   ```
   Add only extensions you need to keep bundle size small

### Decision Points
| At this step... | If... | Then... |
|---|---|---|
| Step 1 | Building minimal editor | Skip StarterKit, install individual extensions |
| Step 2 | Using Next.js | Always install `@tiptap/react` |
| Step 3 | Need tables, mentions, code highlighting | Install `@tiptap/extension-table`, `@tiptap/extension-mention`, `@tiptap/extension-code-block-lowlight` |

### Common Mistakes
- Installing all extensions upfront → Bundle bloat; install only what you need
- Forgetting React integration package → `@tiptap/core` alone won't work with React hooks
- Mixing StarterKit with individual base extensions → StarterKit includes Document, Paragraph, Text; don't re-register them
- Not pinning versions in production → Tiptap evolves fast; use exact versions (`3.11.1` not `^3.11.1`)

### See Also
- → 2.2 React Integration | useEditor hook setup
- Reference: https://tiptap.dev/docs/editor/getting-started/install/nextjs

