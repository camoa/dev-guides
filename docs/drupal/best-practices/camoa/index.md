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
| Prefer Drush commands over custom PHP | [Prefer Drush Commands Over Custom PHP](prefer-drush-commands-over-custom-php.md) | Check whether a Drush command exists before reaching for php:eval or php:script. Built-in commands are tested, idempotent, flag-aware, and self-documenting; php:eval bypasses all of that and accumulates as brittle copy-paste debt. |
| Avoid unnecessary custom modules | [Avoid Unnecessary Custom Modules](avoid-unnecessary-custom-modules.md) | Reuse = CSS + Drupal config (zero new code). Extend = contrib modules, Twig template overrides, preprocess hooks, hook implementations (use the framework's extension points). Create = custom module only when both fail. Contrib is shared infrastructure; your template is yours to patch forever. |
| DDEV + Composer path repo for drupal-recipe | [DDEV + Composer Path Repo for drupal-recipe Packages](ddev-composer-path-repo-drupal-recipe.md) | Path repos symlink recipe packages and the symlink dangles in the DDEV container — force `symlink: false`, run require on host Composer, and use a `vcs` repo for tag-accurate tests. |
| Ship search_index view mode defensively | [Ship core.entity_view_mode.node.search_index Defensively](ship-search-index-view-mode-defensively.md) | Core 11.4 moved the `search_index` view mode out of node; `drupal_cms_search` cloneAs crashes fresh installs. Ship the view mode in your own config/ (Haven pattern) or ship a flat recipe. |
| schemadotorg mapping_type deps post-export | [schemadotorg mapping_type Dependency Enrichment Post-Export](schemadotorg-mapping-type-deps-post-export.md) | Alpha schemadotorg mappings omit their `mapping_type` dep; flat alphabetical import fails. Add the dep post-export and re-apply every export. |
| Pre-stable template consumer stability | [Pre-Stable Template Deps Require Consumer minimum-stability](pre-stable-template-consumer-minimum-stability.md) | Stability flags aren't transitive — a template's pre-stable deps block a plain require. Consumer must set `minimum-stability dev` + `prefer-stable`; document in README AND CI. |
| Rebrand a required theme without forking | [Rebrand a Required Theme Without Forking](rebrand-required-theme-without-forking.md) | Ship neutral logo/favicon as managed files (travel via Default Content) + theme-settings overrides; theme stays byte-identical. Beware Canvas re-seeding brand strings from SDC `examples:`. |
| Canvas versioned-config raw-edit trap | [Canvas Versioned-Config Raw-Edit Trap](canvas-versioned-config-raw-edit-trap.md) | `canvas.component.*` configs hash their settings into `active_version`; raw edits desync it. `site:install` masks it, the recipe CLI validator fails. Recompute hashes from a live install. |
