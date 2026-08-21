---
description: "Complete reference of all 51 DaisyUI components with props, slots, variants, and usage examples"
tldr: "Complete reference of all 51 DaisyUI components with props, slots, variants, and usage examples"
---

# Theme Components Catalog

The theme provides **51 SDC components** organized into 7 groups (Actions, Data display, Feedback, Grid, Layout, Mockup, Navigation). Components with names in parentheses (e.g., `(Tab)`) are internal/child components meant to be used inside a parent component.

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
  - `modal_id` ($ref: `ui-patterns://identifier`) -- Sets `onclick="<modal_id>.showModal()"`. Must be a valid JS identifier -- see the Modal warning below.
  - `drawer_id` ($ref: `ui-patterns://identifier`) -- Changes the whole element to `<label for="<drawer_id>" class="... drawer-button">`. Takes precedence over `url`, so a button with both renders as a label, not a link.
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
  - `force_open` (boolean) -- Adds `modal-open`, rendering the dialog already open. The only way to show an open modal without JS.
  - `responsive_position` (string: `bottom`|`middle`|`top`|`start`|`end`) -- Mobile position
  - `position` (string: `bottom`|`middle`|`top`|`start`|`end`) -- Desktop position (md+)
  - `heading_level` (integer: 2-6, default: 3, set by `modal.twig` via `|default(3)`) -- Title heading tag
- **Slots**: `close_label`, `title`, `message`
- **`modal_id` must be a valid JavaScript identifier.** `button.twig` writes it into an inline handler verbatim: `attributes.setAttribute('onclick', modal_id ~ '.showModal()')`. A hyphenated id such as `my-modal` renders `onclick="my-modal.showModal()"`, which the browser parses as the subtraction `my - modal.showModal()` -- a `ReferenceError`, so the modal never opens. Nothing catches this: UI Patterns' `IdentifierPropType` pattern explicitly allows `-`, and the error only appears in the console. **Use underscores**, as the theme's own story does (`modal.default.story.yml` uses `my_modal_1`).
- Omitting `modal_id` on the modal is safe -- `modal.twig` falls back to `'modal-' ~ random()` -- but then no button can target it.
- **Usage**:
```twig
{{ include('ui_suite_daisyui:button', {
  label: 'Open Modal',
  modal_id: 'my_modal_1',
}, with_context: false) }}

{{ include('ui_suite_daisyui:modal', {
  modal_id: 'my_modal_1',
  title: 'Hello!',
  message: 'This is a modal dialog.',
  close_outside: true,
}, with_context: false) }}
```

## 4.2 Data Display Group

### Accordion

- **Machine name**: `ui_suite_daisyui:accordion`
- **DaisyUI class**: none. `accordion.twig` is a single line -- `<div {{ attributes }}>{{ items }}</div>` -- and DaisyUI 5 has no `accordion` class. Accordion behaviour is entirely a property of the child Collapse components sharing an `accordion_id`.
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
  - `icon` ($ref: `ui-patterns://icon`) -- The alert's icon. **Caller-supplied; there is no default.**
- **Slots**: `title`, `message`, `buttons`
- **Notes**: `alert.twig` contains no SVG and no variant-to-icon mapping -- it renders `icon(icon.pack_id, icon.icon_id, icon.settings)` and nothing else. Pass an `icon` or the alert has none. The theme's own `status-messages.html.twig` passes no icon, so Drupal's status messages render icon-less out of the box. `role="alert"` is set unconditionally.

### Avatar

- **Machine name**: `ui_suite_daisyui:avatar`
- **DaisyUI class**: `avatar`
- **Variants**: default, online, offline
- **Props**:
  - `size` (integer: 8|10|12|16|20|24|28|32, default: 24) -- Tailwind size unit
  - `rounded` (string: `rounded`|`rounded-xl`|`rounded-full`)
  - `mask` (string) -- one of 19 enum values, each **already prefixed**: `mask-squircle`, `mask-heart`, `mask-hexagon`, `mask-hexagon-2`, `mask-decagon`, `mask-pentagon`, `mask-diamond`, `mask-square`, `mask-circle`, `mask-parallelogram` (1-4), `mask-star`, `mask-star-2`, `mask-triangle` (1-4). `avatar.twig` emits `'mask ' ~ mask`, so passing a bare `squircle` yields `class="mask squircle"` -- no shape, no error.
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
  - `actions_position` (string) -- Emitted as `justify-<value>`; defaults to `justify-end` when omitted
  - `size` (string: `xs`|`sm`|`md`|`lg`|`xl`)
  - `border` (string: `border`|`dash`)
  - `url` ($ref: `ui-patterns://url`) -- **Changes the wrapper element** from `<div>` to `<a href>`, making the whole card one link. Watch for nested interactive elements in the `actions` slot when you use it.
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
- **Variants**: `default`, `border`, `lift`, `box` -- emitted as `tabs-<variant>` (`default` emits nothing). These are DaisyUI 5 names; the DaisyUI 4 spellings `lifted`/`bordered`/`boxed` are not accepted and would render unstyled.
- **Props**:
  - `size` (string: `xs`|`sm`|`md`|`lg`|`xl`)
- **Slots**: `items` -- Expects Tab components

### (Tab)

- **Machine name**: `ui_suite_daisyui:tab`
- **DaisyUI class**: `tab`
- **Props**:
  - `active` (boolean) -- Active tab state
