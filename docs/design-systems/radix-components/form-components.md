---
description: "Components for form inputs, form structure, and form element wrappers"
tldr: "Components for form inputs, form structure, and form element wrappers. Use these components to build accessible, Bootstrap-styled forms in Drupal with Radix theme."
---

# Form Components

## When to Use

> Components for form inputs, form structure, and form element wrappers. Use these components to build accessible, Bootstrap-styled forms in Drupal with Radix theme.

## Items

### fieldset
**Description:** Fieldset component for grouping related form elements with legend and description support.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `attributes` | Drupal\Core\Template\Attribute | | The HTML attributes for the fieldset element. |
| `disabled` | ['null', 'boolean'] | | Boolean indicating whether the fieldset element is disabled. |
| `errors` | ['array', 'string', 'null'] | | Any errors for this fieldset element. |
| `required` | ['null', 'boolean'] | | Boolean indicating whether the fieldset element is required. |
| `prefix` | ['array', 'string', 'null'] | | The content to add before the fieldset children. |
| `suffix` | ['array', 'string', 'null'] | | The content to add after the fieldset children. |
| `title_display` | ['array', 'string', 'null'] | | The display setting for the title. |
| `description_display` | ['array', 'string', 'null'] | | The display setting for the description. |
| `fieldset_utility_classes` | array | [] | An array of utility classes. Use to add extra Bootstrap utility classes or custom CSS classes over to this component. |
| `legend_title_utility_classes` | array | [] | An array of utility classes. Use to add extra Bootstrap utility classes or custom CSS classes over to this component. |
| `legend_utility_classes` | array | [] | An array of utility classes. Use to add extra Bootstrap utility classes or custom CSS classes over to this component. |

**Slots:**
| Slot | Description |
|------|-------------|
| `children` | The rendered child elements of the fieldset. |
| `fieldset_suffix` | The rendered suffix of the fieldset. |
| `fieldset_prefix` | The fieldset prefix content. |

**Usage Example:**
```twig
{%
  embed 'radix:fieldset' with {
    disabled: true,
    required: true,
    legend: {
      title: 'Personal Details',
      attributes: create_attribute()
    },
    description: {
      content: 'Please provide your personal details below.',
      attributes: create_attribute()
    }
  }
%}
  {% block children %}
    <div class="mb-3">
      <label for="nameInput" class="form-label">Name</label>
      <input type="text" id="nameInput" class="form-control">
    </div>
  {% endblock %}
{% endembed %}
```

**Gotchas:**
- The `legend` and `description` props must be passed as objects with `title`/`content` and `attributes` properties, not as simple strings.
- When `disabled: true`, all child form elements inherit the disabled state without needing individual disabled attributes.
- Use `legend_utility_classes` for the legend wrapper, `legend_title_utility_classes` for the title itself.

---

### form
**Description:** A form component wrapper. This component is used to create a form element with proper attributes.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `attributes` | Drupal\Core\Template\Attribute | | HTML attributes for the form element. |
| `title_prefix` | array | | Title prefix renderable array. |
| `title_suffix` | array | | Title suffix renderable array. |

**Slots:**
| Slot | Description |
|------|-------------|
| `form_children` | The content block of children. |
| `children` | Default content (children) of the form. |

**Usage Example:**
```twig
{%
  include "radix:form" with {
    attributes: attributes.addClass(['needs-validation']),
  }
%}
```

**Gotchas:**
- This component is a simple wrapper - most form functionality comes from child elements.
- Use `form_children` slot for explicit content placement, or `children` slot for default content.
- For inline forms, you'll need to add Bootstrap's inline form classes manually via `attributes`.

---

### form-element
**Description:** The structure and necessary styling for displaying a form element with label, description, and error handling.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `form_element_attributes` | Drupal\Core\Template\Attribute | | **Dead — not honoured by `form-element.twig`.** Line 73 overwrites it with `attributes ?: create_attribute()`. Pass `attributes` instead. |
| `errors` | ['array', 'string', 'null'] | | Any errors for this form element. |
| `prefix` | ['array', 'string', 'null'] | | The form element prefix. |
| `suffix` | ['array', 'string', 'null'] | | The form element suffix. |
| `required` | ['null', 'boolean'] | | The required marker, or empty if the associated form element is not required. |
| `type` | ['array', 'string', 'null'] | | The type of the element. |
| `name` | ['array', 'string', 'null'] | | The name of the element. |
| `label` | ['array', 'string', 'null'] | | A rendered label element. |
| `label_display` | ['array', 'string', 'null'] | | Label display setting (before, after, invisible, attribute). |
| `description_display` | ['array', 'string', 'null'] | | Description display setting (before, after, invisible). |
| `disabled` | ['array', 'string', 'null'] | | True if the element is disabled. |
| `title_display` | ['array', 'string', 'null'] | | Title display setting. |

