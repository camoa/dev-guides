---
description: "Choose hook_update_N(), hook_post_update_NAME(), or hook_deploy_NAME() for a schema, data, or post-import change, and export what an update hook wrote to config."
tldr: "Use this when a module release must change the schema, stored data or configuration of sites that already run it. Pick one of three update functions; the choice decides whether the change runs before or after config:import."
drupal_version: "11.x"
---

# Update Functions (hook_update_N, post_update, deploy hooks)

## When to Use

Use this when a module release must change the schema, stored data or configuration of sites that already run it. Pick one of three update functions; the choice decides whether the change runs before or after `config:import`.

## The Three Kinds

| Function | File | Provided by | Runs in | Purpose |
|---|---|---|---|---|
| `hook_update_N()` | `{module}.install` | Drupal core | `drush updatedb`, first | Low-level changes: database schema, entity definitions, raw config |
| `hook_post_update_NAME()` | `{extension}.post_update.php` | Drupal core | `drush updatedb`, after every `hook_update_N()` | Data changes that need the full API: entities, config entities |
| `hook_deploy_NAME()` | `{module}.deploy.php` | Drush | `drush deploy:hook`, after `config:import` | One-off changes that must see the imported configuration |

**Naming and tracking:**
- `hook_update_N()` — `{module}_update_{N}`. N is a sequential integer: core major, module major, then a two-digit counter, such as `mymodule_update_10101()`. Core stores the last N run as the module's schema version. Never renumber one.
- `hook_post_update_NAME()` — `{extension}_post_update_{name}`. Functions run in alphabetical order of name. Add a numeric prefix when order matters. Core records each name it ran in key-value collection `post_update`.
- `hook_deploy_NAME()` — `{module}_deploy_{name}`. Also alphabetical, and recorded in key-value collection `deploy_hook`. Drush loads `.deploy.php` from modules and profiles, not themes.

**On module install:**
- No `hook_update_N()` runs. Core sets the schema version to the highest N present, or to `hook_update_last_removed()` if higher.
- No `hook_post_update_NAME()` runs. Core marks every one present, and every name in `hook_removed_post_updates()`, as already run. Use `hook_install()` for install-time work.
- Nothing marks deploy hooks as run. A newly installed module's deploy hooks run at the next `drush deploy:hook`. `drush deploy:mark-complete` skips all pending ones.

All three must stay procedural functions. A `#[Hook]` attribute on `update_N` or `post_update_*` throws a `LogicException` when the container builds. Drush finds deploy hooks by function name in `.deploy.php`, so a class method is never called.

## Execution Order

```
drush updatedb      → every pending hook_update_N() (ascending N per module; hook_update_dependencies() orders across modules)
                    → cache and container rebuild (only if both kinds ran)
                    → every pending hook_post_update_NAME()
drush deploy        → updatedb → config:import → cache:rebuild → deploy:hook
                      (→ cache:warm on core 11.2 and later)
```

`hook_update_N()` and `hook_post_update_NAME()` run **before** the import. `hook_deploy_NAME()` runs **after** it.

**Reference:** Drush `src/Commands/core/DeployCommands.php`, `UpdateDBCommands.php` (`updateBatch()`), `DeployHookCommands.php`; core `core/lib/Drupal/Core/Update/UpdateRegistry.php`

## Decision

| If the change... | Use... | Why |
|---|---|---|
| Alters a table, a field storage or an entity type definition | `hook_update_N()` | Runs first, before any API that reads the new schema |
| Rewrites simple config to match a new schema | `hook_update_N()` | `getEditable()` with `save(TRUE)` is safe here |
| Loads or saves entities or config entities | `hook_post_update_NAME()` | Full bootstrap; entity CRUD in `hook_update_N()` is never safe |
| Resaves config entities to add a new key or dependency | `hook_post_update_NAME()` with `ConfigEntityUpdater` | Batches over every entity of the type |
| Creates site content or config that must exist after this release's import | `hook_deploy_NAME()` | Sees the imported configuration; a site project, not a contrib module |

Recommendation: a contrib module ships `hook_update_N()` and `hook_post_update_NAME()` only. Only Drush runs deploy hooks; `update.php` never does. Keep them in a site's custom code.

## Pattern

