---
description: Components for displaying Drupal content entities, fields, media, and user profiles
---

# Content Display Components

## When to Use

> Components for displaying Drupal content entities, fields, media, and user profiles. Use these when rendering nodes, blocks, taxonomy terms, comments, media items, images, or user profiles in various view modes.

Components for displaying Drupal content entities, fields, media, and user profiles. Use these when rendering nodes, blocks, taxonomy terms, comments, media items, images, or user profiles in various view modes.

### Items

#### node
**Description:** A component template for rendering node entities in Drupal.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `title_attributes` | Drupal\Core\Template\Attribute | | Custom HTML attributes for the node title |
| `attributes` | Drupal\Core\Template\Attribute | | Custom HTML attributes for the node container |
| `content_attributes` | Drupal\Core\Template\Attribute | | Custom HTML attributes for the node content area |
| `title_prefix` | array | | Additional output displayed before the main title tag |
| `title_suffix` | array | | Additional output displayed after the main title tag |
| `display_submitted` | boolean | | Controls visibility of author and date information |
| `author_picture` | string | | URL or path for the author picture |
| `author_name` | string | | Name of the author |
| `date` | string | | Submission date |
| `metadata` | string | | Metadata associated with the node |
| `label` | string | | Label of the node |
| `url` | string\|null | | URL to the node |
| `node_classes` | array | | Classes added to the node container |
| `node_content_classes` | array | | Classes added to the node content area |
| `node_utility_classes` | array | | Bootstrap utility classes for the node |
| `author_utility_classes` | array | | Bootstrap utility classes for the author |
| `node_content_utility_classes` | array | | Bootstrap utility classes for the node content |

**Slots:**
| Slot | Description |
|------|-------------|
| `node_title` | The title of the node |
| `node_metadata` | The metadata of the node |
| `node_title_prefix` | Additional output before the main title tag |
| `node_title_suffix` | Additional output after the main title tag |
| `node_content` | The main content block |
| `content` | The main contents of the node |

**Usage Example:**
```twig
{%
  include 'radix:node' with {
    label: node.label,
    url: node.url,
    display_submitted: true,
    author_name: node.owner.name,
    date: node.created|format_date('medium'),
    content: content,
    node_utility_classes: ['mb-4']
  }
%}
```

**Gotchas:**
- Use `content|without('field_example')` to exclude specific fields from rendering
- `display_submitted` must be true for author/date info to appear
- `node_utility_classes` and `node_content_utility_classes` serve different purposes; use the former for outer spacing/layout, latter for content styling

#### block
**Description:** Customizable block component for displaying various types of content with configurable layout, label, and styling options.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `id` | string | | ID |
| `bundle` | string | | Bundle |
| `layout` | string | default | Determines the layout of the block |
| `plugin_id` | string | | The ID of the block implementation |
| `label` | string\|null\|boolean | | The configured label of the block if visible |
| `title_prefix` | array | | Title prefix |
| `title_suffix` | array | | Title suffix |
| `configuration` | object | | A list of the block's configuration values |
| `attributes` | Drupal\Core\Template\Attribute | | HTML attributes for the main container tag |
| `title_attributes` | Drupal\Core\Template\Attribute | | HTML attributes for the main title tag |
| `content_attributes` | Drupal\Core\Template\Attribute | | HTML attributes for the main content tag |
| `block_html_tag` | string | | The HTML tag for the block |
| `block_classes` | array | | Classes to be added to the block |
| `block_content_classes` | array | | Classes to be added to the block content area |
| `block_utility_classes` | array | | Bootstrap utility classes for the block |
| `block_content_utility_classes` | array | | Bootstrap utility classes for the block content area |

**Slots:**
| Slot | Description |
|------|-------------|
| `block_label` | Slot for the block label |
| `block_content` | Slot for the block content |
| `content` | Default content for Block |

**Usage Example:**
```twig
{%
  include 'radix:block' with {
    block_html_tag: 'aside',
    label: 'Recent Posts',
    content: content,
    block_utility_classes: ['bg-light', 'p-3', 'mb-4'],
    block_content_utility_classes: ['list-unstyled']
  }
%}
```

**Gotchas:**
- `label` can be string, null, or boolean; set to false to hide it entirely
- Separate utility class arrays for block wrapper vs. content allow granular styling control
- `block_html_tag` defaults to semantic tags based on context; override for specific HTML structure

