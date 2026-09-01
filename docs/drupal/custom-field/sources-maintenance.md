---
description: "Source references and maintenance manifest for the custom field guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install
Path: `/home/camoa/workspace/contrib/web/`

## Web Sources
| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Custom Field project page | https://www.drupal.org/project/custom_field | 1.1, 1.2 | 2026-08-16 |
| Custom Field documentation | https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/custom-field | 1.1, 2.1 | 2026-08-16 |
| Field types, widgets & formatters | https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/custom-field/field-types-widgets-formatters | 3.1-3.6, 4.1, 5.1 | 2026-08-16 |
| Entity Query custom fields | https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/custom-field/entity-query-custom-fields | 12.1 | 2026-08-16 |
| Add/remove columns with existing data | https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/custom-field/addremove-columns-to-custom-fields-with-existing-data | 2.2 | 2026-08-16 |
| Extending Custom Field formatter plugins | https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/custom-field/extending-custom-field-formatter-plugins | 15.1 | 2026-08-16 |
| Custom fields vs Paragraphs discussion | https://www.drupal.org/forum/support/post-installation/2018-05-22/difference-between-custom-compound-fields-and-paragraphs | 1.1 | 2026-08-16 |
| Compound fields article | https://theaccidentalcoder.com/compound-fields | 1.1, 2.1 | 2026-08-16 |
| OWASP Top Ten | https://owasp.org/www-project-top-ten/ | 17.1 | 2026-08-16 |
| Drupal secure coding practices | https://www.drupal.org/security/secure-coding-practices | 17.1, 18.1 | 2026-08-16 |
| Drupal coding standards | https://www.drupal.org/docs/develop/standards | 18.1 | 2026-08-16 |
| PHP-FIG PSR-12 | https://www.php-fig.org/psr/psr-12/ | 18.1 | 2026-08-16 |
| GraphQL Compose project | https://www.drupal.org/project/graphql_compose | 14.1 | 2026-08-16 |
| Feeds module project | https://www.drupal.org/project/feeds | 16.1 | 2026-08-16 |
| Custom Field shipped documentation (`docs/` + `mkdocs.yml` in the 5.0.2 release; built from the project's GitLab repository — `mkdocs.yml` declares no `site_url`, so no public address is cited here) | — | 3.1-3.6, 4.1, 5.1, 6.1, 7.1, 15.1 | 2026-08-16 |

Note on the drupal.org handbook pages above: all still resolve with content, but 5.0.0 describes documentation as migrated to the project's own docs system, so treat them as live-but-secondary.

## Code Sources
| Module | Relative Path | Guide Sections | Drupal Version |
|--------|---------------|----------------|----------------|
| Custom Field | modules/contrib/custom_field/ | All sections | 11.4 (5.0.2) |
| Custom Field AI | modules/contrib/custom_field/modules/custom_field_ai/ | 14.1 | 11.4 (5.0.2) |
| Custom Field Entity Browser | modules/contrib/custom_field/modules/custom_field_entity_browser/ | 14.1 | 11.4 (5.0.2) |
| Custom Field GraphQL | modules/contrib/custom_field/modules/custom_field_graphql/ | 14.1 | 11.4 (5.0.2) |
| Custom Field JSON:API | modules/contrib/custom_field/modules/custom_field_jsonapi/ | 14.1 | 11.4 (5.0.2) |
| Custom Field Linkit | modules/contrib/custom_field/modules/custom_field_linkit/ | 11.1, 14.1 | 11.4 (5.0.2) |
| Custom Field Media | modules/contrib/custom_field/modules/custom_field_media/ | 9.1, 14.1 | 11.4 (5.0.2) |
| Custom Field Search API | modules/contrib/custom_field/modules/custom_field_search_api/ | 14.1 | 11.4 (5.0.2) |
| Custom Field SDC | modules/contrib/custom_field/modules/custom_field_sdc/ | 7.1, 14.1, 15.1 | 11.4 (5.0.2) |
| Custom Field Viewfield | modules/contrib/custom_field/modules/custom_field_viewfield/ | 14.1 | 11.4 (5.0.2) |
