---
description: Drupal Modeler API 1.1.x — integrate config entities with visual workflow editors, build Model Owner plugins, Modeler plugins, and manage model data storage and export
guide-meta:
  concepts:
    - Modeler API
    - modeler_api
    - Model Owner
    - ModelOwner
    - ModelOwnerBase
    - Modeler plugin
    - ModelerBase
    - Component value object
    - ComponentSuccessor
    - DataModel entity
    - modeler_api_data_model
    - Workflow Modeler
    - drupal/modeler
    - BPMN.iO
    - bpmn_io
    - visual workflow editor
    - model export
    - Recipe export
    - modeler_api:model:export
    - YAML contexts
    - YAML dependencies
    - template tokens
    - model constraints
    - configEntityBasePath
    - usedComponents
    - addComponent
    - resetComponents
  not:
    - ECA actions (see drupal/eca)
    - ECA events (see drupal/eca)
    - ECA conditions (see drupal/eca)
    - Drupal Workflows module (state machine)
    - Content Moderation
  requires:
    - drupal/plugins
    - drupal/config-management
  complements:
    - drupal/eca
    - drupal/orchestration
  specializes: ""
  category: drupal
---

# Modeler API

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand how Model Owners and Modelers relate | [Architecture: Owners vs Modelers](architecture-owners-vs-modelers.md) | Model Owners (config entity + domain plugins) and Modelers (visual canvas + data format) are decoupled PHP attribute plugins that communicate only through the Component value object via the central Api service. Never let a Modeler reference owner internals. |
| Decide when to use the Modeler API | [When to Use the Modeler API](when-to-use.md) | Use the Modeler API when your module owns a config entity type representing a workflow, rule set, or automation and you want visual editing. ECA 3.1+ mandates it. Implementing a Model Owner gives you CRUD routes, permissions, Recipe export, and metadata for free. |
| Understand the Component value object | [The Component Model](component-model.md) | Component is a transient value object (never stored) that is the universal currency between Model Owners and Modelers. Seven typed constants on Api represent canvas node types; annotations and swimlanes are handled by the API itself and must not be passed to addComponent(). |
| Register my config entity as a Model Owner | [Registering a Model Owner](registering-model-owner.md) | Implement ModelOwnerBase in src/Plugin/ModelerApiModelOwner/ with the #[ModelOwner] attribute, declare configEntityBasePath() for auto-generated routes, and implement usedComponents/resetComponents/addComponent as the save-cycle contract. Constructors are final — use lazy getter injection. |
| Build a new Modeler plugin | [Building a Modeler Plugin](building-a-modeler.md) | Build a Modeler plugin only when Workflow Modeler and BPMN.iO genuinely don't fit. Extend ModelerBase with #[Modeler] attribute, implement parseData/readComponents/getRawData/edit, and use drupalSettings.modeler_api URLs for all JS endpoints — never hardcode them. |
| Understand the DataModel entity and storage options | [DataModel Entity and Storage](data-model-entity-storage.md) | Raw model data (JSON/XML) is stored separately from the structured config entity. Default is third-party settings (portable, good for small models); use STORAGE_OPTION_SEPARATE for large models to avoid config blob limits; STORAGE_OPTION_NONE requires implementing convert() so the modeler can reconstruct from entity config. |
| Understand how routes and permissions are auto-generated | [Routes and Permissions](routes-permissions.md) | Routes and permissions are generated dynamically at container rebuild; you write no route YAML. configEntityBasePath() must return a non-NULL string for CRUD routes to be generated. Use ModelerApiPermissions::getPermissionKey() to build permission strings — never hardcode them. |
| Define YAML-based contexts, dependencies, or template tokens | [YAML Plugin Definitions](yaml-plugin-definitions.md) | Define Contexts in *.modeler_api.contexts.yml to restrict which plugins appear in the palette, Dependencies to enforce predecessor constraints, and Template Tokens for reusable model templates — all without PHP. Use string type keys (start, element, link), not Api integer constants. |
| Export a model as a Recipe or archive | [Import, Export, and Recipe Export](import-export-recipe.md) | Three distribution mechanisms exist: archive export (.tar.gz), Recipe export (full Drupal Recipe directory via ExportRecipe service or drush modeler_api:model:export), and import. Recipe export requires Drush 13+ and populates recipe.yml from the model's metadata — fill in the documentation field before exporting. |
| Choose between Workflow Modeler, BPMN.iO, and Fallback | [The Modeler Landscape](modeler-landscape.md) | Workflow Modeler (drupal/modeler, React Flow + JSON) is the recommended default for new sites; BPMN.iO (drupal/bpmn_io, BPMN XML) is the legacy alternative for BPMN-standard compliance or SVG export. The built-in Fallback modeler is read-only and always present. Both can coexist. |
| Use Drush commands for maintenance | [Drush Commands](drush-commands.md) | Four Drush commands: modeler_api:update (migrate all models after plugin ID changes), modeler_api:disable / modeler_api:enable (bulk status toggle per owner), modeler_api:model:export (generate a Drupal Recipe directory). Run update on dev first — it permanently modifies stored raw data. |
