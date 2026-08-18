---
description: "Components for site navigation, wayfinding, and menu systems"
tldr: "Components for site navigation, wayfinding, and menu systems. Use these for breadcrumbs, tabs, navigation menus, navbars, and pagination across multiple pages."
---

# Navigation Components

## When to Use

> Components for site navigation, wayfinding, and menu systems. Use these for breadcrumbs, tabs, navigation menus, navbars, and pagination across multiple pages.

## Items

### breadcrumb
**Description:** Indicate the current page's location within a navigational hierarchy that automatically adds separators via CSS.

**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `breadcrumb` | array |  | Array of breadcrumb items with url structure |
| `classes` | array |  | **Dead — not honoured by `breadcrumb.twig`.** The template builds its own `breadcrumb_classes` at line 11 and never reads `classes`. Use `breadcrumb_utility_classes` instead. |
| `breadcrumb_attributes` | Drupal\Core\Template\Attribute |  | **Dead — not honoured by `breadcrumb.twig`.** Line 15 overwrites it with `attributes ?: create_attribute()`. Pass `attributes` instead. |

**Slots:**
No slots defined.

**Usage Example:**
```twig
{%
  include 'radix:breadcrumb' with {
    breadcrumb: [
      { text: 'Home', url: '/home' },
      { text: 'Blog', url: '/blog' },
      { text: 'Post Title', url: null }
    ],
    breadcrumb_utility_classes: ['my-custom-class']
  }
%}
```

**Gotchas:**
- Current page (last item) should have `url: null` to prevent self-linking
- Separators are added automatically via CSS, don't add them manually
- Use `breadcrumb_utility_classes` config (not `classes` prop) for utility classes

---

### local-tasks
**Description:** Theme override for rendering primary and secondary local tasks as tabs and pills respectively.

**Status:** experimental

**Props:**
No props defined.

**Slots:**
| Slot | Description |
|------|-------------|
| `primary` | Primary tasks as main navigation items, displayed as tabs |
| `secondary` | Secondary tasks, sub-navigation items |

**Usage Example:**
```twig
{%
  include 'radix:local-tasks' with {
    primary: primary_local_tasks,
    secondary: secondary_local_tasks
  }
%}
```

**Gotchas:**
- Designed specifically for Drupal's local task system (Edit, View, etc. tabs)
- Primary tasks render as tabs, secondary as pills (styling is fixed)
- No prop control over styling, uses Drupal's task structure directly

---

### nav
**Description:** Flexible navigation with several styles, alignments and fill options.

**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `alignment` | string |  | Navigation alignment: `left`, `right`, `center`, `vertical` |
| `style` | string |  | Navigation style: `tabs`, `pills` |
| `fill` | string |  | Fill behavior: `fill`, `justify` |
| `nav_utility_classes` | array |  | Classes for nav container |
| `nav_item_utility_classes` | array |  | Classes for each nav item |
| `nav_link_utility_classes` | array |  | Classes for each nav link |
| `attributes` | Drupal\Core\Template\Attribute |  | HTML attributes |
| `items` | array |  | **Required.** Drupal menu-link items. `nav.twig:41` wraps the entire template in `{% if items %}`, so without it the component renders nothing at all. Absent from the YAML |
| `heading` | object |  | `{ text, level }`; renders a heading above the list (`nav.twig:42-48`). Absent from the YAML |
| `heading_level` | string | h2 | Tag for that heading; falls back to `heading.level`, then `h2` (`nav.twig:39`) |
| `heading_attributes` | Drupal\Core\Template\Attribute |  | Attributes for the heading. `nav.twig:43` calls `.addClass()` on it with no fallback, so it must be supplied whenever `heading` is. Absent from the YAML |
| `heading_utility_classes` | array | [] | Utility classes for the heading (`nav.twig:38`) |
| `dropdown_direction` | string | dropend | `dropstart` or `dropend`. Not used by `nav.twig` itself — it rides the inherited context into `radix:dropdown-menu`, which reads it (`dropdown-menu.twig:24`) for nested items |

**Slots:**
| Slot | Description |
|------|-------------|
| `nav_heading` | The heading text; rendered only when `heading` is passed |
| `nav_items` | Navigation items |

**Usage Example:**
```twig
{%
  include 'radix:nav' with {
    alignment: 'right',
    style: 'pills',
    fill: 'justify',
    items: links,
    nav_link_utility_classes: ['text-dark'],
    nav_item_utility_classes: ['px-2']
  }
%}
```

