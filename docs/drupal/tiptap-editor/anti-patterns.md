---
description: You need to avoid common pitfalls and bad practices.
---

## 19.2 Anti-Patterns & Common Mistakes

### When to Use
You need to avoid common pitfalls and bad practices.

### Anti-Patterns

#### 1. Mutating Editor State Directly
❌ **Wrong:**
```typescript
editor.state.doc = newDoc // NEVER mutate state directly
```

✓ **Right:**
```typescript
editor.commands.setContent(newContent) // Use commands
```

**Why:** ProseMirror state is immutable. Direct mutation breaks transaction system, history, and collaboration.

---

#### 2. Using HTML for Storage
❌ **Wrong:**
```typescript
const html = editor.getHTML()
database.save(html) // Lossy, XSS risk
```

✓ **Right:**
```typescript
const json = editor.getJSON()
database.save(json) // Lossless, structured, safe
```

**Why:** HTML loses schema information, risks XSS, and can't be reliably re-parsed. JSON is the canonical format.

---

#### 3. Not Isolating Editor in React
❌ **Wrong:**
```typescript
function App() {
  const [theme, setTheme] = useState('light')
  const editor = useEditor({ extensions: [StarterKit] })
  return (
    <>
      <ThemeToggle onChange={setTheme} /> {/* Re-renders editor */}
      <EditorContent editor={editor} />
    </>
  )
}
```

✓ **Right:**
```typescript
function EditorComponent() {
  const editor = useEditor({ extensions: [StarterKit] })
  return <EditorContent editor={editor} />
}

function App() {
  const [theme, setTheme] = useState('light')
  return (
    <>
      <ThemeToggle onChange={setTheme} />
      <EditorComponent /> {/* Isolated */}
    </>
  )
}
```

**Why:** Unrelated state changes cause expensive editor re-renders. Isolation prevents this.

---

#### 4. Forgetting to Disable History with Collaboration
❌ **Wrong:**
```typescript
new Editor({
  extensions: [
    StarterKit, // Includes History
    Collaboration.configure({ document: ydoc }),
  ],
})
```

✓ **Right:**
```typescript
new Editor({
  extensions: [
    StarterKit.configure({ history: false }), // Disable
    Collaboration.configure({ document: ydoc }),
  ],
})
```

**Why:** Collaboration has its own Y.js-based history. StarterKit's history conflicts, causing undo/redo bugs.

---

#### 5. Not Sanitizing Link URLs
❌ **Wrong:**
```typescript
Link.configure({
  // No validation
})
```

✓ **Right:**
```typescript
Link.configure({
  validate: (url) => /^https?:\/\//.test(url),
  protocols: ['http', 'https'],
})
```

**Why:** `javascript:`, `data:`, and `vbscript:` URLs are XSS vectors (CVE-2025-14284). Always validate.

---

#### 6. Using React Node Views for Simple Content
❌ **Wrong:**
```typescript
addNodeView() {
  return ReactNodeViewRenderer(({ node }) => (
    <div>{node.attrs.text}</div>
  ))
}
```

✓ **Right:**
```typescript
renderHTML({ node }) {
  return ['div', node.attrs.text]
}
```

**Why:** React node views are 10x slower than HTML rendering. Use HTML unless you need interactivity.

---

#### 7. Not Debouncing Auto-Save
❌ **Wrong:**
```typescript
editor.on('update', ({ editor }) => {
  saveToServer(editor.getJSON()) // Every keystroke!
})
```

✓ **Right:**
```typescript
const debouncedSave = debounce((content) => {
  saveToServer(content)
}, 1000)

editor.on('update', ({ editor }) => {
  debouncedSave(editor.getJSON())
})
```

**Why:** Saving on every keystroke floods the server and degrades UX. Debounce to 1-2 seconds.

---

#### 8. Expecting StarterKit to Include Everything
❌ **Wrong:**
```typescript
new Editor({
  extensions: [StarterKit],
})

editor.commands.setImage({ src: '...' }) // Fails - Image not in StarterKit
```

✓ **Right:**
```typescript
import Image from '@tiptap/extension-image'

new Editor({
  extensions: [StarterKit, Image],
})
```

**Why:** StarterKit is common extensions only. Link, Image, Table, Mention must be installed separately.

---

#### 9. Not Setting `enableContentCheck` in Production
❌ **Wrong:**
```typescript
new Editor({
  extensions: [StarterKit],
  // enableContentCheck defaults to false
})
```

✓ **Right:**
```typescript
new Editor({
  extensions: [StarterKit],
  enableContentCheck: true, // Catch schema violations
  onContentError({ editor, error, disableCollaboration }) {
    console.error(error)
    disableCollaboration() // Prevent syncing bad content
    editor.setEditable(false)
  },
})
```

**Why:** Invalid content silently breaks collaboration. `enableContentCheck` detects this early.

---

#### 10. Using `@extend` in Custom CSS
❌ **Wrong:**
```scss
.custom-node {
  @extend .tiptap; // Bloats selectors
}
```

✓ **Right:**
```scss
.custom-node {
  @include tiptap-styles; // Use mixins
  // Or just apply classes directly in HTML
}
```

**Why:** `@extend` causes selector explosion, making CSS hard to debug and slow to parse. Use mixins or utility classes.

---

### See Also
- ← 19.1 Testing Strategy
- → 18.1 Security Model | XSS prevention
- Reference: https://liveblocks.io/docs/guides/tiptap-best-practices-and-tips

