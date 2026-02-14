---
description: You have React node views and experiencing performance issues.
---

## 17.2 Node View Performance Considerations

### When to Use
You have React node views and experiencing performance issues.

### Problem
React node views are rendered synchronously. Tiptap creates DOM elements and mounts React components for each node view. With many instances (e.g., 100+ nodes), this causes lag.

### Solutions

#### 1. Use Plain HTML for Simple Cases
```typescript
// ❌ SLOW: React component for simple rendering
addNodeView() {
  return ReactNodeViewRenderer(({ node }) => (
    <div className="custom">{node.attrs.text}</div>
  ))
}

// ✓ FAST: Plain HTML rendering
renderHTML({ HTMLAttributes, node }) {
  return ['div', { class: 'custom' }, node.attrs.text]
}
```

#### 2. Virtualize Long Lists
```typescript
// For documents with 100+ node views, use virtual scrolling
import { FixedSizeList } from 'react-window'

// Render only visible items
```

#### 3. Lazy Load Node Views
```typescript
// Load heavy node views on demand
addNodeView() {
  return ReactNodeViewRenderer(
    lazy(() => import('./HeavyComponent'))
  )
}
```

### Decision
| Scenario | Solution | Why |
|---|---|---|
| Simple static content | Plain HTML (`renderHTML`) | 10x faster than React |
| Interactive widgets (few) | React node views | Acceptable performance |
| Interactive widgets (many) | Virtual scrolling | Render only visible |
| Image galleries | Lazy loading | Don't mount all upfront |

### Common Mistakes
- Using React node views for everything → Massive performance cost; use HTML when possible
- Not virtualizing long documents → Mounting 1000+ React components freezes browser
- Complex components in node views → Keep node views simple; complex logic elsewhere
- Not memoizing node view components → Re-render on every editor update

### See Also
- ← 17.1 React Performance
- Reference: https://tiptap.dev/docs/guides/performance#react-node-views-performance

