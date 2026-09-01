---
description: "Source references and maintenance manifest for the htmx guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install

Path: `/home/camoa/workspace/contrib/web/`

## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| HTMX Official Reference | https://htmx.org/reference/ | htmx-attributes, response-headers | 2026-06-07 |
| HTMX Events Documentation | https://htmx.org/events/ | drupal-behaviors, asset-loading | 2026-06-07 |
| HTMX Examples | https://htmx.org/examples/ | production-patterns | 2026-06-07 |
| Drupal Change Record: Ajax subsystem now includes HTMX | https://www.drupal.org/node/3539472 | htmx-overview | 2026-06-07 |
| Drupal 11.3.0 HTMX Blog Post | https://www.drupal.org/about/core/blog/native-htmx-in-drupal-1130-rich-ux-with-up-to-71-less-javascript | htmx-overview | 2026-06-07 |
| Drupal 11.3 HTMX Deep Dive | https://drupal.com.ua/183/how-drupal-113-makes-working-htmx-easier-deep-dive-htmxrequestinfotrait | request-detection | 2026-06-07 |
| Drupal API: Htmx class | https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Htmx!Htmx.php/class/Htmx/11.x | htmx-attributes, response-headers | 2026-06-07 |
| OWASP XSS Prevention Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html | best-practices | 2026-06-07 |
| WCAG 2.1 Quick Reference | https://www.w3.org/WAI/WCAG21/quickref/ | best-practices | 2026-06-07 |
| Drupal Security Best Practices | https://www.drupal.org/docs/security-in-drupal | best-practices | 2026-06-07 |
| Drupal JavaScript API Overview | https://www.drupal.org/docs/drupal-apis/javascript-api/javascript-api-overview | drupal-behaviors | 2026-06-07 |
| Drupal Core Issue #3582309 | https://www.drupal.org/node/3582309 | best-practices | 2026-06-07 |

## Code Sources

| Module | Relative Path | Guide Sections | Drupal Version |
|--------|---------------|----------------|----------------|
| Core HTMX API | core/lib/Drupal/Core/Htmx/ | htmx-attributes, response-headers, request-detection | 11.3.11 |
| Core Render | core/lib/Drupal/Core/Render/MainContent/HtmxRenderer.php | request-response-lifecycle, basic-setup | 11.3.11 |
| Core Event Subscriber | core/lib/Drupal/Core/EventSubscriber/HtmxContentViewSubscriber.php | basic-setup, htmx-controllers | 11.3.11 |
| Core Form | core/lib/Drupal/Core/Form/ | dynamic-forms, request-detection | 11.3.11 |
| Core HTMX JavaScript | core/misc/htmx/ | drupal-behaviors, asset-loading | 11.3.11 |
| Config Module | core/modules/config/src/Form/ConfigSingleExportForm.php | production-example-config-export, dynamic-forms | 11.3.11 |
| Test HTMX Module | core/modules/system/tests/modules/test_htmx/ | dynamic-forms, htmx-controllers, ajax-migration | 11.3.11 |
| Core Tests | core/tests/Drupal/Tests/Core/Htmx/ | core-file-reference | 11.3.11 |
| Vendor HTMX | core/assets/vendor/htmx/htmx.min.js | library-dependencies | 11.3.11 (HTMX 2.0.4) |

---

**Last Updated:** 2026-06-07  
**Drupal Version:** 11.3.11  
**HTMX Version:** 2.0.4
