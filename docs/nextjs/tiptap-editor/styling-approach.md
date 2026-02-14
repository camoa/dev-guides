---
description: You need to style the editor content, UI elements, or integrate with a design system.
---

## 16.1 Styling & Theming Approach

### When to Use
You need to style the editor content, UI elements, or integrate with a design system.

### Pattern
```css
/* Editor container */
.tiptap {
  padding: 1rem;
  min-height: 200px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* Focus outline */
.tiptap:focus {
  outline: 2px solid blue;
}

/* Placeholder */
.tiptap p.is-empty::before {
  content: attr(data-placeholder);
  color: #adb5bd;
  pointer-events: none;
  height: 0;
  float: left;
}

/* Typography */
.tiptap h1 { font-size: 2em; font-weight: bold; }
.tiptap h2 { font-size: 1.5em; font-weight: bold; }
.tiptap p { margin: 1em 0; }
.tiptap ul, .tiptap ol { padding-left: 2em; }

/* Marks */
.tiptap strong { font-weight: bold; }
.tiptap em { font-style: italic; }
.tiptap code {
  background: #f5f5f5;
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-family: monospace;
}

/* Links */
.tiptap a {
  color: blue;
  text-decoration: underline;
  cursor: pointer;
}

/* Code blocks */
.tiptap pre {
  background: #f5f5f5;
  padding: 1em;
  border-radius: 4px;
  overflow-x: auto;
}

.tiptap pre code {
  background: none;
  padding: 0;
  color: inherit;
  font-family: 'Monaco', 'Courier New', monospace;
}

/* Blockquotes */
.tiptap blockquote {
  border-left: 3px solid #ccc;
  padding-left: 1em;
  margin-left: 0;
  font-style: italic;
}

/* Tables */
.tiptap table {
  border-collapse: collapse;
  width: 100%;
}

.tiptap td, .tiptap th {
  border: 1px solid #ccc;
  padding: 0.5em;
}

/* Selection */
.tiptap ::selection {
  background: rgba(0, 123, 255, 0.3);
}

/* Gapcursor (empty block cursor) */
.tiptap .ProseMirror-gapcursor:after {
  border-top: 1px solid black;
}

/* Collaboration cursors */
.tiptap .collaboration-cursor__caret {
  border-left: 2px solid;
  margin-left: -1px;
  pointer-events: none;
  position: relative;
}

.tiptap .collaboration-cursor__label {
  position: absolute;
  top: -1.4em;
  left: -1px;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 3px;
  white-space: nowrap;
}
```

### Integration with Tailwind/CSS-in-JS
```typescript
// Tailwind Typography
import { EditorContent } from '@tiptap/react'

<div className="prose prose-sm max-w-none">
  <EditorContent editor={editor} />
</div>

// Styled Components
import styled from 'styled-components'

const StyledEditor = styled.div`
  .tiptap {
    padding: 1rem;
    border: 1px solid ${props => props.theme.colors.border};

    &:focus {
      outline: 2px solid ${props => props.theme.colors.primary};
    }
  }
`
```

### Common Mistakes
- Not styling ProseMirror-specific classes → Gapcursor, selection, cursors invisible
- Disabling `injectCSS` without custom styles → Editor unusable (invisible cursor)
- Using `::placeholder` for placeholder → Doesn't work; use `.is-empty::before`
- Not styling focus state → Accessibility issue; always add visible focus indicator
- Expecting default styles → Tiptap is headless; you provide all styles

### See Also
- → 16.2 Dark Mode | Theme switching
- Reference: https://tiptap.dev/docs/editor/getting-started/style-editor

