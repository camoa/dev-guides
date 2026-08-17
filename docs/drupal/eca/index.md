---
description: ECA 3.1 (Event-Condition-Action) plugin development — create custom actions, events, and conditions for Drupal ^11.3 / ^12.0
tracks:
  - project: eca
    channel: stable
    declared: "3.1"
    verified: 2026-05-20
guide-meta:
  concepts:
    - ECA module
    - ECA actions
    - ECA events
    - ECA conditions
    - ECA tokens
    - plugin derivers
    - ECA workflows
  not:
    - Rules module
    - Drupal core event system (see drupal/services)
  requires:
    - drupal/plugins
    - drupal/services
  complements:
    - drupal/entities
    - drupal/forms
  specializes: ""
  category: drupal
---

# ECA

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Create a custom Action plugin | [Action Plugin Basics](action-plugin-basics.md) | Create custom Action plugins when you need to perform operations that existing ECA actions cannot handle, such as integrating with external APIs, processing custom data structures, or implementing specialized business logic. |
| Integrate external APIs in actions | [Advanced Action Patterns](advanced-action-patterns.md) | Use advanced action patterns when integrating with external APIs, processing complex data structures with YAML configuration, validating external service responses, or implementing sophisticated error handling. |
| Create custom Events | [Event Plugin Basics](event-plugin-basics.md) | Create custom Event plugins when you need to trigger ECA workflows based on custom application logic, third-party integrations, or domain-specific business events that core Drupal events don't cover. |
| Filter events by entity type/bundle | [Entity-Aware Events](entity-aware-events.md) | Use entity-aware events when you need to filter event triggers by entity type, bundle, or field name. This enables precise workflow targeting without evaluating every entity operation. |
| Create custom Conditions | [Condition Plugin Basics](condition-plugin-basics.md) | Create custom Condition plugins when you need to evaluate business logic that existing conditions don't support, such as checking external API state, validating complex data structures, or implementing domain-specific rules. |
| Compare two values in a condition | [String Comparison Conditions](string-comparison-conditions.md) | Use StringComparisonBase when comparing two values using standard operators (equals, contains, starts with, regex, etc.). The base class provides operator selection and comparison logic; you only implement value retrieval. |
| Add token support to forms | [Token Form Integration](token-form-integration.md) | Add token integration to form fields whenever users need to reference dynamic values from the workflow. Tokens enable accessing event data, global values, and previous action results. |
| Store structured data in tokens | [Complex Token Structures](complex-token-structures.md) | Store complex data structures in tokens when actions need to pass multiple related values, structured results, or collections to downstream actions and conditions. Tokens can hold arrays, objects, and nested data. |
| Inject services into plugins | [Service Injection](service-injection.md) | Inject services when your plugin needs functionality beyond what the base class provides, such as HTTP clients, external APIs, database access, or custom business logic services. |
| Use traits to avoid code duplication | [Reusable Traits](reusable-traits.md) | Use ECA's built-in traits to avoid duplicating complex logic that's already implemented and tested. Traits encapsulate patterns like form field lookup, entity saving, list operations, and YAML configuration. |
| Validate YAML configuration | [YAML Configuration](yaml-configuration.md) | Use YAML configuration fields when plugins need complex, structured configuration that's too cumbersome for multiple form fields, such as API client options, nested settings, or dynamic key-value pairs. |
| Access control for plugin execution | [Access Control Patterns](access-control-patterns.md) | Implement `access()` to validate plugin configuration before execution. This prevents workflows from running with invalid settings, provides clear error messages, and catches problems early. |
| Clean up state after workflow execution | [Cleanup Interface](cleanup-interface.md) | Implement `CleanupInterface` when your event plugin needs to perform cleanup operations after all successor actions complete, such as restoring switched user accounts, releasing resources, or processing accumulated state. |
| Preserve tokens across execution | [Token Receiver Interface](token-receiver-interface.md) | Implement `TokenReceiverInterface` when your event plugin needs to preserve specific tokens across the entire workflow execution, ensuring token data survives even after actions complete. |
| Generate multiple plugins from one class | [Plugin Derivers](plugin-derivers.md) | Use plugin derivers to generate multiple plugin instances from a single class definition. This enables creating variant plugins based on external data (like tamper plugins, field widgets, or AI models) without code duplication. |
| Cache expensive operations | [Performance Patterns](performance-patterns.md) | Apply performance optimizations when plugins perform expensive operations like external API calls, complex calculations, or repeated database queries. Cache results, batch operations, and avoid N+1 queries. |
| Secure external API integrations | [Security Best Practices](security-best-practices.md) | Apply security patterns to all plugins that handle user input, external data, API credentials, or entity access. Security is mandatory, not optional. |
| Test ECA plugins | [Kernel Testing](kernel-testing.md) | Write kernel tests for all ECA plugins to verify configuration, execution logic, token handling, and integration with Drupal services. Kernel tests run faster than browser tests and provide sufficient coverage for most plugin logic. |
| Debug workflows | [Debugging Workflows](debugging-workflows.md) | Debug ECA workflows when actions don't execute as expected, tokens have unexpected values, or conditions evaluate incorrectly. In ECA 3.1 reach for the built-in Process Debugger first; use logger statements for custom plugin observability and production. |
| Avoid common mistakes | [Common Pitfalls](common-pitfalls.md) | Review this section before completing any ECA plugin to avoid the most common mistakes that break plugins or cause maintenance problems. |
| Understand mandatory rules | [Mandatory Rules](mandatory-rules.md) | Use this checklist before completing ANY ECA plugin. These are not optional - violating these rules will cause bugs or break your plugin. |
