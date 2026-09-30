---
description: "Source references and maintenance manifest for the taxonomy guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install

Claims here were checked against a local Drupal install of core and the modules named below, rather than quoted from documentation.
## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Drupal.org User Guide: Taxonomy | https://www.drupal.org/docs/user_guide/en/structure-taxonomy.html | 1.1 | 2026-02-14 |
| Drupal.org Taxonomy About | https://www.drupal.org/docs/7/organizing-content-with-taxonomies/about-taxonomies | 1.1, 5.1 | 2026-02-14 |
| Evolvingweb: How to Organize Content With Taxonomies | https://evolvingweb.com/blog/how-organize-your-drupal-content-taxonomies | 5.1, 13.1 | 2026-02-14 |
| ImageX Media: Taxonomy Overview | https://imagexmedia.com/blog/drupal-organizing-content-with-taxonomy | 1.1 | 2026-02-14 |
| Enterprise Knowledge: Taxonomy Design | https://enterprise-knowledge.com/taxonomy-design-for-drupal/ | 13.1 | 2026-02-14 |
| Drupal.org Configuration Management | https://www.drupal.org/docs/administering-a-drupal-site/configuration-management/managing-your-sites-configuration | 3.1 | 2026-02-14 |
| Drupal.org Content as Configuration | https://www.drupal.org/project/content_as_config | 12.1 | 2026-02-14 |
| Drupal.org Permissions by Term | https://www.drupal.org/project/permissions_by_term | 8.1, 15.1 | 2026-02-14 |
| Seth Shaw: Large Vocab loadTree Error | https://seth-shaw-unlv.github.io/2020-09-07/large_vocab_list_error | 9.1, 15.2 | 2026-02-14 |
| Drupal.org Issue: DB caching for loadTree | https://www.drupal.org/project/drupal/issues/106015 | 15.2 | 2026-02-14 |
| Wishdesk: Architectural Patterns for Complex Taxonomies | https://wishdesk.com/blog/7-game-changing-architectural-patterns-that-scale-complex-drupal-taxonomies-without-killing-performance | 14.1, 15.2 | 2026-02-14 |
| Drupal Recipes Initiative: Default Content | https://project.pages.drupalcode.org/distributions_recipes/default_content.html | 12.1 | 2026-09-30 |
| Drupal.org issue 3479980: Taxonomy fallback display without Views | https://www.drupal.org/project/drupal/issues/3479980 | 12.1 | 2026-09-30 |

## Code Sources

| Module | Relative Path | Guide Sections | Drupal Version |
|--------|---------------|----------------|----------------|
| Taxonomy module | `core/modules/taxonomy/` | All sections | 11.x |
| Taxonomy config schema | `core/modules/taxonomy/config/schema/` | 2.1 | 11.x |
| Tags taxonomy recipe | `core/recipes/tags_taxonomy/` | 3.1, 12.1, 16.1 | 11.4.5 |
| Article tags recipe | `core/recipes/article_tags/` | 4.1, 11.1, 12.1, 16.1 | 11.x |
| Core Recipe API | `core/lib/Drupal/Core/Recipe/` | 12.1 | 11.4.5 |
| Core DefaultContent API | `core/lib/Drupal/Core/DefaultContent/` | 12.1 | 11.4.5 |
| Path module (DefaultContent subscriber) | `core/modules/path/` | 12.1 | 11.4.5 |
| Config StorageComparer | `core/lib/Drupal/Core/Config/StorageComparer.php` | 12.1 | 11.4.5 |
| Basic shortcuts recipe | `core/recipes/basic_shortcuts/` | 12.1 | 11.4.5 |

## Maintenance Notes

- Vocabulary config schema is stable across Drupal 9-11; minimal changes expected
- Term entity added revision support in Drupal 8.7; `new_revision` property added to vocabulary config
- Views plugins use PHP 8 attributes as of Drupal 10; older documentation shows annotations
- Recipe format introduced in Drupal 10.3; examples here are Drupal 11 format
- Recipes import a `content/` folder from Drupal 10.3. The `content:export` command shipped in Drupal 11.3; on 11.2 and earlier, export the content with the contrib Default Content module
- `loadTree()` performance issues documented since Drupal 7; still relevant in Drupal 11

## Version History

| Date | Change |
|------|--------|
| 2026-02-14 | Initial guide creation — Drupal 11.x, comprehensive config-first approach |
| 2026-09-30 | Corrected "Include default terms": core recipes ship terms via `content/`, not contrib-only (verified against core 11.4.5) |
