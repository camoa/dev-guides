---
description: Modeler API architecture — Model Owners vs Modelers, plugin discovery, and the save cycle
tldr: "Model Owners (config entity + domain plugins) and Modelers (visual canvas + data format) are decoupled PHP attribute plugins that communicate only through the Component value object via the central Api service. Never let a Modeler reference owner internals."
drupal_version: "11.x"
---

# Architecture: Owners vs Modelers

## When to Use

> Read this first. Understanding the separation between Model Owners and Modelers is the prerequisite for every other section in this guide.

## Decision

| Role | PHP Plugin Type | What it owns | Examples |
|------|----------------|--------------|---------|
| **Model Owner** | `#[ModelOwner]` | A Drupal config entity type and its domain-specific plugins (events, actions, conditions) | ECA (`eca_ui`), AI Agents, Migrations |
| **Modeler** | `#[Modeler]` | The visual editing canvas, raw data format (JSON/XML), and UI rendering | Workflow Modeler (React Flow/JSON), BPMN.iO (BPMN XML), Fallback |

Neither side knows about the other. All communication flows through the central `Api` service (`modeler_api.service`) using the generic `Component` value object.

## Pattern

**The Save Cycle** — when the user clicks Save in the modeler UI:

```
POST /admin/modeler_api/{type}/{modeler_id}/save
  → Api::prepareModelFromData()
    → ModelerInterface::parseData()       # modeler parses raw data
    → extract metadata (ID, label, version, status, tags, storage…)
    → ModelOwnerInterface::resetComponents()   # owner clears entity storage
    → for each Component from ModelerInterface::readComponents():
        ModelOwnerInterface::addComponent()    # owner maps to domain config
        Component::validate()                  # PluginFormInterface validation
    → Api::validateModelConstraints()          # cardinality rules
    → ModelOwnerInterface::finalizeAddingComponents()
    → config entity saved; raw data stored per storage method
```

**Plugin Discovery:**

| Plugin type | Service ID | Mechanism | File location |
|-------------|-----------|-----------|--------------|
| Model Owner | `plugin.manager.modeler_api.model_owner` | PHP `#[ModelOwner]` attribute | `src/Plugin/ModelerApiModelOwner/` |
| Modeler | `plugin.manager.modeler_api.modeler` | PHP `#[Modeler]` attribute | `src/Plugin/ModelerApiModeler/` |
| Context | `plugin.manager.modeler_api.context` | YAML `*.modeler_api.contexts.yml` | module root |
| Dependency | `plugin.manager.modeler_api.dependency` | YAML `*.modeler_api.dependencies.yml` | module root |
| Template Token | `plugin.manager.modeler_api.template_token` | YAML `*.modeler_api.template_tokens.yml` | module root |

## Common Mistakes

- **Wrong**: Overriding `__construct()` or `create()` in plugin implementations → **Right**: Both `ModelOwnerBase` and `ModelerBase` declare these as `final`. Use lazy getter injection instead.
- **Wrong**: Calling `owner->configEntityTypeId()` from inside a Modeler → **Right**: Modelers must not reference owner internals; use only the `ModelOwnerInterface` API.
- **Wrong**: Assuming the Fallback modeler provides editing → **Right**: `Api::getModeler()` returns `NULL` (not the Fallback) when zero or more than one real modeler is installed.

## See Also

- [Registering a Model Owner](registering-model-owner.md)
- [Building a Modeler Plugin](building-a-modeler.md)
- Reference: `src/Api.php`, `src/Plugin/ModelerApiModelOwner/ModelOwnerInterface.php`, `src/Plugin/ModelerApiModeler/ModelerInterface.php`
