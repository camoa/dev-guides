---
description: UI Suite DaisyUI guides — DaisyUI 5 theme integration with Drupal, 51 SDC components, UI Patterns/Styles/Skins, Tailwind 4, starterkit sub-theming
tracks:
  - project: ui_suite_daisyui
    channel: alpha
    reason: no stable release exists; 5.0.x is alpha-only
    declared: "5.0.0-alpha6"
    verified: 2026-08-16
  - project: ui_patterns
    channel: stable
    declared: "2.0.20"
    verified: 2026-08-16
  - project: ui_styles
    channel: stable
    declared: "8.x-1.21"
    verified: 2026-08-16
  - project: ui_skins
    channel: stable
    declared: "1.2.1"
    verified: 2026-08-16
  - project: ui_icons
    channel: stable
    declared: "^1.1"
    reason: "not a stale declaration — the theme pins ^1.1 in composer.json at 5.0.0-alpha6, so ui_icons 2.0.0 cannot be installed with it. This row stays behind upstream on purpose until the theme widens the constraint; tracked in camoa/dev-guides#35."
    note: "the theme pins `ui_icons: ^1.1` in composer.json at 5.0.0-alpha6 and will not install ui_icons 2.x; drupal/ui-icons documents the project itself, now at 2.0.0"
    verified: 2026-08-16
guide-meta:
  concepts:
    - UI Suite DaisyUI
    - UI Patterns integration
    - UI Styles
    - UI Skins
    - DaisyUI 5 Drupal theme
    - Vite starterkit
    - Tailwind CSS 4 Drupal
    - 51 SDC components
  not:
    - DaisyUI library standalone (see design-systems/daisyui)
    - Radix theme (see design-systems/radix-sdc)
    - UI Patterns source plugins (see drupal/ui-patterns)
  requires:
    - drupal/sdc
    - drupal/ui-patterns
  complements:
    - design-systems/daisyui
    - design-systems/tailwind-tokens
    - drupal/layout-builder
  category: drupal
---

# UI Suite DaisyUI

Drupal theme integrating DaisyUI 5 component library via UI Patterns 2, UI Styles, UI Skins, and UI Icons. Provides 51 Single Directory Components, 35 theme variants, Tailwind CSS 4 integration, and a Vite-based starterkit for sub-theming.

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Decide if UI Suite DaisyUI fits my project | [Overview & Decision](overview-and-decision.md) | When to use UI Suite DaisyUI vs alternatives like Radix, custom Tailwind themes, or UI Suite Bootstrap |
| Understand how UI Patterns, Styles, Skins, and Icons integrate | [Architecture](architecture.md) | How UI Patterns, UI Styles, UI Skins, and UI Icons integrate with DaisyUI components in the theme |
| Install the theme and verify setup | [Installation & Setup](installation-and-setup.md) | Composer install, theme enable, hard dependencies (ui_patterns, ui_icons) vs. optional submodules (ui_patterns_library, ui_styles_library, ui_patterns_layouts) that gate the admin browsers and Layout Builder grids -- most 404s are a missing submodule, not a broken theme. |
| Find a DaisyUI component and its props/slots | [Theme Components Catalog](theme-components-catalog.md) | Complete reference of all 51 DaisyUI components with props, slots, variants, and usage examples |
| Apply utility styles to blocks or Layout Builder sections | [UI Styles Integration](ui-styles-integration.md) | Apply the theme's 10 UI Styles plugins (background/text color, font size, box shadow, width, padding, margin, glass, mask) to blocks, Layout Builder sections, and pattern instances -- there is no border-color, layout, or flexbox/grid style; add those in a sub-theme. |
| Switch DaisyUI themes or customize CSS variables | [UI Skins Integration](ui-skins-integration.md) | Switch between 35 DaisyUI themes and customize 28 CSS design tokens via the admin UI |
| Override a system template with DaisyUI styling | [Template Overrides](template-overrides.md) | 22 Drupal template overrides delegate to DaisyUI SDC components; every form template lives in templates/forms/, not templates/system/, and tab variants use DaisyUI 5 names (lift, border) -- the v4 lifted/bordered/form-control spellings render unstyled. |
| Understand theme preprocess hooks and form styling | [Preprocess & Hooks](preprocess-and-hooks.md) | No hook adds a CSS class to a form element -- hooks in ui_suite_daisyui.theme, includes/form.theme, and includes/settings.theme only compute a config array (#daisy_ui_form); templates/forms/input.html.twig and form-element.html.twig read it and decide the classes. There is no form_alter() and no preprocess_field(). |
| Create a sub-theme with Vite and Tailwind 4 | [Sub-theming Starterkit](sub-theming-starterkit.md) | Create a sub-theme when you need to customize the base theme's components, add new components, override UI Styles, or set up a proper Tailwind/DaisyUI build pipeline. Alpha6 ships a full starterkit with Vite, Tailwind CSS 4, DaisyUI 5, and example component overrides. |
| Decide whether to reuse, override, or create a component | [Component Reuse Decision Tree](component-reuse-decision-tree.md) | When deciding whether to use a base theme component as-is, override it in your sub-theme, or create a new component from scratch. |
| Use DaisyUI components with Layout Builder | [Layout Builder Integration](layout-builder-integration.md) | All 51 components register as Layout Builder layouts once ui_patterns_layouts is enabled -- icon_map only draws the picker thumbnail on the grids, it does not gate registration. Pick by slot shape (card's header/body/footer suit LB regions; button's single label slot does not). |
| Choose between UI Patterns wiring vs Twig include() for blocks → SDC | [SDC Rendering Decision](sdc-rendering-decision.md) | For 1-3 simple block types without per-instance variants, use UI Patterns wiring (native, no templates). For 5+ block types, per-instance variants, or complex multi-field composition, use Twig include() — it avoids 3-level entity_field nesting per slot and reads LB block configuration directly for per-placement variants. |
| Understand the CSS/JS asset pipeline | [Libraries & Assets](libraries-and-assets.md) | Pre-compiled CSS library, CKEditor 5 integration, and Heroicon pack configuration |
| Add custom components or override DaisyUI tokens | [Customization Patterns](customization-patterns.md) | Add custom components, override DaisyUI tokens, and extend base components |
| Follow best practices and avoid common mistakes | [Best Practices & Anti-Patterns](best-practices-and-anti-patterns.md) | When UI Suite DaisyUI fits, recommended patterns, anti-patterns to avoid, and performance considerations |
| Address security and accessibility concerns | [Security & Accessibility](security-and-accessibility.md) | Asset pipeline security, Twig escaping, form security -- the theme touches forms only through #daisy_ui_form config hooks and a theme-settings alter, never hook_form_alter() -- DaisyUI component accessibility, and WCAG concerns. |
| Find source references and maintenance info | [Sources & Maintenance](sources-maintenance.md) |  |
