---
description: Drupal Salesforce Suite — bidirectional sync between Drupal entities and Salesforce objects, authentication, mapping, events, and Drush operations
---

# Drupal Salesforce Suite

| I need to... | Guide |
|---|---|
| Understand the module architecture and components | [Architecture Overview](salesforce-overview.md) |
| Choose between OAuth and JWT authentication | [OAuth Authentication](oauth-authentication.md) |
| Set up JWT bearer token authentication | [JWT Authentication](jwt-authentication.md) |
| Create entity-to-Salesforce field mappings | [Mapping Framework](mapping-framework.md) |
| Configure mappings via admin UI | [Mapping UI & Sync Triggers](mapping-ui.md) |
| Push Drupal entity changes to Salesforce | [Push Synchronization](push-synchronization.md) |
| Pull Salesforce changes into Drupal | [Pull Synchronization](pull-synchronization.md) |
| Choose optional submodules (logger, webform, address, SOAP) | [Optional Submodules](optional-submodules.md) |
| Hook into sync events with EventSubscriber | [Event System](event-system.md) |
| Query and CRUD objects via the REST client | [REST Client API](rest-client-api.md) |
| Build SOQL queries programmatically | [SOQL Query Builder](soql-query-builder.md) |
| Load and create MappedObject entities | [Mapped Objects API](mapped-objects-api.md) |
| Queue entities for push programmatically | [Push Queue Operations](push-queue-operations.md) |
| Create a custom field mapping plugin | [Custom Field Mapping Plugin](custom-field-mapping-plugin.md) |
| Export mappings and manage auth per environment | [Configuration Management](configuration-management.md) |
| Configure cron vs standalone queue processing | [Queue Processing](queue-processing.md) |
| Run Drush commands for push, pull, and maintenance | [Drush Commands](drush-commands.md) |
| Find RestClient, SFID, SObject, and other class references | [Class Reference](class-reference.md) |
| Diagnose auth failures, push/pull not triggering, stuck queues | [Troubleshooting](troubleshooting.md) |
| Optimize caching, queue limits, and API call efficiency | [Performance](performance.md) |
| Create custom auth providers, queue processors, pull workers | [Extension Patterns](extension-patterns.md) |
| Decide submodule selection and events vs plugins vs config | [Decision Framework](decision-framework.md) |