- **Slots**: `link` -- **must be a render array, not an HTML string.**
- **Notes**: `tab.twig` emits no element of its own. Its entire body is `{{ link|set_attribute('role','tab')|add_class('tab') }}`, so the `tab` class, the `role` and the `tab-active` state are all applied *to the slot's own markup*. UI Patterns' `AttributesFilterTrait::addClass()` opens with `if (!\is_array($element)) { return $element; }` -- hand it a plain string like `'<a href="/x">X</a>'` and it comes back untouched: no class, no role, no active state, and no error anywhere. Pass a link render array (`{'#type': 'link', ...}`), or the output of Drupal's own `menu-local-task.html.twig`, which is what the theme does.

  The same filter behaviour applies more mildly elsewhere -- `join`, `carousel`, `hero` and `chat` add a `join-item` or a padding class to slot content the same way. There the string form only loses one utility class; on Tab it loses the component.
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

**Genuinely shared props** (all five grid components declare and read these):

- `container_type` (string: `container mx-auto`|`breakout`|`bg-breakout`, default `container mx-auto` set in Twig) -- Container behavior
- `background_image` ($ref: `ui-patterns://url`) -- Written into an inline `style="background-image: url(...)"`
- `background_size` (string: `bg-auto`|`bg-cover`|`bg-contain`)
- `background_position` (string: 9 Tailwind bg position values)
- `background_repeat` (string: 6 Tailwind bg repeat values)

**Not shared, despite looking like it:**

| Prop family | Where it exists | Breakpoint ceiling |
|---|---|---|
| `gap` / `gap_sm` / `gap_md` / `gap_lg` | `grid_cols`, `grid_2_regions`, `grid_3_regions`, `grid_4_regions` -- **not** `grid_1_region` | `lg`. There is no `gap_xl` or `gap_2xl` on any component. |
| `grid_cols` / `grid_cols_sm` / `grid_cols_md` / `grid_cols_lg` | `grid_cols` only | `lg`. There is no `grid_cols_xl` or `grid_cols_2xl`. |
| `col_span` / `col_start` / `col_end` (+ `_sm` `_md` `_lg`) | the four region grids | `lg` |

The region grids hardcode `grid-cols-12`; there is no way to change the column count on `grid_1_region` through `grid_4_regions`. Only `grid_cols` takes a column count, and only it takes `items`.

> **Do not copy the theme's own `page.html.twig` here.** It passes full class strings into these props -- `col_span: ['col-span-12', 'col-span-12']`, `col_span_lg: ['lg:col-span-3', 'lg:col-span-9']` -- but the grid Twig concatenates, `'col-span-' ~ col_span[0]`, producing `col-span-col-span-12` and `lg:col-span-lg:col-span-3`. The schema is right (`type: integer`, enum 1-12) and the base theme's page template is wrong. Pass integers.

### Grid 1 Region

- **Machine name**: `ui_suite_daisyui:grid_1_region`
- **Slots**: `col_first`
- **Props**: `col_span`, `col_start` + `_lg` / `_md` / `_sm` -- **scalars here**, not arrays, unlike the multi-region grids. `col_span` defaults to `12` in the Twig. No `col_end`, no `gap`.

### Grid 2 Regions

- **Machine name**: `ui_suite_daisyui:grid_2_regions`
- **Slots**: `col_first`, `col_second`
- **Additional props**: `col_span`, `col_start`, `col_end` (arrays of 2) + `_lg` / `_md` / `_sm` -- per-column span/start/end control. `col_span` defaults to `[12, 12]` and `col_span_md` to `[6, 6]` in the Twig, so the two regions stack on mobile and sit side by side from `md` up. Values are **integers** (`6`), not class strings: the Twig emits `'col-span-' ~ col_span[0]`.
- **Additional props**: `gap` (+ `_lg` / `_md` / `_sm`), default `4`

### Grid 3 Regions

- **Machine name**: `ui_suite_daisyui:grid_3_regions`
- **Slots**: `col_first`, `col_second`, `col_third`
- **Additional props**: `col_span`, `col_start`, `col_end` (arrays of 3) + `_lg` / `_md` / `_sm`; `gap` (+ responsive)

### Grid 4 Regions

- **Machine name**: `ui_suite_daisyui:grid_4_regions`
- **Slots**: `col_first`, `col_second`, `col_third`, `col_fourth`
- **Additional props**: `col_span`, `col_start`, `col_end` (arrays of 4) + `_lg` / `_md` / `_sm`; `gap` (+ responsive)

### Grid Cols

- **Machine name**: `ui_suite_daisyui:grid_cols`
- **Slots**: `items` -- Flexible number of items
- **Additional props**: `grid_cols` (default `1`), `grid_cols_md` (default `2`), `grid_cols_lg` (default `4`), `grid_cols_sm`; `gap` (default `4`) + `_lg` / `_md` / `_sm`
- **Notes**: Unlike fixed-region grids, this accepts any number of items and distributes them across the configured column count. It is the only grid with no `icon_map`, so it shows no region diagram in the Layout Builder picker.

## 4.6 Feedback Group

> **Alert** also belongs to this group (`group: Feedback` in `alert.component.yml`) but is documented above under 4.2 for historical reasons. Look for it there.

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
  - `max` (number) -- Maximum value. HTML's own default is `1`, so passing `value: 70` without `max: 100` renders a full bar.
- **Indeterminate requires omitting both props.** `progress.twig` sets the `value` attribute when `value or (not value and max)` -- so `max` alone still emits `value="0"` (an empty determinate bar), and only a `<progress>` with neither attribute animates as indeterminate.

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
