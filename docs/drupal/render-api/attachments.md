---
description: Attaching CSS/JS libraries, drupalSettings, HTML head elements, and HTTP headers to render arrays.
---

# Attachments (#attached)

## When to Use

When your render array needs CSS, JavaScript, drupalSettings, HTTP headers, HTML `<head>` elements, or placeholders. Attachments bubble up from children to parents to page level.

## Attachment Types

| Attachment | Purpose | Example |
|---|---|---|
| `library` | Load CSS/JS asset libraries | `'library' => ['core/drupal.dialog', 'mymodule/behavior']` |
| `drupalSettings` | Pass data to JavaScript | `'drupalSettings' => ['myModule' => ['apiKey' => '123']]` |
| `html_head` | Add elements to `<head>` (meta, link) | `'html_head' => [[$meta_tag, 'meta_description']]` |
| `html_head_link` | Add `<link>` elements | `'html_head_link' => [[['rel' => 'canonical', 'href' => $url]]]` |
| `http_header` | Set HTTP response headers | `'http_header' => [['Cache-Control', 'no-cache']]` |
| `placeholders` | Placeholder replacement (internal) | `'placeholders' => ['<drupal-placeholder>' => [...]]` |
| `feed` | RSS/Atom feeds | `'feed' => [[$url, $title]]` |

## Pattern: Attaching Libraries

```php
$build['interactive_map'] = [
  '#markup' => '<div id="map"></div>',
  '#attached' => [
    'library' => [
      'mymodule/leaflet',  // Defined in mymodule.libraries.yml
    ],
    'drupalSettings' => [
      'myModule' => [
        'mapCenter' => ['lat' => 40.7128, 'lng' => -74.0060],
        'zoom' => 12,
      ],
    ],
  ],
];
```

**Libraries file (`mymodule.libraries.yml`):**

```yaml
leaflet:
  version: 1.x
  css:
    theme:
      css/leaflet.css: {}
  js:
    js/leaflet.js: {}
  dependencies:
    - core/jquery
```

**Reference:** [Adding assets (CSS, JS) to a Drupal module](https://www.drupal.org/docs/develop/creating-modules/adding-assets-css-js-to-a-drupal-module-via-librariesyml)

## Pattern: HTML Head Elements

```php
$build['#attached']['html_head'][] = [
  [
    '#type' => 'html_tag',
    '#tag' => 'meta',
    '#attributes' => [
      'name' => 'description',
      'content' => 'This is a page description.',
    ],
  ],
  'meta_description',  // Unique key to prevent duplicates
];
```

## Pattern: HTTP Headers

```php
$build['#attached']['http_header'][] = [
  'X-Custom-Header',
  'CustomValue',
];

// Prevent caching
$build['#attached']['http_header'][] = [
  'Cache-Control',
  'no-cache, must-revalidate',
];
```

## Bubbling Behavior

Attachments automatically bubble from children to parents during rendering:

```php
// Child component
$child = [
  '#markup' => 'Content',
  '#attached' => ['library' => ['mymodule/child-lib']],
];

// Parent component
$parent = [
  'child' => $child,
  '#attached' => ['library' => ['mymodule/parent-lib']],
];

// Result: Page gets BOTH libraries loaded
// Final #attached: ['library' => ['mymodule/parent-lib', 'mymodule/child-lib']]
```

**Reference:** `core/lib/Drupal/Core/Render/BubbleableMetadata.php` (lines 106-175) -- `mergeAttachments()` logic

## Common Mistakes

- **Forgetting library dependencies** -- JS breaks because jQuery or another dependency didn't load first
- **Not using unique keys in `html_head`** -- Multiple identical meta tags added to page
- **Adding attachments after rendering** -- Too late -- attachments must be present before `renderRoot()` is called
- **Overriding `drupalSettings` instead of merging** -- Use `NestedArray::mergeDeep()` if manually merging; automatic merge uses jQuery.extend() logic
- **Loading libraries globally when only needed on specific routes** -- Hurts performance; attach conditionally

## See Also

- [Cache Metadata in Render Arrays](cache-metadata-render-arrays.md) for bubbling cache metadata
- [Security & Performance](security-performance.md) for library loading best practices
- Reference: [Attaching libraries in render arrays](https://www.drupal.org/docs/drupal-apis/render-api/render-arrays#s-attaching-libraries-in-render-arrays)
