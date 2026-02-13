---
description: You're evaluating whether to reuse, override, or create components
drupal_version: "11.x"
---

## 8. Radix Component Reuse Strategy

### When to Use This Section
- You're evaluating whether to reuse, override, or create components
- You need a catalog of existing Radix SDC components
- You want to extend Radix components in your sub-theme

### 8.1 Radix Component Catalog

#### Pattern: Radix 6.x SDC Components

**Source:** `~/workspace/contrib/web/themes/contrib/radix/components/`

This catalog contains all 57 actual Radix SDC components. Each entry lists key props and slots for quick reference.

#### Atoms (UI Building Blocks)

| Component | Description | Key Props | Slots |
|-----------|-------------|-----------|-------|
| `badge/` | Count/labeling component | `badge_html_tag`, `color`, `badge_url` | `badge_content`, `content` |
| `button/` | Button with variants | `button_html_tag`, `color`, `outline`, `size`, `disabled` | `content` |
| `close-button/` | Dismissal button | `size`, `disabled` | none |
| `heading/` | Configurable headings h1-h6 | `heading_html_tag`, `display`, `title_link` | `heading_content` |
| `image/` | Responsive images | `src`, `alt`, `responsive`, `align`, `thumbnails`, `rounded` | none |
| `input/` | Form text inputs | `type`, `value`, `remove_form_control` | `children` |
| `select/` | Dropdown select input | `select_attributes` | none |
| `spinner/` | Loading indicator | `spinner_html_tag`, `type`, `color`, `size` | `content` |
| `textarea/` | Multiline text input | `value`, `table_utility_classes` | none |

#### Molecules (Composite Components)

| Component | Description | Key Props | Slots |
|-----------|-------------|-----------|-------|
| `button-group/` | Groups buttons/inputs | `vertical`, `size`, `toolbar`, `items` | `content` |
| `dropdown/` | Dropdown menu component | `dropdown_button_content`, `items`, `split_button`, `dropdown_color` | `dropdown_toggler`, `dropdown_menu` |
| `dropdown-menu/` | Dropdown menu items | `items`, `alignment`, `dropdown_direction` | none |
| `fieldset/` | Form fieldset element | `disabled`, `required`, `errors` | `children`, `fieldset_prefix`, `fieldset_suffix` |
| `figure/` | Image with caption | `image`, `caption`, `align` | none |
| `form-element/` | Form field wrapper | `type`, `name`, `label`, `required`, `errors` | `children` |
| `form-element--label/` | Form label | `title`, `title_display`, `required` | none |
| `form-element--radiocheckbox/` | Radio/checkbox wrapper | `type`, `name`, `label`, `disabled` | `children` |
| `list-group/` | Bootstrap list group | `list_group_html_tag`, `numbered`, `horizontal`, `list_group_items` | `list_group_content` |
| `nav-item/` | Single navigation item | `is_active`, `container`, `color`, `placement` | `link` |
| `radios/` | Radio button group | `attributes` | `children` |

#### Organisms (Complex Sections)

| Component | Description | Key Props | Slots |
|-----------|-------------|-----------|-------|
| `accordion/` | Bootstrap accordion | `title`, `flush`, `items`, `open_item_id` | `content` |
| `alert/` | Contextual feedback | `type` (required), `dismissible`, `heading` | `alert_heading`, `content` |
| `breadcrumb/` | Breadcrumb navigation | `breadcrumb` (array), `classes` | none |
| `card/` | Flexible content container | `card_title`, `card_subtitle`, `card_body`, `card_image_src`, `card_border` | `slot_card_image_top`, `slot_card_image_bottom`, `slot_card_body`, `slot_card_links`, `slot_card_footer` |
| `carousel/` | Image/content carousel | `carousel_theme`, `items`, `show_carousel_control`, `autoplay` | `carousel_indicators`, `carousel_inner`, `carousel_caption`, `carousel_control` |
| `collapse/` | Collapsible content | `title`, `button_html_tag`, `direction`, `collapsed` | `collapse_trigger`, `collapse_content` |
| `details/` | Disclosure widget | `title`, `required`, `errors`, `description` | none |
| `modal/` | Layered content overlay | `size`, `id`, `header`, `body`, `footer`, `scrollable`, `close_button` | `modal_header`, `modal_body`, `modal_footer` |
| `nav/` | Flexible navigation | `alignment`, `style`, `fill` | `nav_items` |
| `navbar/` | Responsive header | `navbar_container_type`, `navbar_theme`, `placement`, `navbar_expand` | `branding`, `navigation`, `navbar_toggler` |
| `navbar-brand/` | Navbar branding | `navbar_brand_utility_classes` | `logo` |
| `offcanvas/` | Hidden sidebar | `offcanvas_title`, `placement`, `show_by_default`, `backdrop` | `offcanvas_header`, `offcanvas_body`, `offcanvas_toggler` |
| `pagination/` | Page navigation | `size`, `alignment`, `show_first`, `show_last`, `items` | `pagination_next`, `pagination_previous` |
| `progress/` | Progress indicator | `color`, `valuenow`, `valuemax`, `striped`, `animated` | none |
| `table/` | Data table | `caption`, `header`, `footer`, `colgroups` | `table_caption`, `table_colgroup`, `table_header`, `table_body`, `table_footer` |
| `toasts/` | Toast notifications | `with_wrapper`, `toasts` (array with header/body/autohide) | `content` |

