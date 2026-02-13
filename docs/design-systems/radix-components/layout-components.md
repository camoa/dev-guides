---
description: Components for organizing and containing content in structured layouts
---

# Layout Components

## When to Use

> Components for organizing and containing content in structured layouts. These components help create interactive, collapsible, and organized content presentations including accordions, cards, carousels, modals, and data tables.

## Items

### accordion
**Description:** Accordion component for creating collapsible content sections. See Bootstrap Documentation: https://getbootstrap.com/docs/5.3/components/accordion/
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `title` | string |  | Title text for the accordion |
| `title_tag` | string | h2 | HTML tag for the title. Enum: `h1, h2, h3, h4, h5, h6` |
| `title_link` | string |  | URL for the title link |
| `title_attributes` | Drupal\Core\Template\Attribute |  | A list of HTML attributes for the button |
| `id` | ['integer', 'string'] | 0 | Unique ID for the accordion component |
| `flush` | boolean | false | True if the accordion has no background color or borders |
| `items` | array | [{}] | An array of items inside the accordion. Each item is an object that has title, content, and stay_open properties |
| `open_item_id` | integer | 0 | The index of the item that should be opened by default |
| `accordion_utility_classes` | array | [] | An array of utility classes for the accordion container |
| `accordion_item_utility_classes` | array | [] | An array of utility classes for accordion items |
| `accordion_attributes` | Drupal\Core\Template\Attribute |  | A list of HTML attributes for the accordion |
| `accordion_item_attributes` | Drupal\Core\Template\Attribute |  | A list of HTML attributes for the accordion items |

**Slots:**
| Slot | Description |
|------|-------------|
| `content` | Default content text for the accordion |

**Usage Example:**
```twig
{%
  include 'radix:accordion' with {
    title: 'FAQ Section',
    open_item_id: 1,
    title_tag: 'h2',
    flush: true,
    items: [
      {
        title: 'Item 1',
        title_tag: 'h3',
        content: 'Content 1',
        stay_open: true,
      },
      {
        title: 'Item 2',
        title_tag: 'h3',
        content: 'Content 2',
      },
    ],
  }
%}
```

**Gotchas:**
- Each item in the `items` array requires its own `title_tag` if you want consistency across accordion items
- The `stay_open` property on individual items allows multiple panels to be open simultaneously
- The `flush` option removes default borders and backgrounds, use when nesting in cards or colored containers

### card
**Description:** A flexible and extensible content container. It includes options for headers and footers, a wide variety of content, contextual background colors, and powerful display options. Replaces old panels, wells, and thumbnails from Bootstrap 3.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `card_attributes` | Drupal\Core\Template\Attribute |  | Attributes for the card |
| `card_body` | string |  | Card Body |
| `card_body_tag` | string | div | Card Body HTML Tag Enum: `div, section` |
| `card_title` | string |  | Card Title |
| `card_title_tag` | string | h3 | Card Title HTML Tag Enum: `div, h1, h2, h3, h4, h5, h6` |
| `card_subtitle` | string |  | Card Subtitle |
| `card_subtitle_tag` | string | h5 | Card Subtitle HTML Tag Enum: `h1, h2, h3, h4, h5, h6` |
| `card_text_tag` | string | p | Card Text HTML Tag Enum: `p, span, div` |
| `card_link_text` | string |  | Card Link Text |
| `card_link_url` | string |  | Card Link URL |
| `card_media` | string |  | Card Media |
| `card_image_src` | string |  | Card Image Source URL |
| `card_image_alt` | string |  | Card Image Alternative Text |
| `card_image_cap` | string |  | Image Caption Position Enum: `top, bottom` |
| `card_image_overlays` | boolean | false | Use Image Overlays? |
| `card_header` | string |  | Card Header |
| `card_footer` | string |  | Card Footer |
| `card_border` | boolean | false | Has Card Border? |
| `card_utility_classes` | array | [] | Utility classes for the card component |
| `card_title_utility_classes` | array | [] | Utility classes for the card title |
| `card_subtitle_utility_classes` | array | [] | Utility classes for the card subtitle |
| `card_header_utility_classes` | array | [] | Utility classes for the card header |
| `card_body_utility_classes` | array | [] | Utility classes for the card body |
| `card_text_utility_classes` | array | [] | Utility classes for the card text |
| `card_link_utility_classes` | array | [] | Utility classes for the card link |
| `card_footer_utility_classes` | array | [] | Utility classes for the card footer |
| `card_title_prefix` | array | [] | Additional output to be displayed before the title tag |
| `card_title_suffix` | array | [] | Additional output to be displayed after the title tag |

