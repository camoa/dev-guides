---
description: Components for interactive elements, user feedback, and visual indicators
---

# UI Components

## When to Use

> Components for interactive elements, user feedback, and visual indicators. Use these to provide contextual information, loading states, and user interaction controls.

Components for interactive elements, user feedback, and visual indicators. Use these to provide contextual information, loading states, and user interaction controls.

### Items

#### alert
**Description:** Provide contextual feedback messages for typical user actions with the handful of available and flexible alert messages.
**Status:** stable
**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `type` | string | primary | The type of the alert (primary, secondary, success, danger, warning, info, light, dark). **(required)** |
| `dismissible` | boolean |  | Enable close button for dismissing alert |
| `heading` | string |  | Optional heading text |
| `alert_utility_classes` | array | [] | An array of utility classes. Use to add extra Bootstrap utility classes or custom CSS classes over to this component. |
| `attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the alert element |

**Slots:**
| Slot | Description |
|------|-------------|
| `alert_heading` | The heading of the alert. |
| `content` | The content of the alert. |

**Usage Example:**
```twig
{%
  include 'radix:alert' with {
    type: 'danger',
    heading: 'Important Notice!',
    dismissible: true,
    alert_utility_classes: ['mb-4', 'shadow-sm'],
    content: 'This is an important alert message. Please pay attention!'
  }
%}
```
**Gotchas:**
- `type` prop is required - component will not render properly without it
- For dismissible alerts, Bootstrap JS must be initialized
- Content slot overrides the `content` prop if both are provided

#### badge
**Description:** Documentation and examples for badges, our small count and labeling component.
**Status:** experimental
**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `badge_html_tag` | string | span | The HTML tag to use for the badge. Enum: `span, div, a` |
| `badge_url` | string |  | URL link for Badge when the HTML tag is an anchor link. |
| `color` | string | secondary | Set a background-color with contrasting foreground color. Enum: `primary, secondary, success, info, warning, danger, light, dark` |
| `badge_utility_classes` | array | [] | An array of utility classes. Use to add extra Bootstrap utility classes or custom CSS classes over to this component. |
| `badge_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for the badge element |

**Slots:**
| Slot | Description |
|------|-------------|
| `badge_content` | Badge content block. |
| `content` | Default content for Badge. |

**Usage Example:**
```twig
{%
  include 'radix:badge' with {
    badge_html_tag: 'a',
    badge_url: '/notifications',
    color: 'primary',
    content: '4'
  }
%}
```
**Gotchas:**
- When using `badge_html_tag: 'a'`, must provide `badge_url` for proper link functionality
- `.text-bg-{color}` classes replaced older `.text-{color}` and `.bg-{color}` pattern
- Badge content should be brief - typically numbers or short text

#### button
**Description:** Use Bootstrap custom button styles for actions in forms, dialogs, and more with support for multiple sizes, states, and more.
**Status:** experimental
**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `button_html_tag` | string | button | The HTML tag to use for the button. Enum: `button, a` |
| `url` | string, null |  | URL link for the button when the HTML tag is an anchor link. |
| `id` | string |  | The ID of the button. |
| `color` | string |  | Bootstrap button color. Enum: `primary, secondary, success, danger, warning, info, dark, light, link` |
| `outline` | boolean | false | Use outline style instead of solid background |
| `size` | string |  | Bootstrap button size (btn-sm, btn-lg) |
| `disabled` | boolean | false | Disabled button |
| `button_utility_classes` | array | [] | An array of utility classes. Use to add extra Bootstrap utility classes or custom CSS classes over to this component. |
| `button_attributes` | Drupal\Core\Template\Attribute |  | A list of HTML attributes for the button. |

**Slots:**
| Slot | Description |
|------|-------------|
| `content` | The content for the button |

