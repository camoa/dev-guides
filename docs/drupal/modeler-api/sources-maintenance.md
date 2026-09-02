---
description: "Source references and maintenance manifest for the modeler api guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install

Path: (not yet set — ask user on first use of code sources)

## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Modeler API project page | https://www.drupal.org/project/modeler_api | All | 2026-05-20 |
| ECA Guide (ecaguide.org) | https://ecaguide.org | When to Use, Architecture | 2026-05-20 |
| Workflow Modeler project | https://www.drupal.org/project/modeler | The Modeler Landscape | 2026-05-20 |
| BPMN.iO project | https://www.drupal.org/project/bpmn_io | The Modeler Landscape | 2026-05-20 |
| AI Agents project (ModelOwner example) | https://www.drupal.org/project/ai_agents | Registering a Model Owner | 2026-05-20 |

## Code Sources

Research install path: `dev-guides/eca-src-research/`
(Commit reference: `modeler_api` 1.1.x at `63ec949`)

| Module | Relative path (from research dir) | Guide Sections | Version |
|--------|----------------------------------|----------------|---------|
| modeler_api — core API | `modeler_api/src/Api.php` | Architecture, Component Model, Routes | 1.1.2 |
| modeler_api — ModelOwner attribute | `modeler_api/src/Attribute/ModelOwner.php` | Registering a Model Owner | 1.1.2 |
| modeler_api — Modeler attribute | `modeler_api/src/Attribute/Modeler.php` | Building a Modeler Plugin | 1.1.2 |
| modeler_api — ModelOwnerInterface | `modeler_api/src/Plugin/ModelerApiModelOwner/ModelOwnerInterface.php` | Registering a Model Owner, Routes | 1.1.2 |
| modeler_api — ModelOwnerBase | `modeler_api/src/Plugin/ModelerApiModelOwner/ModelOwnerBase.php` | Registering a Model Owner, Storage | 1.1.2 |
| modeler_api — ModelerInterface | `modeler_api/src/Plugin/ModelerApiModeler/ModelerInterface.php` | Building a Modeler Plugin | 1.1.2 |
| modeler_api — ModelerBase | `modeler_api/src/Plugin/ModelerApiModeler/ModelerBase.php` | Building a Modeler Plugin | 1.1.2 |
| modeler_api — Component | `modeler_api/src/Component.php` | The Component Model | 1.1.2 |
| modeler_api — ComponentSuccessor | `modeler_api/src/ComponentSuccessor.php` | The Component Model | 1.1.2 |
| modeler_api — DataModel entity | `modeler_api/src/Entity/DataModel.php` | DataModel Entity and Storage | 1.1.2 |
| modeler_api — Routes | `modeler_api/src/Routing/Routes.php` | Routes and Permissions | 1.1.2 |
| modeler_api — Permissions | `modeler_api/src/ModelerApiPermissions.php` | Routes and Permissions | 1.1.2 |
| modeler_api — ExportRecipe | `modeler_api/src/ExportRecipe.php` | Import, Export, and Recipe Export | 1.1.2 |
| modeler_api — Settings form | `modeler_api/src/Form/Settings.php` | DataModel Entity and Storage | 1.1.2 |
| modeler_api — Context value object | `modeler_api/src/Context.php` | YAML Plugin Definitions | 1.1.2 |
| modeler_api — Dependency value object | `modeler_api/src/Dependency.php` | YAML Plugin Definitions | 1.1.2 |
| modeler_api — TemplateToken value object | `modeler_api/src/TemplateToken.php` | YAML Plugin Definitions | 1.1.2 |
| modeler_api — Drush commands | `modeler_api/src/Drush/Commands/ModelerApiCommands.php` | Drush Commands | 1.1.2 |
| modeler_api — architecture docs | `modeler_api/docs/architecture/index.md` | Architecture | 1.1.2 |
| modeler_api — guide: creating owner | `modeler_api/docs/guide/creating-model-owner.md` | Registering a Model Owner | 1.1.2 |
| modeler_api — guide: creating modeler | `modeler_api/docs/guide/creating-modeler.md` | Building a Modeler Plugin | 1.1.2 |
| modeler_api — guide: YAML plugins | `modeler_api/docs/guide/yaml-plugins.md` | YAML Plugin Definitions | 1.1.2 |
| Workflow Modeler plugin | `modeler/src/Plugin/ModelerApiModeler/WorkflowModeler.php` | Building a Modeler Plugin, The Modeler Landscape | 1.x |
| ECA ModelOwner plugin | `eca/modules/ui/src/Plugin/ModelerApiModelOwner/Eca.php` | Registering a Model Owner | 3.1.x |
<!-- END PARTITION: sources-maintenance -->
