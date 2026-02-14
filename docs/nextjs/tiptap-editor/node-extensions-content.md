---
description: You need semantic block-level elements for structured content.
---

## 5.2 Content Nodes (Heading, Blockquote, Lists)

### When to Use
You need semantic block-level elements for structured content.

### Items

#### Heading
**Description:** Headings with configurable levels (h1-h6).
**Options:**
| Option | Type | Default | Notes |
|---|---|---|---|
| levels | number[] | [1, 2, 3, 4, 5, 6] | Restrict allowed heading levels |
| HTMLAttributes | Object | {} | Add custom classes/attributes |

**Usage Example:**
```typescript
import Heading from '@tiptap/extension-heading'

Heading.configure({
  levels: [1, 2, 3], // Only h1, h2, h3
  HTMLAttributes: {
    class: 'heading',
  },
})

// Use in commands
editor.commands.setHeading({ level: 2 })
editor.commands.toggleHeading({ level: 3 })
```
**Gotchas:**
- Headings can't contain block nodes (only inline content)
- Level attribute is required when setting a heading

#### Blockquote
**Description:** Block-level quotation container.
**Schema:**
```typescript
content: 'block+' // Can contain multiple block nodes
group: 'block'
```
**Usage Example:**
```typescript
import Blockquote from '@tiptap/extension-blockquote'

editor.commands.setBlockquote()
editor.commands.toggleBlockquote()
```
**Gotchas:**
- Can nest other blockquotes (nested quotes)
- Wraps selection, doesn't replace it

#### BulletList / OrderedList
**Description:** Unordered (bullet) and ordered (numbered) lists.
**Schema:**
```typescript
content: 'listItem+' // Must contain list items
group: 'block'
```
**Usage Example:**
```typescript
import BulletList from '@tiptap/extension-bullet-list'
import OrderedList from '@tiptap/extension-ordered-list'
import ListItem from '@tiptap/extension-list-item'

editor.commands.toggleBulletList()
editor.commands.toggleOrderedList()
```
**Gotchas:**
- Requires ListItem extension (lists can't contain raw paragraphs)
- Nested lists are achieved via ListItem children

#### ListItem
**Description:** Container for list content. Required for BulletList and OrderedList.
**Schema:**
```typescript
content: 'paragraph block*' // Paragraph + optional nested blocks
group: 'listItem'
```
**Gotchas:**
- Must contain at least one paragraph
- Nested lists go in the `block*` portion

### Common Mistakes
- Using lists without ListItem extension → Schema error
- Trying to create headings > configured levels → Command fails silently
- Expecting blockquote styling from extension → You must add CSS
- Nesting lists incorrectly → Lists nest via ListItem children, not direct nesting

### See Also
- → 5.3 Media & Interactive Nodes | Image, table, code block
- Reference: https://tiptap.dev/docs/editor/extensions/nodes/heading