**Slots:**
| Slot | Description |
|------|-------------|
| `children` | The form element content. |

**Usage Example:**
```twig
{% include "radix:form-element" with {
  label: 'Email Address',
  required: true,
  type: 'email',
  name: 'user_email',
  description: {
    content: 'We will never share your email.',
    attributes: create_attribute()
  }
} %}
```

**Gotchas:**
- This is a wrapper component - typically used by Drupal's form system, not manually in templates.
- `label_display: 'invisible'` hides the label visually but keeps it accessible to screen readers.
- `label_display: 'attribute'` creates a tooltip instead of a visible label (checkboxes/radios only).

---

### form-element--label
**Description:** The structure and necessary styling for displaying a form element label.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `title` | ['string', 'null'] | | The label's text. |
| `title_display` | ['string', 'null'] | | Elements title_display setting. |
| `required` | ['null', 'boolean'] | | An indicator for whether the associated form element is required. |
| `attributes` | Drupal\Core\Template\Attribute | | HTML attributes for the label element. |

**Slots:**
None

**Usage Example:**
```twig
{% include "radix:form-element--label" with {
  required: true,
  title: "Email Address",
  attributes: create_attribute().addClass(['form-label']),
} %}
```

**Gotchas:**
- Typically used by Drupal's form rendering system, rarely called manually.
- The required indicator is automatically added when `required: true`.
- Use Bootstrap's `.form-label` class via attributes for consistent styling.

---

### form-element--radiocheckbox
**Description:** A form element wrapper that supports radio and checkbox elements with proper Bootstrap styling.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `form_element_radiocheckbox_attributes` | Drupal\Core\Template\Attribute | | **Dead — not honoured by `form-element--radiocheckbox.twig`.** Line 9 overwrites it with `attributes ?: create_attribute()`. Pass `attributes` instead. |
| `type` | string | | The type of the element (radio or checkbox). |
| `name` | string | | The name of the element. |
| `label` | string | | The label element. |
| `title_display` | ['array', 'string', 'null'] | | Title display setting. |
| `disabled` | ['boolean', 'null', 'string'] | | True if the element is disabled. |
| `errors` | ['array', 'string', 'null'] | | Any errors for this form element. |
| `description_display` | ['array', 'string', 'null'] | | Description display setting. |

**Slots:**
| Slot | Description |
|------|-------------|
| `children` | The input element content. |

**Usage Example:**
```twig
{% include "radix:form-element--radiocheckbox" with {
  type: 'checkbox',
  name: 'agree_terms',
  label: 'I agree to the terms and conditions',
  required: true
} %}
```

**Gotchas:**
- This component automatically applies Bootstrap's `.form-check` wrapper styling.
- For radio buttons, ensure all options in a group share the same `name` attribute.
- Use the standard `form-element` component for text inputs, not this one.

---

### input
**Description:** Give textual form controls an upgrade with custom styles, sizing, focus states, and more.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `type` | string | — | **Dead.** Declared in the YAML, never read by `input.twig`. Set the type through `attributes` instead. |
| `value` | string | — | **Dead.** Declared in the YAML, never read by `input.twig`. Set the value through `attributes` instead. |
| `remove_form_control` | boolean | false | Allows to remove the form-control class. Use mainly for checkboxes and radio buttons. |
| `input_utility_classes` | array | [] | An array of additional utility classes to add to the input. |
| `attributes` | Drupal\Core\Template\Attribute | {} | HTML attributes for the input element. |

**Slots:**
| Slot | Description |
|------|-------------|
| `children` | Optional additional rendered elements. |

**Usage Example:**
```twig
{%
  include 'radix:input' with {
    attributes: create_attribute()
      .setAttribute('type', 'email')
      .setAttribute('placeholder', 'Enter your email')
      .setAttribute('id', 'emailInput'),
    input_utility_classes: ['mb-3'],
  }
%}
```

