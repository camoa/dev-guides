---
description: Drupal Hooks — the OOP hook system in Drupal 11.1+, ordering, theme hooks, what stays procedural, and migrating off .module and .theme files.
guide-meta:
  concepts:
    - OOP hooks
    - Hook attribute
    - hook ordering
    - LegacyHook
    - procedural hooks
    - theme hooks
    - ProceduralHookScanStop
    - skip_procedural_hook_scan
    - hook_requirements replacement
    - .theme deprecation
  not:
    - preprocess variable mechanics (see drupal/twig)
    - theme hook registration (see drupal/twig)
    - template suggestions (see drupal/render-api)
    - events vs hooks (see drupal/solid-principles)
    - hook class organization by concern (see drupal/solid-principles, drupal/dry-principles)
  requires:
    - drupal/services
  complements:
    - drupal/twig
    - drupal/render-api
    - drupal/solid-principles
    - drupal/dry-principles
    - drupal/tdd
  category: drupal
---

# Drupal Hooks

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Choose an implementation style: hook class, procedural function, or both | [Hook Implementation Decision](hook-implementation-decision.md) | Choosing between a #[Hook] class method, a procedural function, or both when adding or converting a hook implementation; the lowest core version supported decides it. |
| Read the #[Hook] attribute reference | [Hook Attribute Anatomy](hook-attribute-anatomy.md) | Writing or reading a #[Hook] attribute: the exact constructor, the three placement forms, discovery rules, and the two exceptions the collector enforces at container build. |
| Order hook implementations, or reorder/remove another module's | [Hook Ordering](hook-ordering.md) | Ordering hook execution with order: on #[Hook], #[ReorderHook], or #[RemoveHook] since 11.2.0, replacing hook_module_implements_alter(). |
| Know which hooks must stay procedural | [Procedural-Only Hooks](procedural-only-hooks.md) | Which hooks (install, update, schema, meta hooks) must stay procedural when converting a module, and what replaces hook_requirements(). |
| Write OOP hooks in a theme | [Theme Hooks (OOP)](theme-hooks-oop.md) | Writing theme hooks as #[Hook] classes since core 11.3.0; the .theme file is deprecated in 11.5.0 (unreleased at verification). |
| Stop the procedural hook scan for performance | [Procedural Scan Performance](procedural-scan-performance.md) | Stopping the procedural hook scan at container build once a module has converted to #[Hook] classes, via skip_procedural_hook_scan or #[ProceduralHookScanStop]. |
| Convert a module or theme off .module/.theme | [Migrating to OOP Hooks](migrating-to-oop-hooks.md) | Converting a module or theme's procedural hooks to #[Hook] classes before Drupal 12.0.0 stops collecting legacy hooks outside the main extension file. |
| Look up a deprecation or landing version | [Hooks Deprecation Timeline](hooks-deprecation-timeline.md) | Reference table of every hook-system mechanism's landed, deprecated, and removed versions with its change record, verified against core 11.4.5. |
| Apply security, performance, and coding standards to hook classes | [Hooks Best Practices](hooks-best-practices.md) | Standards for writing or reviewing a hook class: constructor injection, class shape, naming, security in alter hooks, and production failure modes. |
