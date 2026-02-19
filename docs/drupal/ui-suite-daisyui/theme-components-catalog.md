---
description: Complete reference of all 51 DaisyUI components with props, slots, variants, and usage examples
---

# Theme Components Catalog

The theme provides **51 SDC components** organized into 8 groups. Components with names in parentheses (e.g., `(Tab)`) are internal/child components meant to be used inside a parent component.

## 4.1 Actions Group

### Button

- **Machine name**: `ui_suite_daisyui:button`
- **DaisyUI class**: `btn`
- **Variants**: default, neutral, primary, secondary, accent, info, success, warning, error
- **Props**:
  - `outline` (string: `outline`|`dash`) -- Border style
  - `shape` (string: `square`|`circle`) -- Button shape
  - `size` (string: `xs`|`sm`|`lg`|`xl`) -- Button size
  - `responsive` (boolean) -- Responsive sizing (`btn-xs sm:btn-sm md:btn-md lg:btn-lg xl:btn-xl`)
  - `soft` (boolean) -- Soft color variant
  - `display` (string: `wide`|`block`) -- Display mode
  - `status` (string: `active`|`disabled`) -- Button state
  - `ghost` (boolean) -- Ghost style
  - `link` (boolean) -- Link style
  - `url` ($ref: `ui-patterns://url`) -- Optional URL (renders as `<a>` instead of `<button>`)
  - `modal_id` ($ref: `ui-patterns://identifier`) -- Opens a modal with matching ID
  - `icon` ($ref: `ui-patterns://icon`) -- Heroicon integration
  - `icon_position` (string: `left`|`right`, default: `right`) -- Icon placement
- **Slots**: `label`
- **Usage**:
```twig
{{ include('ui_suite_daisyui:button', {
  variant: 'primary',
  label: 'Click me',
  url: '/node/1',
  size: 'lg',
}, with_context: false) }}
```

### Modal

- **Machine name**: `ui_suite_daisyui:modal`
- **DaisyUI class**: `modal`
- **Props**:
  - `modal_id` ($ref: `ui-patterns://identifier`) -- Matches button's `modal_id` to trigger
  - `close_outside` (boolean) -- Close on backdrop click
  - `close_corner` (boolean) -- Show corner close button
  - `custom_width` (boolean) -- Wide modal (`w-11/12 max-w-5xl`)
  - `responsive_position` (string: `bottom`|`middle`|`top`|`start`|`end`) -- Mobile position
  - `position` (string: `bottom`|`middle`|`top`|`start`|`end`) -- Desktop position (md+)
  - `heading_level` (integer: 2-6, default: 3) -- Title heading tag
- **Slots**: `close_label`, `title`, `message`
- **Usage**:
```twig
{{ include('ui_suite_daisyui:button', {
  label: 'Open Modal',
  modal_id: 'my-modal',
}, with_context: false) }}

{{ include('ui_suite_daisyui:modal', {
  modal_id: 'my-modal',
  title: 'Hello!',
  message: 'This is a modal dialog.',
  close_outside: true,
}, with_context: false) }}
```

## 4.2 Data Display Group

### Accordion

- **Machine name**: `ui_suite_daisyui:accordion`
- **DaisyUI class**: `accordion` (rendered via child Collapse components)
- **Slots**: `items` -- Expects a list of Collapse components with matching `accordion_id`
- **Usage**: Wrap multiple Collapse components with the same `accordion_id`.

### Alert

- **Machine name**: `ui_suite_daisyui:alert`
- **DaisyUI class**: `alert`
- **Group**: Feedback
- **Variants**: default, info, success, warning, error
- **Props**:
  - `heading_level` (integer: 2-6, default: 3)
  - `soft` (boolean) -- Soft color variant
  - `outline` (string: `outline`|`dash`) -- Border style
  - `responsive` (boolean) -- Vertical on mobile, horizontal on `sm:`
- **Slots**: `title`, `message`, `buttons`
- **Notes**: Includes inline SVG icons matching the variant type.

### Avatar

- **Machine name**: `ui_suite_daisyui:avatar`
- **DaisyUI class**: `avatar`
- **Variants**: default, online, offline
- **Props**:
  - `size` (integer: 8|10|12|16|20|24|28|32, default: 24) -- Tailwind size unit
  - `rounded` (string: `rounded`|`rounded-xl`|`rounded-full`)
  - `mask` (string) -- 19 mask shapes (squircle, heart, hexagon, diamond, star, triangle, etc.)
  - `ring` (boolean) -- Ring border
  - `placeholder` (string) -- Text placeholder instead of image
