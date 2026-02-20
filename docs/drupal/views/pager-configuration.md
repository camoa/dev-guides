## 12. Pager Configuration

### When to Use
When controlling how many items display per page and how users navigate through results.

### Pager Types

#### Full Pager
```yaml
pager:
  type: full
  options:
    offset: 0  # Skip first N items
    pagination_heading_level: h4  # Heading level for pager
    items_per_page: 50
    total_pages: null  # Limit number of pages (null = all)
    id: 0  # Pager ID for multiple pagers on same page
    tags:
      next: 'Next ›'
      previous: '‹ Previous'
      first: '« First'
      last: 'Last »'
    quantity: 9  # Number of page links visible
    expose:
      items_per_page: false  # Expose items_per_page
      items_per_page_label: 'Items per page'
      items_per_page_options: '5, 10, 25, 50'
      items_per_page_options_all: false  # Include "All" option
      items_per_page_options_all_label: '- All -'
      offset: false  # Expose offset
      offset_label: Offset
```

Reference: `core/modules/views/config/schema/views.data_types.schema.yml` lines 649-708

#### Mini Pager
```yaml
pager:
  type: mini
  options:
    offset: 0
    items_per_page: 10
    pagination_heading_level: h4
    id: 0
    tags:
      next: 'Next ›'
      previous: '‹ Previous'
```

Shows only Previous/Next, no page numbers.

#### Some (No Pager)
```yaml
pager:
  type: some
  options:
    offset: 0
    items_per_page: 5
```

Displays fixed number of items, no pagination controls.

#### None (Display All)
```yaml
pager:
  type: none
  options:
    offset: 0
```

No pagination, all results displayed.

### Decision
| If you need... | Use... | Why |
|---|---|---|
| Full pagination controls | `full` | Users can jump to any page, see total pages |
| Simple prev/next navigation | `mini` | Cleaner UI, faster queries (no count query) |
| Fixed number of items | `some` | Blocks, teasers, "Recent items" widgets |
| All results on one page | `none` | Small result sets, avoid pagination overhead |

### Pattern
Full pager with exposed items_per_page:

```yaml
pager:
  type: full
  options:
    pagination_heading_level: h4
    items_per_page: 50
    offset: 0
    id: 0
    total_pages: null
    tags:
      next: 'next ›'
      previous: '‹ previous'
      first: '« first'
      last: 'last »'
    expose:
      items_per_page: true
      items_per_page_label: 'Items per page'
      items_per_page_options: '10, 25, 50, 100'
      items_per_page_options_all: false
      offset: false
    quantity: 9
```

Reference: `core/modules/comment/config/optional/views.view.comment.yml` lines 529-550

### Common Mistakes
- Using `full` pager on large datasets without indexes → Count query is slow; consider `mini` pager to skip count
- Exposing `items_per_page` without max limit → Users can request 10,000 items; use reasonable options like `10, 25, 50`
- Setting `items_per_page: 0` expecting "display all" → Use pager type `none` instead
- Multiple pagers on one page with same `id` → Pagers interfere; use unique `id` for each
- Forgetting `offset` when implementing manual pagination → Offset is required to skip already-displayed items
- Using `expose.items_per_page_options_all: true` on large datasets → "All" option can time out or crash; avoid unless dataset is small

### See Also
- Section 5: Block Display — using `some` pager for blocks
- Section 6: REST Export Display — paging API responses
- Section 16: Query Settings — performance impact of pagers

