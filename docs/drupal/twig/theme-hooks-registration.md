---
topic: drupal/twig
guide: theme-hooks-registration
---

## Theme Hooks & Registration

### When to Use
When your module or theme needs to register a new template (not override an existing one), define the variables it accepts, and specify the default template file.

### Decision
| Scenario | Approach | Notes |
|---|---|---|
| Module with reusable component | `hook_theme()` with `variables` key | Defines named variables with defaults |
| Theme element (form element, render type) | `hook_theme()` with `render element` key | Single render element passed to template |
| Override existing hook template | Copy template file to theme | No PHP needed — just copy and rename |
| Add suggestions to existing hook | `hook_theme_suggestions_HOOK()` | Returns array of suggestion strings |
| Alter suggestions for any hook | `hook_theme_suggestions_HOOK_alter()` | Modify `$suggestions` array |

### Pattern

**Registering a theme hook in a module:**
```php
// mymodule/src/Hook/MyModuleHooks.php (Drupal 11 OOP)
#[Hook('theme')]
public function theme(): array {
  return [
    'my_component' => [
      'variables' => [
        'title' => NULL,
        'items' => [],
        'attributes' => [],
      ],
      'template' => 'my-component', // maps to my-component.html.twig
    ],
  ];
}
```

**Using `render element` for form/render elements:**
```php
// The entire render element is passed as $variables['element']
'my_widget' => [
  'render element' => 'element',
  'template' => 'my-widget',
],
```

**Using the theme hook in a render array:**
```php
$build = [
  '#theme' => 'my_component',
  '#title' => $this->t('My Title'),
  '#items' => $items,
  '#attributes' => ['class' => ['my-modifier']],
];
```

**Template file** (`templates/my-component.html.twig`):
```twig
<div{{ attributes }}>
  <h2>{{ title }}</h2>
  {% for item in items %}
    <p>{{ item }}</p>
  {% endfor %}
</div>
```

**Note on template naming:** Variables in `hook_theme()` use underscores (`my_component`). The template file name uses hyphens (`my-component.html.twig`). The `template` key in the registration specifies the filename without extension.

### Common Mistakes
- Defining `#variables` in the render array without registering them in `hook_theme()` → they won't be passed to the template
- Using `#theme` with a hook name that doesn't exist → silent failure (Drupal uses fallback rendering)
- Forgetting `'base hook'` when creating a sub-hook of an existing hook (e.g., a specific field type template) → theming system won't merge suggestions correctly
- Not clearing the theme registry after changing `hook_theme()` → run `drush cr`

### See Also
- Template suggestions → [Template Suggestions](template-suggestions.md)
- Drupal API: `https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Render!theme.api.php/function/hook_theme/11.x`