**Slots:**
| Slot | Description |
|------|-------------|
| `slot_card_image_top` | Slot for the top image of the card |
| `slot_card_image_bottom` | Slot for the bottom image of the card |
| `slot_card_body` | Slot for the body of the card |
| `slot_card_links` | Slot for the link section of the card |
| `slot_card_footer` | Slot for the footer of the card |

**Usage Example:**
```twig
{%
  include 'radix:card' with {
    card_title_tag: 'h4',
    card_title: label,
    card_header: 'Card Header',
    card_footer: 'The card footer',
    card_body: 'This is the card body',
    card_link_url: url,
    card_link_text: 'Read more...',
    card_utility_classes: ['col-4'],
    card_media: content.field_media,
  }
%}
```

**Gotchas:**
- Use `card_media` for rendered media entities instead of `card_image_src` when working with Drupal media
- The `card_image_overlays` option places content over the image, but requires careful text color contrast
- Card links styled with `card_link_utility_classes` can accept button classes like `btn-primary` for styled CTAs

### carousel
**Description:** Carousel component for creating image/content sliders. See Bootstrap Documentation: https://getbootstrap.com/docs/5.3/components/carousel/
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `carousel_theme` | string | light | The theme of the carousel. Enum: `dark, light` |
| `show_carousel_control` | boolean | true | Show carousel control |
| `show_carousel_indicator` | boolean | true | Show carousel indicator |
| `show_carousel_caption` | boolean | true | Show carousel caption |
| `autoplay` | ['string'] |  | Autoplay behavior. Enum: `carousel, true` |
| `id` | ['string'] | 0 | Unique ID for the carousel component |
| `carousel_utility_classes` | ['string', 'array'] |  | Utility classes for the carousel |
| `carousel_item_utility_classes` | ['string', 'array'] |  | Utility classes for carousel items |
| `carousel_caption_utility_classes` | ['string', 'array'] |  | Utility classes for carousel captions |
| `carousel_attributes` | Drupal\Core\Template\Attribute |  | Attributes for the carousel |
| `media_attributes` | Drupal\Core\Template\Attribute |  | Attributes for the carousel media |
| `item_image_attributes` | Drupal\Core\Template\Attribute |  | Attributes for the carousel item image |
| `items` | array | [{}] | An array of items, each with caption_title, caption_title_tag, carousel_caption, caption_content_tag, image_src, image_alt, media, interval |

**Slots:**
| Slot | Description |
|------|-------------|
| `carousel_indicators` | Slot for carousel indicators |
| `carousel_inner` | Slot for carousel inner |
| `carousel_caption` | Slot for carousel caption |
| `carousel_control` | Slot for carousel control |

**Usage Example:**
```twig
{%
  include 'radix:carousel' with {
    show_carousel_control: true,
    show_carousel_indicators: true,
    items: [
      {
        caption_title: 'Item 1',
        interval: 3000,
        image_src: 'https://picsum.photos/id/140/600.jpg',
        caption_content: 'Content 1',
      },
      {
        caption_title: 'Item 2',
        media: content.field_media,
        caption_content: 'Content 2',
      },
    ]
  }
%}
```

