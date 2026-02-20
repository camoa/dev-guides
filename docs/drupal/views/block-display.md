## 5. Block Display

### When to Use
When you need a view placed in block regions, Layout Builder, or programmatically rendered contexts.

### Steps
1. **Add block display** to view
2. **Configure block description** (admin label)
3. **Set block category** for block placement UI
4. **Enable "allow settings"** if block should override items_per_page
5. **Place block** via Block Layout UI or Layout Builder

### Block-Specific Options

#### Block Metadata
```yaml
block_1:
  display_plugin: block
  display_options:
    block_description: 'Recent Articles Block'
    block_category: 'Lists (Views)'
    block_hide_empty: false
```

- **block_description**: Name shown in block placement UI (defaults to view label)
- **block_category**: Category grouping in block UI (defaults to `Lists (Views)`)
- **block_hide_empty**: Hide block if view returns no results

#### Allow Settings (Per-Block Overrides)
```yaml
display_options:
  allow:
    items_per_page: items_per_page
```

When enabled, each block instance can override items_per_page in block config form.

Reference: `core/modules/views/src/Plugin/views/display/Block.php` lines 80-94

### Pattern
Block display with per-instance items_per_page:

```yaml
block_recent:
  id: block_recent
  display_title: 'Recent Items Block'
  display_plugin: block
  position: 2
  display_options:
    block_description: 'Recent content block'
    block_category: 'Content Listings'
    block_hide_empty: true
    allow:
      items_per_page: items_per_page
    pager:
      type: some
      options:
        items_per_page: 5
```

### Layout Builder Integration
Views blocks integrate with Layout Builder automatically. When a view has a block display, it appears in the Layout Builder block selection UI.

**Best practices for Layout Builder:**
- Use descriptive `block_description` — shown in Layout Builder UI
- Group related views with `block_category` — helps editors find blocks
- Enable `allow.items_per_page` — lets editors customize per layout
- Use contextual filters (arguments) for dynamic content — pass entity ID from layout context

Reference: [Add Views to a Layout](https://drupalize.me/tutorial/add-views-layout)
Reference: [Layout Builder Enhancements](https://www.drupal.org/project/layout_builder_enhancements)

### Exposed Filters in Blocks
Block displays support exposed filters via separate exposed filter block:

```yaml
display_options:
  exposed_block: true  # Creates separate exposed filter block
  exposed_form:
    type: basic
```

When `exposed_block: true`, a separate block (`views_exposed_filter_block:{view_id}-{display_id}`) is created containing just the exposed form. Useful for placing filters separate from results.

**Important**: Exposed filters in block displays require AJAX to work correctly without a page refresh (Block.php lines 214-220).

### Common Mistakes
- Exposed filters without AJAX on block displays → Filters submit but block doesn't refresh; enable `use_ajax: true`
- Not setting `block_description` → Block shows view label + display ID; confusing in block UI
- Forgetting `block_hide_empty` on optional blocks → Empty blocks leave gaps in layout
- Overusing `allow` settings → Every allowed setting adds complexity to block config form; only allow what editors truly need

### See Also
- Section 9: Filters & Exposed Filters — configuring exposed filter blocks
- Section 12: Pager Configuration — block-appropriate pagers (mini, some)
- Reference: [ViewsBlock plugin](https://api.drupal.org/api/drupal/core!modules!views!src!Plugin!Block!ViewsBlock.php/11.x)

