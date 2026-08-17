---
description: Drupal Twig theming — template development, field access, preprocess functions, debugging, and contrib tools
tracks:
  - project: drupal
    channel: stable
    verified: 2026-04-16
guide-meta:
  concepts:
    - Twig templates
    - template discovery
    - template hierarchy
    - field access in Twig
    - entity reference traversal
    - attribute system
    - preprocess functions
    - template suggestions
    - Twig functions
    - Twig filters
    - twig_tweak
  not:
    - SDC component development (see drupal/sdc)
    - render arrays (see drupal/render-api)
    - JSX to Twig conversion (see design-systems/jsx-to-twig)
  requires: []
  complements:
    - drupal/render-api
    - drupal/sdc
    - design-systems/radix-components
  specializes: ""
  category: drupal
---

# Drupal Twig Theming

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand how Twig templates work in Drupal | [Twig Overview](twig-overview.md) | When you need to understand how the Twig template engine integrates with Drupal's theme system before diving into specific template work. |
| Name my template file correctly | [Template Discovery & Naming](template-discovery-naming.md) | When you need to create a template file and need to name it correctly, or when your template is not being picked up by Drupal. |
| Know what templates exist in what order | [Template Hierarchy](template-hierarchy.md) | When you need to understand the full rendering chain — which template wraps which — and where to override at each level. |
| Know what variables are available in html/page/node/field templates | [Variables by Template Level](variables-by-template-level.md) | When you need to know exactly what variables are available in a specific template type. |
| Access a field value in a Twig template | [Accessing Field Values](accessing-field-values.md) | This is the most critical section for day-to-day theming. Whenever you need to output, check, or manipulate field data in a Twig template. |
| Follow entity references (node → media → image) | [Entity Reference Traversal](entity-reference-traversal.md) | When a field references another entity (taxonomy term, media, user, paragraph, another node) and you need to access the referenced entity's data in Twig. |
| Loop over multi-value fields | [Multi-Value Fields](multi-value-fields.md) | When a field is configured to allow multiple values and you need to iterate, count, slice, or conditionally access individual items. |
| Add/remove CSS classes and HTML attributes | [The Attribute System](attribute-system.md) | When you need to add, remove, or modify HTML attributes in a template — particularly CSS classes, data attributes, ARIA attributes, and custom element attributes. |
| Write a preprocess function | [Preprocess Functions](preprocess-functions.md) | When you need to prepare data for templates, pass custom variables, modify existing variables, or manipulate the rendering pipeline before a template renders. |
| Pass custom data from PHP to a template | [Adding Variables in Preprocess](adding-variables-preprocess.md) | When you need to pass data from PHP to a Twig template that is not available through the default variable set. |
| Register a new theme hook | [Theme Hooks & Registration](theme-hooks-registration.md) | When your module or theme needs to register a new template (not override an existing one), define the variables it accepts, and specify the default template file. |
| Add or override template suggestions | [Template Suggestions](template-suggestions.md) | When you need Drupal to use a more specific template for certain conditions (specific node type, view mode, user role, etc.) without overriding the base template for all cases. |
| Use url(), path(), link(), file_url(), icon(), dump() in Twig | [Drupal Twig Functions](twig-functions.md) | When you need to generate URLs, attach libraries, create links, or use other Drupal-specific functions from within a Twig template. |
| Use \|t, \|without, \|clean_class, \|render, \|striptags, and 30+ Twig native filters in Twig | [Drupal Twig Filters](twig-filters.md) | When you need to transform, escape, translate, or manipulate variables in Twig templates. |
| Use twig_tweak to render a view/block/entity | [Twig Tweak Module](twig-tweak.md) | When you need to render a view, block, entity, or field from within a Twig template without a preprocess function — particularly useful for CMS-style layouts and quick embeds. |
| Include an SDC component from a Twig template | [SDC in Templates](sdc-in-templates.md) | When including or rendering Single Directory Components from Twig templates, or when a component needs to embed another SDC component. |
| Debug which template is being used | [Template Debugging](template-debugging.md) | When you need to identify which template is rendering, what variables are available, or why output looks wrong. |
| Use extends, include, embed | [Template Inheritance](template-inheritance.md) | When you want to share template structure across multiple templates, or include a sub-template/component as part of a larger template. |
| Know security and performance rules | [Security & Performance](security-performance.md) | When writing or reviewing Twig templates and preprocess functions — these rules apply to all template work. |
| Avoid common Twig mistakes | [Anti-Patterns](anti-patterns.md) | Code review checklist. Review your templates against these patterns before committing. |
| Find the relevant core source files | [Code Reference Map](code-reference-map.md) |  |
| Check source references and maintenance notes | [Sources & Maintenance](sources-maintenance.md) |  |