```php
// mymodule.install — schema; no entity API.
function mymodule_update_10101(): void {
  \Drupal::configFactory()->getEditable('mymodule.settings')
    ->set('limit', 10)->save(TRUE);
}

// mymodule.post_update.php — full API.
function mymodule_post_update_resave_examples(array &$sandbox): void {
  \Drupal::classResolver(\Drupal\Core\Config\Entity\ConfigEntityUpdater::class)
    ->update($sandbox, 'mymodule_example');
}

// mymodule.deploy.php — after config:import (Drush).
function mymodule_deploy_create_home_menu_link(array &$sandbox): string { ... }
```

**Reference:** `core/lib/Drupal/Core/Extension/module.api.php` (`hook_update_N`, `hook_post_update_NAME`), Drush `drush.api.php` (`hook_deploy_NAME`)

## Why Their Config Changes Must Be Exported

An update function that changes configuration changes **active** config only. The sync directory still holds the old values. Production runs `drush deploy`, so `config:import` follows `updatedb` and restores the old export over the change. A key the update removed comes back.

So, on the development site, after new code arrives:

1. `drush updatedb` — runs the update and post-update functions.
2. `drush config:export` — writes their changes to the sync directory.
3. Commit the export with the code.

Never run `drush config:import` between steps 1 and 2. It overwrites the update's changes, and a later `updatedb` does not repeat them. Drupal core issue [#3110362](https://www.drupal.org/project/drupal/issues/3110362), "If an update hook modifies configuration, then old configuration is imported, the changes made by the update hook are forever lost", is still active.

**The inverse, for deploy hooks:** a deploy hook runs after the import. Config it writes on production is not in the export. The next deploy's import removes or reverts it. Run `drush deploy:hook` on the development site too, then export and commit what it wrote.

## Checking What Is Pending

| Command | Pending | Nothing pending | Exit code |
|---|---|---|---|
| `drush updatedb:status` | Table on stdout | Nothing on stdout; "No database updates required." on stderr | 0 either way |
| `drush deploy:hook-status` | Table on stdout | Table headers only on stdout | 0 either way |
| `drush deploy:hook-status --format=tsv` | One line per hook on stdout | Nothing on stdout | 0 either way |

Neither status command fails when work is pending. A script must read stdout, not the exit code.

**Reference:** Drush `UpdateDBCommands::updatedbStatus()` returns `null` when nothing is pending; `DeployHookCommands::status()` returns an empty `RowsOfFields`. consolidation/output-formatters `TsvFormatter` prints no header row by default.

## Removing Old Update Functions

- Removing `hook_update_N()` functions → implement `hook_update_last_removed()` in `.install`, returning the highest removed N. A site whose schema version is lower gets an "Unsupported schema version" requirements error and cannot update.
- Removing `hook_post_update_NAME()` functions → list them in `hook_removed_post_updates()` in `.post_update.php`, mapping each name to the first version without it. A site that never ran one gets a "Missing updates" requirements error. A function still present and listed as removed throws `RemovedPostUpdateNameException`.

**Reference:** `core/modules/system/src/Hook/SystemRequirementsHooks.php` (update phase), `core/includes/update.inc`

## Common Mistakes

- Running `drush cim` before `drush cex` after an update → the update's config changes are lost for good; export first
- Loading or saving entities in `hook_update_N()` → hooks and services may not match the schema yet; use `hook_post_update_NAME()`
- Calling `hook_schema()` or current config schema from an update → the update may run years later; copy the schema into the function and save with `save(TRUE)`
- Renumbering or reusing an update number → the stored schema version skips or repeats it; always add a higher N
- Writing config in a deploy hook only on production → the next import reverts it; run the hook in development and export
- Treating `updatedb:status` exit 0 as "nothing pending" → it exits 0 either way; read stdout
- Relying on alphabetical order by accident in post-update or deploy names → prefix names with numbers when order matters
- Putting update functions in a `#[Hook]` class → the container build throws; keep them procedural

## See Also

- [Deployment Workflows](deployment-workflows.md) — the export, commit and import cycle
- [Config Installer](config-installer.md) — default config is installed on module install only, never on update
- [Config Import/Export](config-import-export.md) — `config:export` and `config:status`
- [Hooks That Must Stay Procedural](../hooks/procedural-only-hooks.md) — `hook_update_N()`, `hook_post_update_NAME()` and their removal hooks
- [Drupal Dependency Update (agentic recipe)](../../agentic-recipes/drupal/dependency-update.md) — the full update sequence that uses these rules
- Reference: [hook_update_N() API](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Extension!module.api.php/function/hook_update_N)
- Reference: [hook_post_update_NAME() API](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Extension!module.api.php/function/hook_post_update_NAME)
- Reference: [Drush deploy command](https://www.drush.org/13.x/deploycommand/)
