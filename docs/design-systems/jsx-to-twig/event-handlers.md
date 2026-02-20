---
description: Convert React event handlers to Drupal behaviors and server-side patterns
drupal_version: "11.x"
---

# Event Handlers to Drupal Behaviors

## When to Use

> Use this when converting React event handlers (`onClick`, `onChange`, `onSubmit`, etc.) to Drupal's server-rendered architecture. React events have NO direct Twig equivalent. The translation requires separating markup (Twig) from behavior (JavaScript or server-side).

## Decision: Event Handler Mapping

| React Event | Drupal Equivalent | When to Use |
|---|---|---|
| `onClick` (toggle, show/hide) | CSS-only (`:checked`, `<details>`) or `data-*` + `Drupal.behaviors` | Prefer CSS-only for simple toggles; use behaviors for complex logic |
| `onClick` (navigation) | Standard `<a href>` link | No JS needed -- server-side navigation |
| `onClick` (API call) | `Drupal.behaviors` + `fetch()` or HTMX `hx-get` | Client-side API call or HTMX for HTML fragment |
| `onChange` (form input) | Drupal Form API `#ajax` callback | Server processes change; returns updated markup |
| `onChange` (live filter/search) | `Drupal.behaviors` + debounced fetch, or HTMX `hx-trigger="keyup changed delay:300ms"` | Client-side filtering or server-side with HTMX |
| `onSubmit` | Drupal Form API | Form submit is always server-side in Drupal |
| `onHover` / `onMouseEnter` | CSS `:hover` pseudo-class | Almost never needs JS; pure CSS |
| `onFocus` / `onBlur` | CSS `:focus` / `:focus-within` or `Drupal.behaviors` | CSS for visual states; JS for complex focus management |
| `onScroll` | `Drupal.behaviors` with `IntersectionObserver` | No Twig involvement; pure JS behavior |
| `onKeyDown` | `Drupal.behaviors` with `addEventListener('keydown')` | Accessibility handlers for keyboard navigation |

## Pattern: CSS-Only Toggle

**React**
```jsx
function Accordion({ title, children }) {
  const [open, setOpen] = useState(false);
  return (
    <div>
      <button onClick={() => setOpen(!open)}>{title}</button>
      {open && <div>{children}</div>}
    </div>
  );
}
```

**Twig** (using HTML `<details>`)
```twig
<details {{ attributes.addClass('collapse') }}>
  <summary class="collapse-title font-semibold">
    {{ title }}
  </summary>
  <div class="collapse-content">
    {{ content }}
  </div>
</details>
```

The `<details>` / `<summary>` HTML elements provide native toggle behavior without any JavaScript.

## Pattern: Data Attributes + Drupal Behavior

**React**
```jsx
function Tabs({ items, defaultIndex = 0 }) {
  const [active, setActive] = useState(defaultIndex);
  return (
    <div>
      {items.map((item, i) => (
        <button key={i} onClick={() => setActive(i)}
          className={i === active ? 'tab-active' : ''}>
          {item.label}
        </button>
      ))}
      <div>{items[active].content}</div>
    </div>
  );
}
```

**Twig** (markup with data attributes)
```twig
<div {{ attributes.addClass('tabs-container') }}
     data-default-index="{{ default_index|default(0) }}">
  <div class="tabs" role="tablist">
    {% for item in items %}
      <button class="tab" role="tab"
              data-tab-index="{{ loop.index0 }}"
              aria-selected="{{ loop.index0 == 0 ? 'true' : 'false' }}">
        {{ item.label }}
      </button>
    {% endfor %}
  </div>
  {% for item in items %}
    <div class="tab-panel" role="tabpanel"
         data-panel-index="{{ loop.index0 }}"
         {{ loop.index0 != 0 ? 'hidden' }}>
      {{ item.content }}
    </div>
  {% endfor %}
</div>
```

**JavaScript behavior** (separate `.js` file in SDC)
```js
(function (Drupal) {
  Drupal.behaviors.tabsComponent = {
    attach(context) {
      const containers = once('tabs', '.tabs-container', context);
      containers.forEach((container) => {
        const tabs = container.querySelectorAll('[role="tab"]');
        const panels = container.querySelectorAll('[role="tabpanel"]');
        tabs.forEach((tab) => {
          tab.addEventListener('click', () => {
            const index = tab.dataset.tabIndex;
            tabs.forEach(t => t.setAttribute('aria-selected', 'false'));
            tab.setAttribute('aria-selected', 'true');
            panels.forEach(p => p.hidden = p.dataset.panelIndex !== index);
          });
        });
      });
    },
  };
})(Drupal);
```

## Key Principle

The separation of concerns in Drupal is absolute:

- **Twig** renders the initial HTML structure with semantic markup, ARIA attributes, and `data-*` attributes
- **JavaScript** (via `Drupal.behaviors`) attaches interactivity after render
- **CSS** handles visual state changes (`:hover`, `:focus`, `:checked`, `[aria-selected="true"]`)

## Common Mistakes

- **Wrong**: Adding `onclick` inline handlers in Twig for complex logic → **Right**: Use `data-*` attributes and `Drupal.behaviors` instead
- **Wrong**: Trying to replicate React's `useState` in Twig → **Right**: Twig is server-rendered once; client state lives in JavaScript
- **Wrong**: Forgetting to use `once()` in behaviors → **Right**: `Drupal.behaviors.attach` runs on every AJAX response; without `once()`, event listeners accumulate

## See Also

- [Conditional Rendering](conditional-rendering.md)
- [Component Composition](composition.md)
- Reference: [Drupal JavaScript API](https://www.drupal.org/docs/develop/drupal-apis/javascript-api/javascript-api-overview)
