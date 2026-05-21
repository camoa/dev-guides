---
description: When to integrate a module with the Modeler API — use cases, decision table, and free features
tldr: "Use the Modeler API when your module owns a config entity type representing a workflow, rule set, or automation and you want visual editing. ECA 3.1+ mandates it. Implementing a Model Owner gives you CRUD routes, permissions, Recipe export, and metadata for free."
drupal_version: "11.x"
---

# When to Use the Modeler API

## When to Use

> Use the Modeler API when your module owns config entities representing workflows, process rules, or automations and you want users to edit them visually. Skip it for simple content entities or modules that already have a specialized editor.

## Decision

| If your module... | Use Modeler API? | Rationale |
|-------------------|-----------------|-----------|
| Owns config entities representing workflows/rules | Yes | This is the primary use case |
| Needs to work with ECA 3.1+ | Yes (mandatory) | ECA 3.1 hard-depends on `modeler_api` |
| Wants to swap visual editors without code changes | Yes | Owner/Modeler decoupling enables this |
| Provides simple content entities | No | Overkill; use field UI |
| Already has its own specialized editor | Maybe | Could still benefit from Recipe export, permissions, and routing |

## Pattern

By implementing a Model Owner plugin with `configEntityBasePath()`, the Modeler API auto-generates:

- Full CRUD routes (collection, add, edit, delete, clone, import, export)
- Enable/disable routes (if entity type has `status` key)
- Per-modeler add/edit/view routes when multiple modelers are installed
- Dynamic permissions per owner and per owner+modeler combination
- Recipe export UI and Drush command
- Replay data UI (if owner opts in via `supportsReplayData()`)
- In-modeler testing UI (if owner opts in via `supportsTesting()`)
- Standardized model metadata: version, tags, documentation, changelog

## Common Mistakes

- **Wrong**: Registering a Model Owner without a config entity → **Right**: The API wraps existing config entity types; it does not create them. You need `@ConfigEntityType` defined first.
- **Wrong**: Assuming BPMN.iO is still the default → **Right**: As of 2025, the Workflow Modeler (`drupal/modeler`) is the recommended option. BPMN.iO is maintained but no longer the primary reference implementation.

## See Also

- [Architecture: Owners vs Modelers](architecture-owners-vs-modelers.md)
- [The Modeler Landscape](modeler-landscape.md)
- Reference: `https://ecaguide.org`, `https://www.drupal.org/project/modeler_api`
