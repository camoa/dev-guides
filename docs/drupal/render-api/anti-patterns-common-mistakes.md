---
description: Anti-patterns to avoid in render arrays -- early rendering, raw HTML, missing cache metadata, XSS vulnerabilities, structural mistakes.
---

# Anti-Patterns & Common Mistakes

## Rendering Anti-Patterns

### DON'T: Render in Preprocess Functions

**WRONG:**

```php
function mymodule_preprocess_node(&$variables) {
  $build = ['#markup' => '<p>Content</p>'];

  // WRONG: Renders too early, loses metadata
  $variables['extra_content'] = \Drupal::service('renderer')->render($build);
}
```

**RIGHT:**

```php
function mymodule_preprocess_node(&$variables) {
  // Pass the render array, let Twig render it
  $variables['extra_content'] = [
    '#markup' => '<p>Content</p>',
    '#cache' => ['contexts' => ['user']],
  ];
}
```

**Why wrong:** Rendering in preprocess loses bubbleable metadata (cache tags, contexts, attachments), prevents other modules from altering, and happens too early in the pipeline.

---

### DON'T: Use Raw HTML Concatenation

**WRONG:**

```php
$output = '<div class="wrapper">';
$output .= '<h2>' . $title . '</h2>';
$output .= '<p>' . $body . '</p>';
$output .= '</div>';

return ['#markup' => $output];
```

**RIGHT:**

```php
return [
  '#type' => 'container',
  '#attributes' => ['class' => ['wrapper']],
  'title' => [
    '#type' => 'html_tag',
    '#tag' => 'h2',
    '#value' => $title,
  ],
  'body' => [
    '#markup' => '<p>' . $body . '</p>',
  ],
];
```

**Why wrong:** HTML concatenation bypasses XSS protection (if variables contain user input), can't be cached at component level, can't be themed/altered, mixes presentation with logic.

---

### DON'T: Use #markup with Unsanitized User Input

**WRONG -- XSS VULNERABILITY:**

```php
$user_name = $_GET['name'];  // User input

return [
  '#markup' => '<p>Hello ' . $user_name . '</p>',
];
// If $user_name = '<script>alert("XSS")</script>', script executes
```

**RIGHT:**

```php
$user_name = $_GET['name'];

return [
  '#markup' => '<p>Hello ' . Html::escape($user_name) . '</p>',
];

// OR use #plain_text (preferred)
return [
  '#type' => 'html_tag',
  '#tag' => 'p',
  '#value' => t('Hello @name', ['@name' => $user_name]),
];
```

**Why wrong:** `#markup` assumes content is already safe. User input must be escaped or use `#plain_text`.

## Cache Anti-Patterns

### DON'T: Forget Cache Contexts

**WRONG:**

```php
$current_user = \Drupal::currentUser();

return [
  '#markup' => '<p>Hello ' . $current_user->getDisplayName() . '</p>',
  '#cache' => [
    'keys' => ['greeting'],
    'max-age' => Cache::PERMANENT,
  ],
];
// Result: First user's name cached, shown to all users
```

**RIGHT:**

```php
return [
  '#markup' => '<p>Hello ' . $current_user->getDisplayName() . '</p>',
  '#cache' => [
    'keys' => ['greeting'],
    'contexts' => ['user'],  // Vary by user
    'max-age' => Cache::PERMANENT,
  ],
];
```

**Why wrong:** Content varies by user but cache doesn't -- wrong user sees wrong content.

---

### DON'T: Forget Cache Tags

**WRONG:**

```php
$config = \Drupal::config('mymodule.settings');
$message = $config->get('welcome_message');

return [
  '#markup' => $message,
  '#cache' => [
    'keys' => ['welcome'],
    'max-age' => Cache::PERMANENT,
  ],
];
// Result: Config changes don't update cached output
```

**RIGHT:**

```php
$config = \Drupal::config('mymodule.settings');

return [
  '#markup' => $config->get('welcome_message'),
  '#cache' => [
    'keys' => ['welcome'],
    'tags' => $config->getCacheTags(),  // Invalidates when config changes
    'max-age' => Cache::PERMANENT,
  ],
];
```

**Why wrong:** Cached content persists after dependencies change -- stale data shown indefinitely.

---

### DON'T: Set max-age => 0 as Default

**WRONG:**

