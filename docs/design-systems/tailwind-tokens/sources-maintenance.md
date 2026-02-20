---
description: Sources and maintenance manifest for Tailwind Tokens guides
---

# Sources & Maintenance

## Web Sources

| Source | Topic | URL | Verified |
|---|---|---|---|
| Tailwind CSS v4 Docs | Theme variables, @theme directive | https://tailwindcss.com/docs/theme | 2026-02 |
| Tailwind CSS v4.0 Blog | Release announcement, architecture | https://tailwindcss.com/blog/tailwindcss-v4 | 2026-02 |
| DaisyUI Colors Docs | Color system, CSS variables | https://daisyui.com/docs/colors/ | 2026-02 |
| DaisyUI Themes Docs | Custom theme syntax, oklch usage | https://daisyui.com/docs/themes/ | 2026-02 |
| DaisyUI v5 Release Notes | New variables, @plugin syntax | https://daisyui.com/docs/v5/ | 2026-02 |
| W3C Design Tokens Spec | DTCG 2025.10 stable specification | https://www.designtokens.org/tr/drafts/format/ | 2026-02 |
| W3C DTCG Community Group | Specification status, announcements | https://www.w3.org/community/design-tokens/ | 2026-02 |
| Figma Variables to Code | Export workflow, Tokens Studio | https://figmafy.com/figma-variables-to-code-tokens-to-tailwind-css-vars/ | 2026-02 |
| oklch.com | Interactive oklch color converter | https://oklch.com/ | 2026-02 |
| LogRocket DaisyUI 5 Guide | DaisyUI v5 feature overview | https://blog.logrocket.com/daisyui-5-whats-new/ | 2026-02 |
| Style Dictionary DTCG Docs | Build tool for token transformation | https://styledictionary.com/info/dtcg/ | 2026-02 |

## Code Sources

| Path | What It Contains |
|---|---|
| ~/workspace/contrib/web/themes/contrib/ui_suite_daisyui/ | UI Suite DaisyUI base theme: CSS vars config, theme skins, component templates |
| ~/workspace/contrib/web/themes/contrib/ui_suite_daisyui/starterkits/ui_suite_daisyui_starterkit/css/ | Starterkit token definitions: @theme, @plugin, @utility patterns |
| ~/workspace/contrib/web/themes/contrib/ui_suite_daisyui/starterkits/ui_suite_daisyui_starterkit/css/utilities/ | Semantic utility classes: typography, grid, spacing, containers |
| ~/workspace/contrib-nextjs/nextjs-app/ | Tailwind v4 reference project (Next.js app with PostCSS) |

## Maintenance Notes

- **Tailwind CSS**: v4 is current stable. Monitor for namespace additions in minor releases (v4.1 added text-shadow, mask utilities).
- **DaisyUI**: v5 is current stable. The 28-variable set is comprehensive; monitor for new variables in future releases.
- **W3C Design Tokens**: Spec reached first stable (2025.10). Composite types and alias syntax are finalized.
- **UI Suite DaisyUI**: Check ui_suite_daisyui.ui_skins.css_variables.yml when upgrading the Drupal module for new/changed variables.
- **Re-verify**: When Tailwind v5 or DaisyUI v6 releases, review namespace changes and update namespace reference and CSS variable reference guides.
