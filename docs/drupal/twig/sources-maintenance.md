## Sources & Maintenance Manifest

### Drupal Research Install
Path: `~/workspace/contrib/web/`

### Web Sources
| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Drupal Theming Guide | https://www.drupal.org/docs/develop/theming-drupal | All | 2026-02-18 |
| Twig in Drupal | https://www.drupal.org/docs/theming-drupal/twig-in-drupal | 1, 13, 14 | 2026-02-18 |
| Working with Twig Templates | https://www.drupal.org/docs/develop/theming-drupal/twig-in-drupal/working-with-twig-templates | 2, 3, 4 | 2026-02-18 |
| Twig Best Practices — Preprocess | https://www.drupal.org/docs/theming-drupal/twig-in-drupal/twig-best-practices-preprocess-functions-and-templates | 9, 10, 20, 21 | 2026-02-18 |
| Twig Coding Standards | https://www.drupal.org/docs/develop/coding-standards/twig-coding-standards | 20, 21 | 2026-02-18 |
| hook_theme() API | https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Render!theme.api.php/function/hook_theme/11.x | 11 | 2026-02-18 |
| hook_theme_suggestions_HOOK API | https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Render!theme.api.php/function/hook_theme_suggestions_HOOK/11.x | 12 | 2026-02-18 |
| hook_theme_suggestions_HOOK_alter API | https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Render!theme.api.php/function/hook_theme_suggestions_HOOK_alter/11.x | 12 | 2026-02-18 |
| Drupalize.me — Hooks | https://drupalize.me/topic/hooks | 9, 11, 12 | 2026-02-18 |
| Drupalize.me — Add Theme Hook Suggestions | https://drupalize.me/tutorial/add-new-theme-hook-suggestions | 12 | 2026-02-18 |
| Drupal at your Fingertips — Twig | https://www.drupalatyourfingertips.com/twig | 5, 13, 14 | 2026-02-18 |
| Drupal at your Fingertips — Hooks | https://www.drupalatyourfingertips.com/hooks | 9, 11 | 2026-02-18 |
| OOP hooks in themes (Drupal 11.3) | https://www.drupal.org/node/3551652 | 9 | 2026-02-18 |
| Preprocess OOP hooks (Drupal 11.2) | https://www.drupal.org/node/3496491 | 9 | 2026-02-18 |
| Accessing raw field values (Drupal issue) | https://www.drupal.org/project/drupal/issues/3314476 | 5 | 2026-02-18 |
| Writing Secure Code for Drupal | https://www.drupal.org/docs/administering-a-drupal-site/security-in-drupal/writing-secure-code-for-drupal | 22 | 2026-02-18 |
| Twig Field Value module | https://www.drupal.org/project/twig_field_value | 5 | 2026-02-18 |
| OWASP XSS | https://owasp.org/www-community/attacks/xss/ | 22 | 2026-02-18 |

### Code Sources
| Module | Relative Path | Guide Sections | Drupal Version |
|--------|---------------|----------------|----------------|
| Twig Template Engine | `core/lib/Drupal/Core/Template/` | 1, 8, 13, 14, 22 | 11.x |
| Theme System | `core/lib/Drupal/Core/Theme/` | 1, 2, 3, 4, 9, 11, 12 | 11.x |
| Theme Render API | `core/lib/Drupal/Core/Render/theme.api.php` | 11, 12 | 11.x |
| Theme system includes | `core/includes/theme.inc` | 9 | 11.x |
| Node module templates | `core/modules/node/templates/` | 3, 4, 5 | 11.x |
| Node theme hooks | `core/modules/node/src/Hook/NodeThemeHooks.php` | 4, 9, 12 | 11.x |
| System module templates | `core/modules/system/templates/` | 3, 4, 8 | 11.x |
| Block module templates | `core/modules/block/templates/` | 4 | 11.x |
| Views module templates | `core/modules/views/templates/` | 4 | 11.x |
| Twig Tweak | `modules/contrib/twig_tweak/` | 15 | 3.x |
