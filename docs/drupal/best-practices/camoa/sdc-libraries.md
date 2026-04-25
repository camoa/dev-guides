---
description: SDC JS that needs global scope must go in theme-level library overrides, not in the SDC's component JS file which only loads when the component renders.
drupal_version: "11.x"
tldr: SDC JS that needs global scope (like AJAX overrides, document-level event listeners) should go in theme-level library overrides, not in the SDC's `{component}.js` file. SDC JS only loads when the component renders.
---

# SDC Libraries

**What:** SDC JS that needs global scope (like AJAX overrides, document-level event listeners) should go in theme-level library overrides, not in the SDC's `{component}.js` file. SDC JS only loads when the component renders.

**Rationale:** Drupal lazy-loads SDC libraries — the JS file ships with the rendered HTML when (and only when) the component appears in the page. That's correct for component-scoped behavior (a button's click handler, a slider's init). It's wrong for global behavior (AJAX response handlers, body-level event listeners, polyfills) that must run on pages where the component isn't rendered.

**When it applies:** Whenever an SDC needs JS that operates outside its own DOM scope. Examples: an SDC that triggers Drupal AJAX commands needs the AJAX command handler available on every page, including pages without the component.

**Example:**

```yaml
# Wrong — global handler in SDC library only loads when component renders
# components/search-bar/search-bar.component.yml
name: Search Bar
libraryDependencies:
  - core/drupal.ajax
js:
  search-bar.js: {}      # ← contains AJAX response override; only loads with component

# Right — split: component-scoped JS in SDC, global JS in theme library
# components/search-bar/search-bar.component.yml
name: Search Bar
js:
  search-bar.js: {}      # ← only the component's own click/init logic

# {theme}.libraries.yml
ajax-overrides:
  js:
    js/ajax-overrides.js: {}
  dependencies:
    - core/drupal.ajax

# {theme}.theme — attach globally
function {theme}_page_attachments(array &$attachments) {
  $attachments['#attached']['library'][] = '{theme}/ajax-overrides';
}
```