```php
// "I don't know caching, so disable it everywhere"
return [
  '#markup' => $static_content,
  '#cache' => ['max-age' => 0],
];
```

**RIGHT:**

```php
// Analyze: does this actually vary? If not, cache it.
return [
  '#markup' => $static_content,
  '#cache' => [
    'keys' => ['static_content', 'section1'],
    'max-age' => Cache::PERMANENT,
  ],
];
```

**Why wrong:** Setting `max-age => 0` destroys performance. Most content CAN be cached with appropriate contexts/tags.

## Structure Anti-Patterns

### DON'T: Mix #markup and Children Confusingly

**WRONG:**

```php
return [
  '#markup' => '<h2>Title</h2>',
  'content' => ['#markup' => '<p>Body</p>'],
];
// Renders: <h2>Title</h2><p>Body</p>
// Confusing: title is property, content is child
```

**RIGHT:**

```php
return [
  'title' => ['#markup' => '<h2>Title</h2>'],
  'content' => ['#markup' => '<p>Body</p>'],
];
// OR
return [
  '#type' => 'container',
  '#prefix' => '<h2>Title</h2>',
  'content' => ['#markup' => '<p>Body</p>'],
];
```

**Why wrong:** Mixing parent `#markup` with children is confusing and order-dependent.

---

### DON'T: Create Deeply Nested Arrays Without Reason

**WRONG:**

```php
return [
  'wrapper' => [
    'container' => [
      'inner_wrapper' => [
        'another_container' => [
          'content' => ['#markup' => 'Hello'],
        ],
      ],
    ],
  ],
];
```

**RIGHT:**

```php
return [
  '#type' => 'container',
  '#attributes' => ['class' => ['content-wrapper']],
  'content' => ['#markup' => 'Hello'],
];
```

**Why wrong:** Unnecessary nesting makes code hard to read and slows rendering.

## Dependency Anti-Patterns

### DON'T: Load Entities Inside Loops Without Caching

**WRONG:**

```php
foreach ($node_ids as $nid) {
  $node = Node::load($nid);  // N queries
  $build[] = ['#markup' => $node->label()];
}
```

**RIGHT:**

```php
$nodes = Node::loadMultiple($node_ids);  // 1 query
foreach ($nodes as $node) {
  $build[] = ['#markup' => $node->label()];
}
```

**Why wrong:** N+1 query problem -- kills performance with large datasets.

---

### DON'T: Call Services Statically Everywhere

**WRONG:**

```php
$renderer = \Drupal::service('renderer');
$entity_manager = \Drupal::entityTypeManager();
$current_user = \Drupal::currentUser();
```

**RIGHT:**

```php
// In services/controllers, use dependency injection
public function __construct(
  RendererInterface $renderer,
  EntityTypeManagerInterface $entity_manager,
  AccountProxyInterface $current_user
) {
  $this->renderer = $renderer;
  $this->entityTypeManager = $entity_manager;
  $this->currentUser = $current_user;
}
```

**Why wrong:** Static calls make code untestable, hide dependencies, violate Drupal coding standards.

## Theme Anti-Patterns

### DON'T: Use #theme Without Defining It

**WRONG:**

```php
return [
  '#theme' => 'my_custom_thing',
  '#data' => $data,
];
// Error: theme hook not found
```

**RIGHT:**

```php
// First implement hook_theme()
function mymodule_theme($existing, $type, $theme, $path) {
  return [
    'my_custom_thing' => [
      'variables' => ['data' => NULL],
      'template' => 'my-custom-thing',
    ],
  ];
}

// Then use it
return [
  '#theme' => 'my_custom_thing',
  '#data' => $data,
];
```

**Why wrong:** Undefined theme hooks cause errors.

---

### DON'T: Forget to Clear Cache After Theme Changes

**WRONG:**

```php
// Add new hook_theme() implementation
// Refresh page expecting it to work
// Doesn't work -- WHY?!
```

**RIGHT:**

```bash
# After adding/modifying hook_theme()
drush cr
```

**Why wrong:** Theme registry is cached. Changes not visible until cache clear.

## See Also

- [Best Practices & Patterns](best-practices-patterns.md) for correct approaches
- [Security & Performance](security-performance.md) for security implications
- Reference: [Twig best practices - preprocess functions and templates](https://www.drupal.org/docs/theming-drupal/twig-in-drupal/twig-best-practices-preprocess-functions-and-templates)
