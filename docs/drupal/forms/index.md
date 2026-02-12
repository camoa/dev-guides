---
description: Forms — choosing the right form base, validation, AJAX
---

# Forms

| I need to... | Guide |
|-------------|-------|
| Create a module settings form | [ConfigFormBase](config-form-base.md) |
| Build a custom input form | [FormBase](form-base.md) |
| Add a confirmation step before an action | [ConfirmFormBase](confirm-form-base.md) |
| Validate form input | [Validation](validation.md) |
| Add dynamic form behavior without page reload | [AJAX](ajax.md) |

## Quick Decision

| Situation | Use |
|-----------|-----|
| Storing module settings in config | ConfigFormBase |
| Processing user input (not config) | FormBase |
| "Are you sure?" before destructive action | ConfirmFormBase |
| Any form that needs dynamic updates | Add AJAX to any of the above |
