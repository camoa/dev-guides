---
description: Use tailwind-merge and clsx together as cn() to safely merge Tailwind classes at runtime, resolving conflicts.
tldr: "Use `clsx` alone for conditional class joining with no override conflicts. Use `twMerge` (via `cn()`) when a consumer needs to override component-internal classes."
---

# tailwind-merge & clsx

## When to Use

> These two utilities solve different problems that arise when composing Tailwind class strings at runtime.

**Installed in this project**: `tailwind-merge@3.5.0`, `clsx@2.1.1`

## The Problem They Solve

- `clsx` — conditional class joining (handles falsy, arrays, objects). No Tailwind knowledge.
- `tailwind-merge` — intelligent class deduplication that understands Tailwind's specificity rules. Prevents `p-2 p-4` from outputting both (keeps last).
- Combined as `cn()` — the standard utility function pattern in shadcn/ui and the broader React+Tailwind ecosystem.

## Decision

| Situation | Use | Why |
|-----------|-----|-----|
| Simple conditional classes, no overrides | `clsx` alone | Zero overhead, handles all conditional patterns |
| Merging classes where later values should override | `twMerge` | Understands `p-2 p-4` → `p-4`, `text-red-500 text-blue-500` → `text-blue-500` |
| Component that accepts a `className` prop | `cn()` (clsx + twMerge) | Allows consumers to override internal styles cleanly |
| High-frequency render path | `clsx` alone if possible | `twMerge` has overhead; profile before adding to hot paths |

## Pattern — cn() Utility Function

```ts
// lib/utils.ts — standard pattern in this project
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Usage
cn('px-4 py-2', isLarge && 'px-6 py-3')    // handles conditions
cn('bg-red-500', props.className)            // consumer override wins
cn('p-2 p-4')                               // → 'p-4' (twMerge deduplicates)
```

## tailwind-merge API

(verified from `node_modules/tailwind-merge/src/index.ts`, v3.5.0):

| Function | Purpose |
|----------|---------|
| `twMerge(...inputs)` | Main function; pre-configured for Tailwind defaults |
| `twJoin(...inputs)` | Like `clsx` but no Tailwind conflict resolution; cheaper |
| `extendTailwindMerge(config)` | Extend the resolver for custom Tailwind utilities |
| `createTailwindMerge(getConfig)` | Create a custom resolver from scratch |

## Extending for Custom Utilities

```ts
import { extendTailwindMerge } from 'tailwind-merge';

// Tell tailwind-merge about your custom utility classes
const twMerge = extendTailwindMerge({
  extend: {
    classGroups: {
      'font-size': [{ text: ['heading', 'label', 'caption'] }],
    },
  },
});
```

## tailwind-merge v3 vs v2

v3 supports Tailwind v4.x; v2 supports v3.x. They are not cross-compatible — upgrading Tailwind v3→v4 requires also upgrading tailwind-merge v2→v3.

## Common Mistakes

- **Using `twMerge` everywhere without profiling** — it runs a regex parser on every call; `clsx` alone is sufficient when override conflicts aren't possible
- **Expecting `twMerge` to handle arbitrary CSS-in-JS strings** — it only understands Tailwind class names
- **Forgetting to update tailwind-merge when upgrading Tailwind** — v2 doesn't know v4 class names and will fail to deduplicate them
- **Using `twJoin` when you actually need conflict resolution** — `twJoin` is fast but doesn't deduplicate; `px-2 px-4` through `twJoin` stays as-is

## See Also

- [Component Patterns](component-patterns.md) (parent section)
- [Class Variance Authority](class-variance-authority.md)
- Reference: https://github.com/dcastil/tailwind-merge
- Reference: https://github.com/lukeed/clsx
