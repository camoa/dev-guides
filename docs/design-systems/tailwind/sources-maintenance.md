---
description: Source references, verified versions, and maintenance notes for the Tailwind CSS design system guides.
---

# Sources & Maintenance

## Source Guide

- **File**: `/tmp/design-system-tailwind.md`
- **Version**: 1.1
- **Last Updated**: 2026-02-19
- **SHA-256**: `1a94018ca2c9cc7eeab076a36f1c90656fd13c0af1e87f5fa977ec0da00e3df6`

## Web Sources

| Source | URL | Guides | Verified |
|--------|-----|--------|----------|
| Tailwind CSS v4.0 Release Blog | https://tailwindcss.com/blog/tailwindcss-v4 | tailwind-v3-vs-v4 | 2026-02-19 |
| Tailwind Installation Docs | https://tailwindcss.com/docs/installation | installation-integration | 2026-02-19 |
| Tailwind PostCSS Installation | https://tailwindcss.com/docs/installation/using-postcss | installation-integration | 2026-02-19 |
| Tailwind Next.js Guide | https://tailwindcss.com/docs/guides/nextjs | installation-integration, v4-configuration | 2026-02-19 |
| Tailwind Theme Variables (v4) | https://tailwindcss.com/docs/theme | v4-configuration, design-token-mapping, custom-theme-extension | 2026-02-19 |
| Tailwind Adding Custom Styles | https://tailwindcss.com/docs/adding-custom-styles | v4-configuration, custom-theme-extension, component-patterns | 2026-02-19 |
| Tailwind Detecting Classes in Source | https://tailwindcss.com/docs/detecting-classes-in-source-files | performance-optimization | 2026-02-19 |
| Tailwind Reusing Styles | https://tailwindcss.com/docs/reusing-styles | component-patterns, apply-guidance | 2026-02-19 |
| Tailwind Responsive Design | https://tailwindcss.com/docs/responsive-design | responsive-design | 2026-02-19 |
| Tailwind Dark Mode | https://tailwindcss.com/docs/dark-mode | dark-mode | 2026-02-19 |
| Tailwind Hover/Focus/States | https://tailwindcss.com/docs/hover-focus-and-other-states | utility-class-reference, accessibility | 2026-02-19 |
| Tailwind Upgrade Guide (v3→v4) | https://tailwindcss.com/docs/upgrade-guide | tailwind-v3-vs-v4, v3-configuration | 2026-02-19 |
| Tailwind v3 Configuration | https://v3.tailwindcss.com/docs/configuration | v3-configuration | 2026-02-19 |
| Class Variance Authority Docs | https://cva.style/docs | class-variance-authority | 2026-02-19 |
| CVA Variants Reference | https://cva.style/docs/getting-started/variants | class-variance-authority | 2026-02-19 |
| Style Dictionary | https://styledictionary.com/ | design-token-mapping, design-system-integration | 2026-02-19 |
| Tailwind Tokens Figma Plugin | https://www.figma.com/community/plugin/1513618945140968492 | design-system-integration | 2026-02-19 |
| Accreditly Tailwind Accessibility | https://accreditly.io/articles/make-the-web-accessible-with-tailwind-css | accessibility | 2026-02-19 |
| Colour A11y for Tailwind | https://colour-a11y.vercel.app/ | accessibility | 2026-02-19 |
| Tailwind Best Practices 2025 | https://www.faraazcodes.com/blog/tailwind-2025-best-practices | best-practices | 2026-02-19 |
| tailwind-merge GitHub | https://github.com/dcastil/tailwind-merge | tailwind-merge-clsx | 2026-02-19 |
| clsx GitHub | https://github.com/lukeed/clsx | tailwind-merge-clsx | 2026-02-19 |

## Code Sources

Verified from Next.js research install at `~/workspace/contrib-nextjs/nextjs-app/`:

| Package | Path | Guides | Version |
|---------|------|--------|---------|
| tailwindcss | `node_modules/tailwindcss/` | tailwind-v3-vs-v4, installation-integration, v4-configuration, utility-class-reference, custom-theme-extension, responsive-design, performance-optimization | 4.2.0 |
| tailwindcss theme | `node_modules/tailwindcss/theme.css` | v4-configuration, design-token-mapping, utility-class-reference, responsive-design | 4.2.0 |
| @tailwindcss/postcss | `node_modules/@tailwindcss/postcss/` | installation-integration | 4.2.0 |
| class-variance-authority | `node_modules/class-variance-authority/dist/index.js` | class-variance-authority | 0.7.1 |
| clsx | `node_modules/clsx/dist/clsx.js` | tailwind-merge-clsx | 2.1.1 |
| tailwind-merge | `node_modules/tailwind-merge/src/` | tailwind-merge-clsx | 3.5.0 |
| Next.js app globals | `src/app/globals.css` | v4-configuration | Next.js 16.1.6 |
| Next.js app layout | `src/app/layout.tsx` | v4-configuration | Next.js 16.1.6 |

## Maintenance Notes

- **Tailwind v4 is actively developed** — verify `@theme` namespace table against `node_modules/tailwindcss/theme.css` when updating.
- **Shadow rename (v3→v4)** — `shadow-sm` → `shadow-xs`, `shadow` → `shadow-sm`. The upgrade tool catches these.
- **tailwind-merge version pairing** — v2.x for Tailwind v3, v3.x for Tailwind v4.
- **CVA v0.7.1** — confirmed exports: `cva`, `cx`, `VariantProps`. Verify on next major version bump.
- **Container query sizes** — verified from `node_modules/tailwindcss/theme.css` v4.2.0. May expand in future versions.
