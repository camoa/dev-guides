---
description: DaisyUI guide sources, verified versions, web references, and code file locations
---

# Sources and Maintenance

## Verified Against

- **DaisyUI** 5.5.18 — installed at `~/workspace/contrib-nextjs/nextjs-app/node_modules/daisyui/`
- **Tailwind CSS** 4.x — CSS-first config, no `tailwind.config.js`
- **Next.js** 16.1.6 — App Router

## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| DaisyUI Official Docs | https://daisyui.com/docs/ | Installation, Theming, Color Tokens, all Components | 2026-02-19 |
| DaisyUI Components Reference | https://daisyui.com/components/ | Actions, Data Display, Navigation, Input, Layout | 2026-02-19 |
| DaisyUI Theming Docs | https://daisyui.com/docs/themes/ | Theming System, Color Tokens | 2026-02-19 |
| DaisyUI GitHub Repository | https://github.com/saadeghi/daisyui | Installation, Theming, Customization, Best Practices | 2026-02-19 |
| WCAG 2.2 — Dialog ARIA Pattern | https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ | Security and Accessibility | 2026-02-19 |
| WCAG 2.2 — Menu Button Pattern | https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/ | Security and Accessibility | 2026-02-19 |

## Code Sources

| Module | Path | Covers |
|--------|------|--------|
| DaisyUI core plugin | `node_modules/daisyui/index.js` | Installation, Customization |
| DaisyUI plugin options | `node_modules/daisyui/functions/pluginOptionsHandler.js` | Installation, Theming |
| DaisyUI Tailwind variables | `node_modules/daisyui/functions/variables.js` | Color System |
| DaisyUI theme objects | `node_modules/daisyui/theme/light/object.js` | Theming, Color System |
| DaisyUI button component | `node_modules/daisyui/components/button/object.js` | Actions, Customization |
| DaisyUI card component | `node_modules/daisyui/components/card/object.js` | Data Display |
| DaisyUI modal component | `node_modules/daisyui/components/modal/object.js` | Actions, Security/Accessibility |
| DaisyUI input component | `node_modules/daisyui/components/input/object.js` | Data Input |
| DaisyUI fieldset component | `node_modules/daisyui/components/fieldset/object.js` | Data Input |
| DaisyUI menu component | `node_modules/daisyui/components/menu/object.js` | Navigation |
| DaisyUI drawer component | `node_modules/daisyui/components/drawer/object.js` | Layout |
| DaisyUI badge component | `node_modules/daisyui/components/badge/object.js` | Data Display |
| DaisyUI alert component | `node_modules/daisyui/components/alert/object.js` | Data Display, Security/Accessibility |
| DaisyUI tab component | `node_modules/daisyui/components/tab/object.js` | Navigation, Security/Accessibility |
| DaisyUI dropdown component | `node_modules/daisyui/components/dropdown/object.js` | Actions, Security/Accessibility |
| DaisyUI stat component | `node_modules/daisyui/components/stat/object.js` | Data Display |
| DaisyUI navbar component | `node_modules/daisyui/components/navbar/object.js` | Navigation |

## Design System Guide Chain

These guides are part of a larger design-to-code pipeline:

- `design_system_recognition_guide.md` — identify design elements
- `design-system-bootstrap-mapping.md` — map to Bootstrap 5.3
- `design-system-radix-sdc-mapping.md` — implement in Drupal Radix + SDCs
- `design-system-tailwind.md` — Tailwind fundamentals (read before this guide)
- `react-design-system.md` — React CVA/TypeScript component patterns
- **This guide** — DaisyUI semantic components on top of Tailwind

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-19 | Initial partitioning from DaisyUI Design System Guide v1.0 |
