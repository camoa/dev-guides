---
description: "Source references and maintenance manifest for the entities guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install
Path: ~/workspace/contrib/web/

## Web Sources
| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Drupal Entity API Documentation | https://www.drupal.org/docs/drupal-apis/entity-api | 1.1, 2.1, 2.2 | 2026-02-12 |
| Working with the Entity API | https://www.drupal.org/docs/drupal-apis/entity-api/working-with-the-entity-api | 1.1, 8.1, 8.2 | 2026-02-12 |
| Entity Types Documentation | https://www.drupal.org/docs/drupal-apis/entity-api/entity-types | 1.1, 7.1 | 2026-02-12 |
| Field Definitions Guide | https://www.drupal.org/docs/drupal-apis/entity-api/defining-and-using-content-entity-field-definitions | 2.4 | 2026-02-12 |
| FieldTypes, Widgets, Formatters | https://www.drupal.org/docs/drupal-apis/entity-api/fieldtypes-fieldwidgets-and-fieldformatters | 3.1, 4.1, 4.2, 4.3 | 2026-02-12 |
| Creating Custom Field Types | https://www.drupal.org/docs/creating-custom-modules/creating-custom-field-types-widgets-and-formatters | 4.1, 4.2, 4.3 | 2026-02-12 |
| Create Custom Field Type | https://www.drupal.org/docs/creating-custom-modules/creating-custom-field-types-widgets-and-formatters/create-a-custom-field-type | 4.1 | 2026-02-12 |
| Create Custom Field Widget | https://www.drupal.org/docs/creating-custom-modules/creating-custom-field-types-widgets-and-formatters/create-a-custom-field-widget | 4.2 | 2026-02-12 |
| Field Types Tutorial (Drupalize.me) | https://drupalize.me/tutorial/field-types | 4.1 | 2026-02-12 |
| Computed Field Values | https://www.drupal.org/docs/drupal-apis/entity-api/dynamicvirtual-field-values-using-computed-field-property-classes | 7.3 | 2026-02-12 |
| Creating Content Entity Type | https://www.drupal.org/docs/drupal-apis/entity-api/creating-a-content-entity-type | 2.3 | 2026-02-12 |
| Display Modes Documentation | https://www.drupal.org/docs/drupal-apis/entity-api/display-modes-view-modes-and-form-modes | 5.2, 5.3 | 2026-02-12 |
| Create Custom Entity Drupal 11 Guide | https://www.augustinfotech.com/blogs/how-to-create-custom-entity-in-drupal-11/ | 2.3 | 2026-02-12 |
| Drupal Security Practices 2025 | https://www.thedroptimes.com/50778/top-drupal-security-practices-2025-threats-tools-and-drupal-11-features | 8.3, 7.1 | 2026-02-12 |
| Drupal 11.2.6 Release | https://www.drupal.org/project/drupal/releases/11.2.6 | 7.1, 8.2 | 2026-02-12 |
| Performance Improvements Drupal 11.3 | https://www.md-systems.ch/en/blog/2025-12-16/performance-improvements-drupal-11-3 | 7.1, 8.2 | 2026-02-12 |

## Code Sources
| Module | Relative Path | Guide Sections | Drupal Version |
|--------|---------------|----------------|----------------|
| Node module | core/modules/node/ | 2.1, 2.2, 2.3, 2.4 | 11.x |
| Field module | core/modules/field/ | 3.2, 3.3, 4.1 | 11.x |
| Entity system core | core/lib/Drupal/Core/Entity/ | 1.1, 2.1, 8.1, 8.3 | 11.x |
| Field plugin base | core/lib/Drupal/Core/Field/ | 4.1, 4.2, 4.3 | 11.x |
| Link field type | core/modules/link/src/Plugin/Field/FieldType/ | 4.1 | 11.x |
| Text field widgets | core/modules/text/src/Plugin/Field/FieldWidget/ | 4.2 | 11.x |
| Image field formatter | core/modules/image/src/Plugin/Field/FieldFormatter/ | 4.3 | 11.x |
| File module | core/modules/file/ | 7.2 | 11.x |
| Image module | core/modules/image/ | 7.2 | 11.x |
| Entity query | core/lib/Drupal/Core/Entity/Query/ | 7.4, 8.2 | 11.x |
| Validation constraints | core/lib/Drupal/Core/Validation/Plugin/Validation/Constraint/ | 8.4 | 11.x |

## Version History
- 2026-07-02 - Added new `field-storage-decision` partition (Field & Storage Decision Order): the ordered, stop-at-first-match dispatch across compound / taxonomy / shared-storage / wrapper-entity / plain-reference / bundle-private core field. Extended `field-storage-configuration` with the shared-storage-by-concern discipline (concern-named not bundle-named, cardinality reconciliation to storage-level max, entity_reference handler settings on the instance not storage, cross-entity-type boundary)
- v2.0 - Complete atomic-ready reformat with security/performance best practices (2026-02-12)
- v1.0 - Initial guide (prior to 2026-02-12)
<!-- END PARTITION: sources-and-maintenance-manifest -->
