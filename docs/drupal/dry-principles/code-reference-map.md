---
description: Reference map of core file locations for DRY patterns - config, services, base classes, traits, plugins, render API, hooks, SDC, and recipes.
---

# Code Reference Map

## Core DRY Patterns by File Location

### Configuration System

- **ConfigFactory**: `core/lib/Drupal/Core/Config/ConfigFactory.php`
- **Config entity base**: `core/lib/Drupal/Core/Config/Entity/ConfigEntityBase.php`
- **Config schema**: `core/config/schema/core.data_types.schema.yml`
- **Example config entity**: `core/modules/node/config/install/node.type.article.yml`

### Services and Dependency Injection

- **Service container**: `core/lib/Drupal/Core/DrupalKernel.php`
- **ContainerInjectionInterface**: `core/lib/Drupal/Core/DependencyInjection/ContainerInjectionInterface.php`
- **Core services**: `core/core.services.yml`
- **Example service**: `core/modules/system/src/SystemManager.php`

### Base Classes

- **ContentEntityBase**: `core/lib/Drupal/Core/Entity/ContentEntityBase.php`
- **ConfigEntityBase**: `core/lib/Drupal/Core/Config/Entity/ConfigEntityBase.php`
- **FormBase**: `core/lib/Drupal/Core/Form/FormBase.php`
- **ConfigFormBase**: `core/lib/Drupal/Core/Form/ConfigFormBase.php`
- **BlockBase**: `core/lib/Drupal/Core/Block/BlockBase.php`
- **PluginBase**: `core/lib/Drupal/Core/Plugin/PluginBase.php`
- **ControllerBase**: `core/lib/Drupal/Core/Controller/ControllerBase.php`

### Traits

- **StringTranslationTrait**: `core/lib/Drupal/Core/StringTranslation/StringTranslationTrait.php`
- **MessengerTrait**: `core/lib/Drupal/Core/Messenger/MessengerTrait.php`
- **LoggerChannelTrait**: `core/lib/Drupal/Core/Logger/LoggerChannelTrait.php`
- **EntityChangedTrait**: `core/lib/Drupal/Core/Entity/EntityChangedTrait.php`
- **EntityPublishedTrait**: `core/lib/Drupal/Core/Entity/EntityPublishedTrait.php`
- **DependencySerializationTrait**: `core/lib/Drupal/Core/DependencyInjection/DependencySerializationTrait.php`

### Plugin System

- **BlockBase**: `core/lib/Drupal/Core/Block/BlockBase.php`
- **DeriverBase**: `core/lib/Drupal/Component/Plugin/Derivative/DeriverBase.php`
- **ContainerFactoryPluginInterface**: `core/lib/Drupal/Core/Plugin/ContainerFactoryPluginInterface.php`
- **Example plugin with DI**: `core/modules/system/src/Plugin/Block/SystemBrandingBlock.php`
- **Example deriver**: `core/modules/system/src/Plugin/Deriver/SystemMenuBlock.php`

### Render API

- **RenderElement base**: `core/lib/Drupal/Core/Render/Element/RenderElementBase.php`
- **FormElement base**: `core/lib/Drupal/Core/Render/Element/FormElementBase.php`
- **Renderer service**: `core/lib/Drupal/Core/Render/Renderer.php`
- **Theme API**: `core/lib/Drupal/Core/Render/theme.api.php`

### Templates

- **Core templates**: `core/themes/stable9/templates/`
- **Example layout templates**: `core/themes/stable9/templates/layout/`
- **Module templates**: `core/modules/system/templates/`

### Hooks and Events

- **Hook attribute**: `core/lib/Drupal/Core/Hook/Attribute/Hook.php`
- **Example hook class**: `core/modules/system/src/Hook/SystemHooks.php`
- **EventSubscriberInterface**: `core/lib/Symfony/Component/EventDispatcher/EventSubscriberInterface.php`

### Single Directory Components

- **SDC module**: `core/modules/sdc/`
- **Component schema**: `core/modules/sdc/src/component.schema.json`
- **Radix components**: `themes/contrib/radix/components/`

### Recipes

- **Core recipes**: `core/recipes/`
- **Recipe documentation**: https://www.drupal.org/docs/extending-drupal/drupal-recipes

## Contrib Modules for DRY Patterns

- **Config Split**: `modules/contrib/config_split/` -- Environment-specific config
- **Features**: `modules/contrib/features/` -- Config packaging (legacy approach, recipes preferred)
- **Devel**: `modules/contrib/devel/` -- Development-only module (use Config Split to enable only in dev)

## Additional Reference Sources

- **Drupal at your Fingertips**: https://www.drupalatyourfingertips.com/ -- Comprehensive Drupal development patterns
- **API Documentation**: https://api.drupal.org/api/drupal/11.x
- **Change Records**: https://www.drupal.org/list-changes/drupal -- Track API changes and best practices

## See Also

- [Best Practices Decision Framework](best-practices-decision-framework.md)
- Universal DRY principles: `dev-dry-principles.md`
- Drupal Form API: `drupal-form-api.md`
- Drupal SDC guide: `design-system-radix-sdc-mapping.md`
