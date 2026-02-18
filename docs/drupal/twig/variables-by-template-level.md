---
topic: drupal/twig
guide: variables-by-template-level
---

## Variables by Template Level

### When to Use
When you need to know exactly what variables are available in a specific template type.

### Items

#### html.html.twig
**Variables set by**: `ThemePreprocess::preprocessHtml()`
| Variable | Type | Description |
|---|---|---|
| `html_attributes` | Attribute | Attributes for `<html>` (lang, dir) |
| `attributes` | Attribute | Attributes for `<body>` |
| `head_title` | array | `['title', 'name', 'slogan']` — use `|safe_join` |
| `page` | render array | The full page render array |
| `page_top` | render array | Content before `<body>` (toolbars) |
| `page_bottom` | render array | Content after page (JS includes) |
| `placeholder_token` | string | Token for CSS/JS placeholders |
| `logged_in` | bool | Is current user authenticated |
| `is_admin` | bool | Has admin permission |
| `root_path` | string | First path segment (e.g., `node`, `user`) |

#### page.html.twig
**Variables set by**: `ThemePreprocess::preprocessPage()`
| Variable | Type | Description |
|---|---|---|
| `page.header` | render array | Header region content |
| `page.content` | render array | Main content region |
| `page.sidebar_first` | render array | First sidebar region |
| `page.sidebar_second` | render array | Second sidebar region |
| `page.footer` | render array | Footer region content |
| `page.primary_menu` | render array | Primary menu region |
| `page.breadcrumb` | render array | Breadcrumb region |
| `base_path` | string | Drupal installation base path (`/`) |
| `front_page` | string | URL of the front page |
| `is_front` | bool | Is this the front page |
| `logged_in` | bool | Is current user authenticated |
| `is_admin` | bool | Has admin permission |
| `node` | Node entity | Only set when route parameter is a node |

#### region.html.twig
**Variables set by**: `ThemePreprocess::preprocessRegion()`
| Variable | Type | Description |
|---|---|---|
| `content` | render array | Blocks inside this region |
| `attributes` | Attribute | Region wrapper attributes |
| `region` | string | Region machine name |

#### block.html.twig
| Variable | Type | Description |
|---|---|---|
| `content` | render array | Block content |
| `label` | string | Block label (if visible) |
| `attributes` | Attribute | Block wrapper attributes (includes unique `id`) |
| `title_attributes` | Attribute | Label element attributes |
| `title_prefix` / `title_suffix` | render array | Contextual links slots |
| `plugin_id` | string | Block plugin ID |
| `configuration` | array | Block configuration values |
| `in_preview` | bool | Block is in layout preview mode |

#### node.html.twig
**Variables set by**: `NodeThemeHooks::preprocessNode()`
| Variable | Type | Description |
|---|---|---|
| `node` | Node entity | The node object (sandbox-restricted access) |
| `content` | array | All field render arrays keyed by field name |
| `label` | render array | Node title field |
| `url` | string | Canonical URL to this node |
| `view_mode` | string | `full`, `teaser`, `search_index`, etc. |
| `attributes` | Attribute | `<article>` element attributes |
| `title_attributes` | Attribute | Title element attributes |
| `content_attributes` | Attribute | Content wrapper attributes |
| `author_attributes` | Attribute | Author info element attributes |
| `author_picture` | render array | Author user picture (if enabled) |
| `author_name` | string | Rendered author name field |
| `date` | string | Rendered date field |
| `display_submitted` | bool | Whether to show author/date |
| `logged_in` | bool | Is current user authenticated |
| `is_admin` | bool | Has admin permission |

#### field.html.twig
**Variables set by**: `FieldPreprocess::preprocessField()`
| Variable | Type | Description |
|---|---|---|
| `items` | array | Each field item: `[{attributes, content}]` |
| `label` | string | Field label |
| `label_hidden` | bool | Whether label display is hidden |
| `label_display` | string | Label display setting: `inline`, `above`, `hidden`, `visually_hidden` |
| `multiple` | bool | Field allows multiple values |
| `attributes` | Attribute | Field wrapper attributes |
| `title_attributes` | Attribute | Label element attributes |
| `entity_type` | string | Parent entity type (`node`, `user`, etc.) |
| `field_name` | string | Machine name of the field |
| `field_type` | string | Field type (`text_long`, `image`, etc.) |

#### views-view.html.twig
| Variable | Type | Description |
|---|---|---|
| `rows` | render array | View results (empty if no results) |
| `header` / `footer` | render array | View header/footer areas |
| `empty` | render array | No results content |
| `exposed` | render array | Exposed filters form |
| `pager` | render array | Pagination links |
| `more` | render array | "More" link |
| `attachment_before` / `attachment_after` | render array | Attachment displays |
| `attributes` | Attribute | Wrapper element attributes |
| `css_name` | string | CSS-safe view name |
| `dom_id` | string | Unique DOM identifier |
| `title` | string | View title (admin preview only) |

### Common Mistakes
- Accessing `{{ node }}` in `page.html.twig` when not on a node route → variable is not always set, always check `{% if node %}`
- Using `{{ content.field_name }}` in `block.html.twig` → block `content` is not a field array
- Expecting `{{ items }}` in `node.html.twig` → use `{{ content.field_name }}` which is the rendered field

### See Also
- Template hierarchy → [Template Hierarchy](template-hierarchy.md)
- Preprocess functions → [Preprocess Functions](preprocess-functions.md)
