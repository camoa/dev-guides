---
description: Design system recognition — 3. atom recognition
---

## 3. Atom Recognition

#### When to Use This Section
- You're analyzing a UI and need to identify the smallest functional building blocks
- You're extracting foundational elements from HTML, Figma, or screenshots
- You need to catalog all atoms before identifying molecules

#### Decision Table: Common Atoms

| Atom Category | Examples | Recognition Cues |
|---------------|----------|------------------|
| **Form Elements** | Input, textarea, select, checkbox, radio | Native HTML form elements |
| **Buttons** | Button, icon button, link | Interactive click targets |
| **Typography** | Heading, paragraph, label, caption | Text elements with semantic tags |
| **Media** | Image, video, icon, avatar | Visual content elements |
| **Indicators** | Badge, tag, status dot, spinner | Visual feedback elements |
| **Dividers** | Horizontal rule, vertical divider | Separators |

#### Pattern: Atom Identification Process

**Step 1: Extract all UI elements**
- Scan the interface for every distinct visual element
- Ignore layout/spacing (those are templates/organisms)
- Focus on elements that cannot be decomposed further

**Step 2: Test decomposability**
- Can it be broken into smaller functional parts?
- If NO → It's an atom
- If YES → It's a molecule or organism

**Step 3: Verify functional independence**
- Does it function on its own?
- If NO (requires context) → May still be atom if structurally minimal
- If YES → Likely atom or molecule

**Reference Sources:**
- Atomic design atoms: [https://atomicdesign.bradfrost.com/chapter-2/#atoms](https://atomicdesign.bradfrost.com/chapter-2/)
- Component examples: [Building better UIs with Atomic Design](https://www.justinmind.com/ui-design/atomic-design)
- Design system examples: [Atomic Design methodology](https://blog.kamathrohan.com/atomic-design-methodology-for-building-design-systems-f912cf714f53)

**Comprehensive Atom Catalog:**

**Form Atoms:**
- Text input (single-line)
- Textarea (multi-line)
- Select dropdown
- Checkbox
- Radio button
- Range slider
- Date picker input
- File upload button
- Toggle/switch

**Button Atoms:**
- Primary button
- Secondary button
- Tertiary/ghost button
- Icon button
- Link button

**Typography Atoms:**
- Heading (h1-h6)
- Paragraph
- Label
- Caption
- Blockquote
- List item

**Media Atoms:**
- Image
- Video player controls (play, pause, volume)
- Icon (SVG/font icon)
- Avatar
- Logo

**Indicator Atoms:**
- Badge (notification count)
- Tag/chip
- Status dot (online/offline)
- Progress bar
- Spinner/loader

**Structural Atoms:**
- Divider (horizontal rule)
- Vertical divider
- Spacer (though often implemented as token/utility)

**Recognition in Different Sources:**

**HTML/CSS:**
- Look for: `<button>`, `<input>`, `<label>`, `<img>`, `<h1>-<h6>`, `<p>`, `<hr>`
- Check class names: `.btn`, `.input`, `.badge`, `.avatar`, `.icon`

**Figma:**
- Base components (not component sets)
- Elements without nested component instances
- Entries in "Assets" panel at lowest hierarchy level

**Screenshots:**
- Smallest distinct visual elements
- Elements that repeat consistently across interface
- Components that don't contain other components

#### Common Mistakes
- **Confusing atoms with tokens** — Tokens are values (colors, spacing); atoms are UI elements (buttons, inputs)
- **Treating compound elements as atoms** — If it contains multiple elements, it's a molecule
- **Missing variant atoms** — Button primary vs secondary are the same atom with different styling
- **Over-atomizing** — Not every CSS class is an atom; focus on functional UI elements

#### See Also
- [4. Molecule Recognition](#4-molecule-recognition)
- [1. Foundation Layer: Design Tokens](#1-foundation-layer-design-tokens)

---
