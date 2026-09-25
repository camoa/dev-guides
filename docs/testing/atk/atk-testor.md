---
description: "Testor, Performant Labs' separate snapshot CLI — install, storage config, the snapshot workflow, and its production-database warning."
tldr: "Testor is a separate Robo CLI (performantlabs/testor), not an ATK or Drush command — install with composer require performantlabs/testor, then testor snapshot:create/list/get/restore/delete. The default snapshot:create --env=@self runs drush sql:sanitize on your LOCAL database before dumping it; run it on a throwaway copy."
drupal_version: "11.x"
---

# ATK Testor Snapshots

## When to Use

> Sharing sanitised database snapshots across developers, QA and preview environments.

## What Testor Is

Testor is a **separate tool**, not part of ATK and not a Drush command set. It is a Robo CLI from Performant Labs (`performantlabs/testor`, source at `github.com/Performant-Labs/testor`). It:

- Stores database and file snapshots on S3-compatible or SFTP storage
- Runs a sanitise command while creating a snapshot
- Defaults to Drupal commands, but any SQL tool works
- Can create Tugboat previews and point ATK's config files at them

ATK's README links it at `github.com/performantlabs/testor`, which returns 404.

## Pattern: install

```bash
composer require performantlabs/testor
vendor/bin/testor self:init
# under DDEV
ddev composer require performantlabs/testor
ddev exec testor self:init
```

`self:init` writes `.testor.yml` (commit it) and `.testor_secret.yml` (keep it local). It appends the secret file to `.gitignore`, but only if `.gitignore` already exists. Under DDEV it also creates a `ddev testor` command.

## Pattern: storage config

The generated `.testor.yml`, trimmed:

```yaml
pantheon:
  site: '[your Pantheon site name]'
sql:
  command: '$(drush sql:connect)'
sqldump:
  command: 'drush sql:dump'
sanitize:
  command: 'drush sql:sanitize'
storage: '[s3|sftp]'
s3:
  config:
    version: 'latest'
    region: ''
    endpoint: '[cluster URL]'
    credentials:
      key: '[access key]'
      secret: '${s3_secret}'
  bucket: '[bucket name]'
sftp:
  host: '[host]'
  user: 'sftpuser'
  key: '/path/to/private/key'
  password: ''
  root: 'sftp/upload'
```

`${name}` resolves from `.testor_secret.yml` or the environment.

## Pattern: workflow

```bash
# Create a sanitised snapshot under the name "qa" and upload it
testor snapshot:create --name=qa --put

# List snapshots
testor snapshot:list --name=qa

# Download the latest "qa" snapshot and import it
testor snapshot:get --name=qa --import

# Or restore in one step (download, import; normalises the site UUID only if --uuid or uuid.value is set)
testor snapshot:restore --name=qa

# Pick an exact snapshot by the name snapshot:list shows
testor snapshot:restore --name=qa --snapshot=<name>

# Delete snapshots by name or prefix (prompts unless -y; use -y in CI)
testor snapshot:delete --name=qa -y
```

`snapshot:create` sanitises when `sanitize.command` is set. `--do-not-sanitize` skips it. `--name` works like a folder, for example `developer` or `preview`.

> **Warning: sanitising changes your local database.** With the default `--env=@self`, `snapshot:create` runs `sanitize.command` (`drush sql:sanitize`) on the **local** database before dumping it. With another Drush alias, it first syncs that database into the local one. Run it on a throwaway copy, not on a developer's working database.

## Decision

| Workflow | Snapshot names |
|---|---|
| Solo developer | One name, for example `developer` |
| Developers + QA | `developer`, `qa` |
| Preview environments | Add `preview`; use `testor preview:create --set` for Tugboat |

## Pattern: integration with CI

```yaml
- name: Restore QA snapshot
  run: ddev exec testor snapshot:restore --name=qa
```

Supply the secret through `.testor_secret.yml` written from a CI secret, or through an environment variable that `${...}` reads.

## Common Mistakes

- **Running `drush testor:*`** — Testor never appears in `drush list`; the binary is `testor`
- **Removing `sanitize.command`** — snapshots then upload unsanitised
- **Committing `.testor_secret.yml`** — `self:init` ignores it in Git for a reason
- **No retention policy** — prune with `snapshot:delete`, or set bucket lifecycle rules

## See Also

- [CI Integration](atk-ci-integration.md)
- [ATK Overview](atk-overview.md)
- Reference: https://github.com/Performant-Labs/testor
