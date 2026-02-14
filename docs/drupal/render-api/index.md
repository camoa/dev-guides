---
description: Drupal Render API decision guides -- render arrays, elements, caching, theming, security, and performance patterns.
---

# Drupal Render API

**Philosophy: Configuration First** -- Prioritize render arrays (the declarative approach) over raw HTML output. Render arrays are data structures that get processed, cached, and themed automatically.

## I need to...

| Task | Guide |
|------|-------|
| Understand when to use render arrays vs other approaches | [Render API Overview](render-api-overview.md) |
| Learn render array structure and syntax | [Render Array Structure](render-array-structure.md) |
| Know what #type, #theme, #markup mean | [Render Properties](render-properties.md) |
| Find the right render element for my output | [Core Render Elements](core-render-elements.md) |
| Use form elements outside forms | [Form Render Elements](form-render-elements.md) |
| Attach CSS/JS libraries to my render array | [Attachments](attachments.md) |
| Add cache metadata to improve performance | [Cache Metadata in Render Arrays](cache-metadata-render-arrays.md) |
| Use the Renderer service programmatically | [The Renderer Service](renderer-service.md) |
| Pass render arrays to Twig templates | [Twig Integration](twig-integration.md) |
| Modify variables before they reach Twig | [Preprocess Functions](preprocess-functions.md) |
| Create theme hooks and suggestions | [Theme Hooks & Suggestions](theme-hooks-suggestions.md) |
| Defer expensive rendering for better caching | [Lazy Builders & Placeholders](lazy-builders-placeholders.md) |
| Create my own render element plugin | [Custom Render Elements](custom-render-elements.md) |
| See common render array patterns | [Render Array Patterns](render-array-patterns.md) |
| Understand main content renderers | [Main Content Renderers](main-content-renderers.md) |
| Follow best practices | [Best Practices & Patterns](best-practices-patterns.md) |
| Avoid common mistakes | [Anti-Patterns & Common Mistakes](anti-patterns-common-mistakes.md) |
| Ensure security and performance | [Security & Performance](security-performance.md) |
| Find core render files and documentation | [Code Reference Map](code-reference-map.md) |
