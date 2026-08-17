---
description: Better Exposed Filters — replace Views exposed filter dropdowns with checkboxes, radio buttons, links, sliders, date pickers, and custom widgets
tracks:
  - project: better_exposed_filters
    channel: stable
    declared: null
    note: no version stated in prose
    verified: 2026-03-30
guide-meta:
  concepts:
    - Better Exposed Filters
    - BEF
    - bef_checkboxes
    - bef_radios
    - bef_links
    - bef_sliders
    - bef_datepicker
    - bef_hidden
    - bef_single
    - bef_number
    - exposed filters
    - auto-submit
    - sort combine
    - soft limit
    - select all none
    - secondary options panel
    - option rewriting
    - noUiSlider
    - FiltersWidget plugin
    - FilterWidgetBase
  not:
    - Facets module (faceted search with counts — see drupal/views)
    - Views core filters (no widget customization needed)
    - Search API facets configuration
  requires:
    - drupal/views
  complements:
    - drupal/views
    - drupal/ajax
  specializes: ""
  category: drupal
---

# Better Exposed Filters

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what BEF does vs core exposed filters | [Overview](overview.md) | Use Better Exposed Filters when you need more control over how Views exposed filters are rendered — replacing default select dropdowns with checkboxes, radio buttons, links, sliders, date pickers, or other widgets. Use core exposed filters… |
| Install BEF and enable it on a View | [Installation & Setup](installation-setup.md) | Use this guide when installing BEF on a Drupal site and enabling it for Views. |
| Configure auto-submit, secondary panel, reset button | [General Settings](general-settings.md) | Use this guide when configuring BEF's global options that apply to all exposed filters on a View — auto-submit, secondary options panel, reset button, and input-required behavior. |
| Use checkboxes or radio buttons for filters | [Checkboxes & Radio Buttons Widget](checkboxes-radio-buttons.md) | Use this widget when you want to replace a select dropdown with checkboxes (multi-select) or radio buttons (single-select) on an exposed filter. Use the Links widget when you want clickable URL-based navigation instead. |
| Render filters as clickable links | [Links Widget](links-widget.md) | Use this widget when you want filters rendered as clickable links instead of form elements — useful for faceted navigation style where each option is a URL. Use checkboxes when form-based interaction (submit button) is preferred. |
| Add range sliders for numeric filters | [Sliders Widget](sliders-widget.md) | Use this widget when you have a numeric filter (price, quantity, rating) and want a visual range slider instead of text inputs. Use the number widget for simple min/max inputs without visual slider. |
| Use HTML5 date pickers | [Date Pickers Widget](datepickers-widget.md) | Use this widget when you have a date filter and want HTML5 `<input type="date">` instead of a text field. Use the hidden widget for date filters you want to set programmatically without user input. |
| Use hidden, single checkbox, or number widgets | [Hidden & Special Widgets](hidden-special-widgets.md) | Use the hidden widget to pre-set filter values without showing them to users. Use the single checkbox widget for boolean filters (on/off). |
| Customize sort display (radio/links/combine) | [Sort Widgets](sort-widgets.md) | Use this guide when you have exposed sort criteria and want radio buttons or links instead of dropdowns, or want to combine sort_by and sort_order into a single control. |
| Customize pager display | [Pager Widgets](pager-widgets.md) | Use this guide when you have an exposed pager (items per page) and want to render it as radio buttons or links instead of a dropdown. |
| Configure auto-submit behavior precisely | [Auto-Submit](auto-submit.md) | Use auto-submit when you want the View to refresh automatically when users change filter values, without requiring a manual "Apply" button click. Avoid auto-submit on mobile without a breakpoint guard. |
| Move filters into a collapsible secondary panel | [Secondary & Collapsible Options](secondary-collapsible.md) | Use secondary options when you have many exposed filters and want to group less-used ones into a collapsible "Advanced options" panel. Use per-filter collapsible when you want individual filters wrapped in their own toggleable details… |
| Rewrite filter option labels or sort them | [Option Rewriting & Sorting](option-rewriting-sorting.md) | Use option rewriting when you need to change display labels of filter options or remove options. Use option sorting when you need alphabetical or key-based ordering instead of the default Views order. |
| Override BEF templates in my theme | [Theming & Templates](theming-templates.md) | Use this guide when you need to customize the HTML output of BEF widgets in your theme. |
| Create a custom BEF widget plugin | [Custom Widget Plugins](custom-widget-plugins.md) | Use this guide when the built-in BEF widgets don't meet your needs and you want to create a custom filter, sort, or pager widget. Use `hook_better_exposed_filters_options_alter()` for simpler runtime changes that don't require a new plugin. |
| Understand BEF's JavaScript behaviors | [JavaScript Behaviors](javascript-behaviors.md) | Use this guide when you need to understand or customize BEF's client-side behavior — auto-submit, sliders, select all/none, soft limit, or link AJAX. |
| Alter BEF options with hooks | [Hooks & Alter Functions](hooks-alter.md) | Use hooks when you need to programmatically modify BEF behavior — changing options, setting slider ranges dynamically, or altering widget availability — without creating a custom widget plugin. |
| Use BEF with AJAX Views, Facets, or Search API | [Integration Patterns](integration-patterns.md) | Use this guide when combining BEF with other Drupal modules — Views AJAX, Facets, Search API, Select2, or Chosen. |
| Understand BEF's config schema for export/import | [Configuration Schema](configuration-schema.md) | Use this guide when exporting/importing BEF configuration, creating custom widgets that need config schema, or debugging config validation errors. |
| Debug BEF issues and avoid anti-patterns | [Common Mistakes](common-mistakes.md) | Use this guide when debugging BEF issues or reviewing BEF configuration for problems. |
