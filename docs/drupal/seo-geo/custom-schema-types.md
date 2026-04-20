---
description: Create custom Schema Metatag plugins for Schema.org types not included in the 25 built-in types — attribute-based plugin system, LocalBusiness example
tldr: "Schema Metatag ships with 25 top-level Schema.org types. When your content needs a type not in that list — LocalBusiness, MedicalEntity, LegalService, EducationalOrganization, SportsTeam — you create a custom plugin."
drupal_version: "11.x"
---

# Custom Schema Types

## When to Use

> Schema Metatag ships with 25 top-level Schema.org types. When your content needs a type not in that list — LocalBusiness, MedicalEntity, LegalService, EducationalOrganization, SportsTeam — you create a custom plugin. Since Schema Metatag 2.2.0, plugins use PHP 8 attributes instead of annotation arrays, making them significantly simpler to write.

## Decision

| Situation | Choice | Why |
|-----------|--------|-----|
| Needed type is in the 25 built-in types | Use existing submodule | No custom code; simpler maintenance |
| Needed type is close to a built-in (e.g., NewsArticle extends Article) | Extend the existing plugin | Inherits all parent properties |
| Completely missing type (LocalBusiness, MedicalEntity) | Create custom plugin | Full control over properties |
| Type needed in one project only | Custom plugin in custom module | Keep contrib clean |
| Type useful across many projects | Consider contrib issue/patch | Share with community |
| Schema.org Blueprints is in use | drush schemadotorg:create-type | No custom PHP needed |

### Built-in Types to Extend vs Start Fresh

| Schema.org type | Built-in parent | Approach |
|----------------|----------------|---------|
| NewsArticle | Article | schema_article covers it; use @type token |
| BlogPosting | Article | schema_article covers it; use @type token |
| LocalBusiness | Organization | Extend organization plugin |
| FoodEstablishment | LocalBusiness | New plugin extending LocalBusiness |
| MedicalOrganization | Organization | New plugin |
| GovernmentOrganization | Organization | New plugin |
| EducationalOrganization | Organization | New plugin |

## Pattern

### Plugin Structure (Attribute-based, Schema Metatag 2.2.0+)

File: `modules/custom/my_module/src/Plugin/metatag/Tag/SchemaLocalBusiness.php`

```php
<?php

namespace Drupal\my_module\Plugin\metatag\Tag;

use Drupal\schema_metatag\Plugin\metatag\Tag\SchemaOrganizationBase;
use Drupal\schema_metatag\SchemaMetatagManager;

/**
 * Provides a plugin for LocalBusiness schema type.
 */
#[\Drupal\schema_metatag\Attribute\SchemaType(
  id: 'schema_local_business',
  label: new \Drupal\Core\StringTranslation\TranslatableMarkup('Schema.org: LocalBusiness'),
  description: new \Drupal\Core\StringTranslation\TranslatableMarkup('A locally-based business, including restaurants, stores, and services.'),
  group: 'schema_local_business',
  weight: 10,
  type: 'LocalBusiness',
  multiple: FALSE,
)]
class SchemaLocalBusiness extends SchemaOrganizationBase {

  /**
   * {@inheritdoc}
   */
  public static function defaultInputValues(): array {
    $items = parent::defaultInputValues();

    // Add LocalBusiness-specific properties
    $items['telephone'] = '';
    $items['priceRange'] = '';
    $items['address'] = [
      '@type' => 'PostalAddress',
      'streetAddress' => '',
      'addressLocality' => '',
      'addressRegion' => '',
      'postalCode' => '',
      'addressCountry' => '',
    ];
    $items['openingHours'] = '';
    $items['geo'] = [
      '@type' => 'GeoCoordinates',
      'latitude' => '',
      'longitude' => '',
    ];

    return $items;
  }

}
```

### Group Definition

Define the metatag group that holds this type. Create `modules/custom/my_module/src/Plugin/metatag/Group/SchemaLocalBusiness.php`:

```php
<?php

namespace Drupal\my_module\Plugin\metatag\Group;

use Drupal\metatag\Plugin\metatag\Group\GroupBase;

/**
 * Provides a metatag group for LocalBusiness schema.
 */
#[\Drupal\metatag\Attribute\MetatagGroup(
  id: 'schema_local_business',
  label: new \Drupal\Core\StringTranslation\TranslatableMarkup('Schema.org: LocalBusiness'),
  description: new \Drupal\Core\StringTranslation\TranslatableMarkup('Schema.org type for local businesses.'),
  weight: 20,
)]
class SchemaLocalBusiness extends GroupBase {}
```

### Token Mapping in Admin UI

After enabling the module (`drush en my_module && drush cr`), configure in the Metatag admin UI at `/admin/config/search/metatag`. The LocalBusiness tab will appear in the Schema.org section:

```
@type:                   LocalBusiness
name:                    [node:title]
telephone:               [node:field_phone]
priceRange:              [node:field_price_range]
address > streetAddress: [node:field_address:address_line1]
address > addressLocality: [node:field_address:locality]
address > addressRegion: [node:field_address:administrative_area]
address > postalCode:    [node:field_address:postal_code]
address > addressCountry: [node:field_address:country_code]
geo > latitude:          [node:field_geolocation:lat]
geo > longitude:         [node:field_geolocation:lng]
openingHours:            Mo-Fr 09:00-17:00
url:                     [node:url:absolute]
```

### Extending Without a Full Plugin

For minor additions to an existing type (e.g., adding one property to Article), use `hook_metatag_tags_alter()`:

```php
/**
 * Implements hook_metatag_tags_alter().
 */
function my_module_metatag_tags_alter(array &$definitions): void {
  // Add a custom property to the existing Article schema plugin
  if (isset($definitions['schema_article'])) {
    // Not the recommended approach for structural changes
    // Use a full custom plugin for significant additions
  }
}
```

## Common Mistakes

- **Wrong**: Using annotation arrays (`@SchemaMetatag(...)`) syntax from Schema Metatag < 2.2.0 → **Right**: Use PHP 8 attributes (`#[SchemaType(...)]`) for any new plugin; annotations are deprecated
- **Wrong**: Creating a custom plugin for a type that's really just a subtype of an existing one → **Right**: For Article subtypes (NewsArticle, BlogPosting), just set the `@type` token value on the built-in schema_article plugin; no custom plugin needed
- **Wrong**: Forgetting to define the Group plugin alongside the Tag plugin → **Right**: Both Tag and Group plugins are required for the admin UI tab to appear correctly
- **Wrong**: Not clearing caches after enabling the custom module → **Right**: Run `drush cr` after any plugin file changes; Drupal caches plugin discovery
- **Wrong**: Hardcoding address values in the plugin class → **Right**: Use the defaultInputValues() method to set empty defaults; populate via tokens in the admin UI
- **Wrong**: Skipping the Rich Results Test after implementing a custom type → **Right**: Google's validator will catch property name errors and missing required fields that PHP does not

## See Also

- [Schema Metatag Setup](schema-metatag-setup.md)
- [Schema Types Reference](schema-types-reference.md)
- [Testing & Validation](testing-validation.md)
- Reference: [Schema Metatag source on git.drupalcode.org](https://git.drupalcode.org/project/schema_metatag)
- Reference: [Schema Metatag plugin examples in contrib](https://git.drupalcode.org/project/schema_metatag/-/tree/3.x/modules)
- Reference: [Schema.org type hierarchy](https://schema.org/docs/full.html)
