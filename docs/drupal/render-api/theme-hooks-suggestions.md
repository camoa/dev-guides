---
description: Creating theme hooks, template suggestions, theme wrappers, and template discovery for custom themed output.
---

# Theme Hooks & Suggestions

## When to Use

When creating custom themed output that needs a Twig template and preprocessable variables. Theme hooks define the contract between code and templates.

## Pattern: Defining a Theme Hook

**In `mymodule.module`:**

```php
/**
 * Implements hook_theme().
 */
function mymodule_theme($existing, $type, $theme, $path) {
  return [
    'mymodule_user_card' => [
      'variables' => [
        'user' => NULL,
        'show_email' => FALSE,
      ],
      'template' => 'mymodule-user-card',  // Creates mymodule-user-card.html.twig
    ],
    'mymodule_product_list' => [
      'variables' => [
        'products' => [],
        'title' => NULL,
      ],
      'template' => 'mymodule-product-list',
    ],
  ];
}
```

**In `templates/mymodule-user-card.html.twig`:**

```twig
<div class="user-card">
  <h3>{{ user.name }}</h3>
  {% if show_email %}
    <p class="email">{{ user.mail }}</p>
  {% endif %}
</div>
```

**Using the theme hook:**

```php
$build = [
  '#theme' => 'mymodule_user_card',
  '#user' => $user,
  '#show_email' => TRUE,
];
```

## Pattern: Theme Hook Suggestions

Suggestions allow template variations based on context. Drupal automatically checks for more specific template names before falling back to the base template.

**Suggestion priority (most specific first):**

```
node--article--full.html.twig        (bundle + view mode)
node--article.html.twig              (bundle)
node--full.html.twig                 (view mode)
node.html.twig                       (base)
```

**Adding custom suggestions in preprocess:**

```php
function mymodule_preprocess_node(&$variables) {
  $node = $variables['node'];

  // Add suggestion based on promoted status
  if ($node->isPromoted()) {
    $variables['theme_hook_suggestions'][] = 'node__promoted';
  }

  // Template priority becomes:
  // node--promoted.html.twig (if promoted)
  // node--article.html.twig
  // node.html.twig
}
```

## Pattern: Using #theme_wrappers

Theme wrappers wrap rendered children in additional theming.

```php
$build = [
  '#markup' => '<p>Inner content</p>',
  '#theme_wrappers' => ['container'],
  '#attributes' => ['class' => ['my-wrapper']],
];

// Renders as:
// <div class="my-wrapper">
//   <p>Inner content</p>
// </div>
```

**Multiple wrappers (applied in order):**

```php
$build = [
  '#markup' => 'Content',
  '#theme_wrappers' => [
    'container',  // Inner wrapper
    'details',    // Outer wrapper
  ],
  '#title' => 'Details Title',
];
```

## Pattern: Render Arrays in Theme Hook Variables

```php
// In hook_theme()
'mymodule_card' => [
  'variables' => [
    'header' => NULL,  // Can be string OR render array
    'body' => NULL,
    'footer' => NULL,
  ],
],

// Usage
$build = [
  '#theme' => 'mymodule_card',
  '#header' => [
    '#type' => 'html_tag',
    '#tag' => 'h2',
    '#value' => $title,
  ],
  '#body' => [
    '#markup' => $body_html,
  ],
  '#footer' => [
    '#type' => 'link',
    '#title' => t('Read more'),
    '#url' => $url,
  ],
];
```

**In template:**

```twig
<div class="card">
  <header>{{ header }}</header>
  <div class="body">{{ body }}</div>
  <footer>{{ footer }}</footer>
</div>
```

## Theme Hook Discovery

Drupal looks for templates in:

1. **Module templates:** `mymodule/templates/`
2. **Theme templates:** `mytheme/templates/`
3. **Nested directories:** `templates/content/`, `templates/navigation/` (organized by feature)

**Template naming:**

- Convert underscores to hyphens: `mymodule_user_card` -> `mymodule-user-card.html.twig`
- Suggestions use double hyphens: `node--article.html.twig`

## Common Mistakes

- **Not clearing cache after adding hook_theme()** -- New theme hooks not discovered until cache clear
- **Misnaming template files** -- Must match hook name with underscores converted to hyphens
- **Forgetting to define variables in hook_theme()** -- Variables undefined in template
- **Not providing default values for optional variables** -- Template errors if variable not passed
- **Overusing suggestions** -- Too many specific templates = maintenance burden; prefer CSS classes + preprocess logic
- **Using `#theme` and `#type` together** -- `#theme` takes precedence; usually use one or the other

## See Also

- [Preprocess Functions](preprocess-functions.md) for modifying theme hook variables
- [Twig Integration](twig-integration.md) for using variables in templates
- Reference: `core/lib/Drupal/Core/Theme/ThemeManagerInterface.php` -- theme rendering
