---
description: Facets common mistakes, anti-patterns, and debugging checklist — issue/cause/solution table and step-by-step debug process
tldr: "Use this guide when debugging facet issues or reviewing a faceted search implementation before going to production."
drupal_version: "11.x"
---

# Common Mistakes

## When to Use

> Use this guide when debugging facet issues or reviewing a faceted search implementation before going to production.

## Decision

| Issue | Cause | Solution |
|---|---|---|
| Facets show IDs not labels | `translate_entity` processor not enabled | Enable "Transform entity ID to label" processor |
| Facet source not available | View not saved | Save the View first, then create facets |
| No AJAX on facet blocks | Block facets don't support AJAX | Use `facets_exposed_filters` + Views AJAX instead |
| Facets disappear on page load | Views caching conflicts with block facets | Disable Views cache or use exposed filters |
| Crawl budget exhausted | No SEO protection on facet URLs | Implement robots.txt + noindex + canonical (see [SEO & Bot Protection](seo-bot-protection.md)) |
| Wrong result counts | Stale search index | Reindex content: `drush sapi-r` |
| "Illegal choice" validation error | Facet value not in allowed list | Check that Search API field is properly indexed |
| Hierarchy not working | Index hierarchy not enabled | Enable "Index hierarchy" processor in Search API, reindex |
| Facet not filtering | Wrong query type for field | Check that field type matches query type (string, date, range) |
| Performance issues with translate_entity | Loading hundreds of entities per request | Index entity labels directly, use `list_item` processor instead |
| Multiple facets on same page conflict | Same filter key on two sources | Use different `filter_key` per facet source |
| Faceted URL not bookmarkable | AJAX without URL update | Use `views_ajax_history` module to update URLs |
| Language mixing in facet results | No language filter on View | Add language filter to the View or use `hook_search_api_query_alter()` |

## Pattern

**Debugging checklist:**

1. **Check Search API index** — Is the field indexed? Is the index up to date?
2. **Check facet source** — Does it match the View display? Is the View saved?
3. **Check processors** — Is `translate_entity` enabled for entity reference fields? Is `url_processor_handler` present (it's locked — it should be)?
4. **Check widget** — Does the widget support the feature you expect?
5. **Check URL** — Are facet parameters appearing in the URL? Use browser dev tools.
6. **Check cache** — Clear all caches: `drush cr`. Enable facets debug mode (`$settings['facets_debug_cacheable_metadata'] = TRUE`).
7. **Check JS console** — Are there JavaScript errors preventing facet interaction?

## Common Mistakes

- **Wrong**: Using block-based facets in 3.x as the default approach → **Right**: Block-based facets are the legacy approach. Exposed filters give you AJAX, BEF integration, and simpler setup.
- **Wrong**: Enabling every available processor → **Right**: Too many processors (especially sort processors) can cause unexpected ordering. Start with defaults: `url_processor_handler`, `translate_entity`, `count_widget_order`, `display_value_widget_order`, `active_widget_order`.
- **Wrong**: Deploying without SEO strategy → **Right**: This is the single most damaging oversight. Implement bot protection before launching.
- **Wrong**: Not designing for mobile → **Right**: Faceted search on mobile needs different UX. Consider collapsible facets, modal filters, or BEF secondary options.

## See Also

- [SEO & Bot Protection](seo-bot-protection.md) — essential for production
- [Facets Exposed Filters](facets-exposed-filters.md) — the recommended approach
- [Processing Pipeline](processing-pipeline.md) — understanding processor execution
