---
description: Inventory and timeline estimation for D7 to D11 migration projects
drupal_version: "11.x"
---

# Assess Migration Scope

## When to Use

Before writing any migration code, complete a comprehensive inventory of your D7 site. Assessment phase prevents mid-migration surprises, scope creep, and timeline failures.

## Decision

| If your site has... | Timeline estimate | Complexity level |
|---|---|---|
| Basic content types, minimal custom code | 3-6 months | Simple |
| Multiple content types, standard custom modules | 6-9 months | Medium |
| Complex paragraphs/field collections, extensive custom code, integrations | 9-12+ months | Complex |

## Pattern

**Assessment checklist (document before starting):**

```bash
# Content inventory
drush sqlq "SELECT type, COUNT(*) FROM node GROUP BY type"
drush sqlq "SELECT name FROM system WHERE type='module' AND status=1" | grep -v "^core$"

# Custom code audit
find sites/all/modules/custom -name "*.module" -o -name "*.inc"
find sites/all/themes/custom -name "*.tpl.php"

# Integration documentation
# Document: External APIs, payment gateways, CRM connections, feeds
```

**Key deliverables:**
1. Content type inventory with field lists
2. Contrib module list with D11 equivalents identified
3. Custom module/theme audit with rewrite/retire decisions
4. External integration documentation
5. Timeline with phased milestones

**Reference**: `/core/modules/migrate_drupal/` for available source plugins

## Common Mistakes

- **Wrong**: Starting code before inventory → **Right**: Creates rework when unexpected dependencies discovered
- **Wrong**: Ignoring contrib module compatibility → **Right**: Some D7 modules have no D11 equivalent, require alternatives
- **Wrong**: Underestimating custom code rewrite time → **Right**: D7 hooks don't map to D11 event subscribers/services
- **Wrong**: Migrating unused content → **Right**: Retire outdated content types to reduce complexity

## See Also

- [Choose migration approach](choose-migration-approach.md) uses assessment results
- [Plan custom code strategy](plan-custom-code-strategy.md) for module decisions
- Reference: [Drupal 11 migration checklist](https://opensenselabs.com/blog/drupal-11-upgrade-checklist-drupal-7-11-migration)
