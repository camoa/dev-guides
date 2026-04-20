---
description: Drupal 7 to 11 migration — decision guides for Migrate API, content strategy, and performance
guide-meta:
  concepts:
    - Migrate API
    - migration definitions
    - process plugins
    - source plugins
    - D7 to D11
    - migration rollback
    - content migration
    - config migration
  not:
    - content import (see drupal/recipes)
    - data feeds import
  requires:
    - drupal/entities
  complements:
    - drupal/config-management
    - drupal/entities
  specializes: ""
  category: drupal
---

# Drupal 7 to 11 Migration

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Choose between standard rebuild, wizard, or retrofit | [Choose Migration Approach](choose-migration-approach.md) | Drupal 7 to 11 is a complete rebuild, not an upgrade. No 1:1 mapping exists for core modules, themes, content types, or custom code. |
| Assess project scope and timeline | [Assess Migration Scope](assess-migration-scope.md) | Before writing any migration code, complete a comprehensive inventory of your D7 site. Assessment phase prevents mid-migration surprises, scope creep, and timeline failures. |
| Map D7 field collections to D11 paragraphs | [Map Content Structure](map-content-structure.md) | After inventory, map D7 content architecture to D11 entity structure. D7 field collections become D11 paragraphs, D7 nodes may become media entities, taxonomy structure may consolidate. |
| Decide rewrite vs retrofit vs retire for custom modules | [Plan Custom Code Strategy](plan-custom-code-strategy.md) | D7 custom modules use hooks, procedural code, and deprecated APIs. D11 requires object-oriented plugins, services, event subscribers. |
| Configure D7 database as migration source | [Configure Migration Sources](configure-migration-sources.md) | Set up D7 database connection as migration source. Core provides source plugins for D7 nodes, users, taxonomy, files. |
| Write YAML migration definitions | [Create Migration Definitions](create-migration-definitions.md) | Migration definitions are YAML files defining source, process, and destination. Core provides templates for D7→D11 migrations. |
| Transform source data with process plugins | [Handle Field Mappings](handle-field-mappings.md) | Process plugins transform source data to destination format. Core provides 50+ plugins for common transformations. |
| Execute migrations with Drush in correct order | [Migrate Content Entities](migrate-content-entities.md) | Execute migrations in dependency order: users first, then taxonomy, files, then nodes. Use Drush commands for batch processing. |
| Migrate content types, views, and configuration | [Migrate Configuration](migrate-configuration.md) | Configuration migration transfers content types, field definitions, views, image styles from D7 to D11. Unlike content, configuration often requires manual recreation due to structural changes. |
| Apply security controls during migration | [Security Best Practices](security-best-practices.md) | Migration introduces security risks: SQL injection in custom sources, XSS in migrated content, access bypass during imports. Apply security controls at source, process, and destination layers. |
| Optimize performance for large migrations | [Performance Optimization](performance-optimization.md) | Large migrations (10,000+ nodes) require memory management, batch processing, and query optimization. Monitor PHP memory, database connections, and migration speed. |
| Validate and test migration results | [Test Migration Results](test-migration-results.md) | Test throughout migration, not just at the end. Use small batches, validate content structure, verify relationships, check for data loss. |
| Debug migration failures and errors | [Debug Migration Failures](debug-migration-failures.md) | Migrations fail for many reasons: missing dependencies, data type mismatches, plugin errors. Use logging, verbose output, and incremental testing to isolate issues. |
| Handle paragraphs and entity references with revisions | [Complex Field Mappings](complex-field-mappings.md) | Paragraphs, entity references with revisions, and nested structures require multi-step process pipelines. Understand target field structure before mapping. |
| Follow proven migration patterns | [Migration Best Practices](migration-best-practices.md) | Follow these patterns to avoid common migration pitfalls. Based on community experience migrating hundreds of D7 sites. |
| Avoid common migration failures | [Anti-Patterns to Avoid](anti-patterns.md) | Learn from common migration failures. These patterns consistently cause project delays, cost overruns, and technical debt. |
