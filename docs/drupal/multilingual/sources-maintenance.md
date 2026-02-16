---
description: Drupal multilingual guide sources and maintenance manifest — web sources, code sources, version history
---

# Sources & Maintenance Manifest

### Drupal Research Install
Path: `/home/camoa/workspace/contrib/web/`

### Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Drupal Multilingual Guide | https://www.drupal.org/docs/administering-a-drupal-site/multilingual-guide | 1.1, 2.1, 6.1 | 2026-02-16 |
| Drupal Multilingual Guide: Choosing Modules | https://www.drupal.org/docs/administering-a-drupal-site/multilingual-guide/choosing-and-installing-multilingual-modules | 2.1 | 2026-02-16 |
| Drupal Multilingual Guide: Translating Interfaces | https://www.drupal.org/docs/administering-a-drupal-site/multilingual-guide/translating-site-interfaces | 9.1 | 2026-02-16 |
| Drupalize.me: Content Translation Config | https://drupalize.me/tutorial/user-guide/language-content-config | 4.1 | 2026-02-16 |
| Pantheon: Drupal Multilingual Best Practices | https://pantheon.io/learning-center/drupal/multilingual | 3.1, 13.1, 18.1 | 2026-02-16 |
| Drupal Translation API Overview | https://www.drupal.org/docs/8/api/translation-api/overview | 10.1, 12.1, 19.1 | 2026-02-16 |
| Drupalize.me: t() Function Standards | https://drupalize.me/tutorial/drupal-code-standards-t-function | 10.1, 19.1 | 2026-02-16 |
| Drupal String Context | https://www.drupal.org/docs/7/api/localization-api/string-context | 10.1 | 2026-02-16 |
| Drupal Twig Translation Filters | https://www.drupal.org/docs/develop/theming-drupal/twig-in-drupal/filters-modifying-variables-in-twig-templates | 12.1 | 2026-02-16 |
| Drupal trans Tag Support | https://www.drupal.org/node/2047135 | 12.1 | 2026-02-16 |
| Drupal trans Tag: Render Arrays | https://www.drupal.org/node/2615198 | 12.1 | 2026-02-16 |
| Specbee: Multilingual SEO & Hreflang | https://www.specbee.com/blogs/multilingual-seo-and-hreflang-how-drupal-makes-it-easier | 13.1 | 2026-02-16 |
| Drupal Cache Contexts | https://www.drupal.org/docs/develop/drupal-apis/cache-api/cache-contexts | 20.1 | 2026-02-16 |
| Medium: Cache Contexts in Drupal | https://medium.com/@ovanes.b/cache-contexts-in-drupal-caching-system-9a8df4bffed0 | 20.1 | 2026-02-16 |
| Drupal Config Translation | https://www.drupal.org/docs/administering-a-drupal-site/multilingual-guide/translating-configuration | 8.1 | 2026-02-16 |
| TMGMT Module | https://www.drupal.org/project/tmgmt | 15.1 | 2026-02-16 |
| TMGMT Documentation | https://www.drupal.org/docs/contributed-modules/translation-management-tool | 15.1 | 2026-02-16 |
| Vardot: TMGMT Workflow | https://www.vardot.com/en-us/ideas/blog/simplify-translation-workflow-management-drupal-sites | 15.1 | 2026-02-16 |
| Drupal API: LanguageNegotiatorInterface | https://api.drupal.org/api/drupal/core!modules!language!src!LanguageNegotiatorInterface.php/interface/LanguageNegotiatorInterface/11.x | 3.1 | 2026-02-16 |
| Drupal API: LanguagesCacheContext | https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Cache!Context!LanguagesCacheContext.php/class/LanguagesCacheContext/11.x | 20.1 | 2026-02-16 |
| Drupal API: TranslatableMarkup | https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21StringTranslation%21TranslatableMarkup.php/class/TranslatableMarkup/10 | 10.1 | 2026-02-16 |
| Drupal API: TwigNodeTrans | https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Template!TwigNodeTrans.php/class/TwigNodeTrans/11.x | 12.1 | 2026-02-16 |
| Drupal API: Internationalization | https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Language!language.api.php/group/i18n/11.x | 21.1 | 2026-02-16 |
| Drupal Issue: content_translation.admin.inc Deprecation | https://www.drupal.org/project/drupal/issues/3560560 | 17.1 | 2026-02-16 |
| Drupal Issue: Entity Query Multilingual | https://www.drupal.org/project/drupal/issues/3092835 | 14.1 | 2026-02-16 |
| Drupal Issue: Views Relationships Langcode | https://www.drupal.org/project/drupal/issues/2737619 | 14.1 | 2026-02-16 |
| Drupal Issue: notExists with Translations | https://www.drupal.org/project/drupal/issues/2933202 | 14.1 | 2026-02-16 |
| Drupal Issue: latestRevision Language Awareness | https://www.drupal.org/project/drupal/issues/3088341 | 7.1, 14.1 | 2026-02-16 |
| Localize.drupal.org | https://localize.drupal.org | 9.1 | 2026-02-16 |

### Code Sources

| Module | Relative Path | Guide Sections | Drupal Version |
|--------|---------------|----------------|----------------|
| Language module | core/modules/language/ | 1.1, 2.1, 3.1, 21.1 | 11.x |
| Locale module | core/modules/locale/ | 1.1, 9.1, 16.1, 21.1 | 11.x |
| Content Translation module | core/modules/content_translation/ | 1.1, 4.1, 5.1, 6.1, 7.1, 11.1, 17.1, 21.1 | 11.x |
| Config Translation module | core/modules/config_translation/ | 1.1, 8.1, 21.1 | 11.x |
| Core Entity API | core/lib/Drupal/Core/Entity/ | 11.1, 21.1 | 11.x |
| Core StringTranslation | core/lib/Drupal/Core/StringTranslation/ | 10.1, 16.1, 21.1 | 11.x |
| Core Template (Twig) | core/lib/Drupal/Core/Template/ | 12.1, 21.1 | 11.x |
| Core Cache API | core/lib/Drupal/Core/Cache/ | 20.1, 21.1 | 11.x |
| TMGMT module | modules/contrib/tmgmt/ | 15.1, 21.1 | 6.x |

---

## Version History

**1.0** (2026-02-16): Initial release
- 22 atomic sections covering complete multilingual system
- Drupal 11.x compatibility verified
- Includes deprecation notice for content_translation.admin.inc (11.4.0)
- Research-backed best practices from 2024-2026 sources
- Code examples from Drupal 11.x core
