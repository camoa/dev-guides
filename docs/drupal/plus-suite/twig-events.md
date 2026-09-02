---
description: Twig Events system — TwigRenderTemplateEvent, entity wrapping with editing attributes, and creating custom template subscribers
tldr: "Subscribe to TwigRenderTemplateEvent to intercept and modify template output during Twig rendering without overriding templates; it fires on every template render so keep subscribers fast."
drupal_version: "11.x"
---

# Twig Events

## When to Use

> When you need to understand how Plus Suite wraps entities for editing during template rendering, or when you need to intercept template rendering.

## How Twig Events Works

The `twig_events` module provides a single event: `TwigRenderTemplateEvent`, dispatched during Twig template rendering. This allows modules to intercept and modify template output without overriding templates.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Need to intercept or modify template output without overriding the template | Subscribe to `TwigRenderTemplateEvent` | The event is dispatched during Twig template rendering, so modules can act without template overrides |

## Pattern: Entity Wrapping

Navigation+ uses `TwigRenderTemplateEvent` via the `EntityUiWrapper` event subscriber to wrap entities with editing attributes:

```html
<!-- Wrapper added by EntityUiWrapper -->
<div data-navigation-plus-entity-wrapper
     data-navigation-plus-view-mode="full"
     data-main-entity="true"
     class="navigation-plus-entity-wrapper layout-builder-entity-wrapper">
  <!-- Entity content -->
</div>
```

## Purpose of Wrapping

1. **JS targeting**: JavaScript can find the entity container for inline editing
2. **View mode tracking**: `data-navigation-plus-view-mode` tells Edit+ which view mode to load forms for
3. **Main entity detection**: `data-main-entity` distinguishes the primary entity from embedded ones
4. **Layout Builder integration**: `layout-builder-entity-wrapper` class used by LB+ for drop zones

## Pattern: Creating Custom Template Subscribers

```php
namespace Drupal\my_module\EventSubscriber;

use Drupal\twig_events\Event\TwigRenderTemplateEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class MyTemplateSubscriber implements EventSubscriberInterface {

  public static function getSubscribedEvents(): array {
    return [TwigRenderTemplateEvent::class => 'onTwigRenderTemplate'];
  }

  public function onTwigRenderTemplate(TwigRenderTemplateEvent $event): void {
    $template_file = $event->getTemplateFile();
    // Read or replace with setTemplateFile(), getVariables()/setVariables(),
    // getOutput()/setOutput()
  }
}
```

## Common Mistakes

- **Do not use Twig Events for heavy processing** — it fires on every template render.
- **Do not assume template rendering order** — events fire as templates are encountered.

## See Also

- [Architecture & Module Map](architecture-module-map.md)
- [Events & Event Subscribers](events-event-subscribers.md)
- Reference: `twig_events/src/Event/TwigRenderTemplateEvent.php`
