---
description: Programmatic access to icon packs and icons in PHP
drupal_version: "11.x"
---

# IconPackManager Service

## When to Use

> Use when you need programmatic access to icon packs and icons in PHP (controllers, services, forms, preprocess) rather than templates.

## Decision

| Method | Returns | Use for... |
|---|---|---|
| `getDefinitions()` | All pack definitions | Listing available packs |
| `getIcon($full_id)` | Single icon data | Rendering specific icon |
| `getIcons($pack_ids)` | Icons from packs | Building icon selectors |
| `hasDefinition($id)` | Boolean | Checking pack exists |

## Pattern

Access IconPackManager service:

```php
<?php
// Via service container
$icon_manager = \Drupal::service('plugin.manager.icon_pack');

// Via dependency injection (preferred)
class MyService {
  public function __construct(
    protected IconPackManagerInterface $iconPackManager
  ) {}

  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('plugin.manager.icon_pack')
    );
  }
}
```

Get all packs:

```php
// Get all pack definitions
$packs = $icon_manager->getDefinitions();

foreach ($packs as $pack_id => $definition) {
  $label = $definition['label'];
  $extractor = $definition['extractor'];
}
```

Get specific icon:

```php
// Get icon data
$icon = $icon_manager->getIcon('my_theme:home');

if ($icon) {
  // Returns IconDefinition object
  $pack_id = $icon->getPackId();
  $icon_id = $icon->getIconId();
  $source = $icon->getSource();
}
```

Render icon in PHP:

```php
// Create render array
$element = [
  '#type' => 'icon',
  '#pack' => 'my_theme',
  '#icon' => 'home',
  '#settings' => [
    'size' => 32,
    'color' => '#007bff',
  ],
];

// In preprocess
function my_theme_preprocess_page(&$variables) {
  $icon_manager = \Drupal::service('plugin.manager.icon_pack');

  $variables['home_icon'] = [
    '#type' => 'icon',
    '#pack' => 'my_theme',
    '#icon' => 'home',
    '#settings' => ['size' => 24],
  ];
}
```

Get icons for form options:

```php
// Build select options from icon pack
$icon_manager = \Drupal::service('plugin.manager.icon_pack');
$icons = $icon_manager->getIcons(['my_theme']);

$options = [];
foreach ($icons as $icon_id => $icon_data) {
  $options[$icon_id] = $icon_data['label'] ?? $icon_id;
}

$form['icon'] = [
  '#type' => 'select',
  '#title' => $this->t('Select Icon'),
  '#options' => $options,
];
```

Reference: `/core/lib/Drupal/Core/Theme/Icon/Plugin/IconPackManager.php`

## Common Mistakes

- **Wrong**: Using static `\Drupal::service()` calls → **Right**: Inject IconPackManager via dependency injection
- **Wrong**: Not checking icon exists → **Right**: Use `getIcon()` return value check before accessing
- **Wrong**: Ignoring cache contexts → **Right**: Icon render arrays include cache tags automatically
- **Wrong**: Building icon markup manually → **Right**: Use render arrays for proper caching and theming
- **Wrong**: Accessing internal plugin properties → **Right**: Use public API methods only

## See Also

- [Icon Slots](icon-slots.md)
- [Caching Strategy](caching-strategy.md)
- Reference: `/core/lib/Drupal/Core/Theme/Icon/IconDefinition.php`
