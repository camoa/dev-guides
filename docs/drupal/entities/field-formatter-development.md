---
description: Custom display formatters for field values in view modes
drupal_version: "11.x"
---

# Field Formatter Development

## When to Use

When creating custom display output for field values in view modes, requiring specialized rendering beyond core label/plain text formatters.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Simple output | Extend FormatterBase | Render field values in view modes |
| Linked output | Build render arrays with #type => link | Leverage render system for access control |
| Complex markup | Use #theme render arrays | Proper caching and preprocessing |
| External resources | Add #attached libraries | Load CSS/JS only when formatter used |

## Pattern

Custom formatter with PHP 8 attributes:

```php
namespace Drupal\my_module\Plugin\Field\FieldFormatter;

use Drupal\Core\Field\Attribute\FieldFormatter;
use Drupal\Core\Field\FieldItemListInterface;
use Drupal\Core\Field\FormatterBase;

#[FieldFormatter(
  id: "geolocation_map",
  label: new TranslatableMarkup("Map"),
  field_types: ["geolocation"],
)]
class GeolocationMapFormatter extends FormatterBase {

  public function viewElements(FieldItemListInterface $items, $langcode) {
    $elements = [];

    foreach ($items as $delta => $item) {
      $elements[$delta] = [
        '#theme' => 'geolocation_map',
        '#lat' => $item->lat,
        '#lng' => $item->lng,
        '#attached' => [
          'library' => ['my_module/geolocation-map'],
        ],
      ];
    }

    return $elements;
  }
}
```

Template (`templates/geolocation-map.html.twig`):
```twig
<div class="geolocation-map" data-lat="{{ lat }}" data-lng="{{ lng }}">
  {{ lat }}, {{ lng }}
</div>
```

Place in `src/Plugin/Field/FieldFormatter/GeolocationMapFormatter.php`

Reference: `/core/modules/image/src/Plugin/Field/FieldFormatter/ImageFormatter.php`

## Common Mistakes

- **Wrong**: Outputting raw HTML strings → **Right**: Use render arrays for proper caching and security
- **Wrong**: Not sanitizing output → **Right**: ALWAYS use render arrays or Xss::filter() / Html::escape()
- **Wrong**: Missing #attached libraries → **Right**: JavaScript/CSS won't load; use #attached, not drupal_add_library()
- **Wrong**: Forgetting field_types → **Right**: Formatter won't appear as option
- **Wrong**: Loading entities without access checks → **Right**: Use entity access API or build arrays from data only
- **Wrong**: Not implementing settingsForm() → **Right**: No formatter configuration in Field UI

**Security**:
- NEVER output raw user input. Use render arrays with #plain_text or #markup (filtered).
- Check entity access before rendering referenced entities.
- Sanitize URLs with UrlHelper::filterBadProtocol() before rendering links.

**Performance**:
- Use #cache keys/tags/contexts on render arrays for granular caching.
- Lazy load expensive resources (entity loads) only when actually rendering.
- Use #lazy_builder for personalized/uncacheable content within otherwise cacheable fields.

**Development Standards**:
- Return array of render arrays indexed by delta from viewElements()
- Use dependency injection for services (inject via create())
- Implement settingsForm(), settingsSummary(), and defaultSettings() for configurable formatters

## See Also

- [Field Widget Development](field-widget-development.md)
- [Form Display Configuration](form-display-configuration.md)
- Reference: [Field formatters overview](https://www.drupal.org/docs/drupal-apis/entity-api/fieldtypes-fieldwidgets-and-fieldformatters)