#### Page-Level Components

| Component | Description | Key Props | Slots |
|-----------|-------------|-----------|-------|
| `html/` | HTML document structure | `doc_lang`, `body_classes` | `head_start`, `head_end`, `body_start`, `body_end` |
| `page/` | Main page structure | `page_attributes`, `page_utility_classes` | `page_navigation`, `page_content`, `page_footer` |
| `page-content/` | Main content area | `page_header_container_type`, `page_content_container_type` | `page_header`, `page_content` |
| `page-footer/` | Page footer | `footer_utility_classes` | `page_inner_footer` |
| `page-navigation/` | Navigation container | none | `branding`, `left`, `right` |
| `page-title/` | Page heading | `display`, `page_title_utility_classes`, `title_prefix`, `title_suffix` | none |

#### Drupal Integration Components

| Component | Description | Key Props | Slots |
|-----------|-------------|-----------|-------|
| `block/` | Block wrapper | `id`, `bundle`, `layout`, `plugin_id`, `label`, `configuration` | `block_label`, `block_content`, `content` |
| `comment/` | Comment display | `user_picture`, `submitted`, `permalink`, `title` | `content` |
| `field/` | Field display | `label_display`, `field_utility_classes` | none |
| `field-comment/` | Comment field section | `comments`, `comment_form`, `title_prefix`, `title_suffix` | none |
| `form/` | Form wrapper | `title_prefix`, `title_suffix` | `form_children`, `children` |
| `local-tasks/` | Tabs and pills navigation | none | `primary`, `secondary` |
| `media/` | Media entity display | `media_type`, `is_published`, `view_mode` | `content`, `media_content` |
| `node/` | Node entity display | `title_attributes`, `display_submitted`, `author_name`, `date`, `label`, `url` | `node_title`, `node_metadata`, `node_title_prefix`, `node_title_suffix`, `node_content`, `content` |
| `region/` | Drupal region wrapper | `attributes` | `region_content`, `content` |
| `taxonomy/` | Taxonomy term display | `name`, `url`, `view_mode`, `page`, `heading_html_tag` | `taxonomy_title_prefix`, `taxonomy_title`, `taxonomy_title_suffix`, `taxonomy_content` |
| `user/` | User profile display | `view_mode`, `user_utility_classes` | `content` |
| `views-view/` | Views display base | `content`, `views_attributes` (multiple for title/header/rows/footer/pager) | `views_view_wrapper`, `views_view_title`, `views_header`, `views_filters`, `views_attachment_before`, `views_rows`, `views_pager`, `views_attachment_after`, `views_more`, `views_footer`, `views_feed_icons` |
| `views-view--grid/` | Views grid layout | `content`, `attributes` | none |
| `views-view--table/` | Views table display | `title`, `header`, `caption`, `rows`, `responsive`, `sticky`, `bordered` | none |
| `views-view--unformatted/` | Views unformatted rows | `content` | none |

#### Component Status Notes

All components are marked as `experimental` status in Radix 6.x except:
- `alert/` — stable
- All others — experimental

