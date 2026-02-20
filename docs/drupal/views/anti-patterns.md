## 30. Anti-Patterns & Common Mistakes

### When to Use
What NOT to do and WHY.

### Configuration Anti-Patterns

#### Using Views UI for One-Off Queries
**Anti-pattern**: Creating a view for a single-use admin report that only you will ever run.

**Why bad**: Views add overhead (config storage, UI complexity, cache management) for queries that could be 10 lines of EntityQuery code.

**Do instead**: Write custom EntityQuery in controller or drush command. Simpler, faster, clearer intent.

#### Not Exporting Views to Config
**Anti-pattern**: Building views in production UI, never exporting to YAML.

**Why bad**: Views live only in database. Can't version control, can't reproduce on other environments, lost on DB restore, no audit trail.

**Do instead**: Always export production views. Config sync is the Drupal way.

#### Overly Complex Single Views
**Anti-pattern**: One view with 8 displays, 15 relationships, 20 filters, trying to be everything.

**Why bad**: Unmaintainable nightmare. Hard to debug, slow to load in UI, fragile (one change breaks multiple displays).

**Do instead**: Split into multiple focused views. Each view does one thing well.

### Performance Anti-Patterns

#### DISTINCT Without Relationships
**Anti-pattern**: `query.options.distinct: true` on view with no relationships.

**Why bad**: DISTINCT is expensive (sorts all rows to find duplicates). Without relationships, there are no duplicates.

**Do instead**: Only use DISTINCT when multiple relationships cause row multiplication. Test query without DISTINCT first.

#### No Pager on Unbounded Queries
**Anti-pattern**: `pager.type: none` on a view querying all nodes (10,000+ rows).

**Why bad**: Loads entire dataset into memory, times out, crashes page, kills database.

**Do instead**: Always limit results. Use `some` pager for fixed limit, `full`/`mini` for pagination.

#### Tag Cache on Rarely-Changing High-Traffic Views
**Anti-pattern**: Tag-based cache on homepage view of archived content that changes monthly.

**Why bad**: Tag tracking overhead for content that doesn't change. Time-based cache would be more efficient.

**Do instead**: Use time-based cache with long lifespan (24 hours or more) for semi-static content.

### Security Anti-Patterns

#### disable_sql_rewrite on User-Facing Views
**Anti-pattern**: `query.options.disable_sql_rewrite: true` on public article listing.

**Why bad**: **CRITICAL SECURITY ISSUE**. Bypasses ALL node access grants. Unpublished content visible, private content exposed, access control modules ignored.

**Do instead**: Never use on user-facing views. Only for admin-only views with strict permission checks.

#### REST Export Without Authentication
**Anti-pattern**: REST export display with `access: none` or no `auth` setting.

**Why bad**: Public API endpoint exposing potentially sensitive data. No rate limiting, no accountability.

**Do instead**: Always require authentication (`auth: ['basic_auth']`) and set appropriate access permissions.

#### No Contextual Filter Validation
**Anti-pattern**: Contextual filter with `specify_validation: false` accepting arbitrary input.

**Why bad**: Malicious input can cause query errors, expose data, or bypass access checks.

**Do instead**: Always validate contextual filters. Use entity validator with access check for entity reference arguments.

### UX Anti-Patterns

#### Exposed Filters Without Labels
**Anti-pattern**: `expose.label: ''` on exposed filter.

**Why bad**: Form shows field machine name or blank label. Users don't know what the filter does.

**Do instead**: Always set clear, user-friendly labels on exposed filters.

#### Required Exposed Filters
**Anti-pattern**: `expose.required: true` on all exposed filters.

**Why bad**: Users can't view all results. Must always pick a filter value.

**Do instead**: Use `required: false` and set reasonable defaults. Let users refine, not restrict from start.

#### Block Display Without block_description
**Anti-pattern**: Block display with `block_description: ''`.

**Why bad**: Block shows as "View: {view_id} - {display_id}" in block UI. Confusing for site builders.

**Do instead**: Set descriptive `block_description`. "Recent Articles" not "Block 1".

### Maintainability Anti-Patterns

#### Generic Machine Names
**Anti-pattern**: Views named `view_1`, `block_2`, `page`.

**Why bad**: Impossible to understand purpose without opening config. Debugging logs are cryptic.

**Do instead**: Descriptive names: `articles_by_category`, `user_dashboard_recent_activity`.

#### No Admin Labels on Relationships
**Anti-pattern**: Relationship with `admin_label: ''`.

**Why bad**: Views UI shows field name (`uid`) instead of purpose. Can't distinguish multiple relationships to same entity type.

**Do instead**: Always set `admin_label`: "author", "editor", "reviewer".

#### Duplicated Config Across Displays
**Anti-pattern**: Repeating same filter config in every display instead of using `default` display.

**Why bad**: Changing filter requires updating 5 displays. Easy to miss one, creates inconsistency.

**Do instead**: Put shared config in `default` display. Override only what differs in child displays.

### See Also
- Section 29: Best Practices & Patterns — what to do instead
- Section 31: Security & Performance — security details

