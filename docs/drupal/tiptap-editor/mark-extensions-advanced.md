---
description: You need background highlighting, text colors, font sizes, or custom text styling.
---

## 6.3 Highlight & Text Style Marks

### When to Use
You need background highlighting, text colors, font sizes, or custom text styling.

### Items

#### Highlight
**Description:** Background color highlighting for text.
**Options:**
| Option | Type | Default | Notes |
|---|---|---|---|
| multicolor | boolean | false | Allow multiple highlight colors |
| HTMLAttributes | Object | {} | Default attributes |

**Usage Example:**
```typescript
import Highlight from '@tiptap/extension-highlight'

Highlight.configure({
  multicolor: true, // Enable color attribute
})

editor.commands.toggleHighlight() // Default color
editor.commands.toggleHighlight({ color: '#ff0000' }) // Custom color
```
**Gotchas:**
- `multicolor: false` ignores color attribute
- No color picker UI (build separately)

#### TextStyle
**Description:** Base extension for inline text styling (color, font-size, etc.).
**Usage Example:**
```typescript
import TextStyle from '@tiptap/extension-text-style'
import Color from '@tiptap/extension-color'

// TextStyle is required for Color extension
editor.commands.setColor('#ff0000')
editor.commands.unsetColor()
```
**Gotchas:**
- TextStyle alone does nothing (it's a base)
- Required for Color, FontSize, FontFamily extensions

#### Subscript / Superscript
**Description:** Subscript (H₂O) and superscript (E=mc²) formatting.
**HTML:** Renders as `<sub>` and `<sup>` tags.
**Usage Example:**
```typescript
import Subscript from '@tiptap/extension-subscript'
import Superscript from '@tiptap/extension-superscript'

editor.commands.toggleSubscript()
editor.commands.toggleSuperscript()
```
**Gotchas:**
- Subscript and superscript are mutually exclusive (can't have both)
- Often used together (install both extensions)

### Common Mistakes
- Using Color without TextStyle → Extension fails; TextStyle is required dependency
- Expecting highlight to apply to block nodes → Highlight is a mark (inline only)
- Not providing color picker UI → Extensions don't include UI; build separately
- Applying subscript + superscript simultaneously → They exclude each other

### See Also
- ← 6.1 Basic Text Formatting Marks
- → 7.1 StarterKit Bundle | Common extension sets
- Reference: https://tiptap.dev/docs/editor/extensions/marks/highlight

