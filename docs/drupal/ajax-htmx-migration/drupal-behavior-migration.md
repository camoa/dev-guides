---
description: Migrate Drupal behaviors for HTMX swaps — behaviors work identically, update from jQuery.once to the once() API
drupal_version: "11.x"
---

# Drupal Behavior Migration

## When to Use

> Use this when migrating Drupal behaviors that attach/detach on AJAX swaps. Behaviors work identically with HTMX — the `htmx:drupal:load` and `htmx:drupal:unload` events trigger `Drupal.attachBehaviors()` and `Drupal.detachBehaviors()` automatically.

## Decision

| What changes | What stays the same |
|---|---|
| `jQuery.once()` → `once()` API | `attach` / `detach` structure |
| `$('.class', context)` → `once('id', '.class', context)` | `trigger === 'unload'` check |
| jQuery wrapping | `context` parameter as swapped element |

## Pattern

**BEFORE:**
```javascript
(function ($, Drupal, once) {
  Drupal.behaviors.myContent = {
    attach: function (context, settings) {
      $('.ajax-content', context).once('my-content').each(function() {
        $(this).data('plugin', new MyPlugin(this));
      });
    },
    detach: function (context, settings, trigger) {
      if (trigger === 'unload') {
        $('.ajax-content', context).each(function() {
          var plugin = $(this).data('plugin');
          if (plugin) plugin.destroy();
        });
      }
    }
  };
})(jQuery, Drupal, once);
```

**AFTER:**
```javascript
(function (Drupal, once) {
  Drupal.behaviors.myContent = {
    attach: function (context, settings) {
      // context is the HTMX-swapped element
      once('my-content', '.ajax-content', context).forEach(function(el) {
        el.myPlugin = new MyPlugin(el);
      });
    },
    detach: function (context, settings, trigger) {
      if (trigger === 'unload') {
        once.remove('my-content', '.ajax-content', context).forEach(function(el) {
          if (el.myPlugin) el.myPlugin.destroy();
        });
      }
    }
  };
})(Drupal, once);
```

## Common Mistakes

- **Thinking behaviors need changes** → They do not. Behaviors work the same with HTMX. The `context` parameter is the swapped element
- **Not using `once()` API** → Modern Drupal uses the `once()` function, not jQuery `.once()`. Update to the new API
- **Expecting different trigger values** → HTMX uses the same `trigger` values: `'unload'` when content is removed, `'serialize'` before submit
- **Removing jQuery too aggressively** → If your behavior uses jQuery internally, that is fine. Only the `once` API must be native
- **Not testing detach** → `htmx:drupal:unload` fires before swap. Verify your cleanup actually runs

## See Also

- Previous: [Custom AJAX Command Migration](custom-ajax-command-migration.md)
- Next: [Accessibility Migration](accessibility-migration.md)
- Reference: [Drupal once API](https://www.drupal.org/node/3158256)
- Source: `/core/misc/htmx/htmx-behaviors.js`