- **Slots**: `image`

### (Avatar Group)

- **Machine name**: `ui_suite_daisyui:avatar_group`
- **DaisyUI class**: `avatar-group`
- **Slots**: `items` -- Expects a list of Avatar components
- **Notes**: Internal component (parenthesized name).

### Badge

- **Machine name**: `ui_suite_daisyui:badge`
- **DaisyUI class**: `badge`
- **Variants**: default, primary, secondary, accent, neutral, info, success, warning, error
- **Props**:
  - `outline` (string: `outline`|`dash`)
  - `size` (string: `xs`|`sm`|`md`|`lg`|`xl`)
  - `soft` (boolean)
  - `ghost` (boolean)
- **Slots**: `label`

### Card

- **Machine name**: `ui_suite_daisyui:card`
- **DaisyUI class**: `card`
- **Variants**: default, side, responsive (`lg:card-side`)
- **Props**:
  - `heading_level` (integer: 2-6, default: 2)
  - `image_bottom` (boolean) -- Image below body
  - `centered` (boolean) -- Centered body with rounded image
  - `image_full` (boolean) -- Full-bleed image
  - `actions_top` (boolean) -- Actions above title
  - `size` (string: `xs`|`sm`|`md`|`lg`|`xl`)
  - `border` (string: `border`|`dash`)
- **Slots**: `image`, `title`, `text`, `actions`
- **Usage**:
```twig
{{ include('ui_suite_daisyui:card', {
  variant: 'default',
  title: 'Card Title',
  text: 'Card description text.',
  size: 'md',
  border: 'border',
}, with_context: false) }}
```

### Carousel

- **Machine name**: `ui_suite_daisyui:carousel`
- **DaisyUI class**: `carousel`
- **Variants**: default (snap start), center, end
- **Props**:
  - `carousel_id` ($ref: `ui-patterns://identifier`) -- Auto-generated if empty
  - `full_width` (boolean) -- Full-width items
  - `vertical` (boolean) -- Vertical orientation
  - `half_width` (boolean) -- Half-width items
  - `full_bleed` (boolean) -- Full-bleed style
  - `indicator_buttons` (boolean) -- Show indicator dots
  - `next_prev_buttons` (boolean) -- Show navigation arrows
- **Slots**: `items`

### Chat Bubble

- **Machine name**: `ui_suite_daisyui:chat`
- **DaisyUI class**: `chat`
- **Variants**: default, primary, secondary, accent, info, success, warning, error
- **Props**:
  - `position` (string: `start`|`end`) -- Left or right alignment
- **Slots**: `avatar`, `header`, `time`, `bubble`, `footer`

### Collapse

- **Machine name**: `ui_suite_daisyui:collapse`
- **DaisyUI class**: `collapse`
- **Props**:
  - `collapse_type` (string: `focus`|`checkbox`|`details`) -- Interaction model
  - `collapse_icon` (string: `arrow`|`plus`) -- Icon style
  - `open` (boolean) -- Force open
  - `close` (boolean) -- Force closed
  - `accordion_id` ($ref: `ui-patterns://identifier`) -- For use inside Accordion
  - `checked` (boolean) -- For accordion default-open state
- **Slots**: `title`, `content`

### Diff

- **Machine name**: `ui_suite_daisyui:diff`
- **DaisyUI class**: `diff`
- **Slots**: `item_1`, `item_2`

### Stat

- **Machine name**: `ui_suite_daisyui:stat`
- **DaisyUI class**: `stats`
- **Variants**: default, vertical, responsive
- **Slots**: `items` -- Expects Stat Item components

### (Stat Item)

- **Machine name**: `ui_suite_daisyui:stat_item`
- **DaisyUI class**: `stat`
- **Props**:
  - `reverse_order` (boolean) -- Switch title/value order
  - `centered` (boolean) -- Center alignment
- **Slots**: `figure`, `title`, `value`, `desc`, `actions`

### Table

- **Machine name**: `ui_suite_daisyui:table`
- **DaisyUI class**: `table`
- **Variants**: default, xs, sm, md, lg, xl
- **Props**:
  - `zebra` (boolean) -- Alternating row colors
  - `pinned_rows` (boolean) -- Sticky header/footer
  - `pinned_cols` (boolean) -- Sticky columns
