---
description: You need inline text formatting: bold, italic, underline, strikethrough.
---

## 6.1 Basic Text Formatting Marks

### When to Use
You need inline text formatting: bold, italic, underline, strikethrough.

### Items

#### Bold
**Description:** Bold text formatting.
**HTML:** Renders as `<strong>` tag.
**Keyboard Shortcut:** `Mod-b` (Cmd-b on Mac, Ctrl-b on Windows)
**Usage Example:**
```typescript
import Bold from '@tiptap/extension-bold'

editor.commands.setBold()
editor.commands.toggleBold()
editor.commands.unsetBold()
```
**Gotchas:**
- StarterKit includes Bold by default
- Input rule: `**text**` auto-converts to bold

#### Italic
**Description:** Italic text formatting.
**HTML:** Renders as `<em>` tag.
**Keyboard Shortcut:** `Mod-i`
**Usage Example:**
```typescript
import Italic from '@tiptap/extension-italic'

editor.commands.toggleItalic()
```
**Gotchas:**
- Input rule: `*text*` or `_text_` auto-converts to italic
- Marks can overlap (bold + italic simultaneously)

#### Strike
**Description:** Strikethrough text.
**HTML:** Renders as `<s>` tag.
**Keyboard Shortcut:** `Mod-Shift-s`
**Usage Example:**
```typescript
import Strike from '@tiptap/extension-strike'

editor.commands.toggleStrike()
```
**Gotchas:**
- Input rule: `~~text~~` auto-converts to strikethrough

#### Underline
**Description:** Underlined text.
**HTML:** Renders as `<u>` tag.
**Keyboard Shortcut:** `Mod-u`
**Usage Example:**
```typescript
import Underline from '@tiptap/extension-underline'

editor.commands.toggleUnderline()
```
**Gotchas:**
- NOT included in StarterKit (install separately)
- Avoid overuse (confused with links)

#### Code
**Description:** Inline code formatting.
**HTML:** Renders as `<code>` tag.
**Keyboard Shortcut:** `Mod-e`
**Usage Example:**
```typescript
import Code from '@tiptap/extension-code'

editor.commands.toggleCode()
```
**Gotchas:**
- Excludes all other marks (can't have bold code)
- Input rule: `` `text` `` auto-converts to code
- Different from CodeBlock (inline vs block)

### Common Mistakes
- Mixing inline Code mark with CodeBlock node → They're separate; Code is inline, CodeBlock is block-level
- Expecting underline in StarterKit → Not included; install separately
- Not disabling input rules for literal markdown → Use `enableInputRules: false` if you don't want auto-conversion
- Applying marks to nodes that exclude them → Code blocks exclude bold/italic marks

### See Also
- → 6.2 Link Mark | URL handling
- → 6.3 Highlight & Text Style | Advanced marks
- Reference: https://tiptap.dev/docs/editor/extensions/marks

