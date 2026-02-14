---
description: Export config from active storage to sync directory and import config from sync to active using Drush commands.
---

# Config Import/Export (Drush)

## When to Use

When you need to export config from active storage to sync directory, or import config from sync directory to active storage using Drush commands.

## Core Drush Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `drush cex` | Export all active config to sync | After making config changes locally |
| `drush cim` | Import all sync config to active | After pulling config changes from Git |
| `drush config:status` | Show differences between active and sync | Before import to review changes |
| `drush config:diff NAME` | Show diff for specific config | Debugging config changes |
| `drush config:export NAME` | Export single config item | Selective export |
| `drush config:import NAME` | Import single config item | Selective import |
| `drush config:inspect NAME` | Show config structure and schema | Debugging schema issues |

## Example: Export Workflow

```bash
# Export all config to sync directory
drush cex -y

# Export without confirmation prompt
drush config:export --yes

# Export to custom directory
drush config:export --destination=/tmp/config

# Export single config item
drush config:export system.site

# Export and show differences
drush config:export --diff
```

## Example: Import Workflow

```bash
# Check what will be imported
drush config:status

# Show diff for specific config
drush config:diff views.view.frontpage

# Import all config
drush cim -y

# Import single config item
drush config:import views.view.frontpage

# Import and skip modules/themes
drush cim --partial

# Import with dry-run (show changes without importing)
drush config:import --preview=list
```

**Reference:** Drush commands defined in `/core/modules/config/src/Commands/ConfigCommands.php`

## Config Status Output

```bash
$ drush config:status
# Output format:
# State      Name                       Label
# Changed    system.site                Site information
# Removed    views.view.archive         Archive view
# New        block.block.custom_block   Custom block
```

**State meanings:**
- `Changed` — Exists in both, values differ
- `New` — Exists in sync, not in active (will be created)
- `Removed` — Exists in active, not in sync (will be deleted)
- `Identical` — No changes (not shown by default)

## Import/Export Options

**Export Options:**
- `--yes` / `-y` — Skip confirmation
- `--destination=DIR` — Export to custom directory
- `--diff` — Show diff before exporting
- `--include-modules` — Include enabled modules list

**Import Options:**
- `--yes` / `-y` — Skip confirmation
- `--partial` — Import config without enabling/disabling modules
- `--preview=list` — Dry-run, show what would change
- `--source=DIR` — Import from custom directory
- `--diff` — Show diff before importing

## Common Mistakes

- Running `drush cex` in production — Exports production-specific config to Git
- Not using `-y` flag in scripts — Import/export hangs waiting for confirmation
- Importing without checking status first — Blind import, don't know what changes
- Using `--partial` incorrectly — Skips module enable/disable, causes dependency errors
- Not clearing cache after import — Old cached config active
- Exporting with active overrides — Overridden values exported instead of stored values

## See Also

- [Config Synchronization](config-synchronization.md) — sync workflow
- [Config Split](config-split.md) — splitting config by environment
- [Deployment Workflows](deployment-workflows.md) — deployment patterns
- Reference: [Drush Config Commands](https://www.drush.org/latest/commands/config_export/)
