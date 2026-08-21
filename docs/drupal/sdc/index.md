---
description: Single Directory Components (SDC) — component architecture, development patterns, and best practices
tracks:
  - project: drupal
    channel: stable
    verified: 2026-02-19
guide-meta:
  concepts:
    - "*.component.yml"
    - single directory components
    - SDC
    - component schema
    - Twig components
    - component libraries
  not:
    - UI Patterns
    - story.yml
    - source plugins
    - Storybook.js
  requires: []
  complements:
    - drupal/ui-patterns
    - drupal/twig
    - drupal/storybook
  specializes: ""
  category: drupal
---

# Single Directory Components (SDC)

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand SDC architecture and plugin system | [SDC Architecture](sdc-architecture.md) | Discovery recursively scans components/ directories in the active theme, base themes, and modules with no precedence between them — the component ID is provider:{basename of the .component.yml}. Precedence applies only to replacement: ComponentNegotiator picks a winner among candidates that declare replaces, active theme before base themes before module fallback. |
| Know component file structure and naming | [Component File Structure](component-file-structure.md) | Every sibling file (.twig, .css, .js) must match the .component.yml basename, not the directory name — machineName is derived from the plugin ID, which is the YAML basename. Renaming the directory does not fix a 'component not found' error; check the basename match instead. |
| Define component YAML schema properly | [Component YAML Schema](component-yaml-schema.md) | Core validates props against the schema but never strips undeclared ones and never applies YAML default: — the Twig's ?? / \|default() is the only real default. There is no libraryDependencies key; use libraryOverrides: dependencies:. Read the .twig, not the YAML, to learn a component's real API. |
| Write Twig templates for SDCs | [Twig Templates in SDCs](twig-templates-in-sdcs.md) | A slot arrives differently on each call path — {% embed %} gives a block override, include() gives a context variable, #type: component gives both. Default to rendering every slot through {% block %} with the fallback inside it; testing a slot-named variable around a {% block %} breaks the {% embed %} path with no error. |
| Add SCSS/CSS to components with proper scoping | [SCSS/CSS in SDCs](scss-css-in-sdcs.md) | Use BEM to scope component CSS and prevent collisions; prefer CSS custom properties for theming values that variants override. Never use @extend or !important — fix selector specificity or use mixins/utility classes instead. |
| Add JavaScript with Drupal.behaviors | [JavaScript in SDCs](javascript-in-sdcs.md) | Attach behavior with Drupal.behaviors + once() scoped to context, never document.querySelectorAll, and implement detach for cleanup. Declare JS dependencies via libraryOverrides: dependencies: — there is no libraryDependencies key. |
| Compose components (include/embed/render) | [Component Composition](component-composition.md) | Use include() for props-only inclusion (with with_context = false); use embed only when the child renders that slot through {% block name %} — if it prints a bare {{ name }} or wraps it in {% if %}, your block override is silently discarded. Render arrays are for preprocessing/controllers/hooks. |
| Decide between props and slots | [Props vs Slots Decision Framework](props-vs-slots-decision-framework.md) | Use props for structured, typed, validated data that drives logic; use slots for unstructured renderable content. Prop validation is a dev-time, assert()-gated lint that never mutates data, and slot required: is not a real key — pick the shape based on the data, not on an enforcement guarantee neither one gives you. |
| Create component variants (enum vs separate) | [Component Variants](component-variants.md) | The Component Variants API landed in Drupal 11.2, not 11.1 — variants: is silently ignored on 11.1 and earlier. #variant only copies into $props['variant'] and adds a data-component-variant attribute; it never declares or restricts a variant prop, so declare variant as an enum prop too if you want it validated. |
| Replace Drupal templates with SDCs | [Replacing Templates with SDCs](replacing-templates-with-sdcs.md) | replaces is not themes-only — modules can replace components too, with a theme in the active hierarchy winning over a module fallback. The replacement schema must be compatible (required props match, shared props' type/enum lists are supersets), not identical; a narrowing replacement throws IncompatibleComponentSchema at cache rebuild, in production too. |
| Test SDCs (Storybook, visual regression) | [Testing SDCs](testing-sdcs.md) | The theme key is enforce_prop_schemas, not enforce_sdc_schemas — a misspelling turns nothing on and reports nothing. Production never validates props (the check is assert()-gated), so development with zend.assertions=1 is the only place a schema violation surfaces; test each slot call path (embed, include, render element) individually since the render element hides embed-only bugs. |
| Optimize performance (libraries, caching) | [Performance](performance.md) | Libraries auto-generate per component and load only when the component renders; libraryOverrides is the only key core reads for dependency ordering (core/drupal is appended automatically). A js: or css: key in libraryOverrides replaces the auto-discovered entry rather than adding to it. |
| Prevent XSS and security issues | [Security](security.md) | Prop validation is assert()-gated, non-mutating, and skips undeclared props entirely — pattern/format/enum on a prop never stands between user input and markup. Sanitize at the boundary (UrlHelper::stripDangerousProtocols, Xss::filter) and rely on Twig auto-escaping plus the Attribute object, not on schema validation. |
| Avoid anti-patterns and code review issues | [Anti-Patterns](anti-patterns.md) | The two highest-impact anti-patterns: wrapping {% block name %} in {% if name %} silently drops content on the embed path with no error, and narrowing a replacement's schema throws IncompatibleComponentSchema at cache rebuild in production. Both trace back to THE MECHANISM — the YAML declares, the Twig (and SchemaCompatibilityChecker) decide. |
| Integrate SDC with UI Patterns 2.x | [UI Patterns 2 Integration](ui-patterns-2-integration.md) | UI Patterns 2 reads component.yml directly — no separate pattern file needed — and exposes SDCs as blocks/layouts/views plugins via sub-modules. It is the one consumer that reads YAML default:, so keep default: in step with the Twig's ?? / \|default(); if they disagree, UI-configured and Twig-called instances render differently. |
