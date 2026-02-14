---
description: Complete reference for render array properties -- universal, lifecycle, and advanced properties with usage examples.
---

# Render Properties

## When to Use

Every render array uses properties -- these control access, caching, theming, HTML attributes, and rendering behavior.

## Core Properties Reference

### Universal Properties (all render elements)

| Property | Type | Purpose | Example |
|---|---|---|---|
| `#access` | bool/AccessResult | Show/hide element based on permissions | `#access => $user->hasPermission('view content')` |
| `#cache` | array | Cache keys, contexts, tags, max-age | `#cache => ['keys' => ['node', $nid], 'tags' => ['node:1']]` |
| `#weight` | int | Sort order (lower = earlier) | `#weight => -10` |
| `#attributes` | array | HTML attributes (class, id, data-*) | `#attributes => ['class' => ['button', 'primary']]` |
| `#markup` | string/Markup | Raw HTML output (XSS filtered) | `#markup => '<p>Hello</p>'` |
| `#plain_text` | string | Text with all HTML escaped | `#plain_text => '<script>alert("XSS")</script>'` renders as text |
| `#type` | string | Render element plugin to use | `#type => 'container'` |
| `#theme` | string/array | Theme hook to use | `#theme => 'item_list'` |
| `#theme_wrappers` | array | Theme hooks to wrap around rendered children | `#theme_wrappers => ['container']` |

### Rendering Lifecycle Properties

| Property | Type | Purpose | Example |
|---|---|---|---|
| `#pre_render` | array | Callbacks before rendering | `#pre_render => [[MyClass::class, 'preRender']]` |
| `#post_render` | array | Callbacks after rendering | `#post_render => [[MyClass::class, 'postRender']]` |
| `#lazy_builder` | array | Lazy building callback + args | `#lazy_builder => ['\Drupal\mymodule\MyBuilder::build', [$nid]]` |
| `#attached` | array | Libraries, drupalSettings, etc. | `#attached => ['library' => ['core/drupal.dialog']]` |

### Advanced Properties

| Property | Type | Purpose | Example |
|---|---|---|---|
| `#printed` | bool | Prevent double-rendering (internal) | `#printed => TRUE` |
| `#prefix` | string | HTML before element | `#prefix => '<div class="wrapper">'` |
| `#suffix` | string | HTML after element | `#suffix => '</div>'` |
| `#allowed_tags` | array | HTML tags allowed in #markup | `#allowed_tags => ['a', 'em', 'strong']` |
| `#create_placeholder` | bool | Generate placeholder for lazy builder | `#create_placeholder => TRUE` |
| `#sorted` | bool | Skip sorting children (already sorted) | `#sorted => TRUE` |

**Reference:** `core/lib/Drupal/Core/Render/Element/RenderElementBase.php` (lines 40-120) -- comprehensive property documentation

## Pattern: Common Property Combinations

```php
// Cached, access-controlled, themed container
$build['section'] = [
  '#type' => 'container',
  '#access' => $this->currentUser()->hasPermission('view content'),
  '#attributes' => ['class' => ['content-section'], 'id' => 'main'],
  '#cache' => [
    'keys' => ['section', 'main'],
    'contexts' => ['user.permissions'],
    'tags' => ['config:system.site'],
    'max-age' => Cache::PERMANENT,
  ],
  '#attached' => [
    'library' => ['mymodule/section-behavior'],
  ],
];
```

## Common Mistakes

- **Using `#markup` with unsanitized user input** -- XSS vulnerability. Use `#plain_text` or properly sanitize first
- **Forgetting `#access` on sensitive content** -- Content renders even if user shouldn't see it
- **Setting `#cache` without appropriate contexts/tags** -- Stale cache shown to wrong users or not invalidated when dependencies change
- **Mixing `#markup` and children** -- `#markup` is prepended to `#children`; use `#theme` instead for structured output
- **Not bubbling `#attached` in custom code** -- CSS/JS libraries don't load because metadata doesn't reach page attachments

## See Also

- [Attachments](attachments.md) for `#attached` details
- [Cache Metadata in Render Arrays](cache-metadata-render-arrays.md) for `#cache` best practices
- [Security & Performance](security-performance.md) for XSS protection
- Reference: [Cacheability of render arrays](https://www.drupal.org/docs/drupal-apis/render-api/cacheability-of-render-arrays)
