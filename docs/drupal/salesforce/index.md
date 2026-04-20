---
description: Drupal Salesforce Suite — bidirectional sync between Drupal entities and Salesforce objects, authentication, mapping, events, and Drush operations
guide-meta:
  concepts:
    - Salesforce Suite
    - OAuth authentication
    - JWT authentication
    - entity mapping
    - push synchronization
    - pull synchronization
    - SOQL queries
    - MappedObject
    - Salesforce REST client
  not:
    - CRM Core
    - HubSpot integration
  requires:
    - drupal/entities
    - drupal/services
  complements:
    - drupal/config-management
    - drupal/caching
  specializes: ""
  category: drupal
---

# Drupal Salesforce Suite

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand the module architecture and components | [Architecture Overview](salesforce-overview.md) | Use the Salesforce module suite when you need bidirectional synchronization between Drupal entities and Salesforce objects. The base module is always required; submodules are added based on sync direction and features needed. |
| Choose between OAuth and JWT authentication | [OAuth Authentication](oauth-authentication.md) | Use OAuth when interactive user authorization is needed or for single-org integrations. Use JWT when server-to-server automation is required, no interactive auth is possible, or multiple orgs are involved. |
| Set up JWT bearer token authentication | [JWT Authentication](jwt-authentication.md) | Use JWT when you need server-to-server authentication without interactive authorization. Use the GovCloud plugin only for Salesforce Government Cloud instances. |
| Create entity-to-Salesforce field mappings | [Mapping Framework](mapping-framework.md) | Use `salesforce_mapping` for any entity sync between Drupal and Salesforce. It provides the `SalesforceMapping` config entity (defines the relationship) and `MappedObject` content entity (tracks individual record links). |
| Configure mappings via admin UI | [Mapping UI & Sync Triggers](mapping-ui.md) | Use the mapping UI for initial setup, simple mappings, and site builder workflows. Use code/config for complex mappings, multi-site deployments, and version-controlled configuration. |
| Push Drupal entity changes to Salesforce | [Push Synchronization](push-synchronization.md) | Use `salesforce_push` when you need to send Drupal entity changes to Salesforce. Use `async = TRUE` for production (queue-based, non-blocking). |
| Pull Salesforce changes into Drupal | [Pull Synchronization](pull-synchronization.md) | Use `salesforce_pull` when you need to import Salesforce object changes into Drupal. Use `pull_trigger_date` for incremental sync of large datasets. |
| Choose optional submodules (logger, webform, address, SOAP) | [Optional Submodules](optional-submodules.md) | Enable optional submodules only when you need their specific functionality. The `salesforce_example` module is for development reference only — never enable in production. |
| Hook into sync events with EventSubscriber | [Event System](event-system.md) | Use EventSubscriber pattern for all Salesforce customization. The legacy hook system is deprecated. |
| Query and CRUD objects via the REST client | [REST Client API](rest-client-api.md) | Use `salesforce.client` (`RestClient`) when you need programmatic, non-mapping-driven access to Salesforce objects — direct CRUD, raw SOQL queries, custom Apex REST calls, or fetching binary attachments. |
| Build SOQL queries programmatically | [SOQL Query Builder](soql-query-builder.md) | Use `SelectQuery` for programmatic SOQL queries with conditions. Use `SelectQueryRaw` for complex queries with subqueries or syntax not supported by the builder. |
| Load and create MappedObject entities | [Mapped Objects API](mapped-objects-api.md) | Use the `MappedObjectStorage` service when you need to programmatically query or manage the link between Drupal entities and Salesforce records — checking sync status, loading by SFID, or creating links manually. |
| Queue entities for push programmatically | [Push Queue Operations](push-queue-operations.md) | Use the `queue.salesforce_push` service when you need to programmatically queue entities for push outside of the normal entity save trigger — for example, in migrations, batch operations, or after importing data bypassing hooks. |
| Create a custom field mapping plugin | [Custom Field Mapping Plugin](custom-field-mapping-plugin.md) | Create a custom field mapping plugin when built-in plugins (`Properties`, `Token`, `Constant`, etc.) cannot express the mapping logic needed — calculated values, custom field types, or complex transformations reusable across multiple… |
| Export mappings and manage auth per environment | [Configuration Management](configuration-management.md) | Use Drupal's standard config management (drush config:export/import) for mappings. Never commit auth credentials to version control — consumer secrets are not exported and must be configured per environment. |
| Configure cron vs standalone queue processing | [Queue Processing](queue-processing.md) | Use cron-based processing for standard setups. Use standalone endpoints when you need higher-frequency processing, custom scheduling (Jenkins, external cron), or separation from Drupal's cron run. |
| Run Drush commands for push, pull, and maintenance | [Drush Commands](drush-commands.md) | Use Drush commands for manual queue processing, debugging, maintenance operations, and resyncing data. All commands are namespaced under `salesforce:`, `salesforce_mapping:`, `salesforce_push:`, and `salesforce_pull:`. |
| Find RestClient, SFID, SObject, and other class references | [Class Reference](class-reference.md) | Use this reference when implementing custom code that interacts with the Salesforce module's PHP classes directly. All paths are relative to `/web/modules/contrib/salesforce/`. |
| Diagnose auth failures, push/pull not triggering, stuck queues | [Troubleshooting](troubleshooting.md) | Use this guide when sync is not working as expected. Enable `salesforce_logger` first to capture errors. |
| Optimize caching, queue limits, and API call efficiency | [Performance](performance.md) | Optimize Salesforce sync performance when experiencing high API usage, slow entity saves, or large queue backlogs. The primary levers are: caching object metadata, async queue processing, and selective field/record queries. |
| Create custom auth providers, queue processors, pull workers | [Extension Patterns](extension-patterns.md) | Use these extension points when built-in auth providers, queue processors, or pull workers cannot meet your requirements — for example, custom SSO auth, bulk API processing, or complex pull transformations not achievable via events. |
| Decide submodule selection and events vs plugins vs config | [Decision Framework](decision-framework.md) | Use this guide when starting a Salesforce integration to select the right submodules and approach. Return to it when deciding whether to use events, custom plugins, or plain configuration. |
