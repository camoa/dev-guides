---
description: Components for HTML structure, page layout, and regions
---

# Page Structure Components

## When to Use

> Components for HTML structure, page layout, and regions. Use these for rendering the complete HTML document, page wrapper, regions, and block wrappers in Drupal templates.

Components for overall page layout, regions, and structural wrappers. These are the foundational components that create the skeleton of every Drupal page in Radix.

### Items

#### html
**Description:** This provides structure for an entire HTML document, from DOCTYPE declaration to closing HTML tag.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `doc_lang` | string | en | Defines the language used in the HTML document. Default language is English (en). |
| `body_classes` | array | [] | An array of utility classes applied to the body of the HTML document. |
| `body_utility_classes` | array | [] | An array of utility classes for general use across the HTML document. |
| `attributes` | Drupal\Core\Template\Attribute |  |  |

**Slots:**
| Slot | Description |
|------|-------------|
| `head_start` | Serves as a container for metadata (data about data) and is placed between the `<head>` tags. |
| `head_end` | Optional. Can contain information or elements to be included at the end of the head. |
| `body_start` | Defines the document's body and contains all the contents of an HTML document, such as text, hyperlinks, images, tables, lists, etc. |
| `body_end` | Optional. Can contain information or elements to be included at the end of the document. |

**Usage Example:**
```twig
{%
  embed "radix:html" with {
    attributes: { class: ['custom-class'], id: 'custom-page-id' },
    doc_lang: 'en',
    body_utility_classes: ['overflow-hidden']
 }
%}
  {% block body_end %}
    <!-- JS code that needs to run at the end of the body tag -->
  {% endblock %}
{% endembed %}
```

**Gotchas:**
- This component is typically only used in html.html.twig template overrides, not in node/block templates
- Use `embed` instead of `include` when you need to populate slots
- The `logged_in`, `root_path`, and `node_type` variables are auto-populated by Drupal's preprocess, not passed as props

#### page
**Description:** The main page component that gives the structural outline for every page.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `page_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the page component. |
| `page_utility_classes` | array |  | Additional utility classes added to the page component. |

**Slots:**
| Slot | Description |
|------|-------------|
| `page_navigation` | The navigation section of the page. |
| `page_content` | The main content area of the page. |
| `page_footer` | The footer section of the page, contains information that appears on the bottom of each page. |

**Usage Example:**
```twig
{%
  embed 'radix:page' with {
    page_attributes: attributes.addClass('custom-page'),
    page_utility_classes: ['d-flex', 'flex-column', 'min-vh-100']
  }
%}
  {% block page_navigation %}
    {% include 'radix:page-navigation' %}
  {% endblock %}
  {% block page_content %}
    {{ page.content }}
  {% endblock %}
{% endembed %}
```

**Gotchas:**
- The page component expects nested page-navigation, page-content, and page-footer components
- Used in page.html.twig template, not for individual nodes
- Don't confuse `page_utility_classes` (for structural styling) with content-specific classes

#### page-content
**Description:** The main content component of a page, including a header section and main content area.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `page_header_container_type` | ['string', 'boolean'] |  | container type. Enum: `false, sm, md, lg, xl, xxl, fluid` |
| `page_header_container_utility_classes` | array |  | Additional utility classes added to the header section of the main content area. |
| `page_content_container_type` | ['string', 'boolean'] |  | container type. Enum: `false, sm, md, lg, xl, xxl, fluid` |
| `page_content_container_utility_classes` | array |  | Additional utility classes added to the main content area of the page. |
| `content_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the main content area of the page. |
| `page_main_utility_classes` | array |  | Additional utility classes added to the main content area of the page. |
| `page_header_container_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the header section of the main content area. |
| `page_content_container_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the main content area of the page. |

**Slots:**
| Slot | Description |
|------|-------------|
| `page_header` | The header section of the main content area. |
| `page_content` | The actual content within the main content area. |

**Usage Example:**
```twig
{%
  embed 'radix:page-content' with {
    content_attributes: content_attributes,
    page_header_container_type: false,
    page_header_container_utility_classes: ['my-5'],
    page_content_container_type: 'xxl',
    page_content_container_utility_classes: ['py-4']
  }
%}
  {% block page_header %}
    {{ page.header }}
  {% endblock %}
  {% block page_content %}
    {{ page.content }}
  {% endblock %}
{% endembed %}
```

**Gotchas:**
- Setting container type to `false` removes the Bootstrap container wrapper entirely (full-width content)
- The `page_header_container_type` and `page_content_container_type` can have different values for asymmetric layouts
- Don't confuse `content_attributes` (wrapper attributes) with the actual page content

