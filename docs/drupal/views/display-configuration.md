---
description: When configuring common options shared across all display types: title, access, cache, pager, style, fields, filters, sorts.
drupal_version: "11.x"
---

## 3. Display Configuration

### When to Use
When configuring common options shared across all display types: title, access, cache, pager, style, fields, filters, sorts.

### Common Display Options

#### Display Behavior
| Option | Type | Purpose | Default |
|--------|------|---------|---------|
| `title` | text | Display title (page title, block title) | View label |
| `enabled` | boolean | Whether display is active | `true` |
| `display_description` | label | Admin-only description | Empty |
| `display_comment` | label | Admin note for this display | Empty |

#### Content Options
| Option | Mapping | Purpose |
|--------|---------|---------|
| `fields` | sequence | Field configurations (Section 8) |
| `filters` | sequence | Filter criteria (Section 9) |
| `sorts` | sequence | Sort criteria (Section 10) |
| `arguments` | sequence | Contextual filters (Section 10) |
| `relationships` | sequence | Entity relationships (Section 11) |

#### Presentation Options
| Option | Mapping | Purpose |
|--------|---------|---------|
| `pager` | mapping | Pager configuration (Section 12) |
| `style` | mapping | Output format (table, list, grid) (Section 15) |
| `row` | mapping | Row rendering (fields, entity, teaser) (Section 15) |
| `header` | sequence | Header area content |
| `footer` | sequence | Footer area content |
| `empty` | sequence | No results behavior |

#### System Options
| Option | Mapping | Purpose |
|--------|---------|---------|
| `access` | mapping | Access control (Section 14) |
| `cache` | mapping | Caching strategy (Section 13) |
| `query` | mapping | Query settings (Section 16) |
| `exposed_form` | mapping | Exposed form configuration |

#### UI Options
| Option | Type | Purpose |
|--------|------|---------|
| `css_class` | string | Custom CSS class for wrapper |
| `use_ajax` | boolean | Enable AJAX for paging/filters |
| `use_more` | boolean | Show "more" link |
| `use_more_text` | label | Customize "more" link text |
| `link_display` | string | Display ID to link "more" to |
| `link_url` | text | Custom URL for "more" link |
| `show_admin_links` | boolean | Show contextual links for admins |

### Pattern
Default display with common options:

```yaml
display:
  default:
    id: default
    display_title: Default
    display_plugin: default
    position: 0
    display_options:
      title: 'My View Title'
      css_class: 'my-custom-view'
      use_ajax: false
      access:
        type: perm
        options:
          perm: 'access content'
      cache:
        type: tag
      pager:
        type: full
        options:
          items_per_page: 10
      style:
        type: table
      row:
        type: fields
```

Reference: `core/modules/views/config/schema/views.data_types.schema.yml` lines 4-281

### Common Mistakes
- Setting `use_ajax: true` on block displays without exposed filters → AJAX requires exposed form; without it, AJAX does nothing useful and adds overhead
- Forgetting `css_class` sanitization → Views auto-sanitizes, but avoid special characters anyway
- Not overriding defaults in child displays → Change in "default" display affects all displays unless overridden
- Using `link_url` without checking token availability → Tokens work, but entity must be available in context

### See Also
- Section 4-7: Specific display types (page, block, REST export, feed, attachment)
- Section 8-16: Detailed configuration for fields, filters, sorts, pager, cache, access
- Reference: [Drupal Views Configuration API](https://www.drupal.org/docs/drupal-apis/configuration-api/configuration-schemametadata)