**Gotchas:**
- When `autoplay` is set to `'carousel'`, it autoplays on page load; when set to `'true'`, it only starts after user interaction
- Each item can have an `interval` property (in milliseconds) to control individual slide timing
- Use `media` property for Drupal media entities instead of `image_src` for better media handling

### collapse
**Description:** Collapse component for creating expandable/collapsible content sections. See Bootstrap Documentation: https://getbootstrap.com/docs/5.3/components/collapse/
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `title` | string |  | Title text for the collapse component |
| `button_html_tag` | string | button | The HTML tag to use for the button. Enum: `button, a` |
| `id` | ['integer', 'string'] | 0 | Unique ID for the collapse component |
| `direction` | string | vertical | Direction of the collapse. Enum: `vertical, horizontal` |
| `collapsed` | boolean | true | True if the collapse component is initially collapsed |
| `content` | string |  | Default content text for the collapse component |
| `collapse_content_classes` | array |  | Additional classes for the collapse content |
| `collapse_content_utility_classes` | array |  | Additional utility classes for the collapse content |

**Slots:**
| Slot | Description |
|------|-------------|
| `collapse_trigger` | Placeholder for the trigger, defaults to a button |
| `collapse_content` | Placeholder for content within the collapse component |

**Usage Example:**
```twig
{%
  include 'radix:collapse' with {
    title: 'Read More About This Topic',
    button_html_tag: 'button',
    id: 'collapse-123',
    direction: 'vertical',
    content: 'This is detailed content about the topic.',
  }
%}
```

**Gotchas:**
- The `id` prop must be unique on the page to avoid collision with Bootstrap's JavaScript targeting
- Setting `direction` to `horizontal` requires careful width management of the collapsed content container
- Unlike accordion, collapse components don't manage "exclusive open" behavior by default