- **Slots**: `header`, `body`, `footer` -- Each expects Table Row components

### (Table Row)

- **Machine name**: `ui_suite_daisyui:table_row`
- **Slots**: `content` -- Expects Table Cell components

### (Table Cell)

- **Machine name**: `ui_suite_daisyui:table_cell`
- **Props**:
  - `tag` (string: `th`|`td`, default: `td`)
- **Slots**: `content`

### Timeline

- **Machine name**: `ui_suite_daisyui:timeline`
- **DaisyUI class**: `timeline`
- **Variants**: default (horizontal), vertical
- **Slots**: `items` -- Expects Timeline Item components

### (Timeline Item)

- **Machine name**: `ui_suite_daisyui:timeline_item`
- **Props**:
  - `timeline_box_start` (boolean) -- Box around start content
  - `timeline_box_end` (boolean) -- Box around end content
  - `icon` ($ref: `ui-patterns://icon`)
  - `hr_before` (boolean) -- Horizontal rule before
  - `hr_after` (boolean) -- Horizontal rule after
- **Slots**: `timeline_start`, `timeline_end`

### List

- **Machine name**: `ui_suite_daisyui:list`
- **DaisyUI class**: `list`
- **Slots**: `title`, `rows` -- Expects List Row components
- **Notes**: Vertical layout to display information in rows. Use with `list_row` child components.

### (List Row)

- **Machine name**: `ui_suite_daisyui:list_row`
- **DaisyUI class**: `list-row`
- **Slots**: `number`, `avatar`, `title`, `subtitle`, `text`, `actions`
- **Notes**: Internal component (parenthesized name). When both `number` and `avatar` are provided, the title/subtitle column gets `list-col-grow`. The `text` slot can use `list-col-wrap` class to wrap to the next row.

### Prose

- **Machine name**: `ui_suite_daisyui:prose`
- **DaisyUI class**: `prose` (from Tailwind Typography plugin)
- **Slots**: `content`
- **Notes**: Wraps content in Tailwind's `prose` class for WYSIWYG/formatted text. Requires the `@tailwindcss/typography` plugin (included in the starterkit build pipeline).

## 4.3 Navigation Group

### Breadcrumbs

- **Machine name**: `ui_suite_daisyui:breadcrumbs`
- **DaisyUI class**: `breadcrumbs`
- **Props**:
  - `items` ($ref: `ui-patterns://links`) -- Breadcrumb items with title and url
  - `max_width` (boolean) -- Enable horizontal scroll when overflowing

### Link

- **Machine name**: `ui_suite_daisyui:link`
- **DaisyUI class**: `link`
- **Variants**: default, primary, secondary, accent, neutral, success, info, warning, error
- **Props**:
  - `url` ($ref: `ui-patterns://url`)
  - `underline_hover` (boolean) -- Show underline only on hover
- **Slots**: `label`

### Menu

- **Machine name**: `ui_suite_daisyui:menu`
- **DaisyUI class**: `menu`
- **Variants**: 10 variants combining orientation and size: `vertical__xs` through `vertical__xl`, `horizontal__xs` through `horizontal__xl`
- **Props**:
  - `items` ($ref: `ui-patterns://links`) -- Menu items with title, url, and optional below
  - `collapsible` (string: `open`|`closed`) -- Collapsible sub-menus using `<details>`
- **Notes**: Supports nested menus. The Twig template uses recursive macros for both collapsible and non-collapsible rendering.

### Pagination

- **Machine name**: `ui_suite_daisyui:pagination`
- **DaisyUI class**: `join` (pagination wrapper)
- **Props**:
  - `size` (string: `xs`|`sm`|`md`|`lg`|`xl`)
  - `items` ($ref: `ui-patterns://links`)

### Steps

- **Machine name**: `ui_suite_daisyui:steps`
- **DaisyUI class**: `steps`
- **Variants**: default, vertical, vertical_responsive
- **Props**:
  - `scrollable` (boolean) -- Scrollable wrapper
- **Slots**: `items` -- Expects Step components

### Step

- **Machine name**: `ui_suite_daisyui:step`
- **DaisyUI class**: `step`
- **Variants**: default, neutral, primary, secondary, accent, info, success, warning, error
- **Props**:
  - `empty_data_content` (boolean)
  - `icon` ($ref: `ui-patterns://icon`)
  - `data_content` (string) -- `data-content` attribute value
