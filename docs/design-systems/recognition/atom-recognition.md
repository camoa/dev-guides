---
description: Identify the smallest functional UI building blocks that cannot be decomposed further
---

# Atom Recognition

## When to Use

> Use when analyzing a UI and need to identify foundational elements. Use before identifying molecules — atoms are the base components.

## Decision

| Atom Category | Examples | Recognition Cues |
|---------------|----------|------------------|
| **Form Elements** | Input, textarea, select, checkbox, radio | Native HTML form elements |
| **Buttons** | Button, icon button, link | Interactive click targets |
| **Typography** | Heading, paragraph, label, caption | Text elements with semantic tags |
| **Media** | Image, video, icon, avatar | Visual content elements |
| **Indicators** | Badge, tag, status dot, spinner | Visual feedback elements |
| **Dividers** | Horizontal rule, vertical divider | Separators |

## Pattern

**Atom Identification Process:**

```
1. Extract all UI elements
   - Scan interface for distinct visual elements
   - Ignore layout/spacing

2. Test decomposability
   - Can it be broken into smaller functional parts?
   - NO → Atom
   - YES → Molecule or organism

3. Verify functional independence
   - Does it function on its own?
   - Structurally minimal?
```

**Comprehensive Atom Catalog:**

| Category | Atoms |
|----------|-------|
| Form | Text input, textarea, select, checkbox, radio, range slider, file upload, toggle |
| Button | Primary, secondary, tertiary, icon button, link button |
| Typography | Heading (h1-h6), paragraph, label, caption, blockquote |
| Media | Image, video, icon, avatar, logo |
| Indicator | Badge, tag, status dot, progress bar, spinner |
| Structural | Divider, vertical divider |

**Source Recognition:**

- **HTML/CSS**: `<button>`, `<input>`, `<label>`, `<img>`, class names like `.btn`, `.badge`
- **Figma**: Base components (not component sets), lowest hierarchy in Assets panel
- **Screenshots**: Smallest distinct visual elements that repeat consistently

## Common Mistakes

- **Wrong**: Tokens (colors, spacing) classified as atoms → **Right**: Atoms are UI elements; tokens are values
- **Wrong**: Search bar (input + button) as atom → **Right**: Compound elements are molecules
- **Wrong**: Button primary vs secondary as separate atoms → **Right**: Same atom, different variant styling
- **Wrong**: Every CSS class is an atom → **Right**: Focus on functional UI elements, not utility classes

## See Also

- [Molecule Recognition](./molecule-recognition.md)
- [Design Tokens](./design-tokens.md)
- Reference: [Atomic Design Atoms](https://atomicdesign.bradfrost.com/chapter-2/#atoms)
