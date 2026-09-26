---
description: "Source references and maintenance manifest for the Composer guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install
Claims here were checked against Composer and composer-patches source at the tags below, read on GitHub, and against drupal.org documentation. No Composer command was run for this version of the guide.

## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Updating Drupal core via Composer | https://www.drupal.org/docs/updating-drupal/updating-drupal-core-via-composer | 1.0, 5.0 | 2026-09-24 |
| Updating Modules and Themes using Composer | https://www.drupal.org/docs/updating-drupal/updating-modules-and-themes-using-composer | 1.0, 2.0 | 2026-09-24 |
| Composer CLI documentation | https://getcomposer.org/doc/03-cli.md | 1.0, 2.0, 4.0, 5.0 | 2026-09-24 |
| Composer config documentation | https://getcomposer.org/doc/06-config.md | 4.0 | 2026-09-24 |
| Composer Patches: Defining patches | https://docs.cweagans.net/composer-patches/usage/defining-patches/ | 3.0 | 2026-09-24 |
| Composer Patches: Recommended workflows | https://docs.cweagans.net/composer-patches/usage/recommended-workflows/ | 3.0 | 2026-09-24 |
| Composer Patches: Commands | https://docs.cweagans.net/composer-patches/usage/commands/ | 3.0 | 2026-09-24 |
| cweagans/composer-patches on Packagist | https://packagist.org/packages/cweagans/composer-patches | 3.0 | 2026-09-24 |
| Drupal core issue #3564942 | https://www.drupal.org/project/drupal/issues/3564942 | 3.0 | 2026-09-24 |
| Carlos Ospina, "From Fear to Freedom" | https://www.youtube.com/watch?v=UGfrvVQjCQw | 5.0 | 2026-09-24 |

## Code Sources

| Module | Relative Path | Guide Sections | Drupal Version |
|--------|---------------|----------------|----------------|
| Composer (`composer/composer`, tag 2.10.3) | `doc/03-cli.md`, `doc/06-config.md`, `CHANGELOG.md`, `src/Composer/Installer.php`, `src/Composer/Command/RequireCommand.php` | 1.0, 2.0, 4.0 | Composer 2.10.3 |
| composer-patches 1.x (`cweagans/composer-patches`, tag 1.7.3) | `src/Patches.php` | 3.0 | 1.7.3 |
| composer-patches 2.x (`cweagans/composer-patches`, tag 2.0.0) | `src/Plugin/Patches.php` | 3.0 | 2.0.0 |

---

**Version:** 1.0
**Last Updated:** 2026-09-24
**Drupal Version:** 10.x, 11.x
**Guide Type:** Atomic-Ready Single File
