---
description: Drupal Form API decision guides - choose the right pattern, element, and approach
tracks:
  - project: drupal
    channel: stable
    verified: 2026-02-12
guide-meta:
  concepts:
    - Form API
    - FormBase
    - ConfigFormBase
    - ConfirmFormBase
    - form elements
    - form validation
    - form submission
    - multi-step forms
    - form alter
    - "#states"
    - FormState
  not:
    - admin list builders (see drupal/config-forms)
    - AJAX form callbacks (see drupal/ajax)
  requires: []
  complements:
    - drupal/ajax
    - drupal/config-forms
    - drupal/render-api
    - drupal/services
  category: drupal
---

# Drupal Form API

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand Form API basics | [Overview](overview.md) | Use Form API when you need user input with validation and CSRF protection. Use render arrays for display-only content. |
| Choose the right base class | [Architecture: Core Classes](architecture-core-classes.md) | Choose the appropriate base class based on your form's purpose. Use FormBase for general forms, ConfigFormBase for settings, ConfirmFormBase for confirmations. |
| Understand form lifecycle and caching | [Architecture: Lifecycle](architecture-lifecycle.md) | Understand the lifecycle to know when to cache forms (multi-step, AJAX) and where to place logic (buildForm vs submitForm). |
| Build a standard form with business logic | [Pattern: FormBase](pattern-standard-form.md) | Use FormBase for general-purpose forms with custom business logic. Use ConfigFormBase for settings, EntityForm for entities, ConfirmFormBase for confirmations. |
| Build an admin settings form | [Pattern: ConfigFormBase](pattern-config-form.md) | Use ConfigFormBase for admin settings and system configuration. Use FormBase for non-configuration data or temporary workflow data. |
| Build a delete/confirm dialog | [Pattern: ConfirmFormBase](pattern-confirm-form.md) | Use ConfirmFormBase for delete operations and irreversible actions. Use FormBase for forms with additional input fields. |
| Choose the right form elements | [Elements: Overview](elements-overview.md) | Choose element types based on data type and UI needs. All elements are plugins discovered from Element/ directory. |
| Use text, number, date inputs | [Elements: Input](elements-input.md) | Choose specific input types for HTML5 validation and mobile keyboard hints. Use textfield for generic text, email for emails, number for numeric input. |
| Use select, radio, checkbox, file uploads | [Elements: Selection](elements-selection.md) | Choose selection elements based on number of options and whether multiple selections are allowed. Use entity_autocomplete for >50 options. |
| Group elements and add buttons | [Elements: Grouping](elements-grouping.md) | Use grouping elements to organize form structure and improve UX. Choose containers for AJAX wrappers, fieldsets for visual grouping, details for collapsible sections. |
| Understand element callbacks | [Elements: Lifecycle](elements-lifecycle.md) | Use #process for adding child elements, #after_build for accessing complete tree, #pre_render for final display modifications. |
| Validate form input | [Validation Architecture](validation-architecture.md) | Use element-level validation for single-field checks, form-level for cross-field validation, typed config for automatic schema validation. |
| Validate only specific fields (multi-step) | [Validation: Partial](validation-partial.md) | Use partial validation for multi-step forms with "Previous" buttons, "Save draft" vs "Publish" buttons, or progressive disclosure forms. |
| Handle form submission and redirects | [Submission Architecture](submission-architecture.md) | Understand submission handler priority to control execution order. Always redirect after successful submit to prevent form resubmission. |
| Add AJAX to forms | [AJAX Architecture](ajax-architecture.md) | Use AJAX when you need server-side logic or dynamic options. Use #states for simple show/hide (faster, client-side only). |
| Secure AJAX and use advanced patterns | [AJAX: Security](ajax-security.md) | Always use render arrays in AJAX callbacks (auto-escaped). Use AJAX commands for multiple element updates. |
| Use FormState methods | [Form State Methods](form-state-methods.md) | Use getValue() for submitted values (sanitized), set()/get() for persistent storage across rebuilds, setTemporaryValue() for single-request data. |
| Build multi-step forms | [Multi-Step Forms](multi-step-forms.md) | Use multi-step forms for complex workflows requiring user input across multiple pages. Always enable caching with setCached(TRUE). |
| Alter existing forms | [Form Alter System](form-alter-system.md) | Use specific form alter hooks (hook_form_FORM_ID_alter) for performance. Use generic hook_form_alter only when altering multiple forms. |
| Use #states for conditional fields | [Form States System](form-states-system.md) | Use #states for client-side show/hide and enable/disable. Use AJAX when server-side logic or dynamic options needed. |
| Submit forms programmatically | [Programmatic Submission](programmatic-submission.md) | Use programmatic submission for batch operations, migrations, automated testing, and cron jobs. Never for user-submitted forms. |
| Optimize form performance | [Performance Optimization](performance-optimization.md) | Optimize forms when buildForm() takes >200ms, AJAX callbacks >300ms, or you have >50 options. Target: <1s load, <2s submit. |
| Follow development standards | [Development Standards](development-standards.md) | Development standards and anti-patterns - opinionated best practices and critical mistakes to avoid |
| Secure forms against attacks | [Security Best Practices](security-best-practices.md) | Security best practices - CSRF, XSS, SQL injection, and file upload security |
| Make quick decisions | [Decision Trees](decision-trees.md) | Decision trees and quick reference matrices for form development |
| Find documentation and examples | [API References](api-references.md) | API references, core files, documentation links, and community resources |