#### field
**Description:** Field container divisions with attributes.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `label_display` | string | | Display the label of the field |
| `field_utility_classes` | array | [] | Bootstrap utility classes for the field wrapper |
| `field_title_utility_classes` | array | [] | Bootstrap utility classes for the field title |
| `field_item_utility_classes` | array | [] | Bootstrap utility classes for each field item |
| `title_attributes` | Drupal\Core\Template\Attribute | | HTML attributes for the title |
| `attributes` | Drupal\Core\Template\Attribute | | HTML attributes for the containing element |

**Slots:**
No slots defined.

**Usage Example:**
```twig
{%
  include 'radix:field' with {
    label_hidden: false,
    multiple: true,
    label: 'Tags',
    items: content.field_tags['#items'],
    field_utility_classes: ['mb-3'],
    field_item_utility_classes: ['badge', 'bg-secondary', 'me-1']
  }
%}
```

**Gotchas:**
- Use theme hook suggestions (e.g., `field--node--field-foo--article.html.twig`) for field-specific overrides
- `field_item_utility_classes` applies to each item wrapper; useful for multi-value fields with badges or grid layouts
- Access items via `content.field_name['#items']` in preprocessors; in templates use `items` variable

#### field-comment
**Description:** The structure and necessary styling for displaying a field comment section.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `field_comment_attributes` | Drupal\Core\Template\Attribute | | Attributes for the field comment section |
| `title_prefix` | array | | Prefix for the title of the field comment section |
| `title_suffix` | array | | Suffix for the title of the field comment section |
| `comments` | string | | The comments for the field |
| `comment_form` | string | | The comment form |

**Slots:**
No slots defined.

**Usage Example:**
```twig
{%
  include 'radix:field-comment' with {
    comments: content.comment,
    comment_form: content.comment_form,
    field_comment_attributes: create_attribute().addClass('mt-4')
  }
%}
```

**Gotchas:**
- Automatically renders both comments list and form; no need to manually include form
- Comment threading handled by Drupal core; component focuses on styling wrapper

#### comment
**Description:** The structure and necessary styling for displaying a comment.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `attributes` | Drupal\Core\Template\Attribute | | HTML attributes for the comment wrapper |
| `content_attributes` | Drupal\Core\Template\Attribute | | HTML attributes for the comment content |
| `classes` | array | | Comment CSS Classes |
| `new_indicator_timestamp` | integer | | New Indicator Timestamp |
| `user_picture` | string | | User picture URL |
| `user_picture_alt` | string | | User Picture Alt Text |
| `submitted` | string | | Submitted Comment Information |
| `permalink` | string | | Permalink |
| `title` | string | | Comment Title |
| `title_prefix` | array | | Title Prefix |
| `title_suffix` | array | | Title Suffix |
| `title_attributes` | Drupal\Core\Template\Attribute | | HTML attributes for the title |
| `parent` | string | | Parent Comment |

**Slots:**
| Slot | Description |
|------|-------------|
| `content` | Content |

**Usage Example:**
```twig
{%
  include 'radix:comment' with {
    user_picture: author.user_picture.entity.uri.value,
    user_picture_alt: author.name.value,
    submitted: 'By ' ~ author_name ~ ' on ' ~ created|format_date('medium'),
    title: comment.subject.value,
    content: content
  }
%}
```

**Gotchas:**
- `new_indicator_timestamp` used by Drupal core to highlight new comments; component doesn't style this automatically
- Threading is managed via `parent` prop; ensure preprocessing handles nested comments correctly

#### media
**Description:** A theme override for a media item display in Drupal. This includes configurations for media type, published status, and view mode.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `media_type` | string | | The bundle classification of the media object (auto-generated, cleaned for class) |
| `is_published` | boolean | | Flag indicating whether media is published; adds "media--unpublished" class when false |
| `media_utility_classes` | array | | Bootstrap utility classes for the media item |
| `view_mode` | string | | The view mode classification (cleansed for class addition) |
| `media_attributes` | Drupal\Core\Template\Attribute | | Additional HTML attributes for the media item |

**Slots:**
| Slot | Description |
|------|-------------|
| `content` | The rendered media item content |
| `media_content` | Alias for content |

**Usage Example:**
```twig
{%
  include 'radix:media' with {
    media: media_item,
    content: content,
    view_mode: 'full',
    media_utility_classes: ['ratio', 'ratio-16x9']
  }
%}
```

**Gotchas:**
- `media_type` automatically generates classes like `media--image` or `media--video`; don't override manually
- Use `media_utility_classes` with Bootstrap ratio classes for responsive video embeds
- `is_published` check is preprocessed; unpublished media gets distinct styling class automatically

