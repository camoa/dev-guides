---
description: Common render array patterns -- progressive enhancement, conditional access, weighted ordering, entity views, item lists, AJAX responses, debugging.
---

# Render Array Patterns

## When to Use

Common scenarios have established patterns -- use these proven approaches rather than reinventing solutions.

## Pattern: Progressive Enhancement

Build base HTML, enhance with JavaScript via `#attached`:

```php
$build['interactive_map'] = [
  '#theme' => 'mymodule_map_fallback',
  '#locations' => $locations,
  '#attributes' => ['class' => ['map-container'], 'id' => 'map'],
  '#attached' => [
    'library' => ['mymodule/interactive-map'],
    'drupalSettings' => [
      'myModule' => [
        'mapId' => 'map',
        'locations' => $locations,
      ],
    ],
  ],
];
```

**Benefits:**

- Works without JavaScript (graceful degradation)
- JavaScript enhances existing HTML
- Content accessible to crawlers/screen readers

---

## Pattern: Conditional Access

```php
$node = Node::load($nid);
$access_result = $node->access('view', NULL, TRUE);

$build['content'] = [
  '#access' => $access_result,
  'title' => ['#markup' => '<h2>' . $node->label() . '</h2>'],
  'body' => $node->get('body')->view('full'),
];

// Bubble access result's cache metadata
\Drupal::service('renderer')->addCacheableDependency($build, $access_result);
```

**Why capture access result as object:**

- Contains cache metadata (contexts, tags)
- Prevents caching the wrong access decision for different users

---

## Pattern: Weighted Ordering

```php
$build = [];

$build['header'] = [
  '#markup' => '<h1>Page Title</h1>',
  '#weight' => -100,  // Render first
];

$build['sidebar'] = [
  '#type' => 'container',
  '#weight' => 10,  // Render last
];

$build['content'] = [
  '#markup' => '<p>Main content</p>',
  '#weight' => 0,  // Default, middle
];

// Renders in order: header, content, sidebar
```

**Weight ranges:**

- `-100 to -10`: Headers, critical content
- `-9 to 9`: Default content
- `10 to 100`: Footers, supplementary content

---

## Pattern: Render Array from Entity View

```php
$node = Node::load($nid);

// Full render array for entity
$view_builder = \Drupal::entityTypeManager()->getViewBuilder('node');
$build = $view_builder->view($node, 'teaser');

// Contains all fields, proper cache metadata, theme hooks
```

**View modes:** `full`, `teaser`, `rss`, custom modes defined in entity view display config

---

## Pattern: Item List

```php
$build['list'] = [
  '#theme' => 'item_list',
  '#items' => [
    ['#markup' => 'Item 1'],
    ['#markup' => 'Item 2'],
    [
      '#type' => 'link',
      '#title' => t('Item 3 is a link'),
      '#url' => Url::fromRoute('mymodule.page'),
    ],
  ],
  '#list_type' => 'ul',  // 'ul', 'ol', or custom
  '#title' => t('My List'),
  '#attributes' => ['class' => ['custom-list']],
  '#wrapper_attributes' => ['class' => ['list-wrapper']],
];
```

---

## Pattern: Render Cache Keys from Multiple Variables

```php
$build['complex_content'] = [
  '#markup' => $this->generateContent($user, $config),
  '#cache' => [
    'keys' => [
      'mymodule',
      'complex_content',
      $user->id(),
      $config->id(),
    ],
    'contexts' => ['user', 'languages:language_interface'],
    'tags' => array_merge(
      $user->getCacheTags(),
      $config->getCacheTags()
    ),
  ],
];
```

**Cache keys convention:**

- `['module_name', 'component_name', ...identifiers]`
- Identifiers make the cache unique for this specific render

---

## Pattern: Render Array in AJAX Response

```php
use Drupal\Core\Ajax\AjaxResponse;
use Drupal\Core\Ajax\ReplaceCommand;

public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  $build = [
    '#theme' => 'mymodule_result',
    '#data' => $this->fetchData(),
  ];

  $response = new AjaxResponse();
  $response->addCommand(new ReplaceCommand('#result-container', $build));

  return $response;
}
```

**AJAX commands automatically render the array before sending to client.**

---

## Pattern: Inline Attachments (Small CSS/JS)

```php
$build['styled_box'] = [
  '#markup' => '<div class="special-box">Content</div>',
  '#attached' => [
    'library' => ['mymodule/special-box'],
    'drupalSettings' => ['myModule' => ['mode' => 'fancy']],
    // Inline CSS (use sparingly)
    'html_head' => [[
      [
        '#type' => 'html_tag',
        '#tag' => 'style',
        '#value' => '.special-box { border: 2px solid red; }',
      ],
      'special_box_inline_style',
    ]],
  ],
];
```

**Best practice:** Use libraries instead of inline styles; inline only for dynamic/computed values

---

## Pattern: Debugging Render Arrays

```php
// In development
$build['debug'] = [
  '#type' => 'details',
  '#title' => 'Debug: Render Array',
  '#open' => TRUE,
  'content' => [
    '#markup' => '<pre>' . print_r($build, TRUE) . '</pre>',
  ],
];

// Or use Kint (if devel module installed)
kint($build);
```

## Common Mistakes

- **Not reusing patterns** -- Solving already-solved problems inefficiently
- **Mixing patterns inconsistently** -- Makes codebase hard to understand
- **Over-engineering simple cases** -- Sometimes `#markup` is enough

## See Also

- [Best Practices & Patterns](best-practices-patterns.md) for architectural guidance
- Reference: [Render Array Examples](https://webdev.iac.gatech.edu/ddcb/render-twig/render-array-examples)
