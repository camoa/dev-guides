---
description: "Drupal Behavior Migration — migrate Drupal behaviors that attach/detach on AJAX swaps to HTMX swaps"
tldr: "Behaviors work identically with HTMX — htmx:drupal:load and htmx:drupal:unload trigger attachBehaviors()/detachBehaviors() automatically. The only real change is swapping jQuery's .once() for the modern once() API."
drupal_version: "11.x"
---

# Drupal Behavior Migration

## When to Use

> Migrate Drupal behaviors that attach/detach on AJAX swaps. Good news: behaviors work identically with HTMX. The `htmx:drupal:load` and `htmx:drupal:unload` events trigger `Drupal.attachBehaviors()` and `Drupal.detachBehaviors()` automatically.

## Pattern

**BEFORE: AJAX Behavior**
```javascript
(function ($, Drupal, once) {
  Drupal.behaviors.myContent = {
    attach: function (context, settings) {
      // Use jQuery.once to prevent reattachment
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

**AFTER: HTMX Behavior (Minimal Changes)**
```javascript
(function (Drupal, once) {
  Drupal.behaviors.myContent = {
    attach: function (context, settings) {
      // 'context' will be the HTMX-swapped element
      // Use once API (modern, no jQuery)
      once('my-content', '.ajax-content', context).forEach(function(el) {
        el.myPlugin = new MyPlugin(el);
      });
    },
    detach: function (context, settings, trigger) {
      // 'trigger' will be 'unload' for HTMX removals
      if (trigger === 'unload') {
        once.remove('my-content', '.ajax-content', context).forEach(function(el) {
          if (el.myPlugin) el.myPlugin.destroy();
        });
      }
    }
  };
})(Drupal, once);
```

Reference: `/core/misc/htmx/htmx-behaviors.js`

## Common Mistakes

- **Thinking behaviors need changes** → They don't! Behaviors work the same with HTMX. The `context` parameter is the swapped element
- **Not using once API** → Modern Drupal uses `once()` function, not jQuery `.once()`. Update to the new API
- **Expecting different trigger values** → HTMX uses same `trigger` values as AJAX: `'unload'` when content removed, `'serialize'` before submit, etc.
- **Removing jQuery too aggressively** → If your behavior uses jQuery internally, that's fine. Just the once API should be native
- **Not testing detach** → HTMX's `htmx:drupal:unload` fires before swap. Test that your cleanup actually runs

## See Also

- Previous: [Custom AJAX Command Migration](custom-ajax-command-migration.md)
- Next: [Accessibility Migration](accessibility-migration.md)
- Reference: [Drupal once API](https://www.drupal.org/node/3158256)
