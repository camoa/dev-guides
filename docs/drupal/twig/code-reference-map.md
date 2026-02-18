---
topic: drupal/twig
guide: code-reference-map
---

## Code Reference Map

### Core Template Engine
| File | Purpose |
|---|---|
| `core/lib/Drupal/Core/Template/TwigExtension.php` | All Drupal Twig functions and filters |
| `core/lib/Drupal/Core/Template/TwigEnvironment.php` | Twig environment setup, sandbox configuration |
| `core/lib/Drupal/Core/Template/Attribute.php` | Attribute class — `addClass()`, `setAttribute()`, etc. |
| `core/lib/Drupal/Core/Template/TwigSandboxPolicy.php` | Allowed methods/prefixes/classes in sandbox |
| `core/lib/Drupal/Core/Template/DebugExtension.php` | Debug functions and template path comments |
| `core/lib/Drupal/Core/Template/TwigNodeTrans.php` | `{% trans %}` tag implementation |
| `core/lib/Drupal/Core/Template/ComponentsTwigExtension.php` | SDC Twig functions |
| `core/lib/Drupal/Core/Template/TwigThemeEngine.php` | Template rendering engine |

### Theme System
| File | Purpose |
|---|---|
| `core/lib/Drupal/Core/Theme/ThemeManager.php` | Template rendering, preprocess calling, default variables |
| `core/lib/Drupal/Core/Theme/Registry.php` | Theme hook registry, template discovery |
| `core/lib/Drupal/Core/Theme/ThemePreprocess.php` | OOP implementations: `preprocessHtml()`, `preprocessPage()`, `preprocessRegion()` |
| `core/includes/theme.inc` | Legacy procedural preprocess functions (deprecated in 11.2) |
| `core/lib/Drupal/Core/Render/theme.api.php` | `hook_theme()`, `hook_theme_suggestions_HOOK()` documentation |

### Core Templates
| Path | Templates |
|---|---|
| `core/modules/system/templates/` | `html.html.twig`, `page.html.twig`, `region.html.twig`, `field.html.twig`, `block.html.twig` |
| `core/modules/node/templates/` | `node.html.twig` and field variants |
| `core/modules/node/src/Hook/NodeThemeHooks.php` | `preprocessNode()`, `themeSuggestionsNode()` |
| `core/modules/views/templates/` | `views-view.html.twig` and display format templates |
| `core/themes/stark/templates/` | Minimal reference templates |
| `core/themes/claro/templates/` | Modern admin theme patterns |

### Contrib Modules
| Path | Purpose |
|---|---|
| `modules/contrib/twig_tweak/src/TwigTweakExtension.php` | All twig_tweak functions and filters |

### Drupal API Reference
| Topic | URL |
|---|---|
| `hook_theme()` | `https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Render!theme.api.php/function/hook_theme/11.x` |
| `hook_theme_suggestions_HOOK()` | `https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Render!theme.api.php/function/hook_theme_suggestions_HOOK/11.x` |
| `hook_theme_suggestions_HOOK_alter()` | `https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Render!theme.api.php/function/hook_theme_suggestions_HOOK_alter/11.x` |
| Theming Drupal Guide | `https://www.drupal.org/docs/develop/theming-drupal` |
| Twig in Drupal | `https://www.drupal.org/docs/theming-drupal/twig-in-drupal` |
| Twig at your Fingertips | `https://www.drupalatyourfingertips.com/twig` |