#### page-footer
**Description:** Component for the page footer.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the footer component. |
| `footer_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes specifically for the footer. |
| `footer_utility_classes` | array |  | Additional utility classes to add to the footer. |

**Slots:**
| Slot | Description |
|------|-------------|
| `page_inner_footer` | The main contents of the footer. |

**Usage Example:**
```twig
{%
  embed 'radix:page-footer' with {
    footer_utility_classes: ['bg-dark', 'text-light', 'py-5']
  }
%}
  {% block page_inner_footer %}
    {{ page.footer }}
  {% endblock %}
{% endembed %}
```

**Gotchas:**
- Both `attributes` and `footer_attributes` are available; `footer_attributes` is more specific
- Typically embedded in the page component's `page_footer` slot
- Footer regions must be defined in your theme's .info.yml file

#### page-navigation
**Description:** The navigation component of a page, containing the site branding and main navigation.
**Status:** experimental

**Props:**
No props defined.

**Slots:**
| Slot | Description |
|------|-------------|
| `branding` | The branding section of the navigation. |
| `left` | The left side of the navigation. |
| `right` | The right side of the navigation. |

**Usage Example:**
```twig
{%
  embed 'radix:page-navigation'
%}
  {% block branding %}
    {{ page.header }}
  {% endblock %}
  {% block left %}
    {{ page.primary_menu }}
  {% endblock %}
  {% block right %}
    {{ page.secondary_menu }}
  {% endblock %}
{% endembed %}
```

**Gotchas:**
- No props means no customization via parameters; use slots for all content
- The left/right slots don't automatically create a navbar structure; you may need additional nav components
- Region placement depends on your theme's layout configuration

#### page-title
**Description:** The Title component is responsible for rendering the page's main heading using the h1 HTML tag.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `display` | string |  | When you need a heading to stand out, consider using a display heading—a larger, slightly more opinionated heading style. Enum: `display-1, display-2, display-3, display-4, display-5, display-6` |
| `page_title_utility_classes` | array | [] | An array of utility classes. Use to add extra Bootstrap utility classes or custom CSS classes over to this component. |
| `title_attributes` | Drupal\Core\Template\Attribute |  |  |
| `title_prefix` | array |  | An array of renderable elements that are displayed before the title. |
| `title_suffix` | array |  | An array of renderable elements that are displayed after the title. |

**Slots:**
No slots defined.

**Usage Example:**
```twig
{%
  include 'radix:page-title' with {
    title: title,
    display: 'display-3',
    page_title_utility_classes: ['text-primary', 'mb-4'],
    title_attributes: title_attributes,
    title_prefix: title_prefix,
    title_suffix: title_suffix
  }
%}
```

**Gotchas:**
- The `title` variable itself comes from Drupal's page variables, not from props
- `title_prefix` and `title_suffix` are typically populated by modules (e.g., contextual links), don't override unless necessary
- Display classes (`display-1` through `display-6`) are much larger than regular h1 styling

#### region
**Description:** The structure and necessary styling for displaying a Drupal region.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `attributes` | Drupal\Core\Template\Attribute |  |  |

**Slots:**
| Slot | Description |
|------|-------------|
| `region_content` | The block of the main content. |
| `content` | The content of the region. |

**Usage Example:**
```twig
{%
  embed 'radix:region' with {
    attributes: attributes.addClass('sidebar').setAttribute('role', 'complementary')
  }
%}
  {% block content %}
    {{ content }}
  {% endblock %}
{% endembed %}
```

**Gotchas:**
- Both `region_content` and `content` slots exist; use `content` for most cases
- Region templates are called automatically by Drupal for each defined region
- The `attributes` typically include region-specific classes automatically added by Drupal

### Common Mistakes
- **Using include instead of embed for slot-based components**: page, page-content, page-footer, page-navigation, html, and region all use slots and require `embed` + `block` syntax
- **Forgetting container types control Bootstrap wrappers**: Setting container type to `false` removes the wrapper entirely (useful for full-width hero sections)
- **Mixing page structure components in wrong contexts**: These components have a hierarchy (html → page → page-content/page-navigation/page-footer → region) and should not be used arbitrarily in node or block templates
- **Overriding auto-populated Drupal variables**: Variables like `logged_in`, `root_path`, `title_prefix`, and `title_suffix` are set by Drupal's preprocess functions and shouldn't be manually overridden

### See Also
- Navigation Components section for navbar, nav, menu components
- Layout Components section for container and grid components
- Form Components section for form structure elements
