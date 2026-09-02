---
description: "Drupal core HTMX implementation file index — PHP classes, JavaScript files, configuration, production examples, and test files"
tldr: "Use this to locate Drupal core HTMX implementation files for deeper understanding or debugging. Documentation may lag behind code, so check the actual core implementation rather than relying on the test module as a best-practices reference."
drupal_version: "11.x"
---

# Core File Reference

## When to Use

> You need to locate Drupal core HTMX implementation files for deeper understanding or debugging.

## Core PHP Classes

| File | Purpose | Key Contents |
|------|---------|--------------|
| `/core/lib/Drupal/Core/Htmx/Htmx.php` | Main API class | 30+ attribute methods, 11 header methods, `applyTo()`, `createFromRenderArray()` |
| `/core/lib/Drupal/Core/Htmx/HtmxRequestInfoTrait.php` | Request detection | 8 methods: `isHtmxRequest()`, `getHtmxTriggerName()`, etc. |
| `/core/lib/Drupal/Core/Htmx/HtmxLocationResponseData.php` | Location header data | Constructor with 9 parameters for complex redirects |
| `/core/lib/Drupal/Core/Render/MainContent/HtmxRenderer.php` | Minimal response renderer | Creates minimal HTML structure with noindex meta tag |
| `/core/lib/Drupal/Core/EventSubscriber/HtmxContentViewSubscriber.php` | Route option handler | Processes `_htmx_route: TRUE` option |
| `/core/lib/Drupal/Core/Form/FormBase.php` | Form base class | Includes HtmxRequestInfoTrait (line 48) |
| `/core/lib/Drupal/Core/Form/FormBuilder.php` | Form builder | Automatic form_build_id OOB swap (lines 782-790) |

## JavaScript Files

| File | Purpose | Key Contents |
|------|---------|--------------|
| `/core/assets/vendor/htmx/htmx.min.js` | HTMX library | Version 2.0.4 vendor library |
| `/core/misc/htmx/htmx-utils.js` | Utilities | `Drupal.htmx.mergeSettings()`, `Drupal.htmx.addAssets()` |
| `/core/misc/htmx/htmx-assets.js` | Asset loading | `ajax_page_state` integration, differential loading, history cleanup |
| `/core/misc/htmx/htmx-behaviors.js` | Behaviors integration | Custom events `htmx:drupal:load`, `htmx:drupal:unload` |

## Configuration

| File | Purpose | Key Contents |
|------|---------|--------------|
| `/core/core.libraries.yml` | Library definitions | `htmx` (vendor), `drupal.htmx` (integration) at lines 617-634, 833-841 |
| `/core/core.services.yml` | Service definitions | `htmx_content_view_subscriber`, `main_content_renderer.htmx` |

## Production Examples

| File | Purpose | Key Patterns |
|------|---------|--------------|
| `/core/modules/config/src/Form/ConfigSingleExportForm.php` | Config export form | Cascading selects, OOB updates, history push |
| `/core/modules/system/tests/modules/test_htmx/src/Form/HtmxTestForm.php` | Test form | Dependent fields, `swapOob('true')`, trigger detection |
| `/core/modules/system/tests/modules/test_htmx/src/Controller/HtmxTestAttachmentsController.php` | Test controller | Asset attachment, basic HTMX patterns |
| `/core/modules/system/tests/modules/test_htmx/src/Form/HtmxTestAjaxForm.php` | Coexistence example | AJAX inserting HTMX content |

## Test Files

| File | Purpose |
|------|---------|
| `/core/tests/Drupal/Tests/Core/Htmx/HtmxAttributesTest.php` | Attribute method tests |
| `/core/tests/Drupal/Tests/Core/Htmx/HtmxHeadersTest.php` | Header method tests |
| `/core/tests/Drupal/Tests/Core/Htmx/HtmxUtilitiesTest.php` | Utility method tests |
| `/core/tests/Drupal/Tests/Core/Htmx/HtmxRequestInfoTest.php` | Request trait tests |
| `/core/tests/Drupal/KernelTests/Core/Htmx/HtmxRendererTest.php` | Renderer tests |
| `/core/tests/Drupal/FunctionalTests/Htmx/HtmxRendererCacheTest.php` | Cache header tests |
| `/core/tests/Drupal/FunctionalJavascriptTests/Core/Htmx/HtmxDynamicFormTest.php` | Dynamic form tests |
| `/core/tests/Drupal/Nightwatch/Tests/htmx/htmxTest.js` | Asset loading tests |

## Test Module Structure

Complete working example at `/core/modules/system/tests/modules/test_htmx/`:

- `test_htmx.info.yml` — Module definition
- `test_htmx.routing.yml` — Routes with `_htmx_route` examples
- `test_htmx.libraries.yml` — Custom library definition
- `src/Controller/HtmxTestAttachmentsController.php` — Controller patterns
- `src/Form/HtmxTestForm.php` — Dynamic form patterns
- `src/Form/HtmxTestAjaxForm.php` — AJAX/HTMX coexistence
- `js/behavior.js` — Custom behavior example
- `css/style.css` — Custom styles

## Common Mistakes

- Not checking actual core implementation — Documentation may lag behind code
- Assuming test module is production-ready — It's for testing, not best practices reference
- Using deprecated patterns from older versions — Always check current Drupal version
- Not reading inline documentation — `Htmx.php` has extensive PHPDoc

## See Also

- Previous: [AJAX Migration](ajax-migration.md)
- Reference: [Drupal API Documentation](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Htmx!Htmx.php/class/Htmx/11.x)
- Reference: [HTMX Official Documentation](https://htmx.org/reference/)
