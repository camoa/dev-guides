---
description: "Salesforce queue processing — cron vs standalone endpoints, configuration, scheduling decisions"
tldr: "Use cron-based processing for standard setups. Use standalone endpoints when you need higher-frequency processing, custom scheduling (Jenkins, external cron), or separation from Drupal's cron run."
drupal_version: "11.x"
---

# Queue Processing

## When to Use

> Use cron-based processing for standard setups. Use standalone endpoints when you need higher-frequency processing, custom scheduling (Jenkins, external cron), or separation from Drupal's cron run.

## Decision: Cron vs Standalone

| Approach | Use When |
|---|---|
| Cron-based processing | Standard setup, manageable volume |
| Standalone push endpoint | Custom scheduling, high-frequency push |
| Standalone pull endpoint | Custom scheduling, high-frequency pull |
| Per-mapping standalone flag | Mix of cron and standalone for different mappings |

**Decision Point - Cron vs Standalone:**
- Cron: Simple setup, standard Drupal workflow
- Standalone: Custom scheduling, higher frequency, separate from site cron

## Cron-Based Processing

**Push Queue:**
- Processes during cron run
- Global limit: `salesforce.settings:global_push_limit`
- Per-mapping limit: `salesforce_mapping.[id]:push_limit`
- Failed items retry up to `push_retries` times

**Pull Queue:**
- Populates during cron based on `pull_frequency` and `pull_trigger_date`
- Processes via standard Drupal queue workers
- Max queue size: `salesforce.settings:pull_max_queue_size`

```
Push: salesforce.settings:global_push_limit (default 10,000/run)
      Per-mapping: salesforce_mapping.[id]:push_limit
      Failed retry: salesforce_mapping.[id]:push_retries

Pull: Populated by pull_frequency and pull_trigger_date
      Max queue: salesforce.settings:pull_max_queue_size
```

## Standalone Queue Processing

**Configuration:**
- Global: `salesforce.settings:standalone = TRUE`
- Per-mapping push: `salesforce_mapping.[id]:push_standalone = TRUE`
- Per-mapping pull: `salesforce_mapping.[id]:pull_standalone = TRUE`

**Endpoints:**
- Push: `/salesforce/push/process-standalone`
- Pull: `/salesforce/pull/process-standalone`

**Standalone Setup:**
1. Enable standalone mode in config
2. Configure external scheduler (Jenkins, cron job, etc.)
3. HTTP request to standalone endpoint
4. Optional: Pass parameters for specific mappings/limits

```yaml
# Global (salesforce.settings.yml)
standalone: true

# Per-mapping
push_standalone: true
pull_standalone: true
```

## Common Mistakes

- **Wrong**: Enabling standalone mode globally without also setting per-mapping standalone flags → **Right**: Global standalone enables the endpoints; per-mapping flags control which mappings use them
- **Wrong**: Not monitoring `salesforce_push_queue` for items where `fails > 0` → **Right**: Set up monitoring or periodic `drush queue:list` checks; failed items will not retry beyond `push_retries`

## See Also

- [Push Synchronization](push-synchronization.md)
- [Pull Synchronization](pull-synchronization.md)
- [Configuration Management](configuration-management.md)
- [Performance](performance.md)
- [Drush Commands](drush-commands.md)