**Usage Example:**
```twig
{%
  include 'radix:button' with {
    color: 'primary',
    size: 'btn-lg',
    content: 'Submit Form',
    button_utility_classes: ['w-100']
  }
%}
```
**Gotchas:**
- When using `button_html_tag: 'a'`, must provide `url` prop or it will render as non-clickable
- For disabled anchor buttons, add `aria-disabled="true"` via `button_attributes`
- Link style buttons (`color: 'link'`) don't have solid backgrounds but still need proper contrast

#### button-group
**Description:** Creates a group of buttons or inputs.
**Status:** experimental
**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `vertical` | boolean | false | Whether to render the button group vertically. |
| `size` | string | md | The size of the button group. Enum: `sm, md, lg` |
| `aria_label` | string |  | The aria-label attribute of the button group. |
| `toolbar` | boolean | false | Whether to render the button group as a toolbar. |
| `toolbar_aria_label` | string |  | The aria-label attribute of the toolbar. |
| `items` | array | [] | An array of buttons or inputs. |
| `button_group_attribute` | Drupal\Core\Template\Attribute |  | HTML attributes for the button group |

**Slots:**
| Slot | Description |
|------|-------------|
| `content` | Content text for the button group. |

**Usage Example:**
```twig
{%
  include 'radix:button-group' with {
    size: 'lg',
    aria_label: 'Pagination controls',
    items: [
      { content: 'Previous', color: 'primary' },
      { content: 'Next', color: 'primary' }
    ]
  }
%}
```
**Gotchas:**
- `aria_label` is required for accessibility when using button groups
- For toolbars containing multiple button groups, set `toolbar: true` and provide `toolbar_aria_label`
- Items structure depends on content - use content slot for complex layouts

#### close-button
**Description:** A generic close button for dismissing content like modals and alerts.
**Status:** experimental
**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `size` | string |  | Bootstrap button size class (btn-sm, btn-lg) |
| `disabled` | boolean | false | Disabled button |

**Slots:**
No slots defined.

**Usage Example:**
```twig
{%
  include 'radix:close-button' with {
    size: 'btn-sm',
    disabled: false,
    close_button_attributes: create_attribute()
      .setAttribute('data-bs-dismiss', 'modal')
  }
%}
```
**Gotchas:**
- Requires `data-bs-dismiss` attribute to work with Bootstrap dismissible components (modal, toast, alert)
- Bootstrap JS must be initialized for dismiss functionality
- Close button has built-in accessibility markup (aria-label="Close")

#### dropdown
**Description:** Toggle contextual overlays for displaying lists of links and more with the Bootstrap dropdown plugin.
**Status:** experimental
**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `items` | array |  | Menu Items |
| `dropdown_button_content` | string |  | Dropdown button content |
| `dropdown_button_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for dropdown button |
| `dropdown_button_html_tag` | string | button | The HTML tag to use for the button. Enum: `button, a` |
| `dropdown_button_url` | string |  | Dropdown button URL |
| `dropdown_size` | string |  | Bootstrap button size. Enum: `null, btn-sm, btn-lg` |
| `split_button` | boolean | false | Split button style |
| `dropdown_utility_classes` | array |  | Dropdown utility classes |
| `dropdown_item_utility_classes` | array |  | Dropdown item utility classes |
| `dropdown_button_utility_classes` | array |  | Dropdown button utility classes |
| `dropdown_menu_utility_classes` | array |  | Dropdown menu utility classes |
| `dropdown_color` | string |  | Bootstrap button color. Enum: `primary, secondary, success, danger, warning, info, dark, light, link` |
| `outline` | boolean | false | Use outline style for button |
| `disabled` | boolean | false | Disabled button |
| `dropdown_item_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for dropdown items |
| `dropdown_menu_attributes` | Drupal\Core\Template\Attribute |  | HTML attributes for dropdown menu |

**Slots:**
| Slot | Description |
|------|-------------|
| `dropdown_toggler` | Dropdown toggler |
| `dropdown_menu` | Dropdown menu |

