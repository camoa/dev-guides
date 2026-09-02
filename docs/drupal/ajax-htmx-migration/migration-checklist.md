---
description: "Migration Checklist — step-by-step verification for each AJAX to HTMX migration"
tldr: "Use this checklist for every individual AJAX to HTMX migration to ensure nothing is missed, covering pre-migration review, code changes, testing, and post-migration cleanup."
drupal_version: "11.x"
---

# Migration Checklist

## When to Use

> Step-by-step verification checklist for each AJAX to HTMX migration. Use this to ensure nothing is missed.

## Pre-Migration Checklist

- [ ] **Document current behavior** — Record what the AJAX implementation does
- [ ] **Identify AJAX pattern** — Dependent dropdown, wizard, load more, etc.
- [ ] **Check contrib dependencies** — Does any contrib module hook into this?
- [ ] **Review JavaScript** — Custom AJAX commands or event hooks?
- [ ] **Accessibility baseline** — How does it work with screen reader now?

## Migration Code Changes

- [ ] **Remove `#ajax` properties** — Replace with `Htmx` class configuration
- [ ] **Delete callback methods** — Move logic into `buildForm()` checking `getHtmxTriggerName()`
- [ ] **Remove `AjaxResponse` usage** — Controllers return render arrays
- [ ] **Update routing** — Add `_htmx_route: TRUE` or use `onlyMainContent()`
- [ ] **Add wrapper attributes** — Elements need CSS-selectable targets
- [ ] **Configure HTMX targeting** — Set `select()` and `target()` correctly
- [ ] **Add swap strategy** — Choose correct swap: `outerHTML`, `innerHTML`, `beforeend`, etc.
- [ ] **Handle browser history** — Use `pushUrl()` for bookmarkable state
- [ ] **Migrate JavaScript events** — Convert AJAX events to HTMX events
- [ ] **Update custom commands** — Convert to trigger headers + event listeners

## Testing Checklist

- [ ] **Manual testing** — Feature works as before
- [ ] **Browser back/forward** — Navigation works correctly
- [ ] **Multiple rapid clicks** — No race conditions
- [ ] **Form validation errors** — Server-side validation displays
- [ ] **JavaScript behaviors** — Libraries attach to swapped content
- [ ] **Screen reader testing** — Updates announced (NVDA/JAWS/VoiceOver)
- [ ] **Keyboard navigation** — Tab order and focus management work
- [ ] **Visual regression** — No layout or styling breaks
- [ ] **Cross-browser** — Chrome, Firefox, Safari, Edge
- [ ] **Mobile devices** — Touch interactions work

## Post-Migration Checklist

- [ ] **Update module documentation** — Document HTMX usage
- [ ] **Remove unused AJAX code** — Delete old callbacks, commands
- [ ] **Update JavaScript comments** — Reference HTMX events not AJAX
- [ ] **Code review** — Team review of changes
- [ ] **Regression testing** — Other features still work
- [ ] **Performance check** — No slowdown from new approach

## See Also

- Previous: [Migration Strategy Best Practices](migration-strategy-best-practices.md)
- Reference: Complete migration examples in this guide
