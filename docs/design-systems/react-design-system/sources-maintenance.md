---
description: Source references, verified package versions, and maintenance notes for the React design system guides.
---

# Sources and Maintenance

## Verified Package Versions

| Package | Version | Guides |
|---------|---------|--------|
| React | 19.2.3 | composition-patterns, typescript-patterns, performance |
| Next.js | 16.1.6 | composition-patterns, component-organization |
| Tailwind CSS | 4.2.0 | tailwind-integration, variant-management, design-token-consumption |
| `@radix-ui/react-slot` | 1.2.4 | children-and-slot-patterns, composition-patterns |
| `@radix-ui/react-dialog` | 1.1.15 | composition-patterns |
| `@radix-ui/react-tabs` | 1.1.13 | composition-patterns |
| `@radix-ui/react-accordion` | 1.2.12 | composition-patterns |
| `class-variance-authority` | 0.7.1 | tailwind-integration, variant-management |
| `tailwind-merge` | 3.5.0 | tailwind-integration |
| `clsx` | 2.1.1 | tailwind-integration |
| `react-hook-form` | 7.71.1 | form-components |
| `@testing-library/react` | 16.3.2 | testing |
| `@storybook/react` | 10.2.10 | storybook-integration |
| `lucide-react` | 0.575.0 | accessibility-patterns |

## Code Sources

All paths relative to `~/workspace/contrib-nextjs/nextjs-app/`

| File | Purpose |
|------|---------|
| `src/app/globals.css` | Tailwind v4 CSS-first token setup — verified source for design-token-consumption |
| `node_modules/@radix-ui/react-slot/dist/index.js` | Slot mergeProps behavior — verified source for children-and-slot-patterns |
| `node_modules/@radix-ui/react-dialog/dist/index.js` | Compound component + Context pattern — verified source for composition-patterns |
| `node_modules/@radix-ui/react-tabs/dist/index.js` | useControllableState pattern — verified source for composition-patterns |
| `node_modules/class-variance-authority/dist/index.js` | CVA exports (cva, cx, VariantProps) — verified source for tailwind-integration |
| `node_modules/tailwind-merge/dist/bundle-cjs.js` | Class group conflict resolution — verified source for tailwind-integration |

## Web Sources

| Source | URL | Guides |
|--------|-----|--------|
| Radix UI Primitives | https://www.radix-ui.com/primitives/docs/overview/introduction | component-architecture-decisions, composition-patterns, accessibility-patterns |
| Radix UI — Composition (asChild) | https://www.radix-ui.com/primitives/docs/guides/composition | children-and-slot-patterns |
| CVA Docs | https://cva.style/docs | tailwind-integration, variant-management |
| tailwind-merge | https://github.com/dcastil/tailwind-merge | tailwind-integration |
| tailwind-variants | https://www.tailwind-variants.org/docs/introduction | tailwind-integration, variant-management |
| shadcn/ui Button | https://ui.shadcn.com/docs/components/button | component-architecture-decisions, children-and-slot-patterns |
| shadcn/ui Theming | https://ui.shadcn.com/docs/theming | design-token-consumption |
| React TypeScript Cheatsheet | https://react-typescript-cheatsheet.netlify.app/ | typescript-patterns |
| Kent C. Dodds — Compound Components | https://kentcdodds.com/blog/compound-components-with-react-hooks | composition-patterns |
| WAI-ARIA Authoring Practices | https://www.w3.org/WAI/ARIA/apg/ | accessibility-patterns |
| Storybook CSF3 | https://storybook.js.org/docs/api/csf | storybook-integration |
| react-hook-form | https://react-hook-form.com/advanced-usage | form-components |
| Tailwind CSS v4 Upgrade Guide | https://tailwindcss.com/docs/v4-upgrade | design-token-consumption |
| React Docs — memo | https://react.dev/reference/react/memo | performance |
| React 19 release blog | https://react.dev/blog/2024/12/05/react-19 | composition-patterns, typescript-patterns |
| React Testing Library | https://testing-library.com/docs/react-testing-library/intro/ | testing |
| jest-axe | https://github.com/nickcolley/jest-axe | testing |
| OWASP Top 10 | https://owasp.org/www-project-top-ten/ | best-practices-and-anti-patterns |

## Source Guide

- **Path**: `/tmp/react-design-system.md`
- **Guide version**: 1.1
- **Last updated**: 2026-02-19
- **Partitioned**: 2026-02-19 by Carlos Ospina

## Maintenance Notes

- This guide covers React/Next.js ecosystem, not Drupal
- Tailwind v4 patterns (CSS-first `@theme inline`) differ significantly from v3 (`tailwind.config.ts`); do not merge v3 and v4 instructions
- React 19 ref-as-prop changes mean `forwardRef` is deprecated but still functional; both patterns are shown in composition-patterns
- CVA v0.7.1 exports: `cva`, `cx` (clsx re-export), `VariantProps` — the `cx` export is NOT tailwind-merge aware
- `@radix-ui/react-slot` 1.2.4: Slot className merging uses simple string join, NOT tailwind-merge; callers must resolve conflicts before passing to Slot
