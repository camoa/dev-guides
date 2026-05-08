---
description: ATK Testor — Drush-based sanitised database snapshot management with S3/SFTP storage and per-category targeting.
tldr: Testor is ATK's Drush command set for pushing and pulling sanitised DB snapshots to S3-compatible or SFTP storage, categorised by audience (dev, qa, tugboat-base). Always use --sanitize when pushing; store access keys in env vars or CI secrets, never in YAML.
drupal_version: "11.x"
---

# ATK Testor Snapshots

## When to Use

> Use Testor when you need to share sanitised database snapshots across team members and environments, or reset a test environment to a known state in CI.

## Decision

| Workflow | Categories |
|---|---|
| Solo dev | `dev` only |
| Dev + QA team | `dev`, `qa` |
| Dev + QA + preview environments | `dev`, `qa`, `tugboat-base`, `staging` |
| Anonymous public dataset | `demo` |

## Pattern

### Storage config — S3-compatible

```yaml
# config/automated_testing_kit.testor.yml
storage:
  type: s3
  endpoint: https://s3.us-west-2.amazonaws.com
  bucket: my-team-snapshots
  region: us-west-2
  access_key_id_env: AWS_ACCESS_KEY_ID
  secret_access_key_env: AWS_SECRET_ACCESS_KEY

categories:
  - dev
  - qa
  - tugboat-base
```

### Storage config — SFTP

```yaml
storage:
  type: sftp
  host: snapshots.example.com
  port: 22
  user: testor
  key_path: ~/.ssh/testor_key
  base_path: /home/testor/snapshots
```

### Workflow commands

```bash
# Pull latest dev snapshot
drush testor:pull dev

# Create a sanitized snapshot of current DB and push under "qa" category
drush testor:snapshot --sanitize
drush testor:push qa

# List available snapshots
drush testor:list
drush testor:list --category=qa
```

Verify exact subcommand spelling against `drush list | grep atk` — the interface has evolved and some teams remember `teststore:*` prefixes from earlier versions.

### Integration with CI

```yaml
# In a GitHub Actions step before tests run
- name: Pull QA snapshot
  run: ddev drush testor:pull qa
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.TESTOR_KEY }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.TESTOR_SECRET }}
```

## Common Mistakes

- **Wrong**: Pushing un-sanitised snapshots → **Right**: always use `--sanitize`; leaks PII otherwise
- **Wrong**: Storing access keys in `.testor.yml` → **Right**: use env vars or CI secrets
- **Wrong**: No retention policy → **Right**: snapshot bucket grows forever; configure lifecycle rules

## See Also

- [CI Integration](atk-ci-integration.md)
- [Helper Functions](atk-helper-functions.md) — `testorPull()`, `testorPush()`, `testorReset()` helpers
- Reference: `src/Commands/TestorCommands.php` in the module
