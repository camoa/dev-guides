---
description: When to use render arrays vs other approaches for generating HTML output in Drupal.
---

# Render API Overview

**Philosophy: Configuration First** -- Prioritize render arrays (the declarative approach) over raw HTML output. Render arrays ARE Drupal's configuration-first approach to output -- they're data structures that get processed, cached, and themed automatically.

## When to Use

When you need to generate HTML output in Drupal -- controllers, blocks, forms, field formatters, views, any module that produces page content.

## Decision: Render Array vs Other Approaches

| If you need... | Use... | Why |
|---|---|---|
| Structured page content with theming, caching, access control | Render arrays | Drupal's configuration-first approach -- data structures that get processed, cached, themed automatically |
| Direct HTML string output (emails, feeds, non-HTML) | `renderInIsolation()` + render array | Even for simple HTML, use render arrays then convert to string -- preserves metadata until final rendering |
| Raw HTML you're 100% responsible for sanitizing | `Markup::create()` with `#markup` | DANGEROUS -- bypasses XSS protection. Only for trusted, already-sanitized HTML |
| Themed output following site design | `#theme` property in render array | Delegates to theme system, allows preprocess alterations, follows theme inheritance |
| Form elements | Form API (which builds render arrays) | Form API is a specialized layer on top of Render API with validation, submission, CSRF protection |

## Pattern: Basic Render Array

```php
// In a controller or block build method
return [
  '#type' => 'container',
  '#attributes' => ['class' => ['my-wrapper']],
  'title' => [
    '#type' => 'html_tag',
    '#tag' => 'h2',
    '#value' => $this->t('Hello World'),
  ],
  'content' => [
    '#markup' => '<p>' . $this->t('This is content.') . '</p>',
  ],
];
```

**Reference:** `core/lib/Drupal/Core/Render/RendererInterface.php` -- full rendering process documented in `render()` method comments (lines 91-342)

## Common Mistakes

- **Calling `render()` inside preprocess functions** -- Pass render arrays to Twig, let Twig render them automatically -- preserves metadata bubbling
- **Using raw HTML concatenation instead of render arrays** -- Bypasses caching, theming, access control, and security filters
- **Not understanding the difference between `renderRoot()` and `render()`** -- Use `renderRoot()` only at final response stage; `render()` is for internal recursive rendering
- **Rendering too early** -- Keep data as render arrays as long as possible; render at the last responsible moment to maximize cacheability

## See Also

- [The Renderer Service](renderer-service.md) for programmatic rendering
- [Best Practices & Patterns](best-practices-patterns.md) for architectural guidance
- Reference: [Render API documentation](https://www.drupal.org/docs/drupal-apis/render-api)
