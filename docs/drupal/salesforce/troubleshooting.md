---
description: "Salesforce troubleshooting — auth failures, push not triggering, pull not creating entities, field mapping issues, stuck queues, API limits"
tldr: "Use this guide when sync is not working as expected. Enable `salesforce_logger` first to capture errors."
drupal_version: "11.x"
---

# Troubleshooting

## When to Use

> Use this guide when sync is not working as expected. Enable `salesforce_logger` first to capture errors. Check logs at `/admin/reports/dblog` filtered by "salesforce".

## Decision

| Symptom | First Check | Debug Tool |
|---|---|---|
| "RestClient is not initialized" | Auth provider configured and authorized | `drush sflp`, `drush sfrt` |
| Push not triggering | Sync trigger enabled on mapping | `salesforce_push_queue` table, `drush queue:list` |
| Pull not creating entities | `pull_create` trigger enabled, SOQL returns records | `PULL_PREPULL` event, entity validation logs |
| Field mapping not working | Direction correct, field exists on both sides | `PUSH_PARAMS` event, `objectDescribe()` |
| Queue stuck / growing | Failed items in `salesforce_push_queue` | `drush queue:list`, check `fails > 0` |
| API limit errors | Check `Sforce-Limit-Info` response header | `$client->getApiUsage()` |

## Authentication Issues

**Symptom:** "RestClient is not initialized" error

**Check:**
1. Auth provider configured: `/admin/config/salesforce`
2. Credentials entered correctly
3. Authorization completed
4. Token not expired (check `key_value` table for `salesforce.access_token`)

**Debug:**
- Service: `plugin.manager.salesforce.auth_providers`
- Method: `getToken()`, `getProvider()`
- Location: `/web/modules/contrib/salesforce/src/SalesforceAuthProviderPluginManager.php`

## Push Not Triggering

**Check:**
1. Mapping exists for entity type/bundle
2. Sync trigger enabled: `sync_triggers.push_create` / `push_update` / `push_delete`
3. Queue items created: Check `salesforce_push_queue` table
4. Push queue processing: Check cron, standalone endpoint
5. Event subscribers not vetoing: Check `PUSH_ALLOWED` event

**Debug:**
- Enable `salesforce_logger` module
- Check logs: `/admin/reports/dblog` (filter: salesforce)
- Examine queue: `drush queue:list` → `salesforce_push`

## Pull Not Creating Entities

**Check:**
1. Pull trigger configured: `sync_triggers.pull_create` / `pull_update`
2. SOQL query returns records: Test query in Salesforce Developer Console
3. Pull frequency not throttling: Check last pull timestamp
4. WHERE clause not filtering all records
5. Entity creation not failing validation

**Debug:**
- Event: `PULL_PREPULL` - Check if veto called
- Event: `PULL_PRESAVE` - Check entity before save
- Entity validation errors: Check logs

## Field Mapping Not Working

**Check:**
1. Field mapping direction correct
2. Drupal field exists on bundle
3. Salesforce field exists on object
4. Field types compatible
5. Required fields populated

**Debug:**
- Event: `PUSH_PARAMS` - Examine params before API call
- Event: `PULL_ENTITY_VALUE` - Examine values during pull
- Object describe: Check field metadata via `objectDescribe()`

## API Limits

**Monitor:**
- Service: `salesforce.client`
- Method: `getApiUsage()`
- Header: `Sforce-Limit-Info` in API responses

**Optimization:**
- Reduce pull frequency
- Lower global/mapping limits
- Use selective WHERE clauses
- Batch operations during off-peak

```php
$client = \Drupal::service('salesforce.client');
$usage = $client->getApiUsage(); // Returns usage from Sforce-Limit-Info header
```

## Queue Stuck/Growing

**Diagnose:**
- Check queue size: `drush queue:list`
- Check failed items: Query `salesforce_push_queue` with `fails > 0`
- Check cron running: `drush core:cron`
- Check processor: Default `rest` plugin available

**Resolution:**
- Increase limits: `global_push_limit`, `push_limit`
- Fix mapping errors causing failures
- Clear failed items: Custom query to delete permanent failures
- Process manually: `drush sfpush` / `drush sfpull`

```bash
drush queue:list                    # Check salesforce_push queue size
drush core:cron                     # Trigger manual cron
drush sfpushq                       # Manually process push queue
drush sfpq                          # Manually process pull queue
```

## Common Mistakes

- **Wrong**: Debugging push failures without enabling `salesforce_logger` → **Right**: Enable `salesforce_logger` first; it captures all sync errors to dblog
- **Wrong**: Assuming pull is broken when it's just throttled by `pull_frequency` → **Right**: Check when the last pull ran; the module tracks timestamps and skips runs within `pull_frequency` seconds
- **Wrong**: Running `drush sfpushq` in production to fix a stuck queue without first diagnosing why items are failing → **Right**: Check `fails > 0` items in `salesforce_push_queue` to understand the error before processing

## See Also

- [Push Synchronization](push-synchronization.md)
- [Pull Synchronization](pull-synchronization.md)
- [Queue Processing](queue-processing.md)
- [Drush Commands](drush-commands.md)
- [Performance](performance.md)
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_logger/`
