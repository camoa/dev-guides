---
description: Plus Suite — WYSIWYG page builder on top of Layout Builder with drag-and-drop, inline editing, nested layouts, and pluggable modes/tools
guide-meta:
  concepts:
    - plus_suite
    - layout_builder_plus
    - lb_plus
    - navigation_plus
    - edit_plus
    - tempstore_plus
    - field_sample_value
    - section_library
    - dropzonejs
    - twig_events
    - inline editing
    - drag and drop page builder
    - layout block
    - nested layouts
    - promoted blocks
    - mode plugins
    - tool plugins
    - block properties
    - sample value generator
    - WYSIWYG page builder
    - Edit Mode
  not:
    - Canvas
    - Experience Builder
    - Gutenberg
    - React page builder
    - Layout Builder (core only)
  requires:
    - drupal/layout-builder
    - drupal/sdc
  complements:
    - drupal/ui-patterns
    - drupal/blocks
    - drupal/media
    - drupal/recipes
  category: drupal
tracks:
  - project: plus_suite
    channel: stable
    declared: 1.1.21
    note: 1.1.21 is the current tag and replaces a policy-violating 1.1.x-dev pin, but only installation-setup.md was re-read in the 2026-08-16 sweep; the other 28 guides still reflect the 1.1.x dev branch and the component module versions they describe were not re-checked
    verified: 2026-04-08
---