- **Slots**: `text`

### Tabs

- **Machine name**: `ui_suite_daisyui:tabs`
- **DaisyUI class**: `tabs`
- **Variants**: default, border (bordered), lift (lifted), box (boxed)
- **Props**:
  - `size` (string: `xs`|`sm`|`md`|`lg`|`xl`)
- **Slots**: `items` -- Expects Tab components

### (Tab)

- **Machine name**: `ui_suite_daisyui:tab`
- **DaisyUI class**: `tab`
- **Props**:
  - `active` (boolean) -- Active tab state
- **Slots**: `link`

## 4.4 Layout Group

### Divider

- **Machine name**: `ui_suite_daisyui:divider`
- **DaisyUI class**: `divider`
- **Variants**: default, primary, secondary, accent, neutral, success, warning, info, error
- **Props**:
  - `orientation` (string: `default` [vertical], `horizontal`, `responsive`)
  - `position` (string: `start`|`end`) -- Content alignment
- **Slots**: `content`

### Footer

- **Machine name**: `ui_suite_daisyui:footer`
- **DaisyUI class**: `footer`
- **Variants**: default, center
- **Props**:
  - `links` ($ref: `ui-patterns://links`) -- Footer navigation links (each first level in `<nav>`)
  - `links_break` (integer: 1-3) -- Break links into columns
  - `social_title` (string) -- Social section heading
  - `heading_level` (integer: 2-6, default: 6)
- **Slots**: `social`, `aside`

### Hero

- **Machine name**: `ui_suite_daisyui:hero`
- **DaisyUI class**: `hero`
- **Props**:
  - `heading_level` (integer: 1-6, default: 1)
  - `reverse` (boolean) -- Reverse content order
  - `centered` (boolean) -- Center text
  - `responsive_centered` (boolean) -- Centered on mobile, left-aligned on `lg:`
  - `overlay_image` ($ref: `ui-patterns://url`) -- Background image with overlay
- **Slots**: `aside`, `title`, `text`, `button`
- **Usage**:
```twig
{{ include('ui_suite_daisyui:hero', {
  title: 'Welcome',
  text: '<p>Hero description text.</p>',
  centered: true,
}, with_context: false) }}
```

### Join

- **Machine name**: `ui_suite_daisyui:join`
- **DaisyUI class**: `join`
- **Variants**: default, vertical, vertical_responsive
- **Slots**: `items`

### Stack

- **Machine name**: `ui_suite_daisyui:stack`
- **DaisyUI class**: `stack`
- **Variants**: default, top, bottom, start, end
- **Slots**: `items`

### Drawer

- **Machine name**: `ui_suite_daisyui:drawer`
- **DaisyUI class**: `drawer`
- **Variants**: default, end
- **Props**:
  - `drawer_id` ($ref: `ui-patterns://identifier`) -- Used with Button component to toggle
  - `open` (boolean) -- Open by default
- **Slots**: `content`, `sidebar`
- **Notes**: Grid layout that can show/hide a sidebar on the left or right side of the page.

### Navbar

- **Machine name**: `ui_suite_daisyui:navbar`
- **DaisyUI class**: `navbar`
- **Slots**: `start`, `center`, `end`
- **Notes**: Used directly by the page template. The three slots map to `navbar-start`, `navbar-center`, `navbar-end`.

## 4.5 Grid Group

All grid components share common props for responsive layout control.

**Shared Grid Props** (present on all grid components):

- `container_type` (string: `container mx-auto`|`breakout`|`bg-breakout`) -- Container behavior
- `background_image` ($ref: `ui-patterns://url`) -- Section background image
- `background_size` (string: `bg-auto`|`bg-cover`|`bg-contain`)
- `background_position` (string: 9 Tailwind bg position values)
- `background_repeat` (string: 6 Tailwind bg repeat values)
- `gap` / `gap_sm` / `gap_md` / `gap_lg` / `gap_xl` / `gap_2xl` (integer: 0|2|4|8|12) -- Responsive gaps
- `grid_cols` / `grid_cols_sm` through `grid_cols_2xl` (integer: 1-12) -- Responsive column counts

### Grid 1 Region

- **Machine name**: `ui_suite_daisyui:grid_1_region`
- **Slots**: `col_first`

### Grid 2 Regions

