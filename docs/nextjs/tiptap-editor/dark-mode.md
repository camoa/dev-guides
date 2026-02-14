---
description: You need to support light and dark themes.
---

## 16.2 Dark Mode & Theme Switching

### When to Use
You need to support light and dark themes.

### Pattern
```css
/* Light theme (default) */
.tiptap {
  background: white;
  color: black;
}

.tiptap code {
  background: #f5f5f5;
  color: #333;
}

/* Dark theme */
[data-theme="dark"] .tiptap {
  background: #1e1e1e;
  color: #d4d4d4;
}

[data-theme="dark"] .tiptap code {
  background: #2d2d2d;
  color: #d4d4d4;
}

[data-theme="dark"] .tiptap a {
  color: #4fc3f7;
}

[data-theme="dark"] .tiptap blockquote {
  border-left-color: #555;
}

/* System preference */
@media (prefers-color-scheme: dark) {
  .tiptap {
    background: #1e1e1e;
    color: #d4d4d4;
  }
}
```

### React Implementation
```typescript
'use client'

import { useTheme } from 'next-themes'

export default function Editor() {
  const { theme } = useTheme()

  const editor = useEditor({
    extensions: [StarterKit],
    editorProps: {
      attributes: {
        class: theme === 'dark' ? 'tiptap dark' : 'tiptap',
      },
    },
  })

  return <EditorContent editor={editor} />
}
```

### Common Mistakes
- Hardcoding colors in extensions → Use CSS variables for theme switching
- Not updating syntax highlighting theme → Code blocks stay light in dark mode
- Forgetting collaboration cursor colors → Other users' cursors invisible in dark mode
- Not testing contrast ratios → WCAG AA requires 4.5:1 contrast

### See Also
- ← 16.1 Styling Approach

