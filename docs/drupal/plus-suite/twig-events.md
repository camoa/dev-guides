---
description: Twig Events system — TwigRenderTemplateEvent, entity wrapping with editing attributes, and creating custom template subscribers
tldr: "Use Twig Events to intercept template rendering without overriding templates. Be aware it fires on every template render — use sparingly."
drupal_version: "11.x"
---

# Twig Events

## When to Use

> Use Twig Events to intercept template rendering without overriding templates. Be aware it fires on every template render — use sparingly.

## Decision

| Use Case | Approach |
|----------|----------|
| Wrap entities with editing attributes | Subscribe to `TwigRenderTemplateEvent` (navigation_plus does this) |
| Modify template output without override | Subscribe to `TwigRenderTemplateEvent` |
| Template-specific changes | Override the template directly |

## Pattern

**Entity wrapping** — Navigation+ uses `TwigRenderTemplateEvent` via `EntityUiWrapper` to add:

```html
<div data-navigation-plus-entity-wrapper
     data-navigation-plus-view-mode="full"
     data-main-entity="true"
     class="navigation-plus-entity-wrapper layout-builder-entity-wrapper">
  <!-- Entity content -->
</div>
```

Purpose: JS targeting for inline editing, view mode tracking, main entity detection, Layout Builder drop zone integration.

**Custom template subscriber:**

```php
namespace Drupal\my_module\EventSubscriber;

use Drupal\twig_events\Event\TwigRenderTemplateEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class MyTemplateSubscriber implements EventSubscriberInterface {

  public static function getSubscribedEvents(): array {
    return [TwigRenderTemplateEvent::class => 'onTwigRenderTemplate'];
  }

  public function onTwigRenderTemplate(TwigRenderTemplateEvent $event): void {
    $template = $event->getTemplate();
    // Modify template variables or output
  }
}
```

## Common Mistakes

- **Wrong**: Using Twig Events for heavy processing → **Right**: It fires on every template render including cached renders; keep subscribers fast
- **Wrong**: Assuming template rendering order → **Right**: Events fire as templates are encountered; do not depend on order

## See Also

- [Architecture & Module Map](architecture-module-map.md)
- [Events & Event Subscribers](events-event-subscribers.md)
- Reference: `twig_events/src/Event/TwigRenderTemplateEvent.php`
