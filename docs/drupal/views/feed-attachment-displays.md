---
description: When you need RSS/Atom feeds or attaching views to other display outputs.
drupal_version: "11.x"
---

## 7. Feed & Attachment Displays

### When to Use
When you need RSS/Atom feeds or attaching views to other display outputs.

### Feed Displays

#### Configuration
```yaml
feed_1:
  display_plugin: feed
  display_options:
    path: rss/articles.xml
    style:
      type: rss
      options:
        description: 'Latest articles'
        uses_fields: false
    row:
      type: node_rss
      options:
        view_mode: rss
```

- **path**: URL for feed (typically ends in .xml)
- **style**: Usually `rss` style plugin
- **row**: Entity RSS row plugin with view mode

#### Feed Auto-Discovery
Add feed link to page display:

```yaml
page_1:
  display_options:
    displays:
      feed_1: feed_1  # Attaches feed to this page display
```

This adds `<link rel="alternate" type="application/rss+xml">` to page head.

### Attachment Displays

#### Configuration
```yaml
attachment_1:
  display_plugin: attachment
  display_options:
    displays:
      page_1: page_1  # Which display to attach to
    attachment_position: before  # before or after
    inherit_arguments: true
    inherit_exposed_filters: true
```

- **displays**: Map of display IDs to attach to
- **attachment_position**: `before` or `after` the main display output
- **inherit_arguments**: Use same contextual filter values as parent
- **inherit_exposed_filters**: Use same exposed filter values as parent

#### Use Cases
- Summary rows before main table
- Totals/aggregates after results
- Alternative view of same data (e.g., chart before table)

### Pattern
RSS feed with page display link:

```yaml
display:
  default:
    display_plugin: default
    display_options:
      title: 'Article Listing'
      # ... shared config

  page_1:
    display_plugin: page
    display_options:
      path: articles
      displays:
        feed_1: feed_1  # Enables feed link on page

  feed_1:
    display_plugin: feed
    display_options:
      path: articles/rss.xml
      style:
        type: rss
        options:
          description: 'Latest articles from the site'
      row:
        type: node_rss
        options:
          view_mode: rss
      pager:
        type: some
        options:
          items_per_page: 20
```

### Common Mistakes
- Feed without pager limit → Generates huge XML; always set items_per_page on feeds
- Attachment inheriting filters incorrectly → Attachment may return empty results if filters don't make sense for both displays
- Not setting `attachment_position` → Defaults to `before`; explicit is better
- Feed path without .xml extension → Not required but breaks client expectations

### See Also
- Section 15: Style & Row Plugins — RSS style and row options
- Section 12: Pager Configuration — limiting feed items