**Usage Example:**
```twig
{%
  include 'radix:dropdown' with {
    dropdown_button_content: "Actions",
    dropdown_color: 'secondary',
    dropdown_size: 'btn-sm',
    split_button: true,
    outline: true,
    items: [
      { title: 'Edit', url: '/edit' },
      { title: 'Delete', url: '/delete' }
    ]
  }
%}
```
**Gotchas:**
- Bootstrap dropdown JS plugin must be initialized for toggle functionality
- When using `split_button: true`, dropdown button is split from main action button
- Items need proper structure with `title` and `url` keys

#### dropdown-menu
**Description:** A dropdown menu component. This component is used to create a dropdown menu.
**Status:** experimental
**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `items` | array |  | Menu Items |
| `attributes` | Drupal\Core\Template\Attribute |  | HTML attributes |
| `dropdown_menu_utility_classes` | array |  | Additional utility classes that can be added to the nav component. These classes should be defined in your theme's CSS. |
| `nav_utility_classes` | array |  | Additional utility classes that can be added to the nav component. |
| `nav_link_utility_classes` | array |  | Additional utility classes that can be added to the nav links. |
| `alignment` | string |  | Alignment of the nav component. Enum: `null, right, center, vertical` |
| `dropdown_direction` | string |  | Dropdown Direction. Enum: `dropstart, dropend` |

**Slots:**
No slots defined.

**Usage Example:**
```twig
{%
  include 'radix:dropdown-menu' with {
    items: item.below,
    alignment: 'right',
    dropdown_direction: 'dropend'
  }
%}
```
**Gotchas:**
- Typically used within nav or dropdown components, not standalone
- `items` must be properly structured menu array (typically `item.below` from Drupal menu)
- Direction controls (dropstart/dropend) affect where submenu appears

#### progress
**Description:** Progress components are built with two HTML elements, some CSS to set the width, and a few attributes.
**Status:** experimental
**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `progress_utility_classes` | array | [] | An array of utility classes. Use to add extra Bootstrap utility classes or custom CSS classes over to this component. |
| `progress_bar_utility_classes` | array | [] | An array of utility classes. Use to add extra Bootstrap utility classes or custom CSS classes over to this component. |
| `color` | string |  | The color of the progress bar. Enum: `primary, secondary, success, danger, warning, info, light, dark` |
| `label` | string, integer, null |  | Aria label for the progress bar. |
| `stacked` | boolean | false | True if the progress bar should be stacked. |
| `valuenow` | integer, string, null | 0 | The current value of the progress bar. |
| `valuemins` | integer | 0 | The minimum value of the progress bar. |
| `valuemax` | integer | 100 | The maximum value of the progress bar. |
| `height` | integer | 16 | The height of the progress bar. |
| `striped` | boolean | true | True if the progress bar should be striped. |
| `animated` | boolean | true | True if the progress bar should be animated. |

**Slots:**
No slots defined.

**Usage Example:**
```twig
{%
  include 'radix:progress' with {
    color: 'success',
    animated: true,
    striped: true,
    label: '60% Complete',
    height: 20,
    valuenow: 60,
    valuemax: 100
  }
%}
```
**Gotchas:**
- `valuenow` as percentage is calculated automatically from `valuenow/valuemax * 100`
- Animated stripes only work when `striped: true` and `animated: true` are both set
- For stacked progress bars, use nested includes with different colors

#### spinner
**Description:** Indicate the loading state of a component or page with Bootstrap spinners, built entirely with HTML, CSS, and no JavaScript.
**Status:** experimental
**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `spinner_html_tag` | string | div | Having the spinner as div or span. Enum: `div, span` |
| `type` | string | border | Spinner type. Enum: `border, grow` |
| `color` | string |  | Built with current Color. Enum: `primary, secondary, success, danger, warning, info, dark, light` |
| `size` | string |  | Make a smaller spinner. Enum: `sm` |
| `hidden_status` | boolean | true | Hidden spinner status message. |
| `spinner_utility_classes` | array | [] | An array of utility classes that can be used to add extra Bootstrap utility classes or custom classes to this component. |
| `spinner_attributes` | Drupal\Core\Template\Attribute |  | A list of HTML attributes for the Spinner element. |
| `spinner_status_attributes` | Drupal\Core\Template\Attribute |  | A list of HTML attributes for the Spinner status element. |

