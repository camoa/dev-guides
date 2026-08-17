---
description: Search API common mistakes — issue/cause/solution table and debugging checklist for sitewide search problems
tldr: "Use this when debugging search issues or reviewing a Search API implementation."
drupal_version: "11.x"
---

# Common Mistakes & Anti-Patterns

## When to Use

> Use this when debugging search issues or reviewing a Search API implementation.

## Decision

| Issue | Cause | Solution |
|---|---|---|
| Search returns no results | Index empty or not indexed | `drush sapi-i` to index, `drush sapi-s` to check status |
| Results in wrong order | Not sorted by relevance | Add "Search: Relevance" sort descending in Views |
| Restricted content visible | Content Access processor not enabled | Enable Content Access processor on index |
| Facets show IDs not labels | `translate_entity` not enabled on facet | Enable processor on the facet |
| Taxonomy terms wrong after edit | Reference tracking disabled or not reindexed | Enable `track_changes_in_references`, reindex |
| Slow search on DB backend | Too many items for database | Switch to Solr |
| Slow COUNT queries on MySQL | InnoDB COUNT limitation | Use Mini pager or skip result count |
| Memory exhaustion during indexing | Batch size too large | Reduce cron_limit to 10-25 |
| Processors not taking effect | Old data in index | `drush sapi-r && drush sapi-i` |
| Stemmer conflicts on Solr | Duplicate processing | Disable Tokenizer, Stemmer, Stopwords, Ignore case for Solr |
| Core Search module conflicts | Both modules running | `drush pm:uninstall search` |
| Highlight adds latency | Processor too expensive | Disable or use `search_api_skip_processor_highlight` tag |
| Deleted terms show as IDs in facets | Orphaned entity references | Reindex to remove stale references |
| Search returns all content unfiltered | Missing fulltext search exposed filter | Add "Search: Fulltext search" filter to View |

## Pattern

**Debugging checklist:**
1. Check index status: `drush sapi-s` — is the index fully indexed?
2. Check server availability: Admin → Server page → "Server connection" status
3. Check processors: Are the right processors enabled for your backend?
4. Check Views sort: Is "Search: Relevance" added as sort criteria?
5. Check fulltext filter: Is the fulltext search exposed filter present?
6. Check field types: Are facet fields String (not Fulltext)?
7. Test reindex: `drush sapi-r && drush sapi-i`
8. Check permissions: Test as anonymous user
9. Check logs: `drush ws --type=search_api`

## Common Mistakes

- **Wrong**: Not creating key pages as nodes → **Right**: Custom routes/blocks are not indexed. Pages that matter for search should be nodes.
- **Wrong**: Expecting immediate results after content edit when `index_directly: FALSE` → **Right**: Changes appear after next cron run.
- **Wrong**: Not reindexing after processor changes → **Right**: Always reindex after changing processors.

## See Also

- [Installation & Setup](installation-setup.md)
- [Processor Recommendations](processor-recommendations.md)
- [Recommended Module Stacks](recommended-module-stacks.md)
- Reference: https://www.drupal.org/docs/8/modules/search-api/getting-started/common-pitfalls
