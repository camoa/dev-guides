---
description: Decision matrix for choosing Foundation+Extension, Provider Plugin, or Service Collector patterns
tldr: "Use this matrix when starting a new plugin architecture to choose the correct pattern. Consider infrastructure, integration needs, and complexity tradeoffs."
drupal_version: "11.x"
---

# Pattern Selection Decision Matrix

## When to Use

> Use this matrix when starting a new plugin architecture to choose the correct pattern. Consider infrastructure, integration needs, and complexity tradeoffs.

## Decision

### Choose Foundation + Extension When:

| Criteria | Foundation Pattern |
|----------|-------------------|
| **Existing Infrastructure** | ✅ Mature plugin ecosystem exists (Commerce, Entity, Views) |
| **Entity Integration** | ✅ Need bundle fields and entity relationships |
| **Admin Interfaces** | ✅ Want to leverage existing admin UX and workflows |
| **Multiple Plugin Types** | ✅ Gateway + Method Type + Entity Type working together |
| **Service Specialization** | ✅ Optimizing for specific service implementations |
| **User Familiarity** | ✅ Users expect consistent patterns across modules |

### Choose Provider Plugin When:

| Criteria | Provider Pattern |
|----------|-----------------|
| **No Existing System** | ✅ Creating new service category from scratch |
| **Service Abstraction** | ✅ Need consistent API across diverse services |
| **Cross-Cutting Concerns** | ✅ Require proxy, events, caching, monitoring |
| **Provider Agnostic** | ✅ Consumers should work with any provider |
| **External Services** | ✅ Integrating with many different external APIs |
| **User Choice** | ✅ End users select preferred service providers |
| **Distributed Modules** | ✅ Providers as separate contrib modules |

### Choose Service Collector When:

| Criteria | Service Collector Pattern |
|----------|--------------------------|
| **Stateless Aggregation** | ✅ Services execute independently without shared state |
| **REST API First** | ✅ External systems consume services via HTTP API |
| **Webhook Integration** | ✅ Push notifications to external system callbacks |
| **Polling Events** | ✅ Pull-based synchronization (timestamp or ID polling) |
| **Minimal Interface** | ✅ Simple 3-method contract sufficient |
| **Self-describing config** | ✅ Configuration metadata auto-generated from constraints |
| **No annotation overhead** | ✅ Tagged service discovery simpler than plugin discovery |
| **No Plugin Alterations** | ✅ Services don't need `hook_plugin_info_alter` customization |
| **JSON Serialization** | ✅ All data structures must serialize to JSON for REST |
| **No Admin UI Needed** | ✅ External systems provide their own configuration interface |

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
