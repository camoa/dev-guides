---
description: Plan your AJAX to HTMX migration — priorities by risk and ROI, phased workflow, and testing strategy
drupal_version: "11.x"
---

# Migration Strategy Best Practices

## When to Use

> Use this before starting any AJAX to HTMX migration. Plan priorities, rollout phases, and testing to minimize risk.

## Decision

| Priority | Pattern Type | Risk | ROI |
|---|---|---|---|
| High | New features | Low | High — no legacy code to break |
| High | Simple dependent dropdowns | Low | High — common pattern, clean mapping |
| Medium | Multi-step wizards | Medium | Medium — bookmarkable steps are a real gain |
| Medium | Load more / infinite scroll | Low | Medium — better UX with scroll triggers |
| Low | Working AJAX with contrib | High | Low — if it works, do not break it |
| Low | Complex command sequences | High | Low — AJAX is better for this |

## Pattern

**Phase 1 — Preparation:**
```bash
# Inventory all AJAX usage in custom code
grep -r "#ajax" modules/custom/
grep -r "AjaxResponse" modules/custom/
```
- Categorize by complexity: Simple (dropdown), Medium (wizard), Complex (commands)
- Identify contrib dependencies — do contrib modules provide or expect AJAX callbacks?
- Review custom JavaScript for AJAX commands and event hooks

**Phase 2 — Pilot migration:**
- Choose the simplest pattern first — a basic dependent dropdown
- Migrate on a feature branch, isolated from other work
- Test: browser back/forward, JavaScript disabled, screen reader
- Document codebase-specific gotchas before scaling out

**Phase 3 — Iterative rollout:**
- Migrate one pattern per release — do not convert everything at once
- Regression test existing AJAX still works between migrations
- Use hybrid approach where AJAX is genuinely needed

**Phase 4 — Maintenance:**
- Default to HTMX for all new interactive code
- Opportunistically migrate old AJAX when you touch that code
- Track JavaScript errors and accessibility reports

**Testing checklist per migrated pattern:**

- [ ] Functionality — feature works as before
- [ ] Browser history — back/forward buttons work
- [ ] JavaScript disabled — graceful degradation (if required)
- [ ] Screen reader — updates announced properly
- [ ] Multiple rapid triggers — no race conditions
- [ ] Form validation — server-side errors display
- [ ] Drupal behaviors — JavaScript attaches to swapped content
- [ ] Visual regression — no layout or styling breaks

## Common Mistakes

- **Migrating everything at once** → High risk. Migrate incrementally, one pattern per release
- **Not testing browser history** → HTMX changes how back/forward work. Always test bookmarkable URLs and navigation
- **Skipping accessibility testing** → HTMX swaps need explicit ARIA. Test with screen readers, not just sighted review
- **Ignoring JavaScript disabled** → If you supported progressive enhancement before, maintain it. HTMX degrades gracefully
- **Not documenting decisions** → Document why you kept AJAX in specific places so future developers do not undo it

## See Also

- Previous: [Hybrid AJAX-HTMX Approach](hybrid-ajax-htmx-approach.md)
- Next: [Migration Checklist](migration-checklist.md)
- Reference: Drupal core HTMX tests in `/core/modules/system/tests/modules/test_htmx/`
