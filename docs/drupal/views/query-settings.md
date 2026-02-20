## 16. Query Settings

### When to Use
When tuning the underlying database query for performance, distinct results, or query debugging.

### Query Configuration

#### SQL Query Options
```yaml
query:
  type: views_query  # Standard SQL query
  options:
    query_comment: ''  # Comment added to SQL query
    disable_sql_rewrite: false  # Bypass node access query rewrite
    distinct: false  # SELECT DISTINCT
    replica: false  # Use replica database
    query_tags: []  # Tags for query altering (hook_query_TAG_alter)
```

Reference: `core/modules/comment/config/optional/views.view.comment.yml` lines 829-836

#### Options Explained
| Option | Type | Purpose |
|--------|------|---------|
| `query_comment` | string | Adds comment to SQL for debugging/tracking |
| `disable_sql_rewrite` | boolean | **DANGEROUS**: Bypasses node access grants. Never use in production user-facing views. |
| `distinct` | boolean | Removes duplicate rows (useful with multiple relationships) |
| `replica` | boolean | Query replica database (if configured) for read-only queries |
| `query_tags` | sequence | Tags for `hook_query_TAG_alter()` — allows modules to modify query |

### Decision
| If you need... | Use... | Why |
|---|---|---|
| Eliminate duplicate rows from relationships | `distinct: true` | Multiple relationships can cause row multiplication |
| Debug slow queries | `query_comment` | Identifies Views query in slow query log |
| Offload read traffic | `replica: true` | Uses replica database, reduces main DB load |
| Allow custom query modifications | `query_tags` | Hook alter system for contrib/custom modules |
| Bypass access checks (testing ONLY) | `disable_sql_rewrite: true` | **Only for admin/testing views** |

### Pattern
Query with distinct and debugging:

```yaml
query:
  type: views_query
  options:
    query_comment: 'Articles view - main listing'
    disable_sql_rewrite: false
    distinct: true
    replica: false
    query_tags:
      - 'custom_module_alter'
```

### DISTINCT and Relationships
When using multiple relationships, rows can multiply:

**Without DISTINCT:**
```
Node 1 → Tag A → Result row 1
Node 1 → Tag B → Result row 2
Node 2 → Tag A → Result row 3
```
Result: Node 1 appears twice.

**With DISTINCT:**
```
Node 1 → Result row 1 (tags aggregated or ignored)
Node 2 → Result row 2
```

**Trade-off**: DISTINCT slows query performance. Only use when necessary.

### disable_sql_rewrite Security Warning
Setting `disable_sql_rewrite: true` **bypasses all node access grants**. This means:
- Users can see unpublished content
- Content access modules are ignored
- Private content becomes visible

**Only use for:**
- Admin-only views with strict access control
- Migration/development debugging
- Never for user-facing views

### Common Mistakes
- Using `distinct: true` without relationships → Unnecessary performance cost; DISTINCT only needed when relationships cause duplicates
- Setting `disable_sql_rewrite: true` on user-facing views → **CRITICAL SECURITY ISSUE**; exposes private content
- Empty `query_comment` on complex views → Hard to debug slow queries; always add descriptive comment for production views
- Using `replica: true` on write-heavy views → Replica lag can show stale data; only use on read-only views
- Adding `query_tags` without implementing alter hook → Tags do nothing unless module implements `hook_query_TAG_alter()`

### See Also
- Section 11: Relationships — when DISTINCT is necessary
- Section 31: Security & Performance — query performance optimization
- Reference: [views_query schema](https://api.drupal.org/api/drupal/core!modules!views!config!schema!views.data_types.schema.yml/11.x)

