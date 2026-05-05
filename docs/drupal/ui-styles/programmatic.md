---
description: Use UI Styles services and form elements in custom code — reading definitions, embedding the form element, and applying classes to render arrays.
tldr: Use plugin.manager.ui_styles to read definitions, the ui_styles_styles form element type in custom forms, and Drupal\ui_styles\Render\Element::addClasses() to inject classes into render arrays. Store both the selected array and extra string — not just the class string.
drupal_version: "11.x"
---

# Programmatic Use

## When to Use

> Use this guide when writing custom render code that needs to apply UI Styles classes — custom block plugins, render array builders, or custom forms.

## Pattern

**Read style definitions**:

```php
$plugin_manager = \Drupal::service('plugin.manager.ui_styles');
$definitions = $plugin_manager->getDefinitions();
```

**Use the form element** in a custom form:

```php
$form['styles'] = [
  '#type' => 'ui_styles_styles',
  '#default_value' => [
    'selected' => $config->get('styles.selected') ?? [],
    'extra' => $config->get('styles.extra') ?? '',
  ],
  '#drupal_theme' => 'mytheme',  // optional — limits to theme-specific styles
];
```

**Add classes to a render array**:

```php
use Drupal\ui_styles\Render\Element;

$build = ['#markup' => '<div>Hello</div>'];
$build = Element::addClasses($build, ['text-primary', 'p-4']);
```

## Service & Class Reference

| Service / Class | Purpose |
|---|---|
| `plugin.manager.ui_styles` | Discover and manage style definitions |
| `plugin.manager.ui_styles.source` | Discover form widget plugins (Checkbox, Toolbar, Select) |
| `ui_styles.stylesheet_generator` | Generate optimized CSS at runtime |
| `\Drupal\ui_styles\Definition\StyleDefinition` | Value object for a parsed style |
| `\Drupal\ui_styles\Element\Styles` | The `ui_styles_styles` form element |
| `\Drupal\ui_styles\Render\Element` | Static helpers including `addClasses()` |

## Common Mistakes

- **Storing only the class string in custom code** → The form element returns `['selected' => [...], 'extra' => '...']`. Store and reapply both halves
- **Bypassing `Element::addClasses()` and concatenating strings** → The helper handles cache metadata and class deduplication; manual concatenation drops both

## See Also

- [Code Reference](code-reference.md)
- [Style Definition Format](definition-format.md)
- Reference: `src/Render/Element.php`, `src/Element/Styles.php` in the UI Styles module
