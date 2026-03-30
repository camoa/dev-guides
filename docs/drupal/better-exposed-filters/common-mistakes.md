---
description: BEF common mistakes, anti-patterns, and debugging checklist — quick-reference issue/cause/solution table
drupal_version: "11.x"
---

# Common Mistakes & Anti-Patterns

## When to Use

> Use this guide when debugging BEF issues or reviewing BEF configuration for problems.

## Decision

| Issue | Cause | Solution |
|---|---|---|
| BEF options not showing | Exposed form style not set to BEF | Views → Advanced → Exposed Form → Change to "Better Exposed Filters" |
| Widget not available for filter | `isApplicable()` returns FALSE | Check filter type — taxonomy autocomplete, non-standard filters may not be compatible |
| Slider not rendering | Missing noUiSlider library | Verify `/libraries/nouislider/nouislider.min.js` exists |
| Auto-submit fires on every keystroke | No debounce configured | Set `autosubmit_textfield_delay` to 500ms+ and `autosubmit_textfield_minimum_length` to 3+ |
| "Select all/none" disabled | Filter not set to "Allow multiple selections" | Edit the filter → Expose settings → Check "Allow multiple selections" |
| Checkboxes showing instead of radios | Filter allows multiple selections | Uncheck "Allow multiple selections" for radio buttons |
| "Illegal choice" error | Option removed by rewrite but still selected | Ensure rewritten options account for all possible submitted values |
| Collapsible filter won't open | `open_by_default` not set | Enable "Open by default" in advanced filter options |
| Sort combine not working | Sort order not exposed | Enable "Allow people to choose the sort order" in Views |
| Config import fails | Missing config schema for custom widget | Add schema entry in `config/schema/` for your custom widget |
| Links point to wrong page | Exposed form displayed as block | BEF handles this via `#bef_path` — check that the View's page path is correct |
| Nested hierarchy renders flat | "Show hierarchy in dropdown" not checked | Edit the filter → Settings → Check "Show hierarchy in dropdown" |
| JS errors after AJAX | Custom JS not using Drupal.behaviors | Wrap custom JS in `Drupal.behaviors` for proper re-attachment |
| Date picker format mismatch | HTML5 date always uses YYYY-MM-DD | Accept ISO format or configure the date filter to match |

## Pattern

**Debugging BEF:**
1. Enable Twig debug — see template suggestions: `{{ dump(_context) }}`
2. Check drupalSettings — in browser console: `drupalSettings.better_exposed_filters`
3. Inspect form element for `data-bef-*` attributes
4. Check `isApplicable()` — if a widget doesn't appear, the filter type may not be supported
5. Run `drush cex` and inspect the View YAML for BEF settings structure

## Common Mistakes

- **Wrong**: Using BEF to replace Facets for faceted search with counts → **Right**: BEF is for Views exposed forms. For search faceted navigation with counts, use Facets module.
- **Wrong**: Enabling auto-submit, collapsible, secondary, and soft limit all at once → **Right**: Each adds complexity. Start simple and add features incrementally.
- **Wrong**: Testing only without Views AJAX → **Right**: BEF behavior differs with and without AJAX. Test both paths.

## See Also

- [Overview](overview.md)
- [Integration Patterns](integration-patterns.md)
- [Theming & Templates](theming-templates.md)
