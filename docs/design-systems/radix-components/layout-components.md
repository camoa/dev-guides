---
description: "Components for organizing and containing content in structured layouts"
tldr: "Components for organizing and containing content in structured layouts. These components help create interactive, collapsible, and organized content presentations including accordions, cards, carousels, modals, and data tables."
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
| `title_tag` | string | h2 | **Dead — not honoured by `accordion.twig`.** Line 66 hardcodes `heading_html_tag: 'h2'` for the accordion title. Use the per-item `items[].title_tag` (honoured at `accordion.twig:90`, defaults to `h3`). |
| `title_link` | string |  | **Dead — not honoured by `accordion.twig`.** Line 35 assigns it and nothing ever reads it; the accordion title is never rendered as a link. No alternative short of overriding the component. |
| `title_attributes` | Drupal\Core\Template\Attribute |  | A list of HTML attributes for the button |
| `id` | ['integer', 'string'] | `accordion-` + `random(1000)` | Unique ID for the accordion component. The YAML says `0`; `accordion.twig` generates a random ID |
| `flush` | boolean | false | True if the accordion has no background color or borders |
| `items` | array | [] | An array of items inside the accordion. Each item is an object that has title, content, and stay_open properties |
| `open_item_id` | integer | 0 | 1-based index of the item to open. `0` (the default) leaves every item closed |
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
- The component-level `title_tag` is inert — `accordion.twig:66` always renders the accordion title as `h2`. Only the per-item `items[].title_tag` is honoured (`accordion.twig:90`), and it falls back to `h3` per item, so set it on every item if you want a different level
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
| `card_subtitle_tag` | string | div | Card Subtitle HTML Tag Enum: `h1, h2, h3, h4, h5, h6`. The YAML says `h5`; `card.twig` sets `div` |
| `card_text_tag` | string | div | Card Text HTML Tag Enum: `p, span, div`. The YAML says `p`; `card.twig` sets `div` |
| `card_link_text` | string |  | Card Link Text |
| `card_link_url` | string |  | Card Link URL |
| `card_media` | string |  | Card Media |
| `card_image_src` | string |  | Card Image Source URL |
| `card_image_alt` | string |  | Card Image Alternative Text |
| `card_image_cap` | string | top | Image Caption Position Enum: `top, bottom`. Omitting it renders the image above the body |
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
| `show_carousel_indicators` | boolean | true | Show carousel indicators. **Plural.** The `.component.yml` declares the singular `show_carousel_indicator`, but `carousel.twig:46` reads only the plural — the singular is dead |
| `show_carousel_caption` | boolean | true | Show carousel caption |
| `crossfade` | boolean | false | Adds `.carousel-fade` for a crossfade transition (`carousel.twig:57`). Read by the Twig, absent from the YAML |
| `caption_title_tag` | string | h3 | HTML tag for every caption title (`carousel.twig:50`). **Top-level, not per-item** |
| `caption_content_tag` | string | p | HTML tag for every caption content block (`carousel.twig:51`). **Top-level, not per-item** |
| `carousel_indicator_utility_classes` | array | [] | Utility classes for each indicator button (`carousel.twig:99`). Read by the Twig, absent from the YAML |
| `title_attributes` | Drupal\Core\Template\Attribute |  | Attributes passed to each caption heading (`carousel.twig:158`). Read by the Twig, absent from the YAML |
| `autoplay` | ['string'] |  | Autoplay behavior. Enum: `carousel, true` |
| `id` | ['string'] | `carousel-` + `random(1000)` | Unique ID for the carousel component. The YAML says `0`; `carousel.twig` generates a random ID |
| `carousel_utility_classes` | ['string', 'array'] |  | Utility classes for the carousel |
| `carousel_item_utility_classes` | ['string', 'array'] |  | Utility classes for carousel items |
| `carousel_caption_utility_classes` | ['string', 'array'] |  | Utility classes for carousel captions |
| `carousel_attributes` | Drupal\Core\Template\Attribute |  | Attributes for the carousel |
| `media_attributes` | Drupal\Core\Template\Attribute |  | Attributes for the carousel media |
| `item_image_attributes` | Drupal\Core\Template\Attribute |  | Attributes for the carousel item image |
| `items` | array | [] | An array of items, each with `caption_title`, `caption_content`, `image_src`, `image_alt`, `media`, `interval`. The whole component renders nothing when `items` is empty (`carousel.twig:91`). The per-item `carousel_caption`, `caption_title_tag` and `caption_content_tag` listed in the YAML are not read: the caption body key is `caption_content` (`carousel.twig:164`), and the two tag names are top-level props |

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
- The show/hide prop for indicators is `show_carousel_indicators` (plural). The `.component.yml` names it in the singular; passing the singular does nothing
- The per-item caption body key is `caption_content`, not `carousel_caption`

### collapse
**Description:** Collapse component for creating expandable/collapsible content sections. See Bootstrap Documentation: https://getbootstrap.com/docs/5.3/components/collapse/
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `title` | string |  | Title text for the collapse component |
| `button_html_tag` | string | button | The HTML tag to use for the button. Enum: `button, a` |
| `id` | ['integer', 'string'] | `random(1000)` | Unique ID for the collapse component. The YAML says `0`; `collapse.twig` generates a random integer |
| `direction` | string | vertical | Direction of the collapse. Enum: `vertical, horizontal` |
| `collapsed` | boolean | true | True if the collapse component is initially collapsed |
| `content` | string |  | Default content text for the collapse component |
| `collapse_content_classes` | array |  | **Dead — not honoured by `collapse.twig`.** Line 25 rebuilds `collapse_content_classes` from scratch before it is used. Use `collapse_content_utility_classes` instead. |
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

