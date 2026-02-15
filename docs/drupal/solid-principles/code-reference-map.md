---
description: Core code examples demonstrating each SOLID principle in Drupal
drupal_version: "11.x"
---

# Code Reference Map

## When to Use

Need to find core code examples demonstrating each SOLID principle.

## Core Examples by Principle

**Single Responsibility Principle**

- `/core/modules/node/src/NodeGrantDatabaseStorage.php` -- Focused on access grants only
- `/core/modules/node/src/Hook/NodeEntityHooks.php` -- Entity hooks separated from form hooks
- `/core/modules/node/src/Hook/NodeFormHooks.php` -- Form hooks separated from entity hooks
- `/core/lib/Drupal/Core/Form/FormBase.php` -- Form structure only, delegates to services

**Open/Closed Principle**

- `/core/lib/Drupal/Core/Plugin/PluginBase.php` -- Plugin system foundation, open for extension
- `/core/lib/Drupal/Core/Block/BlockBase.php` -- Block plugins extend without modifying core
- `/core/modules/node/src/Hook/NodeEntityHooks.php` -- Using hooks to extend behavior
- `/core/lib/Drupal/Core/Routing/RouteSubscriberBase.php` -- Event subscriber pattern

**Liskov Substitution Principle**

- `/core/lib/Drupal/Core/Entity/ContentEntityBase.php` -- Base contract all content entities honor
- `/core/modules/node/src/Entity/Node.php` -- Extends ContentEntityBase, honors contract
- `/core/lib/Drupal/Core/Form/ConfigFormBase.php` -- Extends FormBase, adds config behavior
- `/core/lib/Drupal/Core/Access/AccessResult.php` -- Immutable value objects, substitutable

**Interface Segregation Principle**

- `/core/lib/Drupal/Core/Entity/EntityInterface.php` -- Minimal base interface
- `/core/lib/Drupal/Core/Entity/EntityOwnerInterface.php` -- Focused on ownership only
- `/core/lib/Drupal/Core/Entity/EntityPublishedInterface.php` -- Focused on published status only
- `/core/lib/Drupal/Core/DependencyInjection/ContainerInjectionInterface.php` -- Single method interface
- `/core/lib/Drupal/user/EntityOwnerTrait.php` -- Trait implementing focused interface

**Dependency Inversion Principle**

- `/core/core.services.yml` -- Service definitions, interface-based dependencies
- `/core/modules/node/node.services.yml` -- Autowiring, service aliases
- `/core/lib/Drupal/Core/Form/FormBase.php` -- ContainerInjectionInterface for DI
- `/core/lib/Drupal/Core/DependencyInjection/AutowireTrait.php` -- Automatic dependency resolution

**Additional Architecture Examples**

- `/core/lib/Drupal/Core/Entity/EntityStorageInterface.php` -- Interface for entity storage
- `/core/lib/Drupal/Core/Config/ConfigFactoryInterface.php` -- Interface for config access
- `/core/lib/Drupal/Core/Database/Connection.php` -- Database abstraction
- `/core/lib/Drupal/Core/Plugin/DefaultPluginManager.php` -- Plugin discovery and instantiation

## See Also

- Reference: All files in `/core/lib/Drupal/Core/`
- Reference: Entity examples in `/core/modules/node/src/Entity/`
- Reference: Plugin examples in `/core/lib/Drupal/Core/Plugin/`