**Gotchas:**
- `items` gates the whole component: `nav.twig:41` renders nothing — not even the `<ul>` — when it is empty. It is not in the `.component.yml`, so nothing warns you
- Three separate utility class props target different elements (nav, item, link)
- `fill` makes items equal width, `justify` makes them fill container proportionally
- Vertical alignment stacks items; conflicts with fill/justify options

---

### nav-item
**Description:** A single navigation item component.

**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `is_active` | boolean |  | Flag for active route highlighting |
| `container` | string |  | Container type: `fixed`, `fluid` |
| `color` | string |  | Color scheme: `light`, `dark` |
| `placement` | string |  | Placement: `fixed-top`, `fixed-bottom`, `sticky-top` |
| `navbar_expand` | [boolean, string] |  | Expand breakpoint: `sm`, `md`, `lg`, `xl` |
| `nav_item_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes |

**Slots:**
| Slot | Description |
|------|-------------|
| `link` | Renderable array representing the link |

**Usage Example:**
```twig
{%
  include 'radix:nav-item' with {
    is_active: true,
    link: {
      '#url': '/about',
      '#title': 'About Us'
    }
  }
%}
```

**Gotchas:**
- Usually used via the `nav` component rather than standalone
- Props like `container` and `placement` are navbar-specific (naming confusion)
- Active state styling requires Bootstrap's `.active` class applied automatically

---

### navbar
**Description:** A responsive navigation header. Includes support for branding, navigation, and collapse plugin.

**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `navbar_container_type` | [string, boolean] |  | Container type: `false`, `sm`, `md`, `lg`, `xl`, `xxl`, `fluid` |
| `navbar_container_utility_classes` | array | [] | Container utility classes. Must be an **array** — `navbar.twig:30` merges it into the container class list |
| `navbar_container_attributes` | Drupal\Core\Template\Attribute |  | Container HTML attributes |
| `navbar_theme` | string |  | Theme: `light`, `dark` |
| `placement` | string |  | Placement: `fixed-top`, `fixed-bottom`, `sticky-top` |
| `navbar_expand` | [boolean, string] | lg | Expand breakpoint: `sm`, `md`, `lg`, `xl`, `xxl`, `false`. Omitting it yields `.navbar-expand-lg`; pass `false` for an always-collapsed navbar |
| `attributes` | Drupal\Core\Template\Attribute |  | **Dead — not honoured by `navbar.twig`.** The template reads `nav_attributes` (line 19) and never `attributes`. Pass `nav_attributes` instead. |

**Slots:**
| Slot | Description |
|------|-------------|
| `branding` | Site branding content |
| `navbar_toggler` | Mobile menu toggler button |
| `left` | Left side of the collapsed nav area |
| `right` | Right side of the collapsed nav area |

`navbar.component.yml` also declares a `navigation` slot, but `navbar.twig` never renders it — the collapse area is split into `left` and `right` instead. Passing `navigation` is a silent no-op.

**Usage Example:**
```twig
{%
  include 'radix:navbar' with {
    navbar_container_type: 'fluid',
    placement: 'sticky-top',
    navbar_theme: 'dark',
    navbar_expand: 'md',
    navbar_utility_classes: ['bg-dark'],
    branding: site_branding,
    left: main_menu,
    right: secondary_menu
  }
%}
```

**Gotchas:**
- **There is no `navigation` slot.** The YAML declares one, the Twig never prints it. Content goes in `left` and `right`, which are the two blocks inside `.navbar-collapse`.
- `navbar_container_type: false` removes the container wrapper entirely
- `navbar_expand` controls mobile breakpoint; `false` means always collapsed
- Container attributes are separate from navbar attributes (two different elements)
- You do **not** need to supply `navbar_toggler`: the block ships a working default button wired to `data-bs-toggle="collapse"` / `data-bs-target=".navbar-collapse"`. Override it only to change that markup, and keep those attributes if you do

---

### navbar-brand
**Description:** Navbar branding component for logo and site name.

**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `navbar_brand_utility_classes` | array | [] | Additional utility classes. Must be an **array** — `navbar-brand.twig:18` does `navbar_brand_utility_classes|join(' ')` and interpolates the result straight into the `class` attribute. |
| `attributes` | Drupal\Core\Template\Attribute |  | **Dead — not honoured by `navbar-brand.twig`.** The template writes `class` and `aria-label` literally (lines 21 and 43) and never prints `attributes`. Use `navbar_brand_utility_classes` for classes; anything else needs a component override. |

**Slots:**
| Slot | Description |
|------|-------------|
| `logo` | Site logo content |

**Usage Example:**
```twig
{%
  include 'radix:navbar-brand' with {
    text: site_name,
    site_slogan: site_slogan,
    image: site_logo,
    path: path('<front>'),
    alt: site_name ~ ' logo'
  }
%}
```

**Gotchas:**
- There is no `slogan` prop — the template reads `site_slogan` (`navbar-brand.twig:29,36`). Passing `slogan` renders nothing
- Config variables (`text`, `path`, `image`) aren't formal props but are documented as template config
- Image dimensions (`width`, `height`) are config options, not props
- Typically used within the `navbar` component's branding slot

---

### pagination
**Description:** Display pagination to indicate a series of related content exists across multiple pages.

**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `size` | string |  | Size: `sm`, `lg` (empty for default) |
| `alignment` | string |  | Alignment: `start`, `end`, `center`, `vertical` |
| `show_first` | boolean | true | Display first page link. On by default; pass `false` to hide |
| `show_last` | boolean | true | Display last page link. On by default; pass `false` to hide |
| `show_ellipsis` | boolean | true | Display ellipsis between page ranges. On by default; pass `false` to hide |
| `pagination_utility_classes` | array |  | Additional utility classes |
| `items` | object |  | **Drupal's pager structure, not a flat list.** The keys `pagination.twig` reads are `items.first`, `items.previous`, `items.pages` (keyed by page number), `items.next`, `items.last` and `items.current`; each of first/previous/next/last is `{ href, text, attributes }`. A falsy `items` renders nothing (`pagination.twig:35`) |
| `ellipses` | object |  | `ellipses.previous` / `ellipses.next` booleans; gate the two "…" items together with `show_ellipsis` (`pagination.twig:62,95`) |
| `current` | integer |  | Current page key; marks the matching `items.pages` entry active (`pagination.twig:71`) |
| `attributes` | Drupal\Core\Template\Attribute |  | Attributes for the wrapping `<nav>` (`pagination.twig:19`) |

**Slots:**
| Slot | Description |
|------|-------------|
| `pagination_next` | Next page link. A Twig **block** with hardcoded markup (`pagination.twig:105`); it renders only when `items.next` exists, and passing `pagination_next` as a variable does nothing. Override it with `{% embed %}` |
| `pagination_previous` | Previous page link. Same: a block at `pagination.twig:52`, gated on `items.previous` |

**Usage Example:**
```twig
{%
  include 'radix:pagination' with {
    size: 'lg',
    alignment: 'center',
    show_first: true,
    show_last: true,
    items: items,
    ellipses: ellipses,
    current: current
  }
%}
```

**Gotchas:**
- `items` is Drupal's pager array (`first`, `previous`, `pages`, `next`, `last`), not a flat list. The `href` / `text` / `pagination_classes` / `pagination_attributes` shape in the `.component.yml` is not what the template reads — and that YAML block is indented outside `props:`, so `items` is not even a declared prop
- `pagination_next` and `pagination_previous` are Twig blocks, not variables: passing them as props is inert, and their content appears only when `items.next` / `items.previous` exist
- Ellipsis display controlled by prop, but ellipsis generation logic must be in your items array

---

## Common Mistakes
- **Mixing navigation types**: Don't use `nav` component for primary site header navigation; use `navbar` instead
- **Container confusion**: Navbar has separate attributes for container vs navbar element; apply classes to correct prop
- **Active state management**: Components don't automatically detect active state; you must pass `is_active: true` based on route
- **Mobile responsiveness**: Navbar requires toggler slot and proper expand breakpoint or mobile menu won't work
- **Breadcrumb current page**: Always set last breadcrumb item url to `null` to prevent self-linking
- **Pagination item structure**: `items` must be Drupal's pager structure (`first`, `previous`, `pages`, `next`, `last`); a flat list of links renders an empty pager

## See Also
- Bootstrap 5.3 Nav documentation: https://getbootstrap.com/docs/5.3/components/navs-tabs/
- Bootstrap 5.3 Navbar documentation: https://getbootstrap.com/docs/5.3/components/navbar/
- Bootstrap 5.3 Breadcrumb documentation: https://getbootstrap.com/docs/5.3/components/breadcrumb/
- Bootstrap 5.3 Pagination documentation: https://getbootstrap.com/docs/5.3/components/pagination/
- [Layout Components](layout-components.md)
- [UI Components](ui-components.md)
