---
description: "Migration Strategy Best Practices — what to migrate first, rollout phases, and testing approach for AJAX to HTMX migration"
tldr: "Plan the migration before starting: prioritize new features and simple dependent dropdowns first, migrate one pattern per release, and always test browser history plus screen readers since HTMX changes both."
drupal_version: "11.x"
---

# Migration Strategy Best Practices

## When to Use

> Plan your AJAX to HTMX migration strategy before starting. This section provides battle-tested approaches for minimizing risk and maximizing success.

## Migration Priorities

| Priority | Pattern Type | Risk | ROI |
|---|---|---|---|
| **High** | New features | Low | High — No legacy code to break |
| **High** | Simple dependent dropdowns | Low | High — Common pattern, clean mapping |
| **Medium** | Multi-step wizards | Medium | Medium — Bookmarkable steps are nice |
| **Medium** | Load more / infinite scroll | Low | Medium — Better UX with scroll triggers |
| **Low** | Working AJAX with contrib | High | Low — If it works, don't break it |
| **Low** | Complex command sequences | High | Low — AJAX better for this |

## Workflow

**Phase 1: Preparation**
1. **Inventory AJAX usage** — Find all `#ajax` properties and `AjaxResponse` returns
   ```bash
   grep -r "#ajax" modules/custom/
   grep -r "AjaxResponse" modules/custom/
   ```
2. **Categorize by complexity** — Simple (dropdown), Medium (wizard), Complex (commands)
3. **Identify contrib dependencies** — Check if contrib modules provide or expect AJAX callbacks
4. **Review JavaScript customizations** — Find custom AJAX commands and event hooks

**Phase 2: Pilot Migration**
1. **Choose simplest pattern** — Start with basic dependent dropdown
2. **Migrate to feature branch** — Don't mix with other work
3. **Test thoroughly** — Browser back/forward, JavaScript disabled, screen readers
4. **Document learnings** — Note gotchas specific to your codebase

**Phase 3: Iterative Rollout**
1. **Migrate one pattern at a time** — Don't convert everything at once
2. **Test between migrations** — Regression test existing AJAX still works
3. **Keep AJAX for edge cases** — Use hybrid approach where needed
4. **Update team documentation** — Document new HTMX patterns for team

**Phase 4: Maintenance**
1. **Default to HTMX for new code** — Unless AJAX is specifically needed
2. **Opportunistic refactoring** — Migrate old AJAX when you touch that code
3. **Monitor for issues** — Track JavaScript errors, accessibility reports

## Testing Strategy

**Essential tests for each migrated pattern:**

- [ ] **Functionality** — Feature works as before
- [ ] **Browser history** — Back/forward buttons work correctly
- [ ] **JavaScript disabled** — Graceful degradation (if required)
- [ ] **Screen reader** — Updates announced properly
- [ ] **Multiple triggers** — Rapid clicks don't cause race conditions
- [ ] **Form validation** — Server-side validation still works
- [ ] **Drupal behaviors** — JavaScript attaches to swapped content
- [ ] **CSS/layout** — No visual regressions

## Common Mistakes

- **Migrating everything at once** → High risk. Migrate incrementally, one pattern per release
- **Not testing browser history** → HTMX changes how back/forward work. Always test bookmarkable URLs and navigation
- **Skipping accessibility testing** → HTMX swaps need explicit ARIA. Test with screen readers, not just sighted review
- **Ignoring JavaScript disabled** → If you supported progressive enhancement before, maintain it. HTMX degrades gracefully with `hx-boost`
- **Not documenting decisions** → Document WHY you kept AJAX in specific places so future developers don't break it

## See Also

- Previous: [Hybrid AJAX-HTMX Approach](hybrid-ajax-htmx-approach.md)
- Next: [Migration Checklist](migration-checklist.md)
- Reference: Testing best practices in Drupal core HTMX tests
