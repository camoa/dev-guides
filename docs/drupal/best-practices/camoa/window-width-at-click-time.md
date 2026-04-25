---
description: Check window.innerWidth at click time, not at Drupal behavior attach time — once() captures a snapshot that goes stale on resize.
drupal_version: "11.x"
tldr: Check `window.innerWidth` at click time, not at Drupal behavior attach time. `once()` runs once at page load — if the window was desktop-width then, mobile behavior breaks on resize.
---

# Window Width at Click Time

**What:** Check `window.innerWidth` at click time, not at Drupal behavior attach time. `once()` runs once at page load — if the window was desktop-width then, mobile behavior breaks on resize.

**Rationale:** Drupal `behaviors.attach` + `once()` is designed to wire up DOM elements once per element lifetime. Reading viewport width inside that wire-up captures a snapshot. If a user loads desktop, then narrows the window (DevTools, side panel, screen rotation), the captured value is stale and the wrong branch runs forever. Reading width inside the click handler reflects the actual viewport at the moment the user interacts.

**When it applies:** Any JS behavior whose action depends on viewport size — mobile drawer vs desktop dropdown, click vs hover, modal vs inline. Resize events ARE fine for layout updates; the rule is specifically about decision-time inside event handlers.

**Example:**

```js
// Wrong — width captured at attach time, never updated
Drupal.behaviors.menu = {
  attach(context) {
    once('menu-init', '.menu-toggle', context).forEach((el) => {
      const isMobile = window.innerWidth < 992;  // ← snapshot, stale on resize
      el.addEventListener('click', () => {
        if (isMobile) openDrawer();
        else openDropdown();
      });
    });
  },
};

// Right — width read at click time
Drupal.behaviors.menu = {
  attach(context) {
    once('menu-init', '.menu-toggle', context).forEach((el) => {
      el.addEventListener('click', () => {
        const isMobile = window.innerWidth < 992;  // ← fresh every click
        if (isMobile) openDrawer();
        else openDropdown();
      });
    });
  },
};
```
