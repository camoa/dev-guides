---
description: Modeler API YAML plugins — Contexts (palette filtering), Dependencies (ordering constraints), Template Tokens (placeholder tokens)
tldr: "Define Contexts in *.modeler_api.contexts.yml to restrict which plugins appear in the palette, Dependencies to enforce predecessor constraints, and Template Tokens for reusable model templates — all without PHP. Use string type keys (start, element, link), not Api integer constants."
drupal_version: "11.x"
---

# YAML Plugin Definitions

## When to Use

> Use this when you want to filter available components by use case (Contexts), enforce ordering constraints (Dependencies), or define placeholder tokens for model templates (Template Tokens) — all without writing PHP.

## Decision

| YAML file | Plugin type | What it does |
|---|---|---|
| `*.modeler_api.contexts.yml` | Context | Restricts which plugins appear in the component palette per use case |
| `*.modeler_api.dependencies.yml` | Dependency | Defines that a plugin can only be used downstream of certain predecessors |
| `*.modeler_api.template_tokens.yml` | Template Token | Defines placeholder tokens for models marked as templates |

## Pattern

**Contexts** — restrict palette plugins per use case:

```yaml
# my_module.modeler_api.contexts.yml
my_base_context:
  topic: 'Commonly used actions'
  model_owner: my_workflow
  components:
    start:
      plugins: [event_a, event_b]
    element:
      plugins: [action_a, action_b]
    link:
      plugins: [condition_a]

my_form_context:
  topic: 'Form-related actions'
  model_owner: my_workflow
  includes: [my_base_context]           # Inherits base plugins; transitive
  components:
    start:
      plugins: [form:form_build]
```

Alter hook: `hook_modeler_api_context_info_alter(array &$definitions)`.

**Dependencies** — enforce predecessor plugin constraints (supports glob `*` wildcards):

```yaml
# my_module.modeler_api.dependencies.yml
my_constraints:
  model_owner: my_workflow
  components:
    element:
      my_form_*:                        # Matches my_form_add, my_form_edit, etc.
        - type: start
          id: form:*                    # Only valid after any form:* event
      specific_action:
        - type: start
          id: form:form_submit
    link:
      eca_form_field_value:
        - type: start
          id: form:form_build
```

Alter hook: `hook_modeler_api_dependency_info_alter(array &$definitions)`.

**Template Tokens** — placeholder tokens for template models:

```yaml
# my_module.modeler_api.template_tokens.yml
my_tokens:
  model_owner: my_workflow
  tokens:
    my-template:
      name: 'My Templates'
      token: my-template
      children:
        config:
          name: 'Configuration'
          token: 'my-template:config'
          purpose: config              # Required on first-level children
          children:
            timeout:
              name: 'Timeout'
              token: 'my-template:config:timeout'
              value: '30'
        select:
          name: 'Select elements'
          token: 'my-template:select'
          purpose: select             # CSS selector branch
          selector: 'form'
```

**Token purposes:**
- `select` — Defines a CSS selector chain; frontend highlights matching DOM elements for the user to pick
- `config` — Provides a configuration value passed through without DOM interaction

Multi-module tokens for the same owner are deep-merged. Alter hook: `hook_modeler_api_template_token_info_alter(array &$definitions)`.

## Common Mistakes

- **Wrong**: Using integer type keys in YAML (e.g., `4:`) → **Right**: YAML plugins use string names (`start`, `element`, `link`, `gateway`, etc.), not the integer constants from `Api`.
- **Wrong**: Defining Dependencies without Contexts → **Right**: Dependencies filter plugins that are not even in the palette. Define a Context first to make plugins visible, then Dependencies to constrain their use.
- **Wrong**: Omitting `purpose` on first-level template token children → **Right**: `TemplateToken::resolvePurpose()` reads `purpose` on the first child level only. Without it, the frontend cannot categorize the token.

## See Also

- [Registering a Model Owner](registering-model-owner.md)
- Reference: `src/Context.php`, `src/Dependency.php`, `src/TemplateToken.php`, `docs/guide/yaml-plugins.md`
