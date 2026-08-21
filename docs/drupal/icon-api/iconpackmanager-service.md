---
description: "IconPackManager's PHP API — getIcons() returns raw discovery data with no label, and render elements use #pack_id/#icon_id, never #pack/#icon"
tldr: "You need programmatic icon access in PHP; getIcons() returns discovery arrays with no label (call getIcon()->getLabel() for that), and the render element properties are #pack_id/#icon_id — #pack/#icon renders nothing, raises nothing."
drupal_version: "11.x"
---

# IconPackManager Service

## When to Use

You need programmatic access to icon packs and icons in PHP (controllers, services, forms, preprocess) rather than templates.

## Decision

| Method | Returns | Use for... |
|---|---|---|
| `getDefinitions()` | All pack definitions, keyed by pack ID | Listing available packs |
| `getIcon(string $full_id)` | `IconDefinitionInterface|null` | Reading one icon's metadata |
| `getIcons(array $allowed_icon_pack = [])` | Raw discovery arrays keyed by `pack:id` | Enumerating icon IDs |
| `listIconPackOptions(bool $with_description = FALSE)` | `pack_id => "Label (count)"` | A pack select element |
| `getExtractorFormDefaults(string $pack_id)` | The pack's settings `default:` values | Seeding a settings form |
| `hasDefinition($id)` | Boolean | Checking pack exists |

`getIcons()` returns the **discovery** payload, not icon objects: each value is the array the extractor built (`['absolute_path' => …, 'source' => …, 'group' => …]`), with no `label`. To get a human label, call `getIcon($full_id)->getLabel()` — or `listIconPackOptions()` if you only need pack-level options.

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

The render element properties are `#pack_id` and `#icon_id` (`Render\Element\Icon::getInfo()`). `#pack` and `#icon` are not recognised: `getInfo()` defaults both real properties to `''`, `getIcon('':'')` returns NULL, `preRenderIcon()` returns the element untouched, and you get blank output with no error.

```php
// Create render array
$element = [
  '#type' => 'icon',
  '#pack_id' => 'my_theme',
  '#icon_id' => 'home',
  '#settings' => [
    'size' => 32,
    'color' => '#007bff',
  ],
];

// In preprocess
function my_theme_preprocess_page(&$variables) {
  $variables['home_icon'] = [
    '#type' => 'icon',
    '#pack_id' => 'my_theme',
    '#icon_id' => 'home',
    '#settings' => ['size' => 24],
  ];
}
```

`IconDefinition::getRenderable('my_theme:home', $settings)` builds the same array from a combined ID, which is convenient when the ID came out of a field or config.

Get icons for form options:

```php
// Build select options from icon pack.
// getIcons() is keyed by the full "pack:id" and its values carry no label,
// so derive the label from the loaded IconDefinition.
$icon_manager = \Drupal::service('plugin.manager.icon_pack');

$options = [];
foreach (array_keys($icon_manager->getIcons(['my_theme'])) as $full_id) {
  $options[$full_id] = $icon_manager->getIcon($full_id)?->getLabel() ?? $full_id;
}

$form['icon'] = [
  '#type' => 'select',
  '#title' => $this->t('Select Icon'),
  '#options' => $options,
];
```

For large packs this loads every icon; prefer `IconDefinition::humanize($icon_id)` when you only need the display string, since that is exactly what `getLabel()` calls.

Reference: `/core/lib/Drupal/Core/Theme/Icon/Plugin/IconPackManager.php`, `/core/lib/Drupal/Core/Render/Element/Icon.php`

## Common Mistakes

- **Wrong**: `#pack` / `#icon` instead of `#pack_id` / `#icon_id` → **Right**: Renders nothing, raises nothing
- **Wrong**: Reading `$icon_data['label']` off `getIcons()` → **Right**: No such key; use `getIcon()->getLabel()`
- **Wrong**: Using static `\Drupal::service()` calls → **Right**: Inject IconPackManager via dependency injection
- **Wrong**: Not checking icon exists → **Right**: `getIcon()` returns NULL for an unknown pack or icon
- **Wrong**: Expecting the render array to carry cache tags → **Right**: It carries none; add your own if the surrounding render array needs them

## See Also

- [Icon Slots](icon-slots.md)
- [Caching Strategy](caching-strategy.md)
- Reference: `/core/lib/Drupal/Core/Theme/Icon/IconDefinition.php`
