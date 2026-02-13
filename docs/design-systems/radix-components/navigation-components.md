---
description: Components for site navigation, wayfinding, and menu systems
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
| `classes` | array |  | Additional CSS classes |
| `breadcrumb_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the breadcrumb container |

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

**Slots:**
| Slot | Description |
|------|-------------|
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
- Three separate utility class props target different elements (nav, item, link)
- `fill` makes items equal width, `justify` makes them fill container proportionally
- Vertical alignment stacks items; conflicts with fill/justify options

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

### navbar
**Description:** A responsive navigation header. Includes support for branding, navigation, and collapse plugin.

**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `navbar_container_type` | [string, boolean] |  | Container type: `false`, `sm`, `md`, `lg`, `xl`, `xxl`, `fluid` |
| `navbar_container_utility_classes` | string |  | Container utility classes |
| `navbar_container_attributes` | Drupal\Core\Template\Attribute |  | Container HTML attributes |
| `navbar_theme` | string |  | Theme: `light`, `dark` |
| `placement` | string |  | Placement: `fixed-top`, `fixed-bottom`, `sticky-top` |
| `navbar_expand` | [boolean, string] |  | Expand breakpoint: `sm`, `md`, `lg`, `xl`, `xxl`, `false` |
| `attributes` | Drupal\Core\Template\Attribute |  | Navbar element HTML attributes |

**Slots:**
| Slot | Description |
|------|-------------|
| `branding` | Site branding content |
| `navigation` | Site navigation content |
| `navbar_toggler` | Mobile menu toggler button |

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
    navigation: main_menu
  }
%}
```

**Gotchas:**
- `navbar_container_type: false` removes the container wrapper entirely
- `navbar_expand` controls mobile breakpoint; `false` means always collapsed
- Container attributes are separate from navbar attributes (two different elements)
- Must provide toggler slot for mobile functionality or it won't collapse properly

### navbar-brand
**Description:** Navbar branding component for logo and site name.

**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `navbar_brand_utility_classes` | array | [] | Additional utility classes |
| `attributes` | Drupal\Core\Template\Attribute |  | HTML attributes |

**Slots:**
| Slot | Description |
|------|-------------|
| `logo` | Site logo content |

**Usage Example:**
```twig
{%
  include 'radix:navbar-brand' with {
    text: site_name,
    slogan: site_slogan,
    image: site_logo,
    path: path('<front>'),
    alt: site_name ~ ' logo'
  }
%}
```

**Gotchas:**
- Config variables (`text`, `path`, `image`) aren't formal props but are documented as template config
- Image dimensions (`width`, `height`) are config options, not props
- Typically used within the `navbar` component's branding slot

### pagination
**Description:** Display pagination to indicate a series of related content exists across multiple pages.

**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `size` | string |  | Size: `sm`, `lg` (empty for default) |
| `alignment` | string |  | Alignment: `start`, `end`, `center`, `vertical` |
| `show_first` | boolean |  | Display first page link |
| `show_last` | boolean |  | Display last page link |
| `show_ellipsis` | boolean |  | Display ellipsis between page ranges |
| `pagination_utility_classes` | array |  | Additional utility classes |
| `items` | array |  | Pagination items with href, text, classes, and attributes |

**Slots:**
| Slot | Description |
|------|-------------|
| `pagination_next` | Next page link |
| `pagination_previous` | Previous page link |

**Usage Example:**
```twig
{%
  include 'radix:pagination' with {
    size: 'lg',
    alignment: 'center',
    show_first: true,
    show_last: true,
    items: pagination_items,
    pagination_next: next_link,
    pagination_previous: prev_link
  }
%}
```

**Gotchas:**
- `items` structure must include specific keys: `href`, `text`, `pagination_classes`, `pagination_utility_classes`, `pagination_attributes`
- Previous/next slots are separate from items array (rendered specially)
- Ellipsis display controlled by prop, but ellipsis generation logic must be in your items array

## Common Mistakes

- **Mixing navigation types**: Don't use `nav` component for primary site header navigation; use `navbar` instead
- **Container confusion**: Navbar has separate attributes for container vs navbar element; apply classes to correct prop
- **Active state management**: Components don't automatically detect active state; you must pass `is_active: true` based on route
- **Mobile responsiveness**: Navbar requires toggler slot and proper expand breakpoint or mobile menu won't work
- **Breadcrumb current page**: Always set last breadcrumb item url to `null` to prevent self-linking
- **Pagination item structure**: Items array must match expected structure (href, text, attributes) or rendering fails

## See Also

- Bootstrap 5.3 Nav documentation: https://getbootstrap.com/docs/5.3/components/navs-tabs/
- Bootstrap 5.3 Navbar documentation: https://getbootstrap.com/docs/5.3/components/navbar/
- Bootstrap 5.3 Breadcrumb documentation: https://getbootstrap.com/docs/5.3/components/breadcrumb/
- Bootstrap 5.3 Pagination documentation: https://getbootstrap.com/docs/5.3/components/pagination/
- [Layout Components](layout-components.md)
- [UI Components](ui-components.md)
