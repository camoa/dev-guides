---
description: Complete reference for all Easy Breadcrumb configuration settings — title resolution, home segment, capitalization, custom paths, and SEO
tldr: "After installing Easy Breadcrumb, configure at `admin/config/user-interface/easy-breadcrumb`. All settings map to `easy_breadcrumb.settings.yml` which can be exported and version-controlled."
drupal_version: "11.x"
---

# Easy Breadcrumb Configuration

## When to Use

> After installing Easy Breadcrumb, configure it at `admin/config/user-interface/easy-breadcrumb`. All settings map to `easy_breadcrumb.settings.yml` which can be exported and version-controlled.

## Items

#### General Settings

| Config key | Type | Purpose |
|---|---|---|
| `applies_admin_routes` | bool | Include admin routes in Easy Breadcrumb (default: `TRUE`) |
| `include_invalid_paths` | bool | Show non-routed path segments as plain text instead of dropping them |
| `include_title_segment` | bool | Add current page title as the final breadcrumb segment |
| `title_segment_as_link` | bool | Make the current page segment a link (requires `include_title_segment`) |
| `title_from_page_when_available` | bool | Use the real page title (via `TitleResolver`) instead of URL slug — **enable this** |
| `remove_repeated_segments` | bool | Remove consecutive duplicate segments |
| `remove_repeated_segments_text_only` | bool | Match on text only (ignores URL) when deduplicating |
| `follow_redirects` | bool | Resolve redirect module redirects to their source paths |

#### Home Segment

| Config key | Type | Purpose |
|---|---|---|
| `include_home_segment` | bool | Add a "Home" link as the first segment |
| `home_segment_title` | string | Label for the home segment (e.g., `"Home"`) |
| `use_site_title` | bool | Use the site name from `system.site:name` as home segment title |
| `home_segment_keep` | bool | Show home segment even on the front page |
| `home_segment_validation_skip` | bool | Skip checking if a path segment duplicates the home page |
| `hide_single_home_item` | bool | Hide the breadcrumb entirely if it only contains the home segment |

#### Title Segment Fallbacks

| Config key | Type | Purpose |
|---|---|---|
| `use_menu_title_as_fallback` | bool | Use the menu link title when no `_title` exists on the route |
| `menu_title_preferred_menu` | string | Machine name of preferred menu (when multiple menus have the same route) |
| `use_page_title_as_menu_title_fallback` | bool | Fall back to page title if menu title not found |
| `alternative_title_field` | string | Field machine name on entities (e.g., `field_breadcrumb_title`) for per-entity title override |

#### Capitalization

| Config key | Type | Options |
|---|---|---|
| `capitalizator_mode` | string | `none`, `ucwords` (Title Case), `ucfirst` (Sentence case), `ucall` (ALL CAPS), `ucforce` (force specific words) |
| `capitalizator_ignored_words` | array | Words to skip during `ucwords` mode (e.g., `['of', 'and', 'the']`) |
| `capitalizator_forced_words` | array | Words to force to uppercase during `ucforce` mode |
| `capitalizator_forced_words_first_letter` | bool | Also capitalize first letter of each segment in `ucforce` mode |
| `capitalizator_forced_words_case_sensitivity` | bool | Case-sensitive matching in `ucforce` mode |

#### Paths Control

| Config key | Type | Purpose |
|---|---|---|
| `excluded_paths` | textarea | Newline-separated paths to exclude from breadcrumb segments. Supports regex (escape `/` as `\/`). Default excludes `search` and `search/node` |
| `replaced_titles` | textarea | Newline-separated `ORIGINAL_TITLE::REPLACEMENT` pairs. Applied after title resolution |
| `custom_paths` | textarea | Newline-separated fully custom breadcrumbs per path. Format: `path :: Crumb1\|/url1 :: Crumb2\|/url2`. Supports `regex!` prefix and `<title>` placeholder |

**Custom paths example:**
```
/news/archive :: News | /news :: Archive | /news/archive
regex!/products/(\w+)/(\d+) :: Products | /products :: $1 | /products/$1 :: Item $2
```

#### Display Limits

| Config key | Type | Purpose |
|---|---|---|
| `limit_segment_display` | bool | Enable segment count limiting |
| `segment_display_limit` | int | Maximum number of segments to show (trims oldest middle segments, preserves Home) |
| `segment_display_minimum` | int | Minimum segments required before showing breadcrumb at all |

#### Truncation

| Config key | Type | Purpose |
|---|---|---|
| `truncator_mode` | bool | Enable title truncation |
| `truncator_length` | int | Maximum character length per title |
| `truncator_dots` | bool | Append `...` after truncated titles |

#### Other

| Config key | Type | Purpose |
|---|---|---|
| `language_path_prefix_as_segment` | bool | On multilingual sites, show the language prefix (`/en`) as a breadcrumb segment |
| `term_hierarchy` | bool | Add all taxonomy term parents in the breadcrumb for the current term |
| `absolute_paths` | bool | Generate absolute URLs for all breadcrumb links |
| `add_structured_data_json_ld` | bool | Output `BreadcrumbList` JSON-LD in the `<head>` |

## Common Mistakes

- Configuring `replaced_titles` without enabling `title_from_page_when_available` — replacements only match resolved titles, not URL slugs
- Setting `segment_display_minimum` to 2 and then wondering why the Home-only breadcrumb disappears — it is working as configured
- Using `excluded_paths` with unescaped slashes — paths like `admin/content` must be written as `admin\/content`

## See Also

- Feature overview → [Easy Breadcrumb Module](easy-breadcrumb-module.md)
- SEO output → [Structured Data (SEO)](structured-data-seo.md)
- Reference: `modules/contrib/easy_breadcrumb/src/EasyBreadcrumbConstants.php`
- Reference: `modules/contrib/easy_breadcrumb/src/Form/EasyBreadcrumbGeneralSettingsForm.php`
