---
description: Validation and testing strategy throughout migration lifecycle
drupal_version: "11.x"
---

# Test Migration Results

## When to Use

Test throughout migration, not just at the end. Use small batches, validate content structure, verify relationships, check for data loss.

## Decision

| Test type | Method | Tools |
|---|---|---|
| Sample data migration | Limited import | `--limit=10` flag |
| Content structure validation | Manual review | Browse migrated nodes |
| Relationship integrity | Query checks | SQL joins, entity browser |
| Performance testing | Full migration on staging | Time tracking, memory monitoring |
| Regression testing | Automated tests | Behat, Cypress |

## Pattern

**Test workflow:**

```bash
# 1. Test with tiny sample
drush migrate:import d7_node_article --limit=10 --update
# Review 10 nodes manually

# 2. Rollback and test batch
drush migrate:rollback d7_node_article
drush migrate:import d7_node_article --limit=100
# Check for patterns, errors

# 3. Validate relationships
drush sqlq "SELECT COUNT(*) FROM node__field_author WHERE field_author_target_id IS NULL"
# Should be 0 - no broken references

# 4. Full staging migration
drush migrate:import --group=d7_content --update
# Monitor memory, time

# 5. Automated tests (Behat example)
Scenario: Migrated article nodes maintain relationships
  Given I am logged in as "admin"
  When I visit "/node/123"
  Then I should see the link "Original Author Name"
  And the "field_category" field should contain "News"
```

**Reference**: `/modules/contrib/migrate_tools/` for testing commands

## Common Mistakes

- **Wrong**: Testing only at the end → **Right**: Compound failures hard to debug
- **Wrong**: Not validating entity references → **Right**: Broken relationships slip through
- **Wrong**: Skipping rollback testing → **Right**: May not be able to undo migration
- **Wrong**: Not documenting test results → **Right**: Repeat same tests, waste time
- **Wrong**: Assuming D11 site ready for production → **Right**: Always do full QA pass

## See Also

- [Debug migration failures](debug-migration-failures.md) for troubleshooting
- Reference: [Drupal testing best practices](https://www.drupal.org/docs/testing)
