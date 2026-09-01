---
description: "Source references and maintenance manifest for the js development guides — web sources, code sources, and version history"
---

# Sources & Maintenance

**Official Drupal Documentation**:
- [JavaScript API Overview](https://www.drupal.org/docs/drupal-apis/javascript-api/javascript-api-overview)
- [Adding Assets to Modules/Themes](https://www.drupal.org/docs/develop/creating-modules/adding-assets-css-js-to-a-drupal-module-via-librariesyml)
- [JavaScript Coding Standards](https://project.pages.drupalcode.org/coding_standards/javascript/best-practice/)
- [AJAX API Documentation](https://www.drupal.org/docs/develop/drupal-apis/ajax-api/core-ajax-callback-commands)
- [JavaScript Testing with Nightwatch](https://www.drupal.org/docs/develop/automated-testing/javascript-testing-using-nightwatch)
- [Accessibility Tools for JavaScript](https://www.drupal.org/docs/drupal-apis/javascript-api/accessibility-tools-for-javascript-in-drupal)
- [Using Single Directory Components](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components)

**Drupal Core Changes**:
- [JavaScript Build Process Removed](https://www.drupal.org/about/core/blog/javascript-build-process-removed) - Drupal 10 ES6 support
- [Remove jQuery.once() Dependency](https://www.drupal.org/node/3158256) - once() migration
- [ES6 Files Deprecated](https://www.drupal.org/node/3305487) - Direct ES6 in .js files
- [drupalSettings CSP Compatible](https://www.drupal.org/node/2513818) - JSON settings format
- [JavaScript Aggregation and Defer](https://www.drupal.org/project/drupal/issues/1587536) - Core issue
- [Header vs Footer JavaScript](https://www.drupal.org/project/drupal/issues/784626) - Default footer loading

**Community Resources**:
- [Drupal at your Fingertips - JavaScript (Selwyn Polit)](https://www.drupalatyourfingertips.com/javascript) - Comprehensive JS patterns, behaviors, libraries (formerly d9book at github.com/selwynpolit/d9book)
- [Drupal at your Fingertips - Forms (Selwyn Polit)](https://www.drupalatyourfingertips.com/forms) - AJAX in forms, library attachment patterns
- [Drupal Book: Replace jQuery.once](https://drupalbook.org/blog/replace-jqueryonce-javascript-once-drupal-10)
- [Lullabot: Nightwatch in Drupal Core](https://www.lullabot.com/articles/nightwatch-in-drupal-core)
- [Lullabot: Single Directory Components](https://www.lullabot.com/articles/getting-single-directory-components-drupal-core)
- [Drupalize.me: SDC Anatomy](https://drupalize.me/tutorial/anatomy-drupal-single-directory-component-sdc)
- [Drupalize.me: Nightwatch Testing](https://drupalize.me/tutorial/functional-javascript-testing-nightwatchjs)
- [Preston So: ES6 for Drupal Developers](https://preston.so/writing/es6-for-drupal-developers-es6-modules-classes-and-promises/)
- [Debounce Functions in Drupal](https://medium.com/@cristinallamas/debounce-functions-in-drupal-js-scripts-3727bdefa11c)

**Performance and Security**:
- [Deferring CSS/JS Resources](https://drupalzone.com/tutorial/performance-optimization/27-reducing-render-blocking-resources)
- [Writing Secure Code for Drupal](https://www.drupal.org/docs/administering-a-drupal-site/security-in-drupal/writing-secure-code-for-drupal)
- [DOM XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html)
- [Debounce vs Throttle Visual Guide](https://drupalsun.com/david-corbacho/2012/10/10/debounce-and-throttle-visual-explanation)
- [Drupal 10 JavaScript Dependency Plan](https://www.drupal.org/project/drupal/issues/3238507)

**Code References**:
- `/core/core.libraries.yml` - Core library definitions
- `/core/misc/drupal.js` - Core Drupal object and behaviors
- `/core/misc/ajax.js` - AJAX framework
- `/core/misc/once.js` - Once API implementation
- `/core/misc/details-aria.js` - Accessibility behavior pattern
- `/core/misc/progress.js` - Complex behavior example
- `/modules/contrib/webform/webform.libraries.yml` - Complex contrib patterns
- `/modules/contrib/webform/js/` - Real-world behavior examples

---
