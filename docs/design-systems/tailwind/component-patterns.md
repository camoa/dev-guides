---
description: Decide when to keep utilities inline, extract to a framework component, or create a component class — the Tailwind extraction decision.
---

# Component Patterns & Style Reuse

## When to Use

> Use when deciding how to handle repeated style patterns — when to extract into a component class, when to use a framework component, and when utilities directly in markup are correct.

## Decision

| Situation | Approach | Rationale |
|-----------|----------|-----------|
| Pattern used once | Keep utilities in markup | No abstraction cost; easy to change |
| Pattern in a loop (same file) | Keep utilities in markup | Loop renders once; no duplication |
| Pattern duplicated across multiple files | Framework component (React/Vue/Twig) | Co-locate styles and structure |
| Pattern needed as CSS class (non-component context) | `@layer components` | When framework components aren't available |
| Variant-heavy component (button, badge, alert) | CVA library | Structured variant management with TypeScript safety |
| Simple one-liner custom utility | `@utility` directive | Adds responsive/state variant support |

## Pattern

```html
<!-- Inline utilities — correct for single-use or loop-rendered patterns -->
<article class="rounded-lg border border-gray-200 p-6 shadow-sm hover:shadow-md transition-shadow">
  <h2 class="text-xl font-semibold text-gray-900 mb-2">Title</h2>
  <p class="text-gray-600 leading-relaxed">Body text</p>
</article>
```

```tsx
// Framework component — correct when pattern repeats across files
function Card({ title, body }: { title: string; body: string }) {
  return (
    <article className="rounded-lg border border-gray-200 p-6 shadow-sm hover:shadow-md transition-shadow">
      <h2 className="text-xl font-semibold text-gray-900 mb-2">{title}</h2>
      <p className="text-gray-600 leading-relaxed">{body}</p>
    </article>
  );
}
```

## Extraction Signal

Copy-pasting the same 8+ utility classes across multiple files = time to create a framework component. The markup IS the component contract — extract to a component, not to CSS.

## See Also

- [@apply Guidance](apply-guidance.md)
- [Class Variance Authority](class-variance-authority.md)
- [tailwind-merge & clsx](tailwind-merge-clsx.md)
- [Dark Mode](dark-mode.md)
- Reference: https://tailwindcss.com/docs/reusing-styles