### details
**Description:** Native HTML details element for creating disclosure widgets from which the user can obtain additional information or controls.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `title` | string |  | The title text for the details element |
| `required` | [boolean, 'null'] |  | Specifies if the details element is required |
| `attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the details element |
| `summary_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the summary element |
| `content_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the details content |
| `errors` | ['array', 'string', 'null'] |  | Any errors for this details element |
| `description` | string |  | The description of the details element |
| `children` | string |  | The rendered child elements of the details element |
| `value` | string |  | The value of the details element |

**Usage Example:**
```twig
{%
  include 'radix:details' with {
    title: 'More Information',
    description: 'Additional details about the topic.',
    children: 'Content that provides more information.',
    value: 'Some important value',
    required: true,
  }
%}
```

**Gotchas:**
- This is a native HTML `<details>` element, not a Bootstrap component, so it has different styling
- The `required` attribute is primarily for form contexts, not general content disclosure
- Browser default styling for `<details>` varies; apply custom styles for consistency

### list-group
**Description:** A series of list items that can be used to display a list of elements with a common style.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `list_group_html_tag` | string | ul | The HTML tag to use for the list group |
| `list_group_item_html_tag` | string | li | The HTML tag to use for the list group item |
| `list_group_item_variants` | string | [] | An array of variants to apply to the list group item |
| `list_group_utility_classes` | array | [] | Utility classes for the list group |
| `list_group_item_utility_classes` | array | [] | Utility classes for the list group item |
| `list_group_attributes` | Drupal\Core\Template\Attribute | {} | Attributes for the list group |
| `list_group_item_attributes` | Drupal\Core\Template\Attribute | {} | Attributes for the list group item |
| `list_group_items` | array |  | An array of items to display in the list group |
| `numbered` | boolean | false | Whether to display the list group items as numbered |
| `horizontal` | boolean | false | Whether to display the list group items horizontally |
| `horizontal_breakpoint` | string |  | The breakpoint at which to switch to horizontal. Enum: `sm, md, lg, xl, xxl` |

**Slots:**
| Slot | Description |
|------|-------------|
| `list_group_content` | Content for Group list |

**Usage Example:**
```twig
{%
  include 'radix:list-group' with {
    numbered: true,
    horizontal: true,
    horizontal_breakpoint: 'lg',
    list_group_item_variants: 'danger',
    list_group_items: [
      { value: 'First item' },
      { value: 'Second item' },
      { value: 'Third item' },
    ]
  }
%}
```

**Gotchas:**
- The `horizontal` option stacks items horizontally, but requires `horizontal_breakpoint` for responsive behavior
- `list_group_item_variants` applies color variants (primary, danger, etc.) to all items; use custom classes for per-item styling
- When using `numbered: true`, the HTML tag automatically becomes `<ol>` regardless of `list_group_html_tag` setting

### modal
**Description:** A Bootstrap Modal component for displaying content in a layered format, such as forms, messages, or custom content, with various customization options for size, behavior, and content.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `size` | string |  | Sets the size of the modal. Enum: `sm, lg, xl, fullscreen` |
| `id` | string |  | The unique identifier for the modal. Random ID generated if not specified |
| `title_id` | string |  | The unique identifier for the modal title. Random ID generated if not specified |
| `fullscreen_responsive` | string |  | Makes the modal fullscreen on specified breakpoints. Options: `sm, md, lg, xl, xxl` |
| `static_backdrop` | boolean |  | If true, clicking the backdrop does not close the modal |
| `vertically_centered` | boolean |  | If true, centers the modal vertically in the viewport |
| `scrollable` | boolean |  | If true, makes the modal's body scrollable if content overflows |
| `header` | string |  | Content for the modal's header, can be plain text or HTML |
| `body` | ['string', 'boolean'] |  | The main content of the modal |
| `footer` | string |  | Content for the modal's footer, typically buttons |
| `close_button` | boolean |  | If true, displays a close button in the modal header |
| `animation` | boolean |  | If true, applies a fade animation to the modal |
| `keyboard` | boolean |  | If true, allows closing the modal with the escape key |
| `modal_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the modal |
| `modal_header_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the modal header |
| `modal_body_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the modal body |
| `modal_dialog_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the modal dialog |
| `modal_title_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the modal title |
| `title_tag` | string | h5 | The HTML tag to use for the modal title |
| `modal_utility_classes` | array |  | Utility classes for the modal |
| `modal_dialog_utility_classes` | array |  | Utility classes for the modal dialog |
| `modal_header_utility_classes` | array |  | Utility classes for the modal header |
| `modal_title_utility_classes` | array |  | Utility classes for the modal title |
| `modal_body_utility_classes` | array |  | Utility classes for the modal body |
| `modal_footer_utility_classes` | array |  | Utility classes for the modal footer |

**Slots:**
| Slot | Description |
|------|-------------|
| `modal_header` | Slot for custom header content |
| `modal_body` | Slot for main body content |
| `modal_footer` | Slot for footer content |

**Usage Example:**
```twig
{%
  include 'radix:modal' with {
    id: 'myModal',
    size: 'lg',
    vertically_centered: true,
    header: 'Modal Title',
    body: 'This is the modal body content.',
    footer: '<button class="btn btn-primary">Save</button>',
    close_button: true,
  }
%}
```

**Gotchas:**
- Modal requires Bootstrap JavaScript to function; ensure Bootstrap bundle is loaded
- The `id` prop must be unique and match the `data-bs-target` attribute of the trigger button
- Setting `static_backdrop: true` prevents accidental closure but can trap users if no close button is provided

