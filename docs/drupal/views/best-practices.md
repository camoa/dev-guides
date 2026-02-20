## 29. Best Practices & Patterns

### When to Use
Guidelines for building maintainable, performant, secure views.

### Configuration Management
- **Export views to config** — Always export production views to YAML; store in version control
- **Use config splits for environment-specific views** — Dev-only debug views shouldn't deploy to production
- **Document complex views in description field** — Future developers (including yourself) will thank you
- **Use descriptive machine names** — `articles_by_category_block` better than `view_1`

### Performance
- **Choose appropriate cache strategy** — Tag-based for dynamic content, time-based for semi-static
- **Limit results with pagers** — Never `pager: none` on unbounded queries
- **Use DISTINCT only when necessary** — Only with relationships that cause row multiplication
- **Index filtered/sorted fields** — Database indexes on fields used in filters and sorts
- **Avoid wildcard LIKE filters** — `title LIKE '%foo%'` can't use indexes; prefix-only (`foo%`) can
- **Use aggregation sparingly** — GROUP BY queries are expensive; only when truly needed

Reference: [Drupal Performance Optimization](https://www.optasy.com/blog/drupal-performance-optimization-17-drupal-caching-best-practices-speed-your-page-load-time)

### Security
- **Always validate contextual filter arguments** — Use `specify_validation: true` and entity validators
- **Set proper access control** — Never use `access: none` on views with sensitive data
- **Never use disable_sql_rewrite on user-facing views** — Bypasses node access grants
- **Sanitize exposed filter input** — Views does this, but verify custom filter plugins do too
- **Limit exposed filter options** — Grouped filters prevent arbitrary input

### Maintainability
- **Use meaningful admin labels** — Especially for relationships and fields (`author` not `uid`)
- **Override defaults in child displays** — Keep shared config in `default` display
- **Limit displays per view** — If view has >5 displays, consider splitting into multiple views
- **Use consistent naming** — Follow project conventions for IDs, labels, paths

### REST Export Specific
- **Require authentication** — Always set `auth` for API endpoints
- **Use serializer format restrictions** — Only enable needed formats (json, xml)
- **Set reasonable items_per_page** — API consumers can overwhelm server; cap at 100 or less
- **Version API paths** — `/api/v1/articles` allows breaking changes without disruption

### Layout Builder Integration
- **Descriptive block_description** — Shows in Layout Builder UI; be specific
- **Enable per-block overrides selectively** — Only allow settings editors actually need
- **Use contextual filters for dynamic content** — Pass entity ID from layout context
- **Group related blocks with block_category** — Helps editors find blocks

Reference: [Improving Layout Builder Experience](https://www.specbee.com/blogs/improving-drupals-layout-builder-experience)

### Accessibility
- **Set pagination_heading_level appropriately** — Match document outline hierarchy
- **Provide table summaries** — `style.options.summary` for screen readers
- **Use semantic HTML in element_type** — `<h3>` for titles, not `<div>`
- **Meaningful link text** — Avoid "Read more"; use "Read more about {{ title }}"

### Common Patterns
- **Admin overview table** — Table style, full pager, exposed filters, bulk operations field
- **Public listing** — Default/grid style, entity row, tag cache, mini pager
- **Block teaser** — Some pager (5 items), entity row with teaser view mode, tag cache
- **JSON API** — REST export, serializer style, data_entity row, time cache, authentication
- **RSS feed** — Feed display, rss style, node_rss row, some pager (20 items)

### See Also
- Section 13: Caching Configuration — cache strategies
- Section 14: Access Control — security patterns
- Section 31: Security & Performance — detailed security guidance