# Plus Suite

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what Plus Suite is and how it differs from core Layout Builder | [Overview](overview.md) | Use Plus Suite when you need a WYSIWYG page builder on top of core Layout Builder with drag-and-drop, inline editing, and nested layouts. Use core Layout Builder when you only need basic block placement via the sidebar form. |
| Install Plus Suite on a new or existing site | [Installation & Setup](installation-setup.md) | Use the DDEV install script for new projects and evaluation. Use manual module installation for existing sites already using Layout Builder. |
| Understand the module architecture and dependencies | [Architecture & Module Map](architecture-module-map.md) | Reference this when you need to understand how Plus Suite's modules relate to each other and which module provides which functionality. |
| Configure Edit Mode and the Navigation+ toolbar | [Edit Mode & Navigation+](edit-mode-navigation-plus.md) | Use Edit Mode for any content type using Layout Builder where editors need WYSIWYG page building. Disable it for read-only, API-sourced, or admin-form-based content types. |
| Create custom editing modes | [Mode Plugins](mode-plugins.md) | Use custom Mode plugins when you need editing modes beyond the built-in Edit Mode — e.g., a Preview mode, Help mode, or workflow-specific mode. |
| Create custom toolbar tools | [Tool Plugins](tool-plugins.md) | Use custom Tool plugins when you need custom tools for the Edit Mode toolbar — e.g., a color picker, annotation tool, or content validation tool. |
| Configure promoted blocks in the drag-and-drop sidebar | [Place Block & Promoted Blocks](place-block-promoted-blocks.md) | Configure which blocks appear in the drag-and-drop sidebar, customize their icons, and understand the block placement flow. |
| Work with nested layouts (layout blocks) | [Nested Layouts](nested-layouts.md) | Use nested layouts when you need blocks-within-blocks that can be treated as one reusable unit. Use section layouts for simple column arrangements. |
| Configure inline field editing | [Inline Editing](inline-editing.md) | Use Edit+ to let users click on any field and edit it directly. Enable inline editing on fields editors change frequently; disable it on computed, read-only, or complex-validation fields. |
| Understand how unsaved changes are stored | [Tempstore Strategy Pattern](tempstore-strategy.md) | Use Tempstore+ to manage unsaved changes across entities and Layout Builder sections. It solves different key generation, collection naming, and workspace awareness needs via the Strategy pattern. |
| Configure placeholder content for new blocks | [Field Sample Value](field-sample-value.md) | Configure placeholder content that appears when new blocks are placed, or create custom sample value generators for specific field types. |
| Save and reuse layout sections | [Section Library](section-library.md) | Use the Section Library to save and reuse Layout Builder sections, with all their blocks, as templates across pages. |
| Handle media drag-and-drop onto the page | [Media Handling](media-handling.md) | Use desktop drag-and-drop or media replacement to handle media in Plus Suite. Both depend on the DropzoneJS module and enyo/dropzone JS library. |
| Configure keyboard shortcuts and user preferences | [Hotkeys & User Settings](hotkeys-user-settings.md) | Configure or customize keyboard shortcuts for tools. Hotkeys are stored per-user and customized via the Settings sidebar. |
| Customize the sidebar panels | [Sidebar System](sidebar-system.md) | Customize sidebar content for your tools or modes. Sidebar visibility is cookie-based, and sidebars rebuild on every tool switch. |
| Understand how entities are wrapped for editing | [Twig Events](twig-events.md) | Subscribe to TwigRenderTemplateEvent to intercept and modify template output during Twig rendering without overriding templates; it fires on every template render so keep subscribers fast. |
| Use Plus Suite with Drupal Workspaces | [Workspaces Integration](workspaces-integration.md) | Use Plus Suite with Drupal Workspaces when you need staged content publishing. Tempstore+ handles workspace isolation automatically via key suffixes. |
| Create block types that integrate with Plus Suite | [Custom Block Types](custom-block-types.md) | Create custom block types for every design component. Use event subscribers to set placement defaults and add design options. |
| Override templates and customize theming | [Theming & Templates](theming-templates.md) | Override color configuration at `/admin/config/content/plus-suite` for brand customization. Override templates only when structural changes are needed. |
| Understand the JavaScript modules and AJAX commands | [JavaScript Architecture](javascript-architecture.md) | Reference this when extending Plus Suite with custom JS, debugging client-side issues, or understanding AJAX command flow. |
| Find the right Plus Suite event to subscribe to | [Events & Event Subscribers](events-event-subscribers.md) | Subscribe to Plus Suite events to customize behavior without overriding core module code. Check this catalog before writing new hooks or overrides. |
| Configure permissions for editors and admins | [Permissions & Access](permissions-access.md) | Apply this permission matrix when setting up roles for content editors and site builders. |
| Understand what the recipe installs and configures | [Recipe Structure](recipe-structure.md) | Reference this when troubleshooting recipe application, understanding what gets installed, or deciding whether to use recipe vs manual installation. |
| Choose between Plus Suite and Canvas | [Plus Suite vs Canvas](plus-suite-vs-canvas.md) | Use Plus Suite when you have existing Layout Builder investment or a PHP-only team. Use Canvas for new Drupal CMS projects prioritizing long-term core alignment. |
| Build a custom design system with Plus Suite | [Custom Design System Integration](custom-design-system.md) | Follow this guide when building Plus Suite for a branded site — custom block types, promoted block icons, sample content generators, and block properties that match your design system. |
| Create custom section layout plugins | [Custom Layout Plugins](custom-layout-plugins.md) | Create custom layout plugins when core's basic one/two/three column layouts don't match your design system's grid. YAML covers most cases; use PHP class only when per-section configuration is needed. |
| Build a complete component end-to-end | [End-to-End Component Creation](end-to-end-component.md) | Follow this walkthrough when creating any new Plus Suite component from scratch. Use the checklist at the end to verify completeness. |
| Use UI Patterns / SDC components with Plus Suite | [UI Patterns & SDC Integration](ui-patterns-sdc-integration.md) | Use UI Patterns layouts as structural section layouts and block_content for content blocks that need inline editing. Do not use UI Patterns blocks as your primary strategy if inline editing is a requirement. |
| Troubleshoot known issues and avoid pitfalls | [Common Mistakes & Known Issues](common-mistakes-known-issues.md) | Read this before starting any Plus Suite implementation and when troubleshooting problems. |