#### image
**Description:** A visually versatile image component with configurable attributes such as alignment, responsiveness, thumbnail style, and rounded edges.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `src` | string\|null | | The URL or path to the image file |
| `alt` | string\|null | | Alternative text for the image (essential for accessibility) |
| `title` | string\|null | | Title attribute for the image (tooltip) |
| `width` | string\|null\|integer | | Width of the image in pixels |
| `height` | string\|null\|integer | | Height of the image in pixels |
| `loading` | string\|null | auto | Image loading behavior: `auto`, `lazy`, or `eager` |
| `align` | string\|null | | Image alignment: `start`, `center`, or `end` |
| `responsive` | boolean | | When true, applies `.img-fluid` (max-width: 100%, height: auto) |
| `thumbnails` | boolean | | Adds `.img-thumbnail` for rounded 1px border appearance |
| `rounded` | boolean | | Applies `.rounded` class for rounded corners |
| `image_utility_classes` | array | [] | Additional Bootstrap utility or custom CSS classes |
| `image_attributes` | Drupal\Core\Template\Attribute | | HTML attributes for the image tag |

**Slots:**
No slots defined.

**Usage Example:**
```twig
{%
  include 'radix:image' with {
    src: file_url(node.field_image.entity.uri.value),
    alt: node.field_image.alt,
    responsive: true,
    loading: 'lazy',
    image_utility_classes: ['rounded', 'shadow-sm']
  }
%}
```

**Gotchas:**
- `responsive: true` makes images scale with parent width; always use for content images
- `loading: 'lazy'` defers loading until image approaches viewport; improves performance but may cause layout shift
- Don't combine `thumbnails: true` with `rounded: true`; use one or the other

#### figure
**Description:** Figure component with alignment options
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `figure_attributes` | Drupal\Core\Template\Attribute | | HTML attributes for the figure element |
| `figure_utility_classes` | array | | Additional classes for the figure component |
| `align` | string | | Alignment of the figure: `left`, `right`, or `center` |
| `image` | string | | The image of the figure component |
| `caption` | string | | The caption of the figure component |

**Slots:**
No slots defined.

**Usage Example:**
```twig
{%
  embed 'radix:figure' with {
    figure_utility_classes: ['my-3'],
    align: 'center',
    caption: 'A scenic view of the mountains at sunset.'
  }
%}
  {% block image %}
    <img src="/path/to/image.jpg" alt="Mountain sunset" class="img-fluid">
  {% endblock %}
{% endembed %}
```

**Gotchas:**
- Use `embed` instead of `include` to populate the `image` block; allows full control over image markup
- `align` uses float/margin utilities; may require clearfix on parent container
- Caption automatically uses `<figcaption>` tag with proper semantic HTML

#### heading
**Description:** All HTML headings, `<h1>` through `<h6>`, are available.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `heading_html_tag` | string | h1 | HTML header tag: `div`, `h1`, `h2`, `h3`, `h4`, `h5`, `h6` |
| `display` | string | | Display heading style: `display-1`, `display-2`, `display-3`, `display-4`, `display-5`, `display-6` |
| `heading_classes` | array | [] | Classes to add to the heading (merges display and utility classes) |
| `heading_utility_classes` | array | [] | Bootstrap utility or custom CSS classes |
| `heading_link_utility_classes` | array | [] | Bootstrap utility classes for the heading link |
| `title_link` | string\|boolean | | Link URL for the title |
| `heading_attributes` | Drupal\Core\Template\Attribute | | HTML attributes for the heading |
| `content` | string | | Content text for the heading |

**Slots:**
| Slot | Description |
|------|-------------|
| `heading_content` | Content text for the heading |

**Usage Example:**
```twig
{%
  include 'radix:heading' with {
    heading_html_tag: 'h2',
    display: 'display-4',
    content: 'Welcome to Our Site',
    title_link: '/about',
    heading_utility_classes: ['mb-3', 'text-primary']
  }
%}
```

**Gotchas:**
- `display` classes create larger, more prominent headings but don't change semantic level (still need correct `heading_html_tag`)
- When `title_link` is set, entire heading becomes a link; use `heading_link_utility_classes` to style
- Use `heading_html_tag: 'div'` when semantic heading isn't appropriate but heading style is needed

