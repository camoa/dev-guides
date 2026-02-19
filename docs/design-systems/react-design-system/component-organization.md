---
description: Structure React design system files using flat folders (small systems) or atomic design (large systems) with explicit barrel exports.
---

# Component Organization

## When to Use

> Use when setting up a design system repository or deciding where to put a new component.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Small-medium system (<50 components) | Flat component folders | Simple; no mental model overhead; easy to navigate |
| Large system or team structure guidance | Atomic design (atoms/molecules/organisms) | Shared vocabulary; consistent grouping decisions |
| Co-located styles/stories/tests | Same folder as component | Easier to find, move, and delete; no cross-directory tracking |
| Public API control | Explicit barrel exports | Prevent consumers from importing internal utilities |
| Monorepo design system package | `packages/ui/` with its own `package.json` | Separate versioning; consumed by multiple apps |

## Pattern

Recommended flat structure (small-medium systems):
```
src/components/
  Button/
    Button.tsx          # Component
    Button.stories.tsx  # Stories
    Button.test.tsx     # Tests
    index.ts            # Re-export: export { Button } from './Button';
  Input/
    ...
  Card/
    ...
index.ts                # Root barrel: export * from './Button'; export * from './Input';
```

Atomic structure (large systems):
```
src/components/
  atoms/          # Button, Input, Icon, Badge, Label
  molecules/      # FormField (Label + Input + Error), SearchBar
  organisms/      # NavigationBar, DataTable, PageHeader
  layout/         # Stack, Flex, Grid, Container
  index.ts        # Single export point
```

Barrel export (explicit — don't re-export internals):
```ts
// components/Button/index.ts
export { Button } from './Button';
export type { ButtonProps } from './Button';
// NOT: export * from './Button' (leaks internal helpers)
```

## Common Mistakes

- **Wrong**: Deep barrel exports with `export * from '...'` at every level → **Right**: Prefer explicit named exports; wildcard re-exports break tree-shaking in some bundlers
- **Wrong**: Mixing component files with page/feature files → **Right**: The components directory is for reusable UI only; page-specific code lives in `app/` or `pages/`
- **Wrong**: No `index.ts` per component folder → **Right**: Always add one; without it callers import from `Button/Button` inconsistently
- **Wrong**: Committing to atomic terminology too early → **Right**: Use flat structure until patterns emerge naturally; rename later
- **Wrong**: Putting test utilities and mock data inside component folders → **Right**: Shared mocks belong in `src/test-utils/`; co-location is for component-specific tests only

## See Also

- [Storybook Integration](storybook-integration.md)
- [Form Components](form-components.md)
- Reference: [Robin Wieruch — React Folder Structure](https://www.robinwieruch.de/react-folder-structure/)
