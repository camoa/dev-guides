---
description: Optimize React design system component render performance using React.memo, useMemo, useCallback, and React.lazy with Suspense.
tldr: "Use when a design system component is causing measurable performance issues, or when designing components that appear in long lists, frequently updating UIs, or high-traffic render paths. Profile first — do not optimize speculatively."
---

# Performance

## When to Use

> When a design system component is causing measurable performance issues, or when designing components that appear in long lists, frequently updating UIs, or high-traffic render paths.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Skip re-render when props unchanged | `React.memo` | Wraps component; skips render if all props shallowly equal |
| Skip expensive class computation | `useMemo` for `cn()` calls | Only beneficial if CVA/cn computation is genuinely expensive (it rarely is) |
| Skip expensive derived values | `useMemo` with dependency array | Memoize filtered/sorted arrays, not primitive calculations |
| Load component only when needed | `React.lazy` + `Suspense` | Reduces initial bundle; appropriate for heavy editors, charts, modals |
| Stop re-render caused by new function ref | `useCallback` | Memoizes event handlers passed to `React.memo` children |
| Let React Compiler handle it | No manual memos | React Compiler (released for React 17+, optimized for 19) auto-memoizes pure components; enable via babel/SWC plugin |

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

Lazy loading for heavy design system components:
```tsx
// Heavy components (rich text editor, chart, code block) should be lazy
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

- Adding `React.memo` to every component "just in case" → shallow comparison has cost too; profile first; memoize only components with proven render waste
- `useMemo` for `cn()` calls → `cn()` is a string concatenation; it's faster than the memo overhead; don't memoize it
- Passing new object/array literals as props to memoized components → `<Badge style={{ color: 'red' }}>` creates new object on every render, defeating `React.memo`
- Using `useCallback` without `React.memo` on the child → `useCallback` only helps when the receiving component is memoized; otherwise it's overhead with no benefit
- Not profiling before optimizing → React DevTools Profiler shows exactly what re-renders and why; don't guess
- Over-splitting components for "performance" → component splitting has its own overhead (more reconciliation nodes); split for code organization, not performance

## See Also

- [Layout Components](layout-components.md)
- [Testing](testing.md)
- Reference: [React memo](https://react.dev/reference/react/memo)
- Reference: [Saeloun — memo vs useMemo](https://blog.saeloun.com/2024/02/15/memo-vs-usememo-when-to-use-each-for-better-react-performance/)
- Reference: [React Docs — useMemo](https://react.dev/reference/react/useMemo)