- **Machine name**: `ui_suite_daisyui:grid_2_regions`
- **Slots**: `col_first`, `col_second`
- **Additional props**: `col_span`, `col_start`, `col_end` (arrays of 2) + responsive variants -- Per-column span/start/end control

### Grid 3 Regions

- **Machine name**: `ui_suite_daisyui:grid_3_regions`
- **Slots**: `col_first`, `col_second`, `col_third`
- **Additional props**: `col_span`, `col_start`, `col_end` (arrays of 3) + responsive variants

### Grid 4 Regions

- **Machine name**: `ui_suite_daisyui:grid_4_regions`
- **Slots**: `col_first`, `col_second`, `col_third`, `col_fourth`
- **Additional props**: `col_span`, `col_start`, `col_end` (arrays of 4) + responsive variants

### Grid Cols

- **Machine name**: `ui_suite_daisyui:grid_cols`
- **Slots**: `items` -- Flexible number of items
- **Notes**: Unlike fixed-region grids, this accepts any number of items and distributes them across the configured column count.

## 4.6 Feedback Group

### Loading

- **Machine name**: `ui_suite_daisyui:loading`
- **DaisyUI class**: `loading`
- **Variants**: default, spinner, dots, ring, ball, bars, infinity
- **Props**:
  - `color` (string: primary|secondary|accent|neutral|info|success|warning|error)
  - `size` (string: `xs`|`sm`|`md`|`lg`|`xl`)

### Progress

- **Machine name**: `ui_suite_daisyui:progress`
- **DaisyUI class**: `progress`
- **Variants**: default, primary, secondary, accent, neutral, info, success, warning, error
- **Props**:
  - `value` (number) -- Current progress value
  - `max` (number) -- Maximum value (omit for indeterminate)

### Toast

- **Machine name**: `ui_suite_daisyui:toast`
- **DaisyUI class**: `toast`
- **Props**:
  - `position_x` (string: `start`|`center`|`end`)
  - `position_y` (string: `top`|`middle`|`bottom`)
- **Slots**: `items`

### Tooltip

- **Machine name**: `ui_suite_daisyui:tooltip`
- **DaisyUI class**: `tooltip`
- **Variants**: default, primary, secondary, accent, neutral, info, success, warning, error
- **Props**:
  - `responsive` (boolean) -- Only show for large screens
  - `data_tip` (string) -- Text content for tooltip (`data-tip` attribute)
  - `open` (boolean) -- Force tooltip open
  - `position` (string: `top`|`bottom`|`left`|`right`)
- **Slots**: `content`, `tooltip_content`

## 4.7 Mockup Group

### Browser Mockup

- **Machine name**: `ui_suite_daisyui:browser_mockup`
- **DaisyUI class**: `mockup-browser`
- **Props**: `toolbar` (string) -- Toolbar text (e.g., URL bar)
- **Slots**: `content`

### Code Mockup

- **Machine name**: `ui_suite_daisyui:code_mockup`
- **DaisyUI class**: `mockup-code`
- **Slots**: `lines` -- Expects Code components

### (Code)

- **Machine name**: `ui_suite_daisyui:code`
- **Props**: `prefix` (string) -- Line prefix (e.g., `$`, `>`)
- **Slots**: `content`

### Phone Mockup

- **Machine name**: `ui_suite_daisyui:phone_mockup`
- **DaisyUI class**: `mockup-phone`
- **Props**: `camera` (boolean) -- Show camera notch
- **Slots**: `content`

### Window Mockup

- **Machine name**: `ui_suite_daisyui:window_mockup`
- **DaisyUI class**: `mockup-window`
- **Slots**: `content`

## Common Mistakes

- **Using wrong prop types** -- Props use JSON Schema types. A `size` prop typed as `string` expects `"lg"`, not `3`. An `integer` prop expects a number. WHY: Type mismatches cause the prop value to be silently ignored.
- **Passing raw HTML to slots expecting components** -- Slots like `items` on Accordion, Tabs, or Timeline expect child component renders, not raw HTML. WHY: The parent component's Twig template iterates over child components that must have the correct structure.
- **Forgetting `accordion_id` on Collapse inside Accordion** -- Collapse components inside an Accordion must all share the same `accordion_id` for the radio-button toggle behavior to work. WHY: The accordion uses HTML `name` attributes to create mutual exclusion.

## See Also

- [DaisyUI Components Reference](https://daisyui.com/components/) -- Original DaisyUI documentation
- `design-system-daisyui.md` -- DaisyUI framework guide
