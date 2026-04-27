---
description: Best Practices — camoa playbook. Opinionated rules for Drupal projects with Radix/Bootstrap sub-themes covering CSS, Layout Builder, responsive images, config, SDC, and JS.
guide-meta:
  concepts:
    - Bootstrap
    - RFS
    - responsive font sizes
    - map-merge
    - media-breakpoint-up
    - mobile-first
    - Layout Builder
    - LB Styles
    - SDC
    - single directory components
    - responsive images
    - image styles
    - view mode
    - metatag
    - BEF
    - better_exposed_filters
    - config_exclude_modules
    - base_field_override
    - Drupal behaviors
    - once()
    - window.innerWidth
    - block template
    - composer module removal
    - config over code
    - hardcoded content
    - Twig templates
  not:
    - UI Patterns
    - Storybook
    - stories.yml
    - design tokens
  requires: []
  complements:
    - drupal/sdc
    - drupal/layout-builder
    - drupal/image-styles
    - drupal/better-exposed-filters
    - drupal/twig
    - drupal/config-management
    - design-systems/radix-sdc
  specializes: ""
  category: drupal
---

# Best Practices — camoa

Opinionated playbook rules for Drupal projects with Radix/Bootstrap sub-themes. Each rule is atomic and citable.

| Rule | Guide | Summary |
|------|-------|---------|
| Bootstrap before custom CSS | [Use Bootstrap Before Custom CSS](use-bootstrap-before-custom-css.md) | Always check if Bootstrap provides a class, mixin, variable, or utility before writing custom SCSS. |
| Never replace Bootstrap maps | [Never Replace Bootstrap Maps](never-replace-bootstrap-maps.md) | Extend Bootstrap maps with `map-merge()` in a map-overrides partial. Never overwrite Bootstrap's `$spacers`, `$theme-colors`, or other maps directly. |
| Font sizing via RFS | [Font Sizing — Always Use RFS](font-sizing-always-use-rfs.md) | Never set `font-size:` directly on headings or body text. Use Bootstrap's `@include font-size()` mixin which handles responsive scaling via RFS. |
| Mobile-first breakpoints | [Mobile-First Breakpoints](mobile-first-breakpoints.md) | Use Bootstrap's `media-breakpoint-up()` for desktop overrides. Define mobile as the base, layer up. Pick the project's stacking breakpoint intentionally. |
| No direct child selectors with LB | [No Direct Child Selectors with Layout Builder](no-direct-child-selectors-with-layout-builder.md) | Layout Builder wraps blocks in variable-depth divs. Never use `>` in selectors that target Layout Builder content. |
| LB styles stay at wrapper level | [LB Styles Must Not Override Component Internals](lb-styles-must-not-override-component-internals.md) | Layout Builder style plugins should apply to the section or block wrapper level. They must not cascade into component-specific elements. |
| Media view mode → responsive image | [Media View Mode → Responsive Image Style](media-view-mode-to-responsive-image-style.md) | Never use the `default` media view mode for content display. Create purpose-specific view modes with responsive image formatters. |
| Responsive image sizing per context | [Responsive Image Sizing Per Context](responsive-image-sizing-per-context.md) | Match responsive image styles to actual display size. A card must not serve hero-sized sources. |
| Sizes-based vs breakpoint-based images | [Sizes-Based vs Breakpoint-Based](sizes-based-vs-breakpoint-based.md) | Use the `sizes` attribute when image width depends on layout. Use breakpoint-specific mappings when art-direction differs per breakpoint. |
| No hardcoded content in templates | [No Hardcoded Content in Templates](no-hardcoded-content-in-templates.md) | All user-facing text must be CMS-editable. Section headings come from block labels or view titles — never from Twig. |
| Config over code | [Config Over Code](config-over-code.md) | Prefer config-only solutions over custom PHP. When unavoidable, use theme preprocess hooks — not controllers or services. |
| Field descriptions via config | [Field Descriptions via Base Field Overrides](field-descriptions-via-base-field-overrides.md) | To add help text to base fields, use `core.base_field_override` config — not `hook_form_alter()`. |
| BEF + AJAX over JS toggles | [BEF + AJAX Over JS Toggles](bef-ajax-over-js-toggles.md) | For filtered-view switchers, use Better Exposed Filters with AJAX — not client-side JS that hides pre-rendered content. |
| Block → SDC via block template | [Block → SDC via Block Template](block-to-sdc-via-block-template.md) | When a block needs to render as an SDC, create a block template that includes the SDC. Don't hardcode SDCs in page templates. |
| SDC JS scope | [SDC Libraries](sdc-libraries.md) | SDC JS that needs global scope must go in theme-level library overrides, not in the SDC's component JS file. |
| Window width at click time | [Window Width at Click Time](window-width-at-click-time.md) | Check `window.innerWidth` at click time, not at Drupal behavior attach time — `once()` captures a stale snapshot. |
| Per-environment module exclusion | [Per-Environment Module Exclusion](per-environment-module-exclusion.md) | Use `$settings['config_exclude_modules']` for modules with environment-specific config (GTM, profiling). |
| Metatag per bundle | [Metatag Per Bundle](metatag-per-bundle.md) | Configure metatag defaults per content type, not globally — each bundle uses different field tokens. |
| Composer module removal order | [Composer Module Removal Order](composer-module-removal-order.md) | Never remove a module from `composer.json` before all environments have uninstalled it via `drush config:import`. |
| Hiding features for launch | [Hiding Features for Launch](hiding-features-for-launch.md) | When temporarily removing a feature, preserve all code — use templates or `#access = FALSE` and document the re-enable path. |
| Drush commands before php:eval | [Use Drush Commands Before php:eval](drush-commands-before-php-eval.md) | Always check whether a Drush command exists for the operation before reaching for `drush php:eval`, `drush php:script`, or `drush sql:query`. `php:eval` is the fallback for genuinely missing commands, not the default. |
