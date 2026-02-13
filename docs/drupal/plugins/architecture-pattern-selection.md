---
description: Choose between Foundation+Extension, Provider Plugin, or Service Collector patterns
drupal_version: "11.x"
---

# Plugin Architecture Pattern Selection

## When to Use

> Choose the pattern that matches your integration context. Foundation+Extension when mature plugin ecosystems exist. Provider Plugin when abstracting diverse services. Service Collector when building REST API-first integrations.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Mature plugin ecosystem exists (Commerce, Views) | Foundation+Extension | Leverage existing infrastructure and admin interfaces |
| No existing plugin ecosystem for service category | Provider Plugin | Create standardized abstraction across diverse providers |
| REST API-first external system integration | Service Collector | Built-in REST endpoints, webhook support, polling events |
| Multiple plugin types working together | Foundation+Extension | Gateway + Method Type + Entity Type coordination |
| Stateless service aggregation | Service Collector | Minimal 3-method interface, tagged service discovery |
| User choice between service providers | Provider Plugin | Cross-cutting infrastructure (proxy, events, caching) |

## Pattern

**Three Proven Architectural Approaches**:

1. **Foundation + Extension Pattern** (Commerce Payment Model)
   - Create foundational plugin ecosystem with multiple plugin types
   - Extensions specialize existing plugin types
   - Leverage existing infrastructure and admin interfaces

2. **Provider Plugin Pattern** (AI Module Model)
   - Create new plugin managers for service provider abstraction
   - Standardize diverse services under consistent interfaces
   - Build cross-cutting infrastructure (proxy, events, caching)

3. **Service Collector Pattern** (Orchestration Module Model)
   - Aggregate stateless services via tagged service collection
   - Minimal interface contracts for simple, focused services
   - REST API-first architecture for external system integration

## Common Mistakes

- **Wrong**: Choosing Foundation+Extension when no ecosystem exists → **Right**: Use Provider Plugin to create new abstraction
- **Wrong**: Building plugin manager for simple REST API services → **Right**: Use Service Collector with tagged services
- **Wrong**: Using Service Collector when plugin alterations needed → **Right**: Use Provider Plugin for flexibility

## See Also

- [Foundation + Extension Pattern](foundation-extension-pattern.md)
- [Provider Plugin Pattern](provider-plugin-pattern.md)
- [Service Collector Pattern](service-collector-pattern.md)
- [Pattern Selection Decision Matrix](pattern-selection-decision-matrix.md)
- Reference: [Drupal Plugin API](https://www.drupal.org/docs/drupal-apis/plugin-api)
