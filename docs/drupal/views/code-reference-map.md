## 32. Code Reference Map

### When to Use
Quick reference to key classes, files, and code locations for Views configuration.

### Core Classes

#### Entity Classes
| Class | Path | Purpose |
|-------|------|---------|
| `View` | `core/modules/views/src/Entity/View.php` | Config entity for views |
| `ViewEntityInterface` | `core/modules/views/src/ViewEntityInterface.php` | Interface for View entity |
| `ViewExecutable` | `core/modules/views/src/ViewExecutable.php` | Executable view instance |

#### Display Plugins
| Class | Path | Purpose |
|-------|------|---------|
| `Page` | `core/modules/views/src/Plugin/views/display/Page.php` | Page display plugin |
| `Block` | `core/modules/views/src/Plugin/views/display/Block.php` | Block display plugin |
| `RestExport` | `core/modules/rest/src/Plugin/views/display/RestExport.php` | REST export display |
| `Feed` | `core/modules/views/src/Plugin/views/display/Feed.php` | Feed display plugin |
| `Attachment` | `core/modules/views/src/Plugin/views/display/Attachment.php` | Attachment display |
| `Embed` | `core/modules/views/src/Plugin/views/display/Embed.php` | Embed display plugin |

#### Cache Plugins
| Class | Path | Purpose |
|-------|------|---------|
| `Tag` | `core/modules/views/src/Plugin/views/cache/Tag.php` | Tag-based cache |
| `Time` | `core/modules/views/src/Plugin/views/cache/Time.php` | Time-based cache |
| `None` | `core/modules/views/src/Plugin/views/cache/None.php` | No caching |

#### Plugin Base Classes (for custom development)
| Class | Path | Purpose |
|-------|------|---------|
| `FieldPluginBase` | `core/modules/views/src/Plugin/views/field/FieldPluginBase.php` | Base for field handlers |
| `FilterPluginBase` | `core/modules/views/src/Plugin/views/filter/FilterPluginBase.php` | Base for filter handlers |
| `SortPluginBase` | `core/modules/views/src/Plugin/views/sort/SortPluginBase.php` | Base for sort handlers |
| `ArgumentPluginBase` | `core/modules/views/src/Plugin/views/argument/ArgumentPluginBase.php` | Base for contextual filters |
| `RelationshipPluginBase` | `core/modules/views/src/Plugin/views/relationship/RelationshipPluginBase.php` | Base for relationships |
| `DisplayPluginBase` | `core/modules/views/src/Plugin/views/display/DisplayPluginBase.php` | Base for display plugins |
| `StylePluginBase` | `core/modules/views/src/Plugin/views/style/StylePluginBase.php` | Base for style plugins |
| `RowPluginBase` | `core/modules/views/src/Plugin/views/row/RowPluginBase.php` | Base for row plugins |
| `CachePluginBase` | `core/modules/views/src/Plugin/views/cache/CachePluginBase.php` | Base for cache plugins |

#### Plugin Attributes (PHP 8)
| Attribute | Path | Purpose |
|-----------|------|---------|
| `ViewsField` | `core/modules/views/src/Attribute/ViewsField.php` | Field handler attribute |
| `ViewsFilter` | `core/modules/views/src/Attribute/ViewsFilter.php` | Filter handler attribute |
| `ViewsSort` | `core/modules/views/src/Attribute/ViewsSort.php` | Sort handler attribute |
| `ViewsArgument` | `core/modules/views/src/Attribute/ViewsArgument.php` | Argument handler attribute |
| `ViewsRelationship` | `core/modules/views/src/Attribute/ViewsRelationship.php` | Relationship attribute |
| `ViewsDisplay` | `core/modules/views/src/Attribute/ViewsDisplay.php` | Display plugin attribute |
| `ViewsStyle` | `core/modules/views/src/Attribute/ViewsStyle.php` | Style plugin attribute |
| `ViewsRow` | `core/modules/views/src/Attribute/ViewsRow.php` | Row plugin attribute |
| `ViewsCache` | `core/modules/views/src/Attribute/ViewsCache.php` | Cache plugin attribute |

#### Block Integration
| Class | Path | Purpose |
|-------|------|---------|
| `ViewsBlock` | `core/modules/views/src/Plugin/Block/ViewsBlock.php` | Views block plugin |
| `ViewsExposedFilterBlock` | `core/modules/views/src/Plugin/Block/ViewsExposedFilterBlock.php` | Exposed filter block |

### Config Schema Files
| File | Path | Purpose |
|------|------|---------|
| `views.schema.yml` | `core/modules/views/config/schema/views.schema.yml` | Main Views config schema |
| `views.data_types.schema.yml` | `core/modules/views/config/schema/views.data_types.schema.yml` | Data type schemas (fields, filters, etc.) |
| `views.field.schema.yml` | `core/modules/views/config/schema/views.field.schema.yml` | Field handler schemas |
| `views.filter.schema.yml` | `core/modules/views/config/schema/views.filter.schema.yml` | Filter plugin schemas |
| `views.sort.schema.yml` | `core/modules/views/config/schema/views.sort.schema.yml` | Sort criteria schemas |
| `views.argument.schema.yml` | `core/modules/views/config/schema/views.argument.schema.yml` | Argument/contextual filter schemas |

### Example Config Files (Core)
| View | Path | Purpose |
|------|------|---------|
| Content admin | `core/modules/node/config/optional/views.view.content.yml` | Node admin listing |
| Comments | `core/modules/comment/config/optional/views.view.comment.yml` | Comment management |
| Taxonomy | `core/modules/taxonomy/config/optional/views.view.taxonomy_term.yml` | Term listing |
| Frontpage | `core/modules/node/config/optional/views.view.frontpage.yml` | Default frontpage |
| User admin | `core/modules/user/config/optional/views.view.user_admin_people.yml` | User listing |

### Services
| Service ID | Class | Purpose |
|------------|-------|---------|
| `views.executable` | `ViewsExecutableFactory` | Creates ViewExecutable instances |
| `plugin.manager.views.display` | `DisplayPluginManager` | Display plugin manager |
| `plugin.manager.views.cache` | `CachePluginManager` | Cache plugin manager |
| `plugin.manager.views.style` | `StylePluginManager` | Style plugin manager |
| `plugin.manager.views.row` | `RowPluginManager` | Row plugin manager |

### Hooks
| Hook | File | Purpose |
|------|------|---------|
| `hook_views_data()` | `views.api.php` | Define views data tables |
| `hook_views_data_alter()` | `views.api.php` | Alter views data |
| `hook_views_pre_view()` | `views.api.php` | Before view execution |
| `hook_views_pre_render()` | `views.api.php` | After query, before render |
| `hook_views_post_render()` | `views.api.php` | After rendering |
| `hook_views_query_alter()` | `views.api.php` | Alter view query |

### Key Methods

#### View Entity
```php
// Load view config entity
$view = \Drupal\views\Entity\View::load('my_view');

// Get executable
$executable = $view->getExecutable();

// Add display
$view->addDisplay('page', 'My Page', 'page_1');

// Get display config
$display = $view->getDisplay('page_1');
```

#### ViewExecutable
```php
// Load and execute
$view = \Drupal\views\Views::getView('my_view');
$view->setDisplay('page_1');
$view->setArguments([123]);
$view->execute();
$results = $view->result;

// Render
$render_array = $view->render();
```

### See Also
- Section 18: Programmatic View Modification — using these classes in code
- Reference: [Drupal Views API documentation](https://api.drupal.org/api/drupal/core!modules!views/11.x)

