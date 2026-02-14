---
description: You need editor enhancements like placeholders, character counts, or file upload handling.
---

## 7.2 Utility Extensions (Placeholder, CharacterCount, FileHandler)

### When to Use
You need editor enhancements like placeholders, character counts, or file upload handling.

### Items

#### Placeholder
**Description:** Show placeholder text when editor is empty.
**Options:**
| Option | Type | Default | Notes |
|---|---|---|---|
| placeholder | string \| function | 'Write something…' | Text or function returning text |
| showOnlyWhenEditable | boolean | true | Hide when editor is read-only |
| showOnlyCurrent | boolean | true | Show only for current node |

**Usage Example:**
```typescript
import Placeholder from '@tiptap/extension-placeholder'

Placeholder.configure({
  placeholder: 'Start typing...',
  showOnlyWhenEditable: true,
  showOnlyCurrent: true, // Only show for focused node
})

// Dynamic placeholder based on node
Placeholder.configure({
  placeholder: ({ node }) => {
    if (node.type.name === 'heading') return 'Enter heading...'
    return 'Write something...'
  },
})
```
**Gotchas:**
- Styled via CSS (`::placeholder` doesn't work; use `.is-empty::before`)
- Placeholder doesn't show if there's any content (even whitespace)

#### CharacterCount
**Description:** Count characters and words, enforce limits.
**Options:**
| Option | Type | Default | Notes |
|---|---|---|---|
| limit | number | null | Maximum character count |
| mode | 'textSize' \| 'nodeSize' | 'textSize' | Count method |

**Usage Example:**
```typescript
import CharacterCount from '@tiptap/extension-character-count'

CharacterCount.configure({
  limit: 1000,
})

// Access counts
editor.storage.characterCount.characters() // 42
editor.storage.characterCount.words() // 8
```
**Gotchas:**
- Limit is enforced (blocks typing when reached)
- `mode: 'nodeSize'` counts all nodes (includes formatting); `textSize` counts only visible characters

#### FileHandler
**Description:** Handle file drops and pastes (images, PDFs, etc.).
**Options:**
| Option | Type | Default | Notes |
|---|---|---|---|
| allowedMimeTypes | string[] | null | Restrict file types |
| onDrop | function | null | Handle file drop |
| onPaste | function | null | Handle file paste |

**Usage Example:**
```typescript
import { FileHandler } from '@tiptap/extension-file-handler'

FileHandler.configure({
  allowedMimeTypes: ['image/jpeg', 'image/png', 'image/gif'],
  onDrop: (currentEditor, files, pos) => {
    files.forEach(file => {
      const url = URL.createObjectURL(file)
      currentEditor.chain().insertContentAt(pos, {
        type: 'image',
        attrs: { src: url },
      }).focus().run()
    })
  },
})
```
**Gotchas:**
- Doesn't handle file uploads (you implement upload logic)
- Using `URL.createObjectURL()` creates temporary URLs (upload to server for persistence)

#### Typography
**Description:** Auto-convert typography (smart quotes, dashes, ellipses).
**Usage Example:**
```typescript
import Typography from '@tiptap/extension-typography'

// Automatically converts:
// "text" → "text" (smart quotes)
// -- → – (en dash)
// --- → — (em dash)
// ... → … (ellipsis)
```
**Gotchas:**
- Can interfere with code/technical writing (disable if needed)

### Common Mistakes
- Not styling Placeholder extension → Invisible without CSS
- Using CharacterCount without displaying count → Users can't see limit
- Forgetting to upload files after FileHandler drop → Temporary blob URLs are lost on refresh
- Enabling Typography in code editors → Converts `--` to en dash in code snippets

### See Also
- → 7.3 UI Extensions | Bubble menu, floating menu
- Reference: https://tiptap.dev/docs/editor/extensions/functionality/placeholder

