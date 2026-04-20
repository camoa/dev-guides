---
description: Plugin Architecture - choose between Foundation+Extension, Provider Plugin, and Service Collector patterns
guide-meta:
  concepts:
    - plugin manager
    - plugin annotations
    - plugin derivatives
    - Foundation+Extension pattern
    - Provider Plugin pattern
    - Service Collector pattern
    - plugin configuration
  not:
    - specific plugin types (blocks, fields, views)
    - ECA plugins (see drupal/eca)
  requires:
    - drupal/services
  complements:
    - drupal/services
    - drupal/entities
    - drupal/blocks
  specializes: ""
  category: drupal
---

# Plugin Architecture

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Choose between plugin patterns | [Architecture Pattern Selection](architecture-pattern-selection.md) | Choose the pattern that matches your integration context. Foundation+Extension when mature plugin ecosystems exist. |
| Extend an existing plugin ecosystem | [Foundation + Extension Pattern](foundation-extension-pattern.md) | Use Foundation+Extension when mature plugin ecosystem exists (Commerce, Views). Use Provider Plugin when creating new service abstraction from scratch. |
| Abstract multiple service providers | [Provider Plugin Pattern](provider-plugin-pattern.md) | Use Provider Plugin when creating new service abstraction across diverse external providers. Use Foundation+Extension when mature plugin ecosystem exists. |
| Aggregate stateless services via tags | [Service Collector Pattern](service-collector-pattern.md) | Use Service Collector for REST API-first external integrations with stateless services. Use Provider Plugin for internal Drupal service abstraction. |
| Register a plugin manager | [Plugin Manager Implementation](plugin-manager-implementation.md) | Use plugin manager for Foundation+Extension and Provider Plugin patterns. Use service collector for Service Collector pattern. |
| Write consumer services | [Service Integration Patterns](service-integration-patterns.md) | Use provider abstraction for internal Drupal services consuming plugins. Use REST API controller pattern for external systems consuming service collectors. |
| Store plugin configuration | [Configuration Architecture](configuration-architecture.md) | Store plugin configuration in entities for Foundation pattern. Use config objects for Provider pattern. |
| Integrate with the event system | [Event System Integration](event-system-integration.md) | Use Provider pattern events for internal Drupal workflow integration. Use Service Collector polling events for external system integration via REST API. |
| See real-world implementation examples | [Real-World Implementation Examples](real-world-examples.md) | Reference these patterns when implementing similar plugin architectures. Commerce Payment for Foundation pattern, AI module for Provider pattern, Orchestration module for Service Collector pattern. |
| Use the decision matrix | [Pattern Selection Decision Matrix](pattern-selection-decision-matrix.md) | Use this matrix when starting a new plugin architecture to choose the correct pattern. Consider infrastructure, integration needs, and complexity tradeoffs. |
| Test plugin architectures | [Testing & Debugging](testing-debugging.md) | Test plugin architectures at unit level for plugin managers and service collectors. Use functional tests for REST API endpoints and integration workflows. |
| Apply security best practices | [Security Best Practices](security-best-practices.md) | Apply these security patterns to every plugin architecture implementation. Plugin systems are vulnerable because they load and execute code dynamically. |
| Optimize performance | [Performance Best Practices](performance-best-practices.md) | Apply these patterns to any plugin system handling more than a handful of plugins or processing external API calls. |
