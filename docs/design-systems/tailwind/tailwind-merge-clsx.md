---
description: Use tailwind-merge and clsx together as cn() to safely merge Tailwind classes at runtime, resolving conflicts.
---

# tailwind-merge & clsx

## When to Use

> Use `clsx` alone for conditional class joining with no override conflicts. Use `twMerge` (via `cn()`) when a consumer needs to override component-internal classes.

## Decision

| Situation | Use | Why |
|-----------|-----|-----|
| Simple conditional classes, no overrides | `clsx` alone | Zero overhead, handles all conditional patterns |
| Merging classes where later values should override | `twMerge` | Understands `p-2 p-4` → `p-4`, `text-red-500 text-blue-500` → `text-blue-500` |
| Component that accepts a `className` prop | `cn()` (clsx + twMerge) | Allows consumers to override internal styles cleanly |
| High-frequency render path | `clsx` alone if possible | `twMerge` has overhead; profile before adding to hot paths |

## Pattern

```ts
// lib/utils.ts — standard cn() pattern
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Usage
cn('px-4 py-2', isLarge && 'px-6 py-3')    // handles conditions
cn('bg-red-500', props.className)            // consumer override wins
cn('p-2 p-4')                               // → 'p-4' (deduplicates)
```

## tailwind-merge API (v3.5.0)

| Function | Purpose |
|----------|---------|
| `twMerge(...inputs)` | Main function; pre-configured for Tailwind defaults |
| `twJoin(...inputs)` | Like `clsx` but no conflict resolution; cheaper |
| `extendTailwindMerge(config)` | Extend resolver for custom Tailwind utilities |
| `createTailwindMerge(getConfig)` | Create a custom resolver from scratch |

## Extending for Custom Utilities

```ts
import { extendTailwindMerge } from 'tailwind-merge';

const twMerge = extendTailwindMerge({
  extend: {
    classGroups: {
      'font-size': [{ text: ['heading', 'label', 'caption'] }],
    },
  },
});
```

## Version Compatibility

| tailwind-merge version | Tailwind CSS version |
|------------------------|----------------------|
| v3.x | v4.x |
| v2.x | v3.x |

Not cross-compatible — upgrading Tailwind v3→v4 requires upgrading tailwind-merge v2→v3.

## Common Mistakes

- **Wrong**: Using `twMerge` everywhere without profiling. **Right**: `clsx` alone is sufficient when override conflicts aren't possible; `twMerge` runs a regex parser on every call.
- **Wrong**: Expecting `twMerge` to handle arbitrary CSS-in-JS strings. **Right**: It only understands Tailwind class names.
- **Wrong**: Using `twJoin` when you need conflict resolution. **Right**: `twJoin` is fast but doesn't deduplicate; use `twMerge` when `px-2 px-4` must resolve to `px-4`.
- **Wrong**: Forgetting to update tailwind-merge when upgrading Tailwind. **Right**: v2 doesn't know v4 class names and will fail to deduplicate them.

## See Also

- [Class Variance Authority](class-variance-authority.md)
- [Component Patterns](component-patterns.md)
- Reference: https://github.com/dcastil/tailwind-merge
- Reference: https://github.com/lukeed/clsx
