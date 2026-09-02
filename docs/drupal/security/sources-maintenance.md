---
description: "Source references and maintenance manifest for the security guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install
Claims here were checked against a local Drupal install of core and the modules named below, rather than quoted from documentation.
## Web Sources
| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Drupal Security Docs | https://www.drupal.org/docs/develop/security | 1, 19 | 2026-02-14 |
| Writing Secure Code Guide | https://www.drupal.org/docs/administering-a-drupal-site/security-in-drupal/writing-secure-code-for-drupal | 3, 9, 13, 19 | 2026-02-14 |
| OWASP Top 10 2021 | https://owasp.org/www-project-top-ten/ | 2 | 2026-02-14 |
| Drupal Security Best Practices 2025 | https://www.thedroptimes.com/50778/top-drupal-security-practices-2025-threats-tools-and-drupal-11-features | 2, 19 | 2026-02-14 |
| Pantheon Drupal Security | https://pantheon.io/learning-center/drupal-security | 2 | 2026-02-14 |
| Drupal Security Advisories | https://www.drupal.org/security | 2, 19 | 2026-02-14 |
| Route Access Checking | https://www.drupal.org/docs/8/api/routing-system/access-checking-on-routes | 3, 5 | 2026-02-14 |
| CSRF Access Checking | https://www.drupal.org/docs/8/api/routing-system/access-checking-on-routes/csrf-access-checking | 12 | 2026-02-14 |
| Entity Access API | https://www.drupal.org/docs/8/api/entity-api/access-checking-for-content-entities | 7 | 2026-02-14 |
| Node Access API | https://www.drupal.org/docs/8/api/node-access-api | 8 | 2026-02-14 |
| Twig Autoescape Change | https://www.drupal.org/node/2296163 | 9, 10 | 2026-02-14 |
| Twig Autoescape Issue | https://www.drupal.org/project/drupal/issues/2297711 | 10 | 2026-02-14 |
| Database API Static Queries | https://www.drupal.org/docs/develop/drupal-apis/database-api/static-queries | 11 | 2026-02-14 |
| D7 Database Access (EOL) | https://www.drupal.org/docs/7/security/writing-secure-code/database-access | 11 | 2026-02-14 |
| Drupal SQL Injection Prevention | https://medium.com/@er_anwar/protecting-your-drupal-site-from-sql-injection-attacks-essential-practices-0493113d7a96 | 11 | 2026-02-14 |
| Simple OAuth Module | https://www.drupal.org/docs/8/modules/simple-oauth | 14 | 2026-02-14 |
| Trusted Callback Change | https://www.drupal.org/node/2966725 | 16 | 2026-02-14 |
| CSP Module | https://www.drupal.org/project/csp | 17 | 2026-02-14 |
| Security Kit Module | https://www.drupal.org/project/seckit | 17 | 2026-02-14 |
| CORS Configuration | https://www.drupal.org/node/2715637 | 17 | 2026-02-14 |
| MDN CSP Documentation | https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP | 17 | 2026-02-14 |
| OWASP File Upload | https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload | 18 | 2026-02-14 |
| Drupal API Reference | https://api.drupal.org/api/drupal | 21 | 2026-02-14 |

## Code Sources
| Module | Relative Path | Guide Sections | Drupal Version |
|--------|---------------|----------------|----------------|
| Core Access | `core/lib/Drupal/Core/Access/` | 1, 3, 5, 6, 12, 21 | 11.x |
| Core Security | `core/lib/Drupal/Core/Security/` | 1, 16, 21 | 11.x |
| Component Utility | `core/lib/Drupal/Component/Utility/` | 9, 10, 13, 21 | 11.x |
| Component Render | `core/lib/Drupal/Component/Render/` | 10, 21 | 11.x |
| Core Database | `core/lib/Drupal/Core/Database/` | 11, 21 | 11.x |
| Core Session | `core/lib/Drupal/Core/Session/` | 14, 15, 21 | 11.x |
| Core Authentication | `core/lib/Drupal/Core/Authentication/` | 14, 21 | 11.x |
| Core Password | `core/lib/Drupal/Core/Password/` | 14, 21 | 11.x |
| User Module | `core/modules/user/` | 4, 14, 21 | 11.x |
| Node Module | `core/modules/node/` | 8, 21 | 11.x |
| File Module | `core/modules/file/` | 18, 21 | 11.x |
| Core Entity | `core/lib/Drupal/Core/Entity/` | 7, 21 | 11.x |
| Core Form | `core/lib/Drupal/Core/Form/` | 12, 13, 21 | 11.x |

---
