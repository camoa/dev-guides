---
description: Optimize React design system component render performance using React.memo, useMemo, useCallback, and React.lazy with Suspense.
---

# Performance

## When to Use

> Use when a design system component is causing measurable performance issues, or when designing components that appear in long lists, frequently updating UIs, or high-traffic render paths. Profile first — do not optimize speculatively.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Skip re-render when props unchanged | `React.memo` | Wraps component; skips render if all props shallowly equal |
| Skip expensive derived values | `useMemo` with dependency array | Memoize filtered/sorted arrays, not primitive calculations |
| Stop re-render caused by new function ref | `useCallback` | Memoizes event handlers passed to `React.memo` children |
| Load component only when needed | `React.lazy` + `Suspense` | Reduces initial bundle; appropriate for heavy editors, charts, modals |
| Let React Compiler handle it | No manual memos | React Compiler (React 17+, optimized for 19) auto-memoizes pure components |

## Pattern

When to add `React.memo` (with a rule):
```tsx
// BEFORE adding React.memo, verify with React DevTools Profiler:
// 1. Component re-renders when parent re-renders with unchanged props
// 2. The re-render is visually noticeable OR in a hot path (long list)

const BadgeCount = React.memo(function BadgeCount({ count }: { count: number }) {
  return <span className="rounded-full bg-primary px-2 text-xs">{count}</span>;
});
// Use when: Badge appears in a list of 100+ items that frequently updates
// Skip when: Badge appears once or twice; memo overhead > render cost
```

Lazy loading for heavy components:
```tsx
const RichTextEditor = React.lazy(() => import('./RichTextEditor'));

function EditorPage() {
  return (
    <React.Suspense fallback={<div className="h-48 animate-pulse bg-muted rounded" />}>
      <RichTextEditor />
    </React.Suspense>
  );
}
```

## Common Mistakes

- **Wrong**: Adding `React.memo` to every component "just in case" → **Right**: Shallow comparison has cost too; profile first with React DevTools Profiler
- **Wrong**: `useMemo` for `cn()` calls → **Right**: `cn()` is string concatenation; it's faster than the memo overhead; never memoize it
- **Wrong**: Passing new object/array literals as props to memoized components → **Right**: `<Badge style={{ color: 'red' }}>` creates a new object on every render, defeating `React.memo`
- **Wrong**: Using `useCallback` without `React.memo` on the child → **Right**: `useCallback` only helps when the receiving component is memoized; otherwise it's pure overhead
- **Wrong**: Not profiling before optimizing → **Right**: React DevTools Profiler shows exactly what re-renders and why; never guess
- **Wrong**: Over-splitting components for "performance" → **Right**: Split for code organization; component splitting has reconciliation overhead

## See Also

- [Layout Components](layout-components.md)
- [Testing](testing.md)
- Reference: [React Docs — memo](https://react.dev/reference/react/memo)
- Reference: [React Docs — useMemo](https://react.dev/reference/react/useMemo)
