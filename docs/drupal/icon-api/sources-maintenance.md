---
description: "Source references and maintenance manifest for the icon api guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install
Path: `~/workspace/contrib/web/`

## Web Sources
| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Icon API Documentation | https://www.drupal.org/docs/develop/drupal-apis/icon-api | 1.1, 1.2, 2.1, 3.1, 3.2, 3.3, 3.4 | 2026-08-18 (superseded by source where they disagree) |
| Icon API Change Record | https://www.drupal.org/node/3490350 | 1.1 | 2026-02-12 |
| UI Icons Module | https://www.drupal.org/project/ui_icons | 3.5, 3.6 | 2026-08-18 (2.0.0 current) |
| UI Icons Documentation | https://project.pages.drupalcode.org/ui_icons/ | 3.6 | 2026-02-13 |
| UI Icons Font Extractor Issue | https://www.drupal.org/project/ui_icons/issues/3466316 | 3.5 | 2026-02-13 |
| Iconify Icons Module | https://www.drupal.org/project/iconify_icons | 1.1, 3.1 | 2026-02-12 |
| Icon API Issue (added `icon()`, commit ed6e929) | https://www.drupal.org/project/drupal/issues/3471494 | 1.1, 5.1 | 2026-08-18 |
| OWASP SVG Security Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/SVG_Security_Cheat_Sheet.html | 10.1 | 2026-02-12 |
| Subresource Integrity (MDN) | https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity | 10.2 | 2026-02-12 |
| Drupal Cache API | https://www.drupal.org/docs/drupal-apis/cache-api/cache-api | 8.1 | 2026-02-12 |
| SDC Documentation | https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components | 7.1, 7.2 | 2026-02-12 |
| Twig Debugging | https://www.drupal.org/docs/theming-drupal/twig-in-drupal/debugging-twig-templates | 11.2 | 2026-02-12 |
| Plugin API | https://www.drupal.org/docs/drupal-apis/plugin-api | 12.1 | 2026-02-12 |

## Code Sources
| Module | Relative Path | Guide Sections | Verified Against |
|--------|---------------|----------------|------------------|
| Icon API Core | core/lib/Drupal/Core/Theme/Icon/ | 1.1, 1.2, 2.1, 8.2 | 11.3.11 |
| IconPackManager | core/lib/Drupal/Core/Theme/Icon/Plugin/IconPackManager.php | 1.2, 2.1, 8.2, 11.1 | 11.3.11 |
| IconsTwigExtension (`icon()`) | core/lib/Drupal/Core/Template/IconsTwigExtension.php | 5.1 | 11.3.11 (signature unchanged since 11.1.0) |
| Icon render element | core/lib/Drupal/Core/Render/Element/Icon.php | 4.1, 6.1, 8.1 | 11.3.11 |
| IconFinder | core/lib/Drupal/Core/Theme/Icon/IconFinder.php | 3.1, 3.2, 3.4, 10.2 | 11.3.11 |
| IconCollector | core/lib/Drupal/Core/Theme/Icon/IconCollector.php | 8.1 | 11.3.11 |
| SvgExtractor | core/lib/Drupal/Core/Theme/Plugin/IconExtractor/SvgExtractor.php | 3.2, 10.1 | 11.3.11 |
| SvgSpriteExtractor | core/lib/Drupal/Core/Theme/Plugin/IconExtractor/SvgSpriteExtractor.php | 3.3 | 11.3.11 |
| PathExtractor | core/lib/Drupal/Core/Theme/Plugin/IconExtractor/PathExtractor.php | 3.4 | 11.3.11 |
| IconDefinition | core/lib/Drupal/Core/Theme/Icon/IconDefinition.php | 4.1, 8.2 | 11.3.11 |
| IconExtractorInterface / Base / WithFinder | core/lib/Drupal/Core/Theme/Icon/ | 3.1, 12.1 | 11.3.11 |
| IconExtractorSettingsForm | core/lib/Drupal/Core/Theme/Icon/IconExtractorSettingsForm.php | 2.1, 4.1 | 11.3.11 |
| Icon pack schema | core/assets/schemas/v1/icon_pack.schema.json | 2.1 | 11.3.11 |
| SDC component schema | core/assets/schemas/v1/metadata.schema.json | 7.1 | 11.3.11 |
| ComponentsTwigExtension / ComponentNodeVisitor | core/lib/Drupal/Core/Template/ | 7.1, 7.2 | 11.3.11 |
| IconFinderTest (remote-URL behaviour) | core/tests/Drupal/Tests/Core/Theme/Icon/IconFinderTest.php | 3.1, 3.3, 10.2 | 11.3.11 |
| UI Icons (font extractor, field, submodules) | modules/contrib/ui_icons/ | 3.5, 3.6 | 1.1.2 installed; 2.0.0 current |

---
