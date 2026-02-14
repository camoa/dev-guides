---
description: Quick reference to core render API files, interfaces, element classes, cache utilities, and documentation links.
---

# Code Reference Map

## When to Use

Quick reference to find the right core files and documentation for render API tasks.

## Core Render API Files

### Primary Interfaces & Services

| File | Purpose |
|---|---|
| `core/lib/Drupal/Core/Render/RendererInterface.php` | Main renderer interface -- `renderRoot()`, `renderInIsolation()`, `render()` |
| `core/lib/Drupal/Core/Render/Renderer.php` | Renderer implementation -- full rendering pipeline (1600+ lines) |
| `core/lib/Drupal/Core/Render/BubbleableMetadata.php` | Cache metadata bubbling logic |
| `core/lib/Drupal/Core/Render/RenderContext.php` | Render context stack for metadata collection |
| `core/lib/Drupal/Core/Render/ElementInfoManager.php` | Render element plugin discovery |
| `core/lib/Drupal/Core/Render/AttachmentsResponseProcessorInterface.php` | Processes `#attached` into HTTP response |

### Render Element Base Classes

| File | Purpose |
|---|---|
| `core/lib/Drupal/Core/Render/Element/RenderElementBase.php` | Base class for generic render elements |
| `core/lib/Drupal/Core/Render/Element/FormElementBase.php` | Base class for form input elements |
| `core/lib/Drupal/Core/Render/Element/ElementInterface.php` | Interface all render elements implement |
| `core/lib/Drupal/Core/Render/Attribute/RenderElement.php` | Attribute for render element plugins |
| `core/lib/Drupal/Core/Render/Attribute/FormElement.php` | Attribute for form element plugins |

### Example Render Elements

**Study these for patterns:**

| File | Element | Key Features |
|---|---|---|
| `core/lib/Drupal/Core/Render/Element/Link.php` | `link` | URL handling, access checking, `#pre_render` |
| `core/lib/Drupal/Core/Render/Element/Container.php` | `container` | Simple wrapper, `#optional` property |
| `core/lib/Drupal/Core/Render/Element/Table.php` | `table` | Complex structure, `#rows` vs children |
| `core/lib/Drupal/Core/Render/Element/Details.php` | `details` | Collapsible element, `#open` state |
| `core/lib/Drupal/Core/Render/Element/HtmlTag.php` | `html_tag` | Arbitrary HTML tags, void elements |
| `core/lib/Drupal/Core/Render/Element/InlineTemplate.php` | `inline_template` | Twig integration |
| `core/lib/Drupal/Core/Render/Element/StatusMessages.php` | `status_messages` | Message queue integration |

### Cache & Performance

| File | Purpose |
|---|---|
| `core/lib/Drupal/Core/Render/RenderCache.php` | Render cache implementation |
| `core/lib/Drupal/Core/Cache/CacheableMetadata.php` | Cache metadata base class |
| `core/lib/Drupal/Core/Cache/CacheContextsManager.php` | Cache context resolution |
| `core/lib/Drupal/Core/Cache/Cache.php` | Cache constants and utilities |

### Placeholders & Lazy Building

| File | Purpose |
|---|---|
| `core/lib/Drupal/Core/Render/Placeholder/PlaceholderStrategyInterface.php` | Placeholder strategy interface |
| `core/lib/Drupal/Core/Render/Placeholder/SingleFlushStrategy.php` | Default placeholder replacement |
| `core/lib/Drupal/Core/Render/Placeholder/ChainedPlaceholderStrategy.php` | Chains multiple strategies (Big Pipe, ESI) |

### Theme System Integration

| File | Purpose |
|---|---|
| `core/lib/Drupal/Core/Theme/ThemeManagerInterface.php` | Theme rendering |
| `core/lib/Drupal/Core/Template/TwigExtension.php` | Twig filters/functions for Drupal |
| `core/lib/Drupal/Core/Template/Attribute.php` | HTML attribute handling |

### Main Content Renderers

| File | Purpose |
|---|---|
| `core/lib/Drupal/Core/Render/MainContent/HtmlRenderer.php` | Standard HTML page rendering |
| `core/lib/Drupal/Core/Render/MainContent/AjaxRenderer.php` | AJAX response rendering |
| `core/lib/Drupal/Core/Render/MainContent/DialogRenderer.php` | Dialog/modal rendering |
| `core/lib/Drupal/Core/Render/MainContent/ModalRenderer.php` | Modal dialog rendering |

## Find Render Elements in Core

```bash
# All render element plugins
ls core/lib/Drupal/Core/Render/Element/

# Form element plugins
grep -l "FormElement" core/lib/Drupal/Core/Render/Element/*.php

# Generic render elements
grep -l "RenderElement" core/lib/Drupal/Core/Render/Element/*.php
```

**109 files in `core/lib/Drupal/Core/Render/`** -- comprehensive render system.

## Key API Documentation

| Topic | URL |
|---|---|
| Render API overview | https://www.drupal.org/docs/drupal-apis/render-api |
| Render arrays | https://www.drupal.org/docs/drupal-apis/render-api/render-arrays |
| Cacheability | https://www.drupal.org/docs/drupal-apis/render-api/cacheability-of-render-arrays |
| Render elements | https://www.drupal.org/docs/drupal-apis/render-api/render-elements |
| Auto-placeholdering | https://www.drupal.org/docs/drupal-apis/render-api/auto-placeholdering |
| Render pipeline | https://www.drupal.org/docs/drupal-apis/render-api/the-drupal-8-render-pipeline |

## Community Resources

| Resource | URL |
|---|---|
| Drupal at your Fingertips: Render Arrays | https://www.drupalatyourfingertips.com/render |
| Drupal at your Fingertips: Twig | https://www.drupalatyourfingertips.com/twig |
| Drupalize.me: Lazy Builders | https://drupalize.me/tutorial/use-lazy-builders-and-placeholders |

## Debugging Tools

```php
// Dump render array structure
kint($build);  // Requires devel module

// Print render array
echo '<pre>' . print_r($build, TRUE) . '</pre>';

// Check cache metadata
$metadata = BubbleableMetadata::createFromRenderArray($build);
kint($metadata->getCacheTags());
kint($metadata->getCacheContexts());
```

```yaml
# Disable render cache (development only)
# In sites/default/services.yml
parameters:
  renderer.config:
    required_cache_contexts: []  # Allow caching without contexts
```

## See Also

- Reference: All sections link back to specific core files
- Reference: [Drupal API documentation](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Render!theme.api.php/group/theme_render)
