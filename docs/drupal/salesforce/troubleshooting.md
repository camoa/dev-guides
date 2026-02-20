---
description: Salesforce troubleshooting — auth failures, push not triggering, pull not creating entities, field mapping issues, stuck queues, API limits
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

## Pattern

**Auth issues checklist:**
1. Auth provider configured: `/admin/config/salesforce`
2. Credentials correct (Consumer Key, Secret, Login URL)
3. Authorization completed (OAuth redirect finished, or JWT key uploaded)
4. Token not expired: check `key_value` table for `salesforce.access_token`

**Push not triggering checklist:**
```
1. Mapping exists for entity type/bundle
2. sync_triggers.push_create or push_update is enabled
3. Queue items exist: SELECT * FROM salesforce_push_queue
4. Cron running: drush core:cron
5. No PUSH_ALLOWED subscriber vetoing: add debug logging temporarily
```

**Pull not creating entities checklist:**
```
1. pull_create trigger enabled in mapping
2. SOQL query returns records (test in Salesforce Developer Console)
3. Pull frequency not throttling: check last pull timestamp
4. WHERE clause not filtering all records
5. Entity validation not failing: check dblog for validation errors
```

**Queue diagnosis:**
```bash
drush queue:list                    # Check salesforce_push queue size
drush core:cron                     # Trigger manual cron
drush sfpushq                       # Manually process push queue
drush sfpq                          # Manually process pull queue
```

**API limit monitoring:**
```php
$client = \Drupal::service('salesforce.client');
$usage = $client->getApiUsage(); // Returns usage from Sforce-Limit-Info header
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