#### taxonomy
**Description:** A component template for rendering taxonomy entities in Drupal.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `title_attributes` | Drupal\Core\Template\Attribute | | Custom HTML attributes for the taxonomy title |
| `taxonomy_attributes` | Drupal\Core\Template\Attribute | | Custom HTML attributes for the taxonomy container |
| `content_attributes` | Drupal\Core\Template\Attribute | | Custom HTML attributes for the taxonomy content area |
| `title_prefix` | array | | Additional output displayed before the main title tag |
| `title_suffix` | array | | Additional output displayed after the main title tag |
| `name` | string | | Name of the taxonomy term |
| `url` | string | | URL to the taxonomy term |
| `taxonomy_classes` | array | | Classes added to the taxonomy container |
| `taxonomy_content_classes` | array | | Classes added to the taxonomy content area |
| `taxonomy_utility_classes` | array | | Bootstrap utility classes for the taxonomy |
| `taxonomy_content_utility_classes` | array | | Bootstrap utility classes for the taxonomy content |
| `page` | boolean | | Flag for the full page state |
| `view_mode` | string | | View mode: `full`, `teaser`, etc. |
| `heading_html_tag` | string | | HTML tag to use for the taxonomy term title |

**Slots:**
| Slot | Description |
|------|-------------|
| `taxonomy_title_prefix` | Additional output before the main title tag |
| `taxonomy_title` | The title of the taxonomy term |
| `taxonomy_title_suffix` | Additional output after the main title tag |
| `taxonomy_content` | Content |

**Usage Example:**
```twig
{%
  include 'radix:taxonomy' with {
    name: term.name.value,
    url: url,
    content: content,
    view_mode: 'full',
    taxonomy_utility_classes: ['mb-4']
  }
%}
```

**Gotchas:**
- Use `content|without('description')` to exclude term description from rendering
- `heading_html_tag` should match page hierarchy; default may not be appropriate for all contexts
- Term display differs significantly between `page: true` (term page) and `page: false` (term reference)

#### user
**Description:** This schema defines properties for rendering a user profile.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `attributes` | Drupal\Core\Template\Attribute | | HTML attributes for the user profile element |
| `view_mode` | string | | View mode for user display: `full`, `teaser`, etc. |
| `user_utility_classes` | array | [] | Additional utility classes for design or styling |

**Slots:**
| Slot | Description |
|------|-------------|
| `content` | The renderable content arrays for the user profile |

**Usage Example:**
```twig
{%
  include 'radix:user' with {
    view_mode: 'compact',
    content: content,
    user_utility_classes: ['d-flex', 'align-items-center', 'gap-3']
  }
%}
```

**Gotchas:**
- Component renders all fields in `content`; use `content|without('field_name')` to exclude specific fields
- User picture/avatar typically rendered as a field within `content`, not separate prop
- View modes must be defined in User entity display settings to work properly

### Common Mistakes

- **Confusing utility class arrays**: Components often have separate utility class props for wrapper vs. content (e.g., `node_utility_classes` vs. `node_content_utility_classes`). Use wrapper classes for spacing/layout, content classes for internal styling.
- **Ignoring theme hook suggestions**: Many components support granular template overrides (e.g., `field--node--field-foo.html.twig`). Don't override the base component when a specific suggestion would suffice.
- **Not using `content|without()`**: When you need to reorder or exclude fields, use `content|without('field_name')` rather than trying to unset in preprocess.
- **Hardcoding media/image paths**: Always use `file_url()` or proper render arrays for media/image sources; don't hardcode paths.
- **Mixing semantic and display styling**: Don't change `heading_html_tag` from `h2` to `h1` just to make text bigger; use `display` prop or utility classes instead.
- **Forgetting accessibility**: Image `alt` attributes are required for accessibility; media components should always include descriptive alt text.
- **Overriding preprocessing unnecessarily**: Many layout customizations can be achieved with utility class props; don't write custom preprocess functions when props exist.

### See Also

- **Forms & Inputs**: form, form-element, input, textarea, select, radios
- **Layout Components**: card, list-group, table
- **Bootstrap Documentation**: [Typography](https://getbootstrap.com/docs/5.3/content/typography/), [Images](https://getbootstrap.com/docs/5.3/content/images/), [Figures](https://getbootstrap.com/docs/5.3/content/figures/)
- **Drupal Theming**: [Template suggestions](https://www.drupal.org/docs/theming-drupal/twig-in-drupal/working-with-twig-templates#s-theme-hook-suggestions), [Preprocess functions](https://www.drupal.org/docs/theming-drupal/twig-in-drupal/drupal-10-twig-template-folder-structure-and-namespace#s-creating-custom-preprocess-hooks)

