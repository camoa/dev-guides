---
description: Drupal Render API decision guides -- render arrays, elements, caching, theming, security, and performance patterns.
guide-meta:
  concepts:
    - render arrays
    - render elements
    - "#type"
    - "#theme"
    - "#markup"
    - attachments
    - lazy builders
    - placeholders
    - Renderer service
    - preprocess functions
    - theme hooks
    - template suggestions
  not:
    - Twig template syntax (see drupal/twig)
    - SDC components (see drupal/sdc)
  requires: []
  complements:
    - drupal/twig
    - drupal/caching
    - drupal/sdc
    - drupal/blocks
  specializes: ""
  category: drupal
---

# Drupal Render API

**Philosophy: Configuration First** -- Prioritize render arrays (the declarative approach) over raw HTML output. Render arrays are data structures that get processed, cached, and themed automatically.

## I need to...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand when to use render arrays vs other approaches | [Render API Overview](render-api-overview.md) | When you need to generate HTML output in Drupal -- controllers, blocks, forms, field formatters, views, any module that produces page content. |
| Learn render array structure and syntax | [Render Array Structure](render-array-structure.md) | Whenever you're building any render array -- understanding structure is foundational to using the Render API. |
| Know what #type, #theme, #markup mean | [Render Properties](render-properties.md) | Every render array uses properties -- these control access, caching, theming, HTML attributes, and rendering behavior. |
| Find the right render element for my output | [Core Render Elements](core-render-elements.md) | When you need pre-built, reusable output patterns -- links, tables, containers, HTML tags, status messages. Render elements are plugins that encapsulate complex rendering logic. |
| Use form elements outside forms | [Form Render Elements](form-render-elements.md) | Form elements can be used **outside of forms** as render-only elements when you need their HTML structure but not their input functionality. Inside forms, they become interactive with validation and submission handling. |
| Attach CSS/JS libraries to my render array | [Attachments](attachments.md) | When your render array needs CSS, JavaScript, drupalSettings, HTTP headers, HTML `<head>` elements, or placeholders. Attachments bubble up from children to parents to page level. |
| Add cache metadata to improve performance | [Cache Metadata in Render Arrays](cache-metadata-render-arrays.md) | Every render array that depends on dynamic data (entities, config, user context, time) needs cache metadata to ensure correct caching and cache invalidation. |
| Use the Renderer service programmatically | [The Renderer Service](renderer-service.md) | When you need to programmatically convert render arrays to HTML strings -- tokens, emails, feeds, AJAX responses, testing, or anywhere outside the normal page rendering flow. |
| Pass render arrays to Twig templates | [Twig Integration](twig-integration.md) | Render arrays are designed to work seamlessly with Twig -- pass them as variables and Twig renders them automatically. This is the standard pattern for theming in Drupal. |
| Modify variables before they reach Twig | [Preprocess Functions](preprocess-functions.md) | When you need to modify or add variables before they reach a Twig template -- add render arrays, compute values, restructure data, add cache metadata. |
| Create theme hooks and suggestions | [Theme Hooks & Suggestions](theme-hooks-suggestions.md) | When creating custom themed output that needs a Twig template and preprocessable variables. Theme hooks define the contract between code and templates. |
| Defer expensive rendering for better caching | [Lazy Builders & Placeholders](lazy-builders-placeholders.md) | When part of your render array is **expensive to generate** or **highly dynamic** (personalized, uncacheable, time-sensitive) but the rest of the page can be cached. Lazy builders defer that part's rendering until after the page is… |
| Create my own render element plugin | [Custom Render Elements](custom-render-elements.md) | When you have complex rendering logic that you reuse across multiple places -- voting widgets, custom table formatters, specialized containers, elements with default behaviors. |
| See common render array patterns | [Render Array Patterns](render-array-patterns.md) | Common scenarios have established patterns -- use these proven approaches rather than reinventing solutions. |
| Understand main content renderers | [Main Content Renderers](main-content-renderers.md) | Understanding how Drupal renders different response types -- HTML pages, AJAX, modal dialogs, iframes. Rarely need to interact with these directly, but helpful for advanced use cases. |
| Follow best practices | [Best Practices & Patterns](best-practices-patterns.md) | Architectural best practices for render arrays -- dependency injection, cache metadata, access checks, testing, and performance optimization. |
| Avoid common mistakes | [Anti-Patterns & Common Mistakes](anti-patterns-common-mistakes.md) | Anti-patterns to avoid in render arrays -- early rendering, raw HTML, missing cache metadata, XSS vulnerabilities, structural mistakes. |
| Ensure security and performance | [Security & Performance](security-performance.md) | Security best practices (XSS protection, access checks, CSRF) and performance optimization (cache strategies, lazy loading, efficient attachments). |
| Find core render files and documentation | [Code Reference Map](code-reference-map.md) |  |
