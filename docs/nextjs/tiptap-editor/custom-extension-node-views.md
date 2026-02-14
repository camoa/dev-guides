---
description: You need custom DOM rendering for a node: interactive widgets, React components, or complex layouts.
---

## 8.3 Node Views & Custom Rendering

### When to Use
You need custom DOM rendering for a node: interactive widgets, React components, or complex layouts.

### Pattern
```typescript
import { Node } from '@tiptap/core'
import { ReactNodeViewRenderer } from '@tiptap/react'

// Define React component for node view
import { NodeViewWrapper } from '@tiptap/react'

function CustomComponent({ node, updateAttributes, selected }) {
  return (
    <NodeViewWrapper className={selected ? 'selected' : ''}>
      <div className="custom-node">
        <input
          type="text"
          value={node.attrs.customAttr}
          onChange={(e) => updateAttributes({ customAttr: e.target.value })}
        />
      </div>
    </NodeViewWrapper>
  )
}

// Register node view
const CustomNode = Node.create({
  name: 'customNode',
  group: 'block',
  atom: true, // Treat as single unit (not editable)

  addAttributes() {
    return {
      customAttr: { default: '' },
    }
  },

  parseHTML() {
    return [{ tag: 'div[data-type="custom"]' }]
  },

  renderHTML({ HTMLAttributes }) {
    return ['div', { 'data-type': 'custom', ...HTMLAttributes }]
  },

  addNodeView() {
    return ReactNodeViewRenderer(CustomComponent)
  },
})
```

### Common Mistakes
- Creating too many React node views → Performance cost; use sparingly (see 17.2 Node View Performance)
- Not wrapping in NodeViewWrapper → Positioning and selection break
- Forgetting `atom: true` for non-editable nodes → Users can place cursor inside
- Mutating node attributes directly → Use `updateAttributes()` function
- Using node views for simple styling → CSS is faster; node views are for interactivity

### See Also
- → 17.2 Node View Performance | React rendering costs
- Reference: https://tiptap.dev/docs/editor/extensions/custom-extensions/node-views

