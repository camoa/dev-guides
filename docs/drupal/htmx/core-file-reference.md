---
description: Drupal core HTMX implementation file index — PHP classes, JavaScript files, configuration, production examples, and test files
drupal_version: "11.x"
---

# Core File Reference

## When to Use

> Use this to locate Drupal core HTMX implementation files for deeper understanding or debugging.

## Decision

**Core PHP classes:**

| File | Purpose |
|------|---------|
| `/core/lib/Drupal/Core/Htmx/Htmx.php` | Main API — 30+ attribute methods, 11 header methods, `applyTo()` |
| `/core/lib/Drupal/Core/Htmx/HtmxRequestInfoTrait.php` | Request detection — 8 methods |
| `/core/lib/Drupal/Core/Htmx/HtmxLocationResponseData.php` | Location header data — 9-parameter constructor |
| `/core/lib/Drupal/Core/Render/MainContent/HtmxRenderer.php` | Minimal response renderer |
| `/core/lib/Drupal/Core/EventSubscriber/HtmxContentViewSubscriber.php` | Handles `_htmx_route: TRUE` option |
| `/core/lib/Drupal/Core/Form/FormBase.php` | Includes HtmxRequestInfoTrait (line 48) |
| `/core/lib/Drupal/Core/Form/FormBuilder.php` | Automatic form_build_id OOB swap (lines 782-790) |

**JavaScript files:**

| File | Purpose |
|------|---------|
| `/core/assets/vendor/htmx/htmx.min.js` | HTMX v2.0.4 vendor library |
| `/core/misc/htmx/htmx-utils.js` | `mergeSettings()`, `addAssets()` |
| `/core/misc/htmx/htmx-assets.js` | Differential loading, history cleanup |
| `/core/misc/htmx/htmx-behaviors.js` | `htmx:drupal:load`, `htmx:drupal:unload` events |

**Production examples:**

| File | Patterns demonstrated |
|------|----------------------|
| `/core/modules/config/src/Form/ConfigSingleExportForm.php` | Cascading selects, OOB updates, history push |
| `/core/modules/system/tests/modules/test_htmx/src/Form/HtmxTestForm.php` | Dependent fields, trigger detection |
| `/core/modules/system/tests/modules/test_htmx/src/Controller/HtmxTestAttachmentsController.php` | Asset attachment, basic patterns |
| `/core/modules/system/tests/modules/test_htmx/src/Form/HtmxTestAjaxForm.php` | AJAX/HTMX coexistence |

**Test files:**

| File | Purpose |
|------|---------|
| `/core/tests/Drupal/Tests/Core/Htmx/HtmxAttributesTest.php` | Attribute method tests |
| `/core/tests/Drupal/Tests/Core/Htmx/HtmxHeadersTest.php` | Header method tests |
| `/core/tests/Drupal/KernelTests/Core/Htmx/HtmxRendererTest.php` | Renderer tests |
| `/core/tests/Drupal/FunctionalJavascriptTests/Core/Htmx/HtmxDynamicFormTest.php` | Dynamic form tests |

## Common Mistakes

- **Wrong**: Not checking actual core implementation → **Right**: Documentation may lag behind code; read the source
- **Wrong**: Assuming test module is production-ready → **Right**: It's for testing, not a best practices reference
- **Wrong**: Not reading inline documentation → **Right**: `Htmx.php` has extensive PHPDoc

## See Also

- [AJAX Migration](ajax-migration.md)
- Reference: [Drupal API Documentation — Htmx class](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Htmx!Htmx.php/class/Htmx/11.x)
- Reference: [HTMX Official Documentation](https://htmx.org/reference/)