#### Common Mistakes
- **Not checking Radix first** — Always review existing components before creating
- **Duplicating Radix components** — Reuse or extend instead
- **Assuming Radix has everything** — Some specialized components may need creation
- **Not reading component YAML** — Props/slots defined in `.component.yml` files
- **Confusing component names** — Component directory name must match file prefix

#### See Also
- [8.2 Reuse Decision Framework](#82-reuse-decision-framework)
- Radix Component Files: `~/workspace/contrib/web/themes/contrib/radix/components/`
- Radix Documentation: https://docs.trydrupal.com/radix/working-with-the-components/

---

### 8.2 Reuse Decision Framework

#### Decision Table: Reuse vs Override vs Create

| Scenario | Decision | Action |
|----------|----------|--------|
| Radix component exists, meets needs | **REUSE** | Use `{% include 'radix:COMPONENT' %}` |
| Radix component exists, needs minor changes | **EXTEND** | Include + add custom wrapper/styles |
| Radix component exists, needs major changes | **OVERRIDE** | Copy to sub-theme, modify |
| Radix component doesn't exist | **CREATE** | New SDC in sub-theme |
| Design system atom = Bootstrap class | **USE BOOTSTRAP** | No SDC needed |

#### Pattern: Decision Process

```
1. Does this match a Radix component?
   YES → Can you use it as-is?
      YES → REUSE via include
      NO → Continue to step 2
   NO → Continue to step 4

2. Are changes minor (styling, props)?
   YES → EXTEND (include + custom SCSS)
   NO → Continue to step 3

3. Are changes major (structure, behavior)?
   YES → OVERRIDE (copy to sub-theme)
   NO → Back to step 2

4. Can Bootstrap utility classes achieve this?
   YES → USE BOOTSTRAP (no SDC)
   NO → CREATE new SDC
```

#### Common Mistakes
- **Creating when extending would work** — Extend Radix components first
- **Extending when reusing would work** — Try Radix as-is
- **Overriding unnecessarily** — Minor changes don't need full override
- **Not documenting decision** — Note why you chose create vs reuse

#### See Also
- [8.3 Overriding Radix Components](#83-overriding-radix-components)
- [3.1 Atom Creation Decision Framework](#31-atom-creation-decision-framework)

---

### 8.3 Overriding Radix Components

#### Pattern: Component Override Process

**Step 1: Copy Radix Component to Sub-Theme**

```bash
# Copy entire component directory
cp -r ~/workspace/contrib/web/themes/contrib/radix/components/button \
      themes/custom/THEME_NAME/components/button
```

**Step 2: Update Component Namespace**

**File: `components/button/button.component.yml`**
```yaml
# Change from experimental to stable if needed
status: stable

# Add custom props if needed
props:
  type: object
  properties:
    # Existing Radix props...

    # NEW: Custom sub-theme prop
    icon:
      type: string
      title: Icon
      description: Optional icon class
```

**Step 3: Customize Component Template**

**File: `components/button/button.twig`**
```twig
{# Radix button base logic... #}

{# NEW: Add icon support #}
{% if icon %}
  <i class="{{ icon }}"></i>
{% endif %}

{# Existing content block... #}
```

**Step 4: Add Custom Styles**

**File: `components/button/button.scss`**
```scss
@import '../../src/scss/init';

// Radix button styles are already in Bootstrap

// NEW: Custom button variant
.btn-custom {
  @include button-variant(
    $background: $custom-color,
    $border: $custom-color,
    $color: color-contrast($custom-color)
  );
}
```

**Step 5: Use Sub-Theme Component**

```twig
{# Use sub-theme version (not Radix) #}
{% include 'THEME_NAME:button' with {
  color: 'custom',
  icon: 'icon-arrow',
  content: 'Click Me',
} %}
```

#### Decision Table: Component Discovery Order

| Priority | Namespace | Location | Example |
|----------|-----------|----------|---------|
| 1 | `THEME_NAME:button` | Sub-theme `components/` | Your override |
| 2 | `radix:button` | Radix `components/` | Radix default |
| 3 | `core:button` | Drupal core (if exists) | Core fallback |

**Drupal discovers components in this order.** Sub-theme components override Radix components.

#### Common Mistakes
- **Not copying entire directory** — Copy all files (`.component.yml`, `.twig`, `.scss`, etc.)
- **Using wrong namespace** — Use `THEME_NAME:` for sub-theme components
- **Not maintaining compatibility** — Keep Radix prop structure when possible
- **Forgetting to document changes** — Note what was customized and why

#### See Also
- [8.1 Radix Component Catalog](#81-radix-component-catalog)
- [3.2 SDC Component Structure](#32-sdc-component-structure)

---

### 8.4 Bootstrap Component Architecture Decision Framework

#### When to Use This Section
- You're implementing Bootstrap components in Radix and need guidance on architecture decisions
- You need to understand when to use specific Bootstrap components
- You want to know customization points and performance considerations for Bootstrap components

#### Layout Components

##### Accordion

**Architecture Decision Framework:** Use for FAQ sections, collapsible content regions, or grouped documentation where space conservation is priority.

**Radix Integration Patterns:** Extends Bootstrap accordion with Drupal entity integration patterns for dynamic content.

**SDC Implementation Strategy:** Create accordion components with configurable trigger/content pairs through Drupal field structures.

**Customization Decision Points:**
- Animation timing — Control expand/collapse speed
- Icon positioning — Left vs right, custom icons
- Accessibility enhancements — ARIA attributes, keyboard navigation
- Multi-expand behavior — Allow multiple panels open simultaneously

**Performance Considerations:**
- Minimize DOM manipulation during expand/collapse
- Optimize for mobile touch interactions
- Consider content lazy loading for large accordion sets

**Official Reference:** [Bootstrap Accordion](https://getbootstrap.com/docs/5.3/components/accordion/)

---

##### Cards

**Architecture Decision Framework:** Primary layout component for content entities, teasers, and structured data presentation.

**Radix Integration Patterns:** Deep integration with Drupal view modes and entity display patterns for consistent content presentation.

**SDC Implementation Strategy:** Card variants as SDC components with configurable header/body/footer regions mapped to Drupal fields.

**Customization Decision Points:**
- Border radius consistency — Match design system tokens
- Shadow depth — Elevation levels for visual hierarchy
- Responsive behavior — Stack vs inline layouts
- Content overflow handling — Truncation, ellipsis, or full display

**Performance Considerations:**
- Optimize image loading for card thumbnails (use responsive images)
- Consider virtual scrolling for large card lists
- Use proper cache metadata for entity-based cards

**Official Reference:** [Bootstrap Cards](https://getbootstrap.com/docs/5.3/components/card/)

---

##### Carousel

**Architecture Decision Framework:** Use for hero sections, image galleries, or featured content rotation with accessibility considerations.

**Radix Integration Patterns:** Integration with Drupal media entities and responsive image system for optimized content delivery.

**SDC Implementation Strategy:** Carousel components with configurable slide content through field collections or media references.

**Customization Decision Points:**
- Auto-play behavior — Balance between engagement and accessibility
- Transition effects — Fade vs slide, timing
- Indicator styling — Dots, thumbnails, or numbers
- Mobile swipe integration — Touch gesture support

**Performance Considerations:**
- Image lazy loading for non-visible slides
- Reduced motion preferences (prefers-reduced-motion)
- Touch gesture optimization for mobile

**Official Reference:** [Bootstrap Carousel](https://getbootstrap.com/docs/5.3/components/carousel/)

---

##### Modal

**Architecture Decision Framework:** Use for overlay content, forms, confirmations, or detailed content views without page navigation.

**Radix Integration Patterns:** Integration with Drupal's dialog system and AJAX framework for dynamic content loading.

**SDC Implementation Strategy:** Modal components with configurable triggers and content sources through Drupal's modal API.

**Customization Decision Points:**
- Background treatment — Backdrop opacity, blur effects
- Animation timing — Open/close transitions
- Size variations — Small, default, large, extra-large
- Mobile responsiveness — Full-screen on mobile option

**Performance Considerations:**
- Focus management (trap focus within modal)
- Backdrop click handling — Close on click or prevent
- Keyboard navigation optimization (ESC to close)

**Official Reference:** [Bootstrap Modal](https://getbootstrap.com/docs/5.3/components/modal/)

---

##### Offcanvas

**Architecture Decision Framework:** Use for navigation menus, filters, secondary content areas that slide in from screen edges.

**Radix Integration Patterns:** Integration with Drupal menu system and responsive navigation patterns.

**SDC Implementation Strategy:** Offcanvas components with configurable placement and content integration through menu structures.

**Customization Decision Points:**
- Slide direction — Left, right, top, bottom
- Overlay treatment — Backdrop or push content
- Responsive breakpoint behavior — When to show/hide
- Close mechanisms — Button, backdrop click, swipe

**Performance Considerations:**
- Touch gesture optimization for mobile
- Animation performance (use transform, not position)
- Content loading strategies (eager vs lazy)

**Official Reference:** [Bootstrap Offcanvas](https://getbootstrap.com/docs/5.3/components/offcanvas/)

---

##### Collapse

**Architecture Decision Framework:** Use for progressive disclosure, expandable sections, or content that needs space-efficient presentation.

**Radix Integration Patterns:** Integration with Drupal's states API for form element interactions and content management.

**SDC Implementation Strategy:** Collapse components with configurable triggers and content regions through field structures.

**Customization Decision Points:**
- Animation timing — Smooth vs quick transitions
- Multiple collapse coordination — Accordion-style behavior
- Icon rotation — Visual feedback on state change
- Accessibility announcements — Screen reader support

**Performance Considerations:**
- Smooth animations using CSS transitions
- Content reflow optimization
- Keyboard interaction support

**Official Reference:** [Bootstrap Collapse](https://getbootstrap.com/docs/5.3/components/collapse/)

---

#### Navigation Components

##### Navbar

**Architecture Decision Framework:** Primary site navigation component requiring mobile-first responsive design and accessibility compliance.

**Radix Integration Patterns:** Deep integration with Drupal menu system, user authentication states, and role-based visibility.

**SDC Implementation Strategy:** Navbar components with configurable menu integration through Drupal's menu API and block system.

**Customization Decision Points:**
- Breakpoint behavior — When to collapse to mobile menu
- Brand placement — Logo size, positioning
- Menu item styling — Hover states, active indicators
- Mobile menu patterns — Offcanvas vs collapse

**Performance Considerations:**
- Mobile menu optimization (minimize JavaScript)
- Scroll behavior — Fixed, sticky, or static positioning
- Fixed positioning performance on mobile

**Official Reference:** [Bootstrap Navbar](https://getbootstrap.com/docs/5.3/components/navbar/)

---

##### Breadcrumb

**Architecture Decision Framework:** Use for deep navigation structures, hierarchical content, or complex site architectures requiring path context.

**Radix Integration Patterns:** Integration with Drupal's menu hierarchy and taxonomy term relationships for automatic breadcrumb generation.

**SDC Implementation Strategy:** Breadcrumb components with configurable separator styling and path generation through Drupal's breadcrumb API.

**Customization Decision Points:**
- Separator styling — Icons vs text characters
- Responsive truncation — Hide middle items on mobile
- Schema markup integration — Structured data for SEO
- Active item treatment — Linked vs plain text

**Performance Considerations:**
- Path calculation efficiency in preprocess
- Responsive text handling (truncation)
- Accessibility announcements (current location)

**Official Reference:** [Bootstrap Breadcrumb](https://getbootstrap.com/docs/5.3/components/breadcrumb/)

---

##### Pagination

**Architecture Decision Framework:** Use for large content sets, search results, or any listing requiring content division across multiple pages.

**Radix Integration Patterns:** Integration with Drupal's pager system and Views module for consistent pagination across content types.

**SDC Implementation Strategy:** Pagination components with configurable page ranges and integration through Drupal's pager API.

**Customization Decision Points:**
- Page number display logic — Show all vs truncated range
- Responsive behavior — Hide some numbers on mobile
- Previous/next styling — Icons, text, or both
- Accessibility improvements — ARIA labels, current page

**Performance Considerations:**
- Smooth page transitions with AJAX
- URL state management
- Keyboard navigation support

**Official Reference:** [Bootstrap Pagination](https://getbootstrap.com/docs/5.3/components/pagination/)

---

##### Tabs/Pills

**Architecture Decision Framework:** Use for content organization, multi-step forms, or related content sections requiring tab-based navigation.

**Radix Integration Patterns:** Integration with Drupal's form API for multi-step processes and field group organization.

**SDC Implementation Strategy:** Tab components with configurable content panels and integration through field group structures.

**Customization Decision Points:**
- Tab orientation — Horizontal vs vertical
- Active state styling — Underline, background, or both
- Responsive behavior — Collapse to accordion on mobile
- Content loading strategies — Load all vs lazy load panels

**Performance Considerations:**
- Content lazy loading (don't render hidden tabs)
- Smooth transitions between tabs
- Accessibility focus management

**Official Reference:** [Bootstrap Navs & Tabs](https://getbootstrap.com/docs/5.3/components/navs-tabs/)

---

#### Form Components

##### Form Controls

**Architecture Decision Framework:** Foundation for all form interactions requiring consistent styling and accessibility across Drupal form elements.

**Radix Integration Patterns:** Deep integration with Drupal Form API, field types, and validation systems for consistent form rendering.

**SDC Implementation Strategy:** Form control components with configurable field types and integration through Drupal's form theme system.

**Customization Decision Points:**
- Input sizing — Small, default, large variants
- Focus states — Border color, shadow effects
- Validation styling — Success, error, warning states
- Disabled state treatment — Visual indicators

**Performance Considerations:**
- Form validation performance (client vs server)
- Accessibility announcements for errors
- Mobile input optimization (proper input types)

**Official Reference:** [Bootstrap Form Controls](https://getbootstrap.com/docs/5.3/forms/form-control/)

---

##### Input Groups

**Architecture Decision Framework:** Use for composite form elements requiring combined inputs, buttons, or additional context elements.

**Radix Integration Patterns:** Integration with Drupal's composite field types and form element grouping patterns.

**SDC Implementation Strategy:** Input group components with configurable addon elements through Drupal's form element structures.

**Customization Decision Points:**
- Addon styling — Icons, text, or buttons
- Sizing consistency — Match input sizes
- Focus behavior — Highlight entire group
- Responsive treatment — Stack on mobile if needed

**Performance Considerations:**
- Focus management across grouped elements
- Keyboard navigation within group
- Accessibility group announcements

**Official Reference:** [Bootstrap Input Groups](https://getbootstrap.com/docs/5.3/forms/input-group/)

---

##### Form Validation

**Architecture Decision Framework:** Essential for user experience requiring real-time feedback and accessibility-compliant error handling.

**Radix Integration Patterns:** Integration with Drupal's form validation system and constraint violation handling.

**SDC Implementation Strategy:** Validation components with configurable error display and integration through Drupal's validation API.

**Customization Decision Points:**
- Error message styling — Inline vs grouped
- Validation timing — On blur, on submit, or real-time
- Success state treatment — Show confirmation
- Accessibility announcements — Screen reader feedback

**Performance Considerations:**
- Real-time validation performance (debounce)
- Error state transitions (smooth animations)
- Screen reader compatibility

**Official Reference:** [Bootstrap Validation](https://getbootstrap.com/docs/5.3/forms/validation/)

---

##### Floating Labels

**Architecture Decision Framework:** Use for modern form aesthetics requiring space-efficient labeling and improved user experience.

**Radix Integration Patterns:** Integration with Drupal's form label system and field type rendering for consistent implementation.

**SDC Implementation Strategy:** Floating label components with configurable label behavior through Drupal's form theme hooks.

**Customization Decision Points:**
- Animation timing — Smooth label transitions
- Label positioning — Inside vs above input
- Placeholder integration — Show or hide
- Accessibility considerations — Proper label association

**Performance Considerations:**
- Animation smoothness (CSS transitions)
- Focus state management
- Screen reader compatibility

**Official Reference:** [Bootstrap Floating Labels](https://getbootstrap.com/docs/5.3/forms/floating-labels/)

---

#### UI Components

##### Buttons & Button Groups

**Architecture Decision Framework:** Primary interaction elements requiring consistent styling, accessibility, and behavioral patterns across all user interfaces.

**Radix Integration Patterns:** Integration with Drupal's button theme system, form actions, and operation links for consistent interaction patterns.

**SDC Implementation Strategy:** Button components with configurable variants and integration through Drupal's theme system and operation definitions.

**Customization Decision Points:**
- Color variations — Match design system
- Sizing consistency — Small, default, large
- Icon integration — Position, spacing
- Loading state handling — Spinner, disabled state

**Performance Considerations:**
- Touch target optimization (min 44x44px)
- Interaction feedback (immediate visual response)
- Loading state management

**Official Reference:** [Bootstrap Buttons](https://getbootstrap.com/docs/5.3/components/buttons/)

---

##### Dropdowns

**Architecture Decision Framework:** Use for action menus, filter controls, or space-constrained navigation requiring overlay positioning.

**Radix Integration Patterns:** Integration with Drupal's menu system and operations dropdown for consistent interaction patterns.

**SDC Implementation Strategy:** Dropdown components with configurable menu items through Drupal's menu API and operation structures.

**Customization Decision Points:**
- Positioning logic — Auto-detect best position
- Animation timing — Fade in/out effects
- Keyboard navigation — Arrow keys, enter, escape
- Mobile touch handling — Tap vs hover

**Performance Considerations:**
- Positioning calculations (Popper.js performance)
- Scroll behavior — Close on scroll or reposition
- Accessibility focus management

**Official Reference:** [Bootstrap Dropdowns](https://getbootstrap.com/docs/5.3/components/dropdowns/)

---

##### Badges

**Architecture Decision Framework:** Use for status indicators, counts, labels, or metadata requiring minimal space and high visibility.

**Radix Integration Patterns:** Integration with Drupal's entity status system and taxonomy term display for consistent labeling.

**SDC Implementation Strategy:** Badge components with configurable content and styling through field formatters and entity display.

**Customization Decision Points:**
- Color coding systems — Status-based colors
- Sizing variations — Match text size
- Positioning within content — Inline vs absolute
- Accessibility considerations — Screen reader text

**Performance Considerations:**
- Content update efficiency
- Responsive scaling
- Screen reader announcements

**Official Reference:** [Bootstrap Badges](https://getbootstrap.com/docs/5.3/components/badge/)

---

##### Alerts

**Architecture Decision Framework:** Critical for user feedback requiring accessible messaging and appropriate visual hierarchy for different message types.

**Radix Integration Patterns:** Integration with Drupal's message system and status notifications for consistent user feedback.

**SDC Implementation Strategy:** Alert components with configurable message types through Drupal's messenger service and theme integration.

**Customization Decision Points:**
- Color coding — Info, success, warning, error
- Dismissal behavior — Closeable or persistent
- Icon integration — Status icons
- Animation timing — Fade in/out

**Performance Considerations:**
- Message queueing (avoid overwhelming user)
- Accessibility announcements (live regions)
- Responsive layout handling

**Official Reference:** [Bootstrap Alerts](https://getbootstrap.com/docs/5.3/components/alerts/)

---

##### Progress Bars

**Architecture Decision Framework:** Use for loading states, completion indicators, or progress visualization requiring clear status communication.

**Radix Integration Patterns:** Integration with Drupal's progress API and batch processing for consistent progress indication.

**SDC Implementation Strategy:** Progress components with configurable states through Drupal's progress system and JavaScript integration.

**Customization Decision Points:**
- Animation smoothness — Transition timing
- Color progression — Single vs gradient
- Label positioning — Inside vs outside bar
- Accessibility announcements — Status updates

**Performance Considerations:**
- Animation performance (CSS vs JavaScript)
- Real-time updates efficiency
- Accessibility progress announcements

**Official Reference:** [Bootstrap Progress](https://getbootstrap.com/docs/5.3/components/progress/)

---

##### Spinners

**Architecture Decision Framework:** Use for loading states requiring minimal space and clear activity indication without specific progress metrics.

**Radix Integration Patterns:** Integration with Drupal's AJAX system and loading states for consistent activity indication.

**SDC Implementation Strategy:** Spinner components with configurable variants through Drupal's AJAX framework and theme integration.

**Customization Decision Points:**
- Animation timing — Speed of rotation
- Size variations — Small, default, large
- Color coordination — Match theme colors
- Accessibility handling — Screen reader text

**Performance Considerations:**
- Animation efficiency (CSS animations)
- Accessibility announcements (loading state)
- Responsive scaling

**Official Reference:** [Bootstrap Spinners](https://getbootstrap.com/docs/5.3/components/spinners/)

---

#### See Also
- [8.1 Radix Component Catalog](#81-radix-component-catalog)
- [3.5 SDC Component Best Practices](#35-sdc-component-best-practices)
- [Design System Bootstrap Mapping Guide](/home/camoa/workspace/claude_memory/guides/design-system-bootstrap-mapping.md)