---
description: Salesforce queue processing — cron vs standalone endpoints, configuration, scheduling decisions
drupal_version: "11.x"
---

# Queue Processing

## When to Use

> Use cron-based processing for standard setups. Use standalone endpoints when you need higher-frequency processing, custom scheduling (Jenkins, external cron), or separation from Drupal's cron run.

## Decision

| Approach | Use When |
|---|---|
| Cron-based processing | Standard setup, manageable volume |
| Standalone push endpoint | Custom scheduling, high-frequency push |
| Standalone pull endpoint | Custom scheduling, high-frequency pull |
| Per-mapping standalone flag | Mix of cron and standalone for different mappings |

## Pattern

**Cron processing limits:**
```
Push: salesforce.settings:global_push_limit (default 10,000/run)
      Per-mapping: salesforce_mapping.[id]:push_limit
      Failed retry: salesforce_mapping.[id]:push_retries

Pull: Populated by pull_frequency and pull_trigger_date
      Max queue: salesforce.settings:pull_max_queue_size
```

**Standalone endpoint configuration:**
```yaml
# Global (salesforce.settings.yml)
standalone: true

# Per-mapping
push_standalone: true
pull_standalone: true
```

**Standalone endpoint URLs:**
- Push: `/salesforce/push/process-standalone`
- Pull: `/salesforce/pull/process-standalone`

**External scheduler setup:**
1. Enable `standalone: true` in `salesforce.settings.yml`
2. Enable `push_standalone` or `pull_standalone` per mapping
3. Configure external scheduler (Jenkins, system cron, etc.)
4. Schedule HTTP requests to the standalone endpoint URLs

## Common Mistakes

- **Wrong**: Enabling standalone mode globally without also setting per-mapping standalone flags → **Right**: Global standalone enables the endpoints; per-mapping flags control which mappings use them
- **Wrong**: Not monitoring `salesforce_push_queue` for items where `fails > 0` → **Right**: Set up monitoring or periodic `drush queue:list` checks; failed items will not retry beyond `push_retries`

## See Also

- [Push Synchronization](push-synchronization.md)
- [Pull Synchronization](pull-synchronization.md)
- [Configuration Management](configuration-management.md)
- [Performance](performance.md)
- [Drush Commands](drush-commands.md)
