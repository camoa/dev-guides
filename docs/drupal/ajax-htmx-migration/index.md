---
description: AJAX to HTMX Migration — pattern-by-pattern guide for replacing Drupal AJAX API with core HTMX in Drupal 11.3+
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
  specializes: ""
  category: drupal
---

# AJAX to HTMX Migration

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand architectural differences before migrating | [AJAX vs HTMX Fundamentals](ajax-vs-htmx-fundamentals.md) | Use AJAX when you need command sequences, modal dialogs, or contrib integration. Use HTMX when you want declarative form interactions, CSS selector targeting, or built-in browser history support. |
| Find the HTMX equivalent of a specific AJAX command | [AJAX Command to HTMX Equivalents](ajax-command-to-htmx-equivalents.md) | Use this reference when converting existing AJAX commands to HTMX patterns. Find the HTMX equivalent of a specific AJAX command before rewriting. |
| Migrate a parent select that updates child select options | [Dependent Dropdown Migration](dependent-dropdown-migration.md) | Use this when migrating a parent select element that dynamically updates a child select element's options based on the parent's value. |
| Migrate multiple dependent selects with bookmarkable URL | [Cascading Selects with URL Migration](cascading-selects-with-url-migration.md) | Use this when migrating multiple dependent selects where each selection updates the next dropdown AND the browser URL (bookmarkable state). |
| Migrate a button that loads content into a container | [Button-Triggered Content Load Migration](button-triggered-content-load-migration.md) | Use this when migrating a button or link that loads dynamic content into a container on click — "Load More", "Refresh", or content panel patterns. |
| Migrate a multi-step wizard with browser back/forward | [Multi-Step Wizard Migration](multi-step-wizard-migration.md) | Use this when migrating multi-step wizard forms where each step is driven by AJAX navigation. HTMX enables bookmarkable steps with browser back/forward button support. |
| Migrate field validation on blur without form submission | [Real-Time Validation Migration](real-time-validation-migration.md) | Use this when migrating field-level validation that runs on blur (focusout) without submitting the form — email availability checks, username validation, format verification. |
| Migrate Load More or infinite scroll patterns | [Infinite Scroll Migration](infinite-scroll-migration.md) | Use this when migrating "Load More" buttons or infinite scroll patterns that append new content to a list — content listings, search results, and feeds. |
| Migrate Add Another / dynamic field addition | [Dynamic Field Addition Migration](dynamic-field-addition-migration.md) | Use this when migrating "Add Another" patterns where clicking a button adds a new form field to the form — multi-value fields and repeating field groups. |
| Migrate custom JavaScript AJAX event hooks | [JavaScript Event Migration](javascript-event-migration.md) | Use this when migrating custom JavaScript that hooks into AJAX events for preprocessing, validation, or post-processing. |
| Migrate custom AJAX commands (CommandInterface) | [Custom AJAX Command Migration](custom-ajax-command-migration.md) | Use this when migrating custom AJAX commands (`CommandInterface` classes) that perform specialized JavaScript operations. HTMX handles these via trigger headers. |
| Migrate Drupal behaviors for HTMX swaps | [Drupal Behavior Migration](drupal-behavior-migration.md) | Use this when migrating Drupal behaviors that attach/detach on AJAX swaps. Behaviors work identically with HTMX — the `htmx:drupal:load` and `htmx:drupal:unload` events trigger `Drupal.attachBehaviors()` and `Drupal.detachBehaviors()`… |
| Migrate screen reader announcements and focus management | [Accessibility Migration](accessibility-migration.md) | Use this when migrating `AnnounceCommand`, `FocusFirstCommand`, and screen reader patterns from AJAX to HTMX. HTMX handles messages automatically but custom announcements need trigger headers. |
| Decide which AJAX patterns NOT to migrate | [When NOT to Migrate](when-not-to-migrate.md) | Use AJAX when you need ordered command sequences, the core dialog system, CSS manipulation, jQuery data API, or when contrib modules expect AJAX callbacks. |
| Use AJAX and HTMX together in the same application | [Hybrid AJAX-HTMX Approach](hybrid-ajax-htmx-approach.md) | Use both AJAX and HTMX in the same application when you need AJAX for specific features (dialogs, contrib) but want HTMX for new form interactions. They coexist without conflict. |
| Plan a safe migration rollout | [Migration Strategy Best Practices](migration-strategy-best-practices.md) | Use this before starting any AJAX to HTMX migration. Plan priorities, rollout phases, and testing to minimize risk. |
| Get a step-by-step migration verification checklist | [Migration Checklist](migration-checklist.md) | Use this checklist for every individual AJAX to HTMX migration to ensure nothing is missed. |
