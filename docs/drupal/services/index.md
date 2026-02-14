---
description: Drupal Services & Dependency Injection decision guides — atomic references for defining services, injection patterns, service tags, event subscribers, and container architecture.
---

# Drupal Services & Dependency Injection

**Drupal 11.x** (applicable to Drupal 10.x+) | **Philosophy**: Services ARE configuration — defined in YAML, managed by the container

## I need to...

| Task | Guide |
|------|-------|
| Understand what services and DI are | [Services & DI Overview](services-di-overview.md) |
| Learn how the service container works | [Service Container Architecture](service-container-architecture.md) |
| Understand the services.yml file structure | [services.yml Schema](services-yml-schema.md) |
| Know all available service definition properties | [Service Definition Properties](service-definition-properties.md) |
| Define a new service | [Defining Services](defining-services.md) |
| Use autowiring for my service | [Autowiring](autowiring.md) |
| Inject services into a controller or form | [Constructor Injection](constructor-injection.md) |
| Inject services into a plugin (block, field formatter) | [Plugin Injection](plugin-injection.md) |
| Decide when to use \Drupal vs dependency injection | [The \Drupal Global Helper](drupal-global-helper.md) |
| Tag a service (event_subscriber, cache.context, etc.) | [Service Tags](service-tags.md) |
| Collect multiple tagged services | [Tagged Service Collectors](tagged-service-collectors.md) |
| Create an event subscriber | [Event Subscribers](event-subscribers.md) |
| Alter existing services | [Service Providers & Altering](service-providers-and-altering.md) |
| Add a compiler pass | [Compiler Passes](compiler-passes.md) |
| Find what core services are available | [Core Services Reference](core-services-reference.md) |
| Use a factory to create services | [Factory Services](factory-services.md) |
| Handle service serialization | [DependencySerializationTrait](dependency-serialization-trait.md) |
| Learn DI best practices | [Best Practices & Patterns](best-practices-and-patterns.md) |
| Avoid common mistakes | [Anti-Patterns & Common Mistakes](anti-patterns-and-common-mistakes.md) |
| Understand security and performance | [Security & Performance](security-and-performance.md) |
| Find code references | [Code Reference Map](code-reference-map.md) |
