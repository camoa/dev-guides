---
description: Using preprocess functions to modify or add variables before Twig templates -- render arrays, cache metadata, pre-render callbacks.
---

# Preprocess Functions

## When to Use

When you need to modify or add variables before they reach a Twig template -- add render arrays, compute values, restructure data, add cache metadata.

## Pattern: Basic Preprocess Function

**Naming convention:** `{module/theme}_preprocess_{hook}(&$variables)`

```php
/**
 * Implements hook_preprocess_HOOK() for node templates.
 */
function mymodule_preprocess_node(&$variables) {
  /** @var \Drupal\node\NodeInterface $node */
  $node = $variables['node'];

  // Add a new variable as a render array
  $variables['author_info'] = [
    '#theme' => 'username',
    '#account' => $node->getOwner(),
  ];

  // Add classes based on node data
  $variables['attributes']['class'][] = 'node--type-' . $node->bundle();

  // Add cache metadata
  $variables['#cache']['tags'][] = 'user:' . $node->getOwnerId();
}
```

**In `node.html.twig`:**

```twig
<article{{ attributes }}>
  {{ author_info }}
  {{ content }}
</article>
```

## Pattern: Adding Render Arrays in Preprocess

**CORRECT -- Pass render arrays:**

```php
function mymodule_preprocess_page(&$variables) {
  // Add a render array
  $variables['copyright'] = [
    '#markup' => '<p>&copy; ' . date('Y') . ' My Site</p>',
    '#cache' => ['contexts' => ['timezone']],
  ];
}
```

**WRONG -- Rendering in preprocess:**

```php
// DON'T DO THIS
function mymodule_preprocess_page(&$variables) {
  $build = ['#markup' => '<p>Copyright</p>'];

  // WRONG: Loses cache metadata, prevents alterations
  $variables['copyright'] = \Drupal::service('renderer')->render($build);
}
```

**Why:** Twig renders everything automatically. Rendering in preprocess:

- Loses bubbleable metadata (cache tags, contexts, attachments)
- Prevents other modules from altering the render array
- Converts structured data to string too early

**Reference:** [Twig best practices - preprocess functions and templates](https://www.drupal.org/docs/theming-drupal/twig-in-drupal/twig-best-practices-preprocess-functions-and-templates)

## Pattern: Modifying Existing Render Arrays

```php
function mymodule_preprocess_node(&$variables) {
  // Hide a field
  $variables['content']['field_internal_notes']['#access'] = FALSE;

  // Change field label
  $variables['content']['field_name']['#title'] = t('Full Name');

  // Add prefix/suffix
  $variables['content']['field_price']['#prefix'] = '<div class="price-wrapper">';
  $variables['content']['field_price']['#suffix'] = '</div>';

  // Change field formatter (if not yet rendered)
  if (isset($variables['content']['field_image'][0])) {
    $variables['content']['field_image'][0]['#image_style'] = 'thumbnail';
  }
}
```

## Pattern: Pre-Render Callbacks

Pre-render callbacks are an alternative to preprocess -- they run later in the rendering pipeline, just before the element is rendered.

```php
// In a render array
$build['section'] = [
  '#type' => 'container',
  '#pre_render' => [
    [MyClass::class, 'preRenderSection'],
  ],
];

// The callback
public static function preRenderSection($element) {
  // Modify element
  $element['#attributes']['class'][] = 'enhanced';

  // Can add children
  $element['timestamp'] = [
    '#markup' => '<time>' . date('c') . '</time>',
  ];

  return $element;
}
```

**Pre-render vs Preprocess:**

| Feature | Pre-render callback | Preprocess function |
|---|---|---|
| When it runs | Just before rendering this element | Before template rendering |
| Scope | Single element | All variables for template |
| Alterability | Less discoverable (attached to element) | More discoverable (hook system) |
| Use case | Element-specific logic | Template variable preparation |

**Reference:** `core/lib/Drupal/Core/Render/Element/RenderElementBase.php` (lines 96-98) -- `#pre_render` documentation

## Decision: Preprocess vs Pre-Render vs Alter Hook

| Need to... | Use... | Why |
|---|---|---|
| Add variables to a template | Preprocess function | Standard pattern for template variable preparation |
| Modify a specific render element before rendering | `#pre_render` callback | Scoped to that element, no global side effects |
| Allow other modules to modify your data | Alter hook (invoke `moduleHandler->alter()`) | Explicitly extensible API |
| Modify render arrays from other modules | `hook_preprocess_HOOK()` or render array alter | Integrate with existing render arrays |

## Common Mistakes

- **Rendering in preprocess instead of passing render arrays** -- Loses metadata, prevents alterations, hurts cacheability
- **Adding raw HTML strings instead of render arrays** -- Bypasses XSS protection, theming, and caching
- **Not adding cache metadata when adding dynamic content** -- Stale cache persists inappropriately
- **Modifying `$variables['elements']` instead of `$variables['content']`** -- Wrong variable; `elements` is input, `content` is processed render array
- **Assuming preprocess runs only once** -- Can run multiple times; avoid expensive operations without caching

## See Also

- [Twig Integration](twig-integration.md) for how Twig uses preprocessed variables
- [Theme Hooks & Suggestions](theme-hooks-suggestions.md) for defining preprocessable hooks
- Reference: [Preprocess and Process Functions](https://jacine.gitbooks.io/theming/content/advanced/preprocess-process.html)
