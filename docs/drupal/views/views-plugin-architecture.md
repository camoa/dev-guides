## 19. Views Plugin Architecture

### When to Use
When Views UI configuration and programmatic view modification aren't sufficient — you need custom data processing, specialized formatting, or integration with non-standard data sources.

### Decision
| If you need... | Use... | Why |
|---|---|---|
| Custom field calculation or formatting | Field Handler | Process and display data per-row with full control over output |
| Custom filtering logic | Filter Handler | Complex filter conditions beyond standard operators |
| Custom sort logic | Sort Handler | Sort by calculated values or complex criteria |
| URL-based filtering with validation | Argument Handler (Contextual Filter) | Extract and validate filter values from URLs |
| Join to related data | Relationship Handler | Make related table data available to view |
| Expose non-entity table to Views | hook_views_data() | Integrate custom tables or external data sources |
| Custom output format | Style Plugin | Control entire result set rendering (grid, calendar, etc.) |
| Per-row rendering logic | Row Plugin | Control single row rendering within a style |
| New display type | Display Plugin | Create new output channels (API endpoints, etc.) |
| Custom cache strategy | Cache Plugin | Specialized caching beyond tag/time-based |

### Plugin Types Hierarchy
- **Handlers** — Process individual aspects of query building:
  - Field: Data retrieval and display
  - Filter: WHERE clause conditions
  - Sort: ORDER BY logic
  - Argument: Contextual filtering from URL
  - Relationship: JOIN operations
- **Display Plugins** — Define how and where view renders (Page, Block, REST, etc.)
- **Style Plugins** — Format entire result set (Table, Grid, List, etc.)
- **Row Plugins** — Format individual rows within a style
- **Cache Plugins** — Define caching strategies

### Pattern: Plugin Discovery
```php
// Views discovers plugins via attributes
#[ViewsField("my_custom_field")]  // Plugin ID
class MyCustomField extends FieldPluginBase { }

// Registered in hook_views_data()
$data['my_table']['my_field'] = [
  'field' => ['id' => 'my_custom_field'],
];
```

Reference: `core/modules/views/src/Plugin/views/` — all plugin base classes

### Common Mistakes
- Creating plugin when config would suffice → Use custom plugins only when UI can't achieve the goal; config is easier to maintain
- Not extending correct base class → Field handlers extend FieldPluginBase, not HandlerBase directly
- Forgetting plugin attribute → Views can't discover plugins without #[ViewsField] etc. attributes
- Not implementing hook_views_data() → Plugin won't appear in Views UI without views data integration
- Mixing concerns across plugin types → Field handlers shouldn't sort, filters shouldn't format — each type has one job

### See Also
- Section 20-28: Individual plugin type workflows
- Section 29: Views Data Integration (hook_views_data)
- Reference: [Views API Overview](https://www.drupal.org/docs/drupal-apis/views-api)

