---
description: Architectural best practices for render arrays -- dependency injection, cache metadata, access checks, testing, and performance optimization.
---

# Best Practices & Patterns

## Core Principles

1. **Configuration First:** Render arrays are data structures, not output. Keep them as arrays until the last responsible moment.
2. **Metadata Bubbling:** Always provide cache metadata. It bubbles up automatically, enabling Drupal's sophisticated caching.
3. **Avoid Early Rendering:** Don't call `render()` in preprocess functions or other pre-output code. Pass render arrays to Twig.
4. **Reuse Over Reinvention:** Use existing render elements and theme hooks before creating custom ones.
5. **Security by Default:** Use `#plain_text` for user input, `#markup` only for trusted/sanitized HTML.

## Architectural Best Practices

### Use Dependency Injection for Renderer

**GOOD:**

```php
namespace Drupal\mymodule\Service;

use Drupal\Core\Render\RendererInterface;

class MyService {

  protected $renderer;

  public function __construct(RendererInterface $renderer) {
    $this->renderer = $renderer;
  }

  public function buildEmail() {
    $build = ['#markup' => 'Email content'];
    return $this->renderer->renderInIsolation($build);
  }

}
```

**BAD:**

```php
// Don't use static service calls
$html = \Drupal::service('renderer')->render($build);
```

**Why:** DI makes code testable, explicit about dependencies, and follows Drupal coding standards.

---

### Provide Complete Cache Metadata

**GOOD:**

```php
$node = Node::load($nid);

$build = [
  '#markup' => $node->label(),
  '#cache' => [
    'keys' => ['node_title', $node->id()],
    'tags' => $node->getCacheTags(),
    'contexts' => ['languages:language_interface'],
    'max-age' => Cache::PERMANENT,
  ],
];
```

**BAD:**

```php
// Missing cache metadata
$build = ['#markup' => $node->label()];
// Result: Not cached, or cached without proper invalidation
```

**Why:** Incomplete metadata causes stale cache (security/correctness issue) or no caching (performance issue).

---

### Use Access Checks with Metadata

**GOOD:**

```php
$access_result = $entity->access('view', NULL, TRUE);

$build = [
  '#access' => $access_result,
  'content' => $view_builder->view($entity),
];

\Drupal::service('renderer')->addCacheableDependency($build, $access_result);
```

**BAD:**

```php
// Boolean access check without metadata
if ($entity->access('view')) {
  $build['content'] = $view_builder->view($entity);
}
// Result: Cached with wrong access decision for some users
```

**Why:** Access checks have cache contexts (user, permissions). Must capture that metadata.

---

### Prefer #type Over #theme for Reusable Elements

**GOOD:**

```php
$build['link'] = [
  '#type' => 'link',
  '#title' => t('Read more'),
  '#url' => Url::fromRoute('node.view', ['node' => $nid]),
];
```

**BAD:**

```php
$build['link'] = [
  '#theme' => 'link',
  '#text' => t('Read more'),
  '#url' => Url::fromRoute('node.view', ['node' => $nid]),
];
```

**Why:** `#type` uses render element plugins with defaults, processing, validation. `#theme` is lower-level.

---

### Structure Complex Render Arrays with Comments

```php
$build = [
  // Hero section
  'hero' => [
    '#type' => 'container',
    '#attributes' => ['class' => ['hero']],
    'title' => ['#markup' => '<h1>' . $title . '</h1>'],
    'image' => $image_render_array,
  ],

  // Main content area
  'content' => [
    '#type' => 'container',
    '#weight' => 0,
    'body' => $body_render_array,
    'related' => $related_content,
  ],

  // Sidebar
  'sidebar' => [
    '#type' => 'container',
    '#weight' => 10,
    'widgets' => $sidebar_widgets,
  ],
];
```

**Why:** Large render arrays are hard to read. Section comments improve maintainability.

## Development Standards

### Follow Drupal Coding Standards

- Use `#` prefix for properties consistently
- Use snake_case for child keys
- Use `'#type' => 'element_name'` format (string values)
- Array formatting: one property per line for readability

### Test Render Arrays

```php
// In a kernel test
public function testRenderArray() {
  $build = [
    '#type' => 'container',
    'content' => ['#markup' => 'Test content'],
  ];

  $renderer = \Drupal::service('renderer');
  $output = $renderer->renderRoot($build);

  $this->assertStringContainsString('Test content', (string) $output);
  $this->assertStringContainsString('<div', (string) $output);  // Container wraps
}
```

**Test cache metadata:**

```php
$this->assertEquals(['user'], $build['#cache']['contexts']);
$this->assertContains('node:1', $build['#cache']['tags']);
```

### Document Custom Properties

```php
/**
 * Provides a user card render element.
 *
 * Properties:
 * - #user: User entity object (required).
 * - #show_email: Boolean, whether to show email. Default: FALSE.
 * - #style: Card style ('compact' or 'full'). Default: 'compact'.
 *
 * Usage example:
 * @code
 * $build['user_card'] = [
 *   '#type' => 'user_card',
 *   '#user' => $user,
 *   '#show_email' => TRUE,
 *   '#style' => 'full',
 * ];
 * @endcode
 */
#[RenderElement('user_card')]
class UserCard extends RenderElementBase {
  // ...
}
```

## Performance Best Practices

### Use Lazy Builders for Personalized/Uncacheable Content

```php
return [
  'static' => [
    '#markup' => '<h2>Product List</h2>',
    '#cache' => ['max-age' => Cache::PERMANENT],
  ],
  'personalized_recommendations' => [
    '#lazy_builder' => ['\Drupal\mymodule\RecommendationBuilder::build', [$user_id]],
    '#create_placeholder' => TRUE,
  ],
];
```

**Result:** Static part cached, personalized part rendered per user.

### Set Appropriate max-age

```php
// User-generated content that changes frequently
'#cache' => ['max-age' => 300],  // 5 minutes

// Configuration-based, rarely changes
'#cache' => ['max-age' => Cache::PERMANENT],

// Time-sensitive (current time, countdowns)
'#cache' => ['max-age' => 60],  // 1 minute
```

### Avoid N+1 Queries in Render Arrays

**BAD:**

```php
foreach ($node_ids as $nid) {
  $build[$nid] = [
    '#markup' => Node::load($nid)->label(),  // N queries
  ];
}
```

**GOOD:**

```php
$nodes = Node::loadMultiple($node_ids);  // 1 query
foreach ($nodes as $nid => $node) {
  $build[$nid] = [
    '#markup' => $node->label(),
  ];
}
```

## See Also

- [Anti-Patterns & Common Mistakes](anti-patterns-common-mistakes.md) for what NOT to do
- [Security & Performance](security-performance.md) for security-specific guidance
- Reference: [Drupal at your Fingertips: Render Arrays](https://www.drupalatyourfingertips.com/render)
