---
description: "Source references and maintenance manifest for the storybook guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install

Claims here were checked against a local Drupal install of core and the modules named below, rather than quoted from documentation.
## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| drupal/storybook module | https://www.drupal.org/project/storybook | storybook-landscape, drupal-storybook-module | 2026-02-20 |
| twig-storybook library (e0ipso) | https://github.com/e0ipso/twig-storybook | drupal-storybook-module | 2026-02-20 |
| Lullabot — New Storybook module for Drupal | https://www.lullabot.com/articles/new-storybook-module-drupal | drupal-storybook-module | 2026-02-20 |
| storybook-addon-sdc (iberdinsky-skilld) | https://github.com/iberdinsky-skilld/sdc-addon | addon-sdc-offline | 2026-02-20 |
| UI Patterns 2 stories docs | https://project.pages.drupalcode.org/ui_patterns/2-authors/1-stories-and-library/ | story-yml-format | 2026-02-20 |
| tyler36/ddev-storybook addon | https://github.com/tyler36/ddev-storybook | ddev-storybook-setup | 2026-02-20 |
| DDEV custom port exposure | https://ddev.readthedocs.io/en/stable/users/extend/custom-ports/ | ddev-storybook-setup | 2026-02-20 |
| Storybook.js argTypes API | https://storybook.js.org/docs/api/arg-types | drupal-storybook-module | 2026-02-20 |
| UI Suite DaisyUI project | https://www.drupal.org/project/ui_suite_daisyui | storybook-landscape, story-yml-format, subtheme-stories | 2026-02-20 |

## Code Sources

| Module/Theme | Relative Path | Guide Sections | Version |
|---|---|---|---|
| UI Suite DaisyUI theme | `themes/contrib/ui_suite_daisyui/components/` | story-yml-format, subtheme-stories | 5.0.x |
| UI Suite DaisyUI starterkit | `themes/contrib/ui_suite_daisyui/starterkits/ui_suite_daisyui_starterkit/components/` | subtheme-stories | 5.0.x |
| UI Patterns library — StoriesSyntaxConverter | `modules/contrib/ui_patterns/modules/ui_patterns_library/src/StoriesSyntaxConverter.php` | story-yml-format | 2.x |
| UI Patterns library — StoryPluginManager | `modules/contrib/ui_patterns/modules/ui_patterns_library/src/StoryPluginManager.php` | story-yml-format | 2.x |
| UI Patterns library — DirectoryWithMetadataDiscovery | `modules/contrib/ui_patterns/modules/ui_patterns_library/src/Discovery/DirectoryWithMetadataDiscovery.php` | story-yml-format | 2.x |
| UI Patterns library — ComponentElementAlter (library) | `modules/contrib/ui_patterns/modules/ui_patterns_library/src/Element/ComponentElementAlter.php` | story-yml-format | 2.x |
| UI Patterns library — TwigExtension | `modules/contrib/ui_patterns/modules/ui_patterns_library/src/Template/TwigExtension.php` | story-yml-format | 2.x |
| UI Patterns library — StoriesSyntaxConversionTest | `modules/contrib/ui_patterns/modules/ui_patterns_library/tests/src/Unit/StoriesSyntaxConversionTest.php` | story-yml-format | 2.x |
| UI Patterns library — story format docs | `modules/contrib/ui_patterns/docs/2-authors/1-stories-and-library.md` | story-yml-format | 2.x |
| UI Icons Patterns — icon story test | `modules/contrib/ui_icons/modules/ui_icons_patterns/tests/modules/ui_icons_patterns_test/components/icon_test/icon_test.component.story.yml` | story-yml-format | 1.x |