**Gotchas:**
- **`type` and `value` do nothing.** `input.twig` renders a single `<input{{ attributes.addClass(input_classes) }}>` and never reads either prop, so `type: 'email'` renders a plain text input with no error. Put both on `attributes`: `.setAttribute('type', 'email').setAttribute('value', 'foo')`.
- By default, `.form-control` class is added automatically. Set `remove_form_control: true` for checkboxes/radios.
- For file inputs, set `attributes.setAttribute('type', 'file')`; `.form-control` is still applied, which is Bootstrap 5's own file-input styling.
- The `children` slot is rarely used - it's mainly for Drupal's internal rendering.

---

### radios
**Description:** A component representing a group of radio buttons in a form, styled and customizable.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `attributes` | Drupal\Core\Template\Attribute | | HTML attributes for the component wrapper element. |

**Slots:**
| Slot | Description |
|------|-------------|
| `children` | The radio buttons that are part of the Radios component. |

**Usage Example:**
```twig
{%
  include 'radix:radios' with {
    attributes: create_attribute().addClass(['mb-3']),
  }
%}
```

**Gotchas:**
- This component is a wrapper for multiple radio inputs, not individual radios.
- Individual radio buttons are typically rendered via `form-element--radiocheckbox`.
- Drupal's Form API automatically uses this component for radio button groups.

---

### select
**Description:** A component representing a dropdown select input in a form, styled and customizable.
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `select_attributes` | Drupal\Core\Template\Attribute | | **Dead — not honoured by `select.twig`.** Line 18 overwrites it with `attributes ?: create_attribute()`. Pass `attributes` instead. |

**Slots:**
None

**Usage Example:**
```twig
{%
  include 'radix:select' with {
    attributes: create_attribute()
      .addClass(['form-select'])
      .setAttribute('id', 'countrySelect'),
    options: country_options
  }
%}
```

**Gotchas:**
- The class this component applies is `.form-control`, not `.form-select` (`select.twig:21`). To get Bootstrap's select styling, add `.form-select` yourself through `attributes` as the example does.
- The `options` variable must be structured correctly (with `type`, `label`, `value`, `selected` properties).
- For optgroups, set `type: 'optgroup'` and include nested `options` array.

---

### textarea
**Description:** A themed component for a multiline form input control (textarea).
**Status:** experimental

**Props:**
| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `attributes` | Drupal\Core\Template\Attribute | | HTML attributes assigned to the textarea element. |
| `value` | string | | The content of the textarea. |
| `textarea_utility_classes` | array | [] | Additional classes merged onto the `<textarea>` (`textarea.twig:18`). The `.component.yml` declares the name as `table_utility_classes`; that name is dead — the Twig reads only `textarea_utility_classes`. |

**Slots:**
None

**Usage Example:**
```twig
{%
  include 'radix:textarea' with {
    value: 'Initial content',
    attributes: create_attribute()
      .setAttribute('rows', '5')
      .setAttribute('placeholder', 'Enter your message'),
    textarea_utility_classes: ['mb-3']
  }
%}
```

**Gotchas:**
- Bootstrap's `.form-control` class is automatically applied.
- `table_utility_classes`, the name in the `.component.yml`, does not work. Pass `textarea_utility_classes` — the only name `textarea.twig` reads.
- Use `attributes.setAttribute('rows', 'N')` to control height, or use utility classes like `.form-control-lg`.

---

## Common Mistakes
- **Using wrong wrapper component**: Radio/checkbox inputs require `form-element--radiocheckbox`, not the standard `form-element`. Text inputs use `form-element`.
- **Forgetting `.form-control` removal**: When using the `input` component for checkboxes/radios, you must set `remove_form_control: true` or styling will break.
- **Passing simple strings to fieldset legend**: The `legend` prop expects an object with `title` and `attributes` keys, not a plain string.
- **Incorrect label_display values**: Valid values are `before`, `after`, `invisible`, and `attribute` (attribute only works for checkboxes/radios). Typos will break label positioning.
- **Not grouping radios with same name**: All radio buttons in a group must share the same `name` attribute, or they won't function as mutually exclusive options.
- **Overriding Bootstrap classes unnecessarily**: These components automatically add Bootstrap form classes (`.form-control`, `.form-select`, `.form-check`). Adding them manually via attributes creates duplicates.

## See Also
- Bootstrap 5.3 Forms Documentation: https://getbootstrap.com/docs/5.3/forms/overview/
- Bootstrap Form Controls: https://getbootstrap.com/docs/5.3/forms/form-control/
- Bootstrap Checks and Radios: https://getbootstrap.com/docs/5.3/forms/checks-radios/
- Drupal Form API Guide (for context on when these components are used)
- Input component (for individual form controls)
- Button component (for form submit buttons)
