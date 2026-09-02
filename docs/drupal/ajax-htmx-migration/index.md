---
description: AJAX to HTMX Migration — pattern-by-pattern guide for replacing Drupal AJAX API with core HTMX in Drupal 11.3+
tracks:
  - project: drupal
    channel: stable
    verified: 2026-06-07
guide-meta:
  concepts:
    - AJAX to HTMX migration
    - AJAX command equivalents
    - dependent dropdown migration
    - multi-step wizard migration
    - hybrid AJAX-HTMX
  not:
    - HTMX from scratch
    - AJAX framework reference
  requires:
    - drupal/ajax
    - drupal/htmx
  complements:
    - drupal/forms
    - drupal/js-development
  category: drupal
---

# AJAX to HTMX Migration

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand architectural differences before migrating | [AJAX vs HTMX Fundamentals](ajax-vs-htmx-fundamentals.md) | Read this before starting a migration to understand the architectural differences between #ajax callbacks and the declarative Htmx class. Never mix #ajax and Htmx attributes on the same element — they conflict and HTMX is ignored. |
| Find the HTMX equivalent of a specific AJAX command | [AJAX Command to HTMX Equivalents](ajax-command-to-htmx-equivalents.md) | Use this table to find the HTMX equivalent of a specific AJAX command before rewriting it. Multiple simultaneous updates use swapOob() — HTMX has no direct equivalent of stacking multiple AjaxResponse commands. |
| Migrate a parent select that updates child select options | [Dependent Dropdown Migration](dependent-dropdown-migration.md) | Migrate a parent select that updates a child select's options on change. Delete the AJAX callback method entirely — HTMX rebuilds the form in buildForm() and getHtmxTriggerName() replaces isRebuilding(). |
| Migrate multiple dependent selects with bookmarkable URL | [Cascading Selects with URL Migration](cascading-selects-with-url-migration.md) | Migrate chained dropdowns where each selection updates the next AND the URL. Use swapOob() to clear downstream fields and pushUrlHeader() to keep the URL in sync — without pushUrlHeader() the state isn't bookmarkable. |
| Migrate a button that loads content into a container | [Button-Triggered Content Load Migration](button-triggered-content-load-migration.md) | Migrate a Load More/Refresh button that loads content into a container. Controllers return render arrays, not AjaxResponse — and select() extracts from the response while target() says where on the page it lands. |
| Migrate a multi-step wizard with browser back/forward | [Multi-Step Wizard Migration](multi-step-wizard-migration.md) | Migrate a multi-step wizard so each step is a distinct URL instead of form-state. Store the step as a route parameter, not $form_state->get('step') — that is what makes pushUrl() and the browser back button work. |
| Migrate field validation on blur without form submission | [Real-Time Validation Migration](real-time-validation-migration.md) | Migrate on-blur field validation (email availability, format checks). HTMX has no ->throttle() method — throttling and debouncing are trigger modifiers: trigger('focusout throttle:1s') or trigger('focusout delay:500ms'). |
| Migrate Load More or infinite scroll patterns | [Infinite Scroll Migration](infinite-scroll-migration.md) | Migrate Load More / infinite-scroll patterns. Button-triggered loading uses swap('beforeend') on click; scroll-triggered loading adds a sentinel element with trigger('revealed') that fires when it enters the viewport. |
| Migrate Add Another / dynamic field addition | [Dynamic Field Addition Migration](dynamic-field-addition-migration.md) | Migrate Add Another patterns for repeating fields. HTMX submissions don't preserve form state like AJAX callbacks — track the count in a hidden field and send the incremented value with vals(). |
| Migrate custom JavaScript AJAX event hooks | [JavaScript Event Migration](javascript-event-migration.md) | Migrate custom JS that hooks preprocessing, validation, or post-processing into AJAX events. HTMX has no Drupal.ajax object — replace jQuery hook overrides with htmx.on('htmx:beforeRequest'/'htmx:afterSwap', ...). |
| Migrate custom AJAX commands (CommandInterface) | [Custom AJAX Command Migration](custom-ajax-command-migration.md) | Migrate custom AJAX commands that perform specialized JS operations. Delete the CommandInterface class — use Htmx::triggerHeader() instead, where the PHP array key becomes the JS event name that htmx.on() listens for. |
| Migrate Drupal behaviors for HTMX swaps | [Drupal Behavior Migration](drupal-behavior-migration.md) | Behaviors work identically with HTMX — htmx:drupal:load and htmx:drupal:unload trigger attachBehaviors()/detachBehaviors() automatically. The only real change is swapping jQuery's .once() for the modern once() API. |
| Migrate screen reader announcements and focus management | [Accessibility Migration](accessibility-migration.md) | Migrate AnnounceCommand/FocusFirstCommand accessibility patterns. HTMX has no built-in focus or announce commands — add aria-live/aria-atomic to containers and use a triggerHeader() + htmx.on('announce') to call Drupal.announce(). |
| Decide which AJAX patterns NOT to migrate | [When NOT to Migrate](when-not-to-migrate.md) | Keep AJAX for ordered command sequences, CSS manipulation, jQuery UI dialogs with complex options, and contrib callbacks. Simple modals can still migrate to HTMX via a native <dialog> plus ->on('::afterSwap', 'showModal()'). |
| Use AJAX and HTMX together in the same application | [Hybrid AJAX-HTMX Approach](hybrid-ajax-htmx-approach.md) | Use AJAX for specific features (dialogs, contrib) and HTMX for new form interactions in the same app. Drupal.attachBehaviors() runs after both AJAX and HTMX swaps, and Drupal.behaviors.htmx initializes HTMX attributes on AJAX-inserted content. |
| Plan a safe migration rollout | [Migration Strategy Best Practices](migration-strategy-best-practices.md) | Plan the migration before starting: prioritize new features and simple dependent dropdowns first, migrate one pattern per release, and always test browser history plus screen readers since HTMX changes both. |
| Get a step-by-step migration verification checklist | [Migration Checklist](migration-checklist.md) | Use this checklist for every individual AJAX to HTMX migration to ensure nothing is missed, covering pre-migration review, code changes, testing, and post-migration cleanup. |
