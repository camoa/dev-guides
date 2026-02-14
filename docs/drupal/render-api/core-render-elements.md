---
description: Reference for built-in render element plugins -- link, table, container, html_tag, inline_template, details, status_messages.
---

# Core Render Elements

## When to Use

When you need pre-built, reusable output patterns -- links, tables, containers, HTML tags, status messages. Render elements are plugins that encapsulate complex rendering logic.

## Common Render Elements

### link

Generates an HTML link with proper URL handling and access checking.

| Property | Type | Default | Notes |
|---|---|---|---|
| `#title` | string/Markup | required | Link text (translatable) |
| `#url` | Url object | required | `Url::fromRoute()` or `Url::fromUri()` |
| `#options` | array | `[]` | Passed to link generator (attributes, query, fragment) |

```php
$build['link'] = [
  '#type' => 'link',
  '#title' => $this->t('View Node'),
  '#url' => Url::fromRoute('entity.node.canonical', ['node' => 1]),
  '#options' => ['attributes' => ['class' => ['button']]],
];
```

**Gotchas:**

- URL must be a `Url` object, not a string
- Access checking happens automatically based on route permissions
- `#attributes` at top level are merged into `#options['attributes']`

**Reference:** `core/lib/Drupal/Core/Render/Element/Link.php`

---

### table

Formats data as an HTML table with headers, rows, optional responsive/sticky behavior.

| Property | Type | Default | Notes |
|---|---|---|---|
| `#header` | array | `[]` | Column headers |
| `#rows` | array | `[]` | Data rows (can use render arrays in cells) |
| `#empty` | string | `''` | Message when no rows |
| `#responsive` | bool | `TRUE` | Add responsive table library |
| `#sticky` | bool | `FALSE` | Sticky headers on scroll |
| `#caption` | string | -- | Table `<caption>` |
| `#footer` | array | -- | Footer rows |

```php
$build['table'] = [
  '#type' => 'table',
  '#header' => [$this->t('Name'), $this->t('Email')],
  '#rows' => [
    [['data' => ['#markup' => 'Alice']], ['data' => ['#markup' => 'alice@example.com']]],
    [['data' => ['#markup' => 'Bob']], ['data' => ['#markup' => 'bob@example.com']]],
  ],
  '#empty' => $this->t('No users found.'),
];
```

**Gotchas:**

- Each cell can be a simple string OR `['data' => render_array, 'colspan' => 2]`
- Can use children instead of `#rows` -- see `Table::preRenderTable()`
- Responsive behavior requires `drupal.tableresponsive` library (auto-attached)

**Reference:** `core/lib/Drupal/Core/Render/Element/Table.php`

---

### container

Wraps children in a `<div>` with attributes. Simplest structural element.

| Property | Type | Default | Notes |
|---|---|---|---|
| `#optional` | bool | `FALSE` | If `TRUE`, don't render if no visible children |
| `#attributes` | array | `[]` | HTML attributes for the `<div>` |

```php
$build['wrapper'] = [
  '#type' => 'container',
  '#attributes' => ['class' => ['content-wrapper'], 'id' => 'main-content'],
  'title' => ['#markup' => '<h2>Title</h2>'],
  'body' => ['#markup' => '<p>Body text.</p>'],
];
```

**Gotchas:**

- Auto-generates `#id` if not set
- With `#optional => TRUE`, empty containers disappear (useful for conditional wrappers)
- `#states` support for showing/hiding based on form element values

**Reference:** `core/lib/Drupal/Core/Render/Element/Container.php`

---

### html_tag

Renders any HTML tag with attributes and value. Escape hatch for semantic HTML.

| Property | Type | Default | Notes |
|---|---|---|---|
| `#tag` | string | required | Tag name (escaped) |
| `#value` | string/Markup | `NULL` | Inner HTML (XSS filtered if string) |
| `#attributes` | array | `[]` | HTML attributes |
| `#noscript` | bool | `FALSE` | Wrap in `<noscript>` |

```php
$build['meta'] = [
  '#type' => 'html_tag',
  '#tag' => 'meta',
  '#attributes' => ['name' => 'description', 'content' => 'Page description'],
];

$build['heading'] = [
  '#type' => 'html_tag',
  '#tag' => 'h1',
  '#value' => $this->t('Welcome'),
];
```

**Gotchas:**

- Void elements (`<br>`, `<img>`, `<input>`, etc.) auto-close -- don't use `#value` with them
- Tag name is escaped -- can't inject arbitrary HTML
- `#value` is XSS filtered unless it's a `Markup` object

**Reference:** `core/lib/Drupal/Core/Render/Element/HtmlTag.php`

---

### inline_template

Renders an inline Twig template with variables. Useful for simple templating without `.html.twig` files.

| Property | Type | Default | Notes |
|---|---|---|---|
| `#template` | string | required | Inline Twig template string |
| `#context` | array | `[]` | Variables available in template |

```php
$build['greeting'] = [
  '#type' => 'inline_template',
  '#template' => '{% trans %}Hello{% endtrans %} <strong>{{ name }}</strong>!',
  '#context' => ['name' => $user->getDisplayName()],
];
```

**Gotchas:**

- Context variables can be strings OR render arrays (Twig auto-renders them)
- No access to full Twig environment globals -- explicitly pass what you need
- Overuse makes code hard to maintain -- prefer real templates for complex HTML

**Reference:** `core/lib/Drupal/Core/Render/Element/InlineTemplate.php`

---

### details

Collapsible details/summary element (HTML `<details>`).

| Property | Type | Default | Notes |
|---|---|---|---|
| `#title` | string | required | Summary text (always visible) |
| `#open` | bool | `FALSE` | Start expanded |
| `#attributes` | array | `[]` | HTML attributes for `<details>` |

```php
$build['advanced'] = [
  '#type' => 'details',
  '#title' => $this->t('Advanced Options'),
  '#open' => FALSE,
  'option1' => ['#markup' => $this->t('Option 1 content')],
  'option2' => ['#markup' => $this->t('Option 2 content')],
];
```

**Gotchas:**

- Native HTML5 `<details>` -- no JavaScript required for basic functionality
- Can nest details elements
- `#open` state not remembered unless you add custom logic

**Reference:** `core/lib/Drupal/Core/Render/Element/Details.php`

---

### status_messages

Renders Drupal status messages (success, warning, error).

```php
$build['messages'] = [
  '#type' => 'status_messages',
];
```

**Gotchas:**

- Automatically picks up all queued messages from `messenger()` service
- Usually added to page template, not individual components
- Messages are displayed once then cleared

**Reference:** `core/lib/Drupal/Core/Render/Element/StatusMessages.php`

## Common Mistakes

- **Using `#type => 'markup'`** -- Doesn't exist. Use `#markup` property instead (no `#type` needed)
- **Not passing required properties** -- Element plugins expect certain properties; check `getInfo()` for defaults
- **Confusing render elements with form elements** -- Many form elements (textfield, select) only work inside forms
- **Assuming all properties work on all elements** -- Each element plugin defines what it supports

## See Also

- [Form Render Elements](form-render-elements.md) for form-specific elements
- [Custom Render Elements](custom-render-elements.md) to create your own
- Reference: [What Are Render Elements?](https://www.drupal.org/docs/drupal-apis/render-api/render-elements/what-are-render-elements)
