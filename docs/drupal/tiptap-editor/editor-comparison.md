---
description: You need to make an informed decision between Tiptap, Lexical, and Slate based on specific project requirements.
---

## 1.2 Editor Comparison Matrix

### When to Use
You need to make an informed decision between Tiptap, Lexical, and Slate based on specific project requirements.

### Decision
| Criteria | Tiptap | Lexical | Slate |
|---|---|---|---|
| Foundation | ProseMirror | Custom (Meta-built) | Custom |
| Framework | Framework-agnostic | React-first | React-only |
| Maturity | Production-ready (2+ years) | Pre-1.0 (needs maturity) | Mature (6+ years) |
| Bundle Size | Small (~40KB) | Very small (~25KB) | Small (~50KB) |
| Performance | Excellent | Excellent | Good |
| Customization | High (extensions) | Very High (nodes) | Extreme (full control) |
| Learning Curve | Moderate | Steep | Steep |
| Collaboration | Yjs/Liveblocks | Yjs (limited) | Yjs/custom |
| Community | Large, active | Growing (Meta backing) | Smaller, dedicated |
| TypeScript | Excellent | Excellent | Good |
| Extension Ecosystem | Extensive | Limited | Moderate |
| Commercial Support | Yes (Tiptap Cloud) | No | No |
| Best For | Production apps today | Future-proof Meta stack | Unique custom editors |

### Pattern
**Tiptap strengths:**
- ProseMirror's battle-tested transaction model
- Modular extension system
- Strong TypeScript support
- Production-ready today
- Excellent documentation

**Lexical strengths:**
- Meta backing (used in Facebook products)
- No external dependencies
- Very high performance
- Low memory usage

**Slate strengths:**
- Complete customization control
- React-native schema model
- Ideal for novel editing experiences

### Common Mistakes
- Choosing Lexical for immediate production needs → Wait for 1.0 release; Tiptap is safer today
- Using Slate for standard rich text → Overkill unless you need extreme customization
- Ignoring bundle size in mobile apps → Lexical wins here; Tiptap second; Slate third
- Not considering collaboration requirements → Tiptap has best Yjs integration; Lexical limited to decorator nodes issue
- Betting on features over maturity → Lexical lacks pure decorations (cursor positioning issues); Tiptap has solved this

### See Also
- ← 1.1 Tiptap Overview
- Reference: https://liveblocks.io/blog/which-rich-text-editor-framework-should-you-choose-in-2025

