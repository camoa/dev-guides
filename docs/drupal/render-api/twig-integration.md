---
description: Passing render arrays to Twig templates -- automatic rendering, conditional output, filters, and read-only array behavior.
---

# Twig Integration

## When to Use

Render arrays are designed to work seamlessly with Twig -- pass them as variables and Twig renders them automatically. This is the standard pattern for theming in Drupal.

## How Render Arrays Work in Twig

**Automatic rendering:** Any render array passed to a Twig template is automatically rendered when printed.

```php
// In a controller or preprocess function
$variables['sidebar'] = [
  '#type' => 'container',
  '#attributes' => ['class' => ['sidebar']],
  'content' => ['#markup' => '<p>Sidebar content</p>'],
];
```

```twig
{# In template.html.twig #}
<div class="layout">
  {{ sidebar }}
  {# Drupal automatically calls renderer on sidebar render array #}
</div>
```

**Reference:** `core/lib/Drupal/Core/Template/TwigExtension.php` -- Twig filters/functions for Drupal

## Pattern: Passing Render Arrays to Templates

**In `hook_theme()` implementation:**

```php
function mymodule_theme($existing, $type, $theme, $path) {
  return [
    'mymodule_card' => [
      'variables' => [
        'title' => NULL,
        'body' => NULL,  // Can be string OR render array
        'footer' => NULL,
      ],
      'template' => 'mymodule-card',
    ],
  ];
}
```

**In preprocess function:**

```php
function mymodule_preprocess_mymodule_card(&$variables) {
  // Body can be a render array
  $variables['body'] = [
    '#theme' => 'item_list',
    '#items' => ['Item 1', 'Item 2'],
  ];

  // Footer can be a render array
  $variables['footer'] = [
    '#type' => 'link',
    '#title' => t('Read more'),
    '#url' => Url::fromRoute('mymodule.page'),
  ];
}
```

**In `templates/mymodule-card.html.twig`:**

```twig
<div class="card">
  <h2>{{ title }}</h2>
  <div class="card-body">
    {{ body }}
    {# Automatically renders item_list #}
  </div>
  <div class="card-footer">
    {{ footer }}
    {# Automatically renders link #}
  </div>
</div>
```

## Pattern: Conditional Rendering in Twig

```twig
{# Check if render array has visible children #}
{% if content.field_image|render|striptags|trim %}
  <div class="image-wrapper">
    {{ content.field_image }}
  </div>
{% endif %}

{# Better: Use render element's #access #}
{# In preprocess: #}
{# $variables['content']['field_image']['#access'] = !$node->get('field_image')->isEmpty(); #}
{% if content.field_image %}
  {{ content.field_image }}
{% endif %}
```

## Pattern: Altering Render Arrays in Twig (Anti-Pattern)

**DON'T DO THIS:**

```twig
{# WRONG: Cannot modify render arrays in Twig #}
{% set content.field_name['#prefix'] = '<div class="wrapper">' %}
{{ content.field_name }}
```

**DO THIS INSTEAD:**

```php
// In preprocess function
function mymodule_preprocess_node(&$variables) {
  $variables['content']['field_name']['#prefix'] = '<div class="wrapper">';
}
```

**Why:** Twig wraps all arrays in `ProtectedRenderArray` -- they're read-only in templates. Modification must happen in preprocess.

**Reference:** [Render arrays can no longer be created or modified in Twig](https://www.drupal.org/node/2932417)

## Useful Twig Filters for Render Arrays

| Filter | Purpose | Example |
|---|---|---|
| `render` | Force rendering (usually automatic) | `{{ content.field_name\|render }}` |
| `without` | Render array excluding certain keys | `{{ content\|without('field_image', 'links') }}` |
| `striptags` | Remove HTML tags from rendered output | `{{ content.body\|render\|striptags }}` |

## Common Mistakes

- **Calling `render()` in preprocess functions** -- Pass render arrays to Twig, let Twig render them automatically
- **Trying to modify render arrays in Twig** -- Arrays are read-only in templates; use preprocess instead
- **Using `{{ content|render }}` unnecessarily** -- `{{ content }}` auto-renders; explicit `|render` only needed in specific edge cases
- **Not understanding `|without` creates a copy** -- Original variable unchanged; use result in new variable if needed
- **Rendering fields individually when `content` already has them** -- `{{ content }}` renders all fields; cherry-pick only if needed

## See Also

- [Preprocess Functions](preprocess-functions.md) for modifying variables before Twig
- Reference: [Twig best practices - preprocess functions and templates](https://www.drupal.org/docs/theming-drupal/twig-in-drupal/twig-best-practices-preprocess-functions-and-templates)
- Reference: [Drupal at your Fingertips: Twig](https://www.drupalatyourfingertips.com/twig)
