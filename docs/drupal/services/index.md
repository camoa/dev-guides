---
description: Drupal Services & Dependency Injection decision guides — atomic references for defining services, injection patterns, service tags, event subscribers, and container architecture.
guide-meta:
  concepts:
    - services.yml
    - dependency injection
    - service container
    - autowiring
    - constructor injection
    - plugin injection
    - service tags
    - tagged service collectors
    - event subscribers
    - service providers
    - compiler passes
    - factory services
  not:
    - plugin architecture patterns (see drupal/plugins)
    - hook system (see drupal/solid-principles)
  requires: []
  complements:
    - drupal/plugins
    - drupal/solid-principles
    - drupal/forms
  specializes: ""
  category: drupal
---

# Drupal Services & Dependency Injection

**Drupal 11.x** (applicable to Drupal 10.x+) | **Philosophy**: Services ARE configuration — defined in YAML, managed by the container

## I need to...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what services and DI are | [Services & DI Overview](services-di-overview.md) | When you need to understand the foundation of modern Drupal architecture — services provide reusable functionality, dependency injection eliminates hard-coded dependencies. |
| Learn how the service container works | [Service Container Architecture](service-container-architecture.md) | When you need to understand how Drupal's service container works under the hood — essential for debugging, optimization, and advanced patterns. |
| Understand the services.yml file structure | [services.yml Schema](services-yml-schema.md) | When you need to understand the structure of *.services.yml files — the foundational configuration format for Drupal services. |
| Know all available service definition properties | [Service Definition Properties](service-definition-properties.md) | When defining a service in *.services.yml — this reference catalog covers all available properties and their purposes. |
| Define a new service | [Defining Services](defining-services.md) | When you need to register a new service with the Drupal container. |
| Use autowiring for my service | [Autowiring](autowiring.md) | When you want the container to automatically resolve constructor arguments based on type hints — reduces YAML boilerplate for services with many dependencies. |
| Inject services into a controller or form | [Constructor Injection](constructor-injection.md) | When injecting services into controllers, forms, or any class that implements `ContainerInjectionInterface` — the standard Drupal dependency injection pattern. |
| Inject services into a plugin (block, field formatter) | [Plugin Injection](plugin-injection.md) | When injecting services into plugins (blocks, field formatters, field widgets, condition plugins, etc.) — plugins receive additional arguments (configuration, plugin_id, plugin_definition) that must be handled. |
| Decide when to use \Drupal vs dependency injection | [The \Drupal Global Helper](drupal-global-helper.md) | When you understand when the \Drupal static helper is appropriate versus when dependency injection is required. |
| Tag a service (event_subscriber, cache.context, etc.) | [Service Tags](service-tags.md) | When you need to mark a service for special processing by compiler passes — tags group services by purpose and enable extensible architectures. |
| Collect multiple tagged services | [Tagged Service Collectors](tagged-service-collectors.md) | When you need to build an extensible system where multiple services can register themselves to be used by a manager service — plugin-like architecture without the plugin API overhead. |
| Create an event subscriber | [Event Subscribers](event-subscribers.md) | When you need to react to events in Drupal — kernel events (request, response, exception), entity events (CRUD operations), or custom events. |
| Alter existing services | [Service Providers & Altering](service-providers-and-altering.md) | When you need to alter existing service definitions, add new services programmatically, or register compiler passes — advanced container manipulation beyond YAML. |
| Add a compiler pass | [Compiler Passes](compiler-passes.md) | When you need custom processing of service definitions during container compilation — validate services, process custom tags, or modify the container graph. |
| Find what core services are available | [Core Services Reference](core-services-reference.md) | When you need to know what core services are available for injection — this catalog covers the most commonly used Drupal services. |
| Use a factory to create services | [Factory Services](factory-services.md) | When a service requires complex instantiation logic, runtime parameters, or conditional creation — factories encapsulate creation logic. |
| Handle service serialization | [DependencySerializationTrait](dependency-serialization-trait.md) | When your service or class is serialized (stored in cache, queued, etc.) and contains injected service dependencies — this trait prevents serializing the entire service object graph. |
| Learn DI best practices | [Best Practices & Patterns](best-practices-and-patterns.md) | When you want to follow established Drupal community standards for services and dependency injection. |
| Avoid common mistakes | [Anti-Patterns & Common Mistakes](anti-patterns-and-common-mistakes.md) | When you want to avoid the most common mistakes developers make with Drupal services and dependency injection. |
| Understand security and performance | [Security & Performance](security-and-performance.md) | When you need to understand the security and performance implications of service design and dependency injection patterns. |
| Find code references | [Code Reference Map](code-reference-map.md) |  |