### offcanvas
**Description:** Build hidden sidebars into your project for navigation, shopping carts, and more with Bootstrap's offcanvas component.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `offcanvas_title_tag` | string | h5 | The tag for the offcanvas title. Enum: `h1, h2, h3, h4, h5, h6` |
| `offcanvas_title` | string |  | The offcanvas title |
| `offcanvas_title_utility_classes` | array | [] | Utility classes for the offcanvas title |
| `offcanvas_content` | string |  | The offcanvas content |
| `offcanvas_button_content` | string |  | The offcanvas button content |
| `show_by_default` | boolean | false | Whether the offcanvas is shown by default |
| `offcanvas_utility_classes` | array | [] | Utility classes for the offcanvas |
| `offcanvas_header_utility_classes` | array | [] | Utility classes for the offcanvas header |
| `offcanvas_body_utility_classes` | array | [] | Utility classes for the offcanvas body |
| `backdrop` | 'string' | true | Whether the offcanvas has a backdrop. Enum: `true, false, static` |
| `body_scrolling` | boolean | false | Whether the body scrolls when offcanvas is open |
| `offcanvas_id` | string |  | The offcanvas id |
| `placement` | string | start | The offcanvas placement. Enum: `start, end, top, bottom` |
| `close_button` | boolean | true | Whether the offcanvas has a close button |
| `offcanvas_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the offcanvas element |
| `offcanvas_title_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the offcanvas title |
| `offcanvas_body_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the offcanvas body |
| `offcanvas_button_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the offcanvas button |

**Slots:**
| Slot | Description |
|------|-------------|
| `offcanvas_header` | Offcanvas header |
| `offcanvas_body` | Offcanvas body |
| `offcanvas_toggler` | Offcanvas toggler |

**Usage Example:**
```twig
{%
  include 'radix:offcanvas' with {
    offcanvas_title_tag: 'h4',
    offcanvas_title: 'Shopping Cart',
    offcanvas_content: 'Cart items here.',
    offcanvas_button_content: 'View Cart',
    placement: 'end',
    close_button: true,
    body_scrolling: false,
  }
%}
```

**Gotchas:**
- The `placement` option controls which side the offcanvas slides from (start=left, end=right in LTR languages)
- Setting `body_scrolling: true` allows scrolling the main page while offcanvas is open, which can confuse users
- Unlike modal, offcanvas `backdrop: 'static'` still allows clicking away to close; use `data-bs-backdrop="static"` in attributes

### table
**Description:** Component for displaying tabular data with Bootstrap styling.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `caption` | [string, 'null'] |  | Caption for the table |
| `colgroups` | array |  | Column Group definitions |
| `header` | array |  | Header row data |
| `footer` | [array, string, 'null'] |  | Footer row data |

**Slots:**
| Slot | Description |
|------|-------------|
| `table_caption` | The caption of the table |
| `table_colgroup` | The column group of the table |
| `table_header` | The header of the table |
| `table_body` | The body of the table |
| `table_footer` | The footer of the table |

**Usage Example:**
```twig
{%
  include 'radix:table' with {
    table_utility_classes: ['table-striped', 'table-hover'],
    caption: 'User Data',
    header: header_cells,
    rows: row_data,
    footer: footer_cells,
    empty: 'No data available',
  }
%}
```

**Gotchas:**
- Bootstrap table variants (striped, bordered, hover) are applied via `table_utility_classes`, not props
- The `colgroups` prop is for defining column widths/styling, often overlooked but important for responsive tables
- Use `table-responsive` utility class to enable horizontal scrolling on small screens

## Common Mistakes

- **Forgetting unique IDs**: Modal, offcanvas, collapse, and accordion components require unique `id` props to function correctly with Bootstrap JavaScript
- **Mixing slots and props**: Many components accept both prop-based content (`card_body`) and slot-based content (`slot_card_body`). Use one approach consistently
- **Ignoring accessibility**: Always provide proper ARIA labels, especially for modals (`title_id`), carousels (captions), and tables (captions)
- **Assuming Bootstrap JS is loaded**: Components like modal, offcanvas, carousel, and collapse require Bootstrap's JavaScript bundle to function

## See Also

- Bootstrap 5.3 Components Documentation: https://getbootstrap.com/docs/5.3/components/
- [Navigation Components](navigation-components.md)
- [Form Components](form-components.md)
