---
description: Configuration Forms — choose form types, build admin interfaces, implement operations
guide-meta:
  concepts:
    - ConfigFormBase
    - FormBase admin
    - ListBuilder
    - dropbutton operations
    - configuration schema
    - settings forms
  not:
    - Form API element types (see drupal/forms)
    - multi-step forms
    - AJAX form patterns
  requires:
    - drupal/forms
  complements:
    - drupal/config-management
    - drupal/entities
    - drupal/services
  specializes: ""
  category: drupal
---

# Configuration Forms

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Choose between FormBase and ListBuilder | [FormBase vs ListBuilder](formbase-vs-listbuilder.md) | Use FormBase/ConfigFormBase when building settings pages or custom admin forms. Use ListBuilder when displaying entity collections with standard CRUD operations. |
| Create a configuration settings form | [ConfigFormBase Pattern](configformbase-pattern.md) | Use ConfigFormBase when building a module settings page that stores configuration in the config system (database + YML export). |
| Build a custom admin table/form | [FormBase Pattern](formbase-pattern.md) | Use FormBase when building custom admin forms that don't fit ConfigFormBase (bulk operations, complex workflows, non-config data). |
| Create an entity collection list | [ListBuilder Pattern](listbuilder-pattern.md) | Use ListBuilder when building entity collection admin pages with standard CRUD operations. |
| Implement dropbutton operations | [Operations Implementation](operations-implementation.md) | Use #type operations when adding action links (Edit, Delete, etc.) to table rows in FormBase or customizing operations in ListBuilder. |
| Define configuration schema | [Configuration Schema](configuration-schema.md) | Use configuration schema when defining structure and validation constraints for configuration stored by ConfigFormBase. |
| Use dependency injection in forms | [Dependency Injection](dependency-injection.md) | Use dependency injection when forms need services (config factory, entity type manager, database, custom services). |
| Secure configuration forms | [Security Best Practices](security-best-practices.md) | All configuration forms must follow security best practices to prevent vulnerabilities. |
| Optimize form performance | [Performance Best Practices](performance-best-practices.md) | Optimize configuration forms to avoid performance bottlenecks, especially forms with many operations or large datasets. |
| Avoid common mistakes | [Common Mistakes](common-mistakes.md) | Reference when debugging form issues or reviewing code. |
