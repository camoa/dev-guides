---
description: Decision matrix for choosing Foundation+Extension, Provider Plugin, or Service Collector patterns
drupal_version: "11.x"
---

# Pattern Selection Decision Matrix

## When to Use

> Use this matrix when starting a new plugin architecture to choose the correct pattern. Consider infrastructure, integration needs, and complexity tradeoffs.

## Decision

### Choose Foundation + Extension When

| Criteria | Why |
|----------|-----|
| Mature plugin ecosystem exists (Commerce, Entity, Views) | Leverage proven infrastructure and admin interfaces |
| Entity integration needed | `BundlePluginInterface` standard workflow for bundle fields |
| Want existing admin UX | Users expect consistent patterns across modules |
| Multiple plugin types working together | Gateway + Method Type + Entity Type coordination |
| Service specialization | Optimizing for specific service implementations |

### Choose Provider Plugin When

| Criteria | Why |
|----------|-----|
| No existing plugin ecosystem | Creating new service category from scratch |
| Service abstraction needed | Consistent API across diverse external services |
| Cross-cutting concerns | Proxy, events, caching, monitoring in main module |
| Provider-agnostic consumers | Consumers should work with any provider implementation |
| User choice of provider | End users select preferred service providers |
| Distributed modules | Providers as separate contrib modules |

### Choose Service Collector When

| Criteria | Why |
|----------|-----|
| Stateless aggregation | Services execute independently without shared state |
| REST API-first | External systems consume services via HTTP API |
| Webhook integration | Push notifications to external system callbacks |
| Polling events | Pull-based synchronization (timestamp or ID polling) |
| Minimal interface | Simple 3-method contract sufficient |
| Self-describing config | Configuration metadata auto-generated from constraints |
| No annotation overhead | Tagged service discovery simpler than plugin discovery |
| No plugin alterations | Services don't need `hook_plugin_info_alter` |

## Pattern

**Implementation Complexity**:
- **Foundation Pattern**: Highest initial setup, lowest extension cost
- **Provider Pattern**: Medium setup cost, very low consumer integration cost
- **Service Collector Pattern**: Lowest setup cost, minimal interface overhead, but limited flexibility

**Maintenance Considerations**:
- **Foundation Pattern**: Extensions must track foundation API changes
- **Provider Pattern**: Main module maintains stable interfaces, providers evolve independently
- **Service Collector Pattern**: All providers tightly coupled to shared DTOs, but minimal contract reduces breaking changes

**REST API Integration**:
- **Foundation Pattern**: Requires custom REST resource implementations
- **Provider Pattern**: Can expose providers via custom REST resources with additional effort
- **Service Collector Pattern**: Built-in REST endpoints, DTOs designed for JSON serialization

**External System Integration**:
- **Foundation Pattern**: Not designed for external integration, focus on Drupal admin workflows
- **Provider Pattern**: Internal service abstraction, can add REST layer but not primary use case
- **Service Collector Pattern**: Primary use case is external system integration via webhooks and polling

## Common Mistakes

- **Wrong**: Choosing pattern based on familiarity alone → **Right**: Match pattern to integration context and requirements
- **Wrong**: Using Service Collector when plugin alterations needed → **Right**: Use Provider Plugin for flexibility
- **Wrong**: Building Provider Plugin when Foundation exists → **Right**: Extend mature ecosystem

## See Also

- [Architecture Pattern Selection](architecture-pattern-selection.md)
- [Foundation + Extension Pattern](foundation-extension-pattern.md)
- [Provider Plugin Pattern](provider-plugin-pattern.md)
- [Service Collector Pattern](service-collector-pattern.md)
- Reference: [Service Tags vs Plugin Managers](https://drupal.stackexchange.com/questions/262545/difference-between-service-and-plugin)
- Reference: [Practical Use Cases of Tagged Services](https://drupal.com.ua/135/practical-use-cases-tagged-services-drupal)