**Slots:**
None defined.

**Usage Example:**
```twig
{%
  include 'radix:details' with {
    title: 'More Information',
    description: 'Additional details about the topic.',
    children: 'Content that provides more information.',
    value: 'Some important value',
    required: true,
    summary_attributes: create_attribute(),
    content_attributes: create_attribute(),
  }
%}
```

**Gotchas:**
- **`summary_attributes` and `content_attributes` are mandatory when you call this component yourself.** `details.twig` calls `summary_attributes.addClass(...)` and `content_attributes.addClass(...)` with no `?:` fallback, and SDC only ever auto-supplies `attributes` — so a bare `include 'radix:details'` throws. Inside Drupal's own `details.html.twig` the form render element supplies both; anywhere else you must pass `create_attribute()` for each.
- This is a native HTML `<details>` element, not a Bootstrap component, so it has different styling
- The `required` attribute is primarily for form contexts, not general content disclosure
- Browser default styling for `<details>` varies; apply custom styles for consistency

### list-group
**Description:** A series of list items that can be used to display a list of elements with a common style.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `list_group_html_tag` | string | ul, or ol when `numbered` is true | The HTML tag to use for the list group. An explicit value always wins over the `numbered` fallback |
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
- `numbered: true` switches the tag to `<ol>` only when `list_group_html_tag` is absent — an explicit `list_group_html_tag` always wins (`list-group.twig:20` is `list_group_html_tag ?? (numbered ? 'ol' : 'ul')`). `numbered: true` together with `list_group_html_tag: 'ul'` gives a `<ul class="list-group-numbered">`

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
| `body` | ['string', 'boolean'] | true | The main content of the modal. Omitting it still renders an empty `.modal-body`; pass `body: false` to suppress it |
| `footer` | string |  | Content for the modal's footer, typically buttons |
| `close_button` | boolean | true | Displays a close button in the modal header. On by default, which also forces a `.modal-header` even with no `header`; pass `false` to remove it |
| `animation` | boolean | true | Applies the `.fade` animation. On by default; pass `false` to disable |
| `keyboard` | boolean | true | Allows closing the modal with Escape. On by default; passing `false` emits `data-bs-keyboard="false"` |
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
| `backdrop` | 'string' | `'true'` (string) | Whether the offcanvas has a backdrop. Enum: `true, false, static`. Pass the **string** `'false'`, not the boolean — `offcanvas.twig` applies the Twig `default` filter, which replaces any falsy value, so boolean `false` is silently turned back into `'true'` |
| `body_scrolling` | boolean | false | Whether the body scrolls when offcanvas is open |
| `offcanvas_id` | string |  | The offcanvas id |
| `placement` | string | start | The offcanvas placement. Enum: `start, end, top, bottom` |
| `close_button` | boolean | true | Whether the offcanvas has a close button |
| `offcanvas_attributes` | Drupal\Core\Template\Attribute |  | **Dead — not honoured by `offcanvas.twig`.** Line 35 unconditionally rebuilds it from `create_attribute()` with `tabindex`, `id`, `data-bs-backdrop` and `data-bs-scroll`; whatever you pass is discarded. Use `offcanvas_utility_classes` for classes; anything else needs a component override. |
| `offcanvas_title_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the offcanvas title. The only offcanvas attribute prop the template actually honours (`offcanvas.twig:56`). |
| `offcanvas_body_attributes` | Drupal\Core\Template\Attribute |  | **Dead — not honoured by `offcanvas.twig`.** Line 55 unconditionally reassigns it to `create_attribute()`. Use `offcanvas_body_utility_classes` for classes. |
| `offcanvas_button_attributes` | Drupal\Core\Template\Attribute |  | **Dead — not honoured by `offcanvas.twig`.** Line 48 unconditionally rebuilds it with `type`, `data-bs-toggle`, `data-bs-target` and `aria-controls`. Override the `offcanvas_toggler` block to change the trigger. |

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
- `backdrop: 'static'` does work — `offcanvas.twig:38` writes the value straight to `data-bs-backdrop`. Do not try to set that attribute yourself: `offcanvas.twig:35` unconditionally rebuilds `offcanvas_attributes` with `create_attribute()`, so anything passed in that prop is discarded

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
| `rows` | array |  | Body row data; each row is `{ attributes, cells, classes, extra_classes }` (`table.twig:61`). Absent from the YAML |
| `empty` | string |  | Message rendered as a single row when `rows` is empty (`table.twig:84`). Absent from the YAML |
| `header_columns` | integer |  | `colspan` for that empty-message cell (`table.twig:87`). Absent from the YAML |
| `striped` | boolean | false | Adds `.table-striped` (`table.twig:14`). Absent from the YAML |
| `no_striping` | boolean | false | Suppresses the per-row `odd`/`even` classes (`table.twig:67`). Absent from the YAML |
| `table_utility_classes` | array | [] | Utility classes merged onto the `<table>` (`table.twig:15`). Absent from the YAML |
| `attributes` | Drupal\Core\Template\Attribute |  | Attributes for the `<table>` element (`table.twig:18`) |

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
- Striping has a dedicated prop: `striped: true` adds `.table-striped` (`table.twig:14`). Only the other variants (bordered, hover) need `table_utility_classes`
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
