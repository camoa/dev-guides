---
description: Step-by-step verification checklist for each AJAX to HTMX migration — pre-migration, code changes, testing, and post-migration
drupal_version: "11.x"
---

# Migration Checklist

## When to Use

> Use this checklist for every individual AJAX to HTMX migration to ensure nothing is missed.

## Decision

| Phase | Item |
|---|---|
| Pre-migration | Document current behavior, identify AJAX pattern, check contrib dependencies, review custom JS, accessibility baseline |
| Code changes | Remove `#ajax`, delete callbacks, remove `AjaxResponse`, update routing, add wrapper attributes, configure HTMX targeting, set swap strategy, handle browser history, migrate JS events, convert custom commands |
| Testing | Functionality, browser history, rapid triggers, form validation, Drupal behaviors, screen reader, keyboard, visual regression, cross-browser, mobile |
| Post-migration | Update docs, remove unused code, code review, regression testing, performance check |

## Pattern

**Pre-Migration:**
- [ ] Document what the AJAX implementation does
- [ ] Identify AJAX pattern — dropdown, wizard, load more, etc.
- [ ] Check contrib dependencies — does any module hook into this?
- [ ] Review JavaScript — custom AJAX commands or event hooks?
- [ ] Accessibility baseline — how does it work with a screen reader now?

**Migration Code Changes:**
- [ ] Remove `#ajax` properties — replace with `Htmx` class configuration
- [ ] Delete callback methods — move logic into `buildForm()` checking `getHtmxTriggerName()`
- [ ] Remove `AjaxResponse` usage — controllers return render arrays
- [ ] Update routing — add `_htmx_route: TRUE` or use `onlyMainContent()`
- [ ] Add wrapper attributes — elements need CSS-selectable targets
- [ ] Configure HTMX targeting — set `select()` and `target()` correctly
- [ ] Add swap strategy — `outerHTML`, `innerHTML`, `beforeend`, etc.
- [ ] Handle browser history — use `pushUrl()` for bookmarkable state
- [ ] Migrate JavaScript events — convert AJAX events to HTMX events
- [ ] Update custom commands — convert to trigger headers + event listeners

**Testing:**
- [ ] Manual testing — feature works as before
- [ ] Browser back/forward — navigation works correctly
- [ ] Multiple rapid clicks — no race conditions
- [ ] Form validation errors — server-side validation displays
- [ ] JavaScript behaviors — libraries attach to swapped content
- [ ] Screen reader testing — updates announced (NVDA/JAWS/VoiceOver)
- [ ] Keyboard navigation — tab order and focus management work
- [ ] Visual regression — no layout or styling breaks
- [ ] Cross-browser — Chrome, Firefox, Safari, Edge
- [ ] Mobile devices — touch interactions work

**Post-Migration:**
- [ ] Update module documentation — document HTMX usage
- [ ] Remove unused AJAX code — delete old callbacks, commands
- [ ] Update JavaScript comments — reference HTMX events not AJAX
- [ ] Code review — team review of changes
- [ ] Regression testing — other features still work
- [ ] Performance check — no slowdown from new approach

## Common Mistakes

- **Skipping the pre-migration review** → Surprises from contrib dependencies or custom JS are much harder to fix after migration
- **Not removing old code** → Leaving dead callbacks and command classes causes confusion and bloat
- **Single-browser testing** → Cross-browser and mobile issues with HTMX differ from AJAX. Test all targets
- **Skipping screen reader testing** → ARIA live region behavior differs across screen readers. Test with actual tools

## See Also

- Previous: [Migration Strategy Best Practices](migration-strategy-best-practices.md)
- Start over: [AJAX vs HTMX Fundamentals](ajax-vs-htmx-fundamentals.md)
- Reference: Complete migration examples throughout this guide
