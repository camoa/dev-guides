---
description: You need images, tables, code blocks, or other rich content types.
---

## 5.3 Media & Interactive Nodes

### When to Use
You need images, tables, code blocks, or other rich content types.

### Items

#### Image
**Description:** Inline or block image with configurable attributes.
**Options:**
| Option | Type | Default | Notes |
|---|---|---|---|
| inline | boolean | false | Render inline with text or as block |
| allowBase64 | boolean | false | Allow base64 encoded images |
| HTMLAttributes | Object | {} | Custom attributes (alt, title, class) |

**Usage Example:**
```typescript
import Image from '@tiptap/extension-image'

Image.configure({
  inline: true,
  allowBase64: true,
})

editor.commands.setImage({ src: 'https://example.com/image.jpg', alt: 'Description' })
```
**Gotchas:**
- By default, images are block-level (not inline)
- No built-in upload handling (implement separately)
- Alt text is not enforced (accessibility concern)

#### Table
**Description:** Full-featured table with rows, cells, and header cells.
**Dependencies:** Requires TableRow, TableCell, TableHeader extensions.
**Usage Example:**
```typescript
import Table from '@tiptap/extension-table'
import TableRow from '@tiptap/extension-table-row'
import TableCell from '@tiptap/extension-table-cell'
import TableHeader from '@tiptap/extension-table-header'

editor.commands.insertTable({ rows: 3, cols: 3, withHeaderRow: true })
editor.commands.addColumnAfter()
editor.commands.deleteRow()
editor.commands.mergeCells()
```
**Gotchas:**
- Table extensions must all be registered together
- No built-in styling (you provide CSS)
- Resizable columns require additional extension

#### CodeBlock
**Description:** Multi-line code block with optional syntax highlighting.
**Options:**
| Option | Type | Default | Notes |
|---|---|---|---|
| languageClassPrefix | string | 'language-' | CSS class prefix |
| HTMLAttributes | Object | {} | Custom attributes |

**Usage Example:**
```typescript
import CodeBlock from '@tiptap/extension-code-block'

editor.commands.setCodeBlock()
editor.commands.toggleCodeBlock()

// With syntax highlighting (requires lowlight)
import CodeBlockLowlight from '@tiptap/extension-code-block-lowlight'
import { lowlight } from 'lowlight'

CodeBlockLowlight.configure({ lowlight })
```
**Gotchas:**
- Marks (bold, italic) don't work inside code blocks (intended)
- Syntax highlighting requires separate lowlight package
- Whitespace is preserved (`white-space: pre`)

#### HorizontalRule
**Description:** Thematic break (horizontal line).
**Usage Example:**
```typescript
import HorizontalRule from '@tiptap/extension-horizontal-rule'

editor.commands.setHorizontalRule()
```
**Gotchas:**
- Not editable once inserted (atom node)
- Input rule: `---` on new line inserts horizontal rule

### Common Mistakes
- Using Image without upload logic → Displays URL but doesn't handle file uploads
- Forgetting Table dependencies → TableRow/Cell/Header must all be registered
- Expecting code block syntax highlighting without lowlight → CodeBlock alone has no highlighting
- Not styling media nodes → Extensions provide structure, not appearance

### See Also
- → 7.2 FileHandler Extension | Drag-and-drop uploads
- Reference: https://tiptap.dev/docs/editor/extensions/nodes/image