**Slots:**
| Slot | Description |
|------|-------------|
| `content` | Spinner content (status text like "Loading...") |

**Usage Example:**
```twig
{%
  include 'radix:spinner' with {
    spinner_html_tag: 'div',
    type: 'border',
    color: 'primary',
    size: 'sm',
    hidden_status: false,
    content: 'Loading...'
  }
%}
```
**Gotchas:**
- Border spinners are more lightweight than grow spinners
- Status text should always be provided via content slot for screen readers
- Use `hidden_status: false` to show loading text visually, or `true` to hide it (but keep for accessibility)

#### toasts
**Description:** Toasts component, see Bootstrap Documentation: https://getbootstrap.com/docs/5.3/components/toasts/
**Status:** experimental
**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `with_wrapper` | boolean | false | True if the toast has an additional wrapper element. |
| `wrapper_classes` | string |  | Additional classes to add to the toast wrapper. |
| `wrapper_aria_live` | string | polite | ARIA live attribute for the toast wrapper. |
| `with_container` | boolean | true | True if the toast should be contained within a div element. |
| `container_classes` | string |  | Additional classes to add to the toast container. |
| `additional_buttons_utility_classes` | array | [] | An array of utility classes. Use to add extra Bootstrap utility classes or custom CSS classes over to this component. |
| `toasts` | array |  | An array of toast objects each containing its own set of properties (header, body, role, autohide, delay, attributes, additional_buttons). |

**Slots:**
| Slot | Description |
|------|-------------|
| `content` | Default content text for the toast. |

**Usage Example:**
```twig
{%
  include 'radix:toasts' with {
    with_container: true,
    container_classes: 'position-fixed bottom-0 end-0 p-3',
    toasts: [
      {
        header: {
          title: 'Success',
          subtitle: 'Just now',
          classes: 'text-success bg-light'
        },
        body: 'Item saved successfully.',
        role: 'alert',
        autohide: true,
        delay: 5000,
        with_close: true
      }
    ]
  }
%}
```
**Gotchas:**
- Requires Bootstrap Toast JS initialization to function (see Radix `_toast-init.js`)
- Positioning via `container_classes` (e.g., `position-fixed bottom-0 end-0 p-3`)
- Each toast in array needs proper structure with header/body objects

#### tooltips
**Description:** Documentation-only component (no component.yml or twig template). See Bootstrap Tooltips Documentation: https://getbootstrap.com/docs/5.3/components/tooltips/
**Status:** Not implemented as SDC
**Props:**
N/A - Use Bootstrap data attributes directly.

**Slots:**
N/A

**Usage Example:**
```twig
{# Apply tooltip via data attributes on any element #}
<button 
  type="button" 
  class="btn btn-secondary" 
  data-bs-toggle="tooltip" 
  data-bs-placement="top" 
  data-bs-title="Tooltip on top">
  Hover me
</button>
```
**Gotchas:**
- Tooltips must be initialized via JavaScript: `const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]'); const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));`
- Radix does not provide a Twig SDC wrapper for tooltips - use Bootstrap's native data attributes
- Tooltips on disabled elements require wrapper element

### Common Mistakes
- Forgetting to initialize Bootstrap JS for interactive components (dropdowns, toasts, tooltips)
- Using dismissible alerts/modals without `data-bs-dismiss` attribute on close buttons
- Not providing required accessibility attributes (`aria-label` for button groups, spinner status text)
- Using anchor button styles without providing `url` prop
- Assuming tooltips work without JS initialization

### See Also
- [Bootstrap Components Documentation](https://getbootstrap.com/docs/5.3/components/)
- Design System Radix SDC Mapping Guide (Section 7: Form Controls & Interactive Elements)
- Drupal JS Development Guide (for initializing Bootstrap components)
