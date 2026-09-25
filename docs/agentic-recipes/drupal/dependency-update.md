---
# Routing block — an orchestrator reads to here and decides.
name: drupal_dependency_update
capability: drupal-dependency-update
description: Use when a Drupal site must update its Composer dependencies — named contrib modules, themes or libraries, the whole site within its constraints, or core along a version path across minors and majors — and carry each update through database updates and a configuration export to a stable point, with nothing pending and every moved package reported.
# Metadata — read only after a match.
label: Drupal dependency update
recipe_schema_version: 1.0.0
version: 0.1.2
# Machine-readable dependency declaration (recipe-loader resolves these without parsing prose).
requires_guides:
  - drupal/config-management/deployment-workflows
  - drupal/config-management/config-import-export
  - drupal/config-management/config-installer
  - drupal/config-management/update-functions
  - drupal/github-actions/multi-environment-deployment
  - drupal/github-actions/code-quality-checks
  - drupal/security/owasp-top-10-in-drupal
  - drupal/composer/composer-update-vs-require
  - drupal/composer/composer-dependency-flags
  - drupal/composer/composer-patches
  - drupal/composer/composer-audit
  - drupal/composer/composer-conflicts
drupal_compatibility: "^8.8 || ^9 || ^10 || ^11 || ^12"
assumes:
  - composer
  - ddev
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Take one of three kinds of update to a stable point on the development site. The kinds are named packages, the whole site, and one step of a core version path. At the stable point the lock file holds the new versions and the database has run every update the new code ships. The active configuration equals the export, and both are committed. No unaccepted advisory or abandoned package remains, and the report names every package that moved. The recipe owns the order of the steps, the stopping rules and the proof. The guides it cites own the mechanics of each command.

## Opinion

**An update is its own change.** We run it as a hot-fix cycle, on a branch that carries nothing else. We refuse to fold it into feature work, because a failure then has one cause. The recipe cannot read a branch's purpose. The report names the branch, and the commit holds only the update.

**Composer changes code, and nothing else.** The database stays untouched until `updatedb` runs. Git is the way back for every file a run changes, tracked and untracked; `composer install` then brings `vendor/` back to the restored lock. The snapshot is the way back for the database.

**Named packages move with their dependencies.** We run `composer update <names…> --with-all-dependencies`, in the long form drupal.org writes. `--with-dependencies` leaves a dependency that is also a root requirement in place, and the update often fails to resolve. A new root constraint, such as a module's major move, is `composer require <name>:<constraint> --with-all-dependencies`.

**A whole-site update is allowed, and nothing moves unnoticed.** A bare `composer update` moves every package the root constraints allow. That is routine maintenance, so we run it. The report lists every package that moved, old version to new, from the lock file before and after.

**Core travels in time.** A major is always crossed the same way. From the latest release of the current major, the site moves to a release of the next major published on the same date. When several minors of the next major have a release on that date, we take the lowest. Inside a major, the site goes straight to the latest release. Projects with very complex custom code step one minor at a time instead, and the input switches that on. Each move is a full cycle that ends at a stable point.

**One step of a core path per run.** A stable point includes a release to production and a fresh production database for the team. The recipe cannot deploy. So each run takes one step, hands back, and names the next step. The next run starts only when the caller confirms the release.

**A stopping point stops the run.** A custom module, a theme, an update hook, a patch or a resolution failure breaks. We stop, report, and do not continue the path. The one break the recipe may resolve itself is a contrib release that claims a core compatibility it does not have. Sequence step 6 states that pin and its lift condition.

**A stable point is proved, not assumed.** The previous version's database runs `updatedb`, then imports the export, and the site works. The configuration gate of `drupal_implement_standards_and_tests` is that proof, and it runs `updatedb` before `config:import`.

**Held packages are a given.** The input names them. We never edit a held package's constraint, in any kind of update, and we never pin one. When a hold blocks a step, we stop and name the hold and the step. The person decides whether to migrate, patch or remove.

**Database updates run before configuration is touched.** `drush deploy` runs `updatedb`, `config:import`, `cache:rebuild`, then `deploy:hook`. On core 11.2 or later it also runs `cache:warm` after `deploy:hook`. `hook_update_N()` and `hook_post_update_NAME()` run inside `updatedb`, before the import. `hook_deploy_NAME()` runs in `deploy:hook`, after it. See `drupal/config-management/update-functions`.

**On the development site, export after the updates, never import.** An update hook may change or remove active configuration. An import from a stale export restores the old values, and a removed key comes back. The method's author saw that cause 500 errors across a multisite. So the sequence is `updatedb`, then `config:export`, then a commit. Drupal core issue #3110362 is open on this loss.

**Default configuration arrives on install only.** Core applies a module's `config/install/` directory when the module is installed, never on update. A new release that ships new default configuration for an installed module does not deliver it. Code that expects it can fatal. A module's `config/optional/` entry can arrive later, when another extension is installed and meets its dependencies. The report names such configuration, and the person imports it or removes the dependent feature. Guide `drupal/config-management/config-installer` carries the mechanics.

**A known advisory or an abandoned package fails the run.** One the project accepts lives in the project's Composer configuration, with its reason. The recipe never accepts one on its own.

**Test the critical path, not everything.** The caller names the pages and flows that must work. The recipe checks those, after every update.

### What this recipe refuses

- A change to a held package's constraint, and a pin on a held package.
- A hand edit of `composer.lock`.
- `config:import` on the development site between `updatedb` and `config:export`, except inside the configuration gate's proof.
- An export that the updated site's active configuration does not match.
- An advisory or abandoned package ignored without an entry in the input.
- A remote merge-request URL as a patch source. Its content changes when the merge request changes.
- A second step of a core path in the same run, and a step before the previous one is released.
- A core step past `core_target`, and a core step backwards.
- Removing a module in the same change. Removal has its own order across environments, in `drupal/best-practices/camoa/composer-module-removal-order`.

## Preconditions

preconditions:
  - id: site-running
    what: the site's DDEV project is running, so Composer and Drush run in its containers
    check: ddev describe -j
    expect: '"status_desc":"running"'
    owner: worktree-environment
  - id: composer-valid
    what: composer.json is valid and composer.lock is current with it before the update
    check: ddev composer validate --no-check-publish
    owner: operator
  - id: drush-present
    what: the project's Drush runs, so updatedb, config:export and the status commands exist
    check: ddev drush version
    owner: operator

Three conditions do not fit the `check:` and `expect:` form: a clean working tree, no update pending, and no configuration difference. Each command exits 0 either way and answers "none" with empty standard output. Sequence step 1 reads them and stops on any, because a precondition cannot express no output.

The Drush and Composer behaviour this recipe relies on was read in Drush 13.7 and Composer 2.10. A site on an older core runs an older Drush, whose output this recipe does not vouch for.

## Input contract

Generic, source-agnostic, supplied by the caller (adapter skill, human operator, or orchestrator).

```yaml
kind: packages | site | core_path   # which of the three updates this run takes

packages:                      # kind: packages only; one entry per package
  - name: string               # Composer name
    constraint: string         # optional; a new root constraint, for a major move.
                               # Absent means the newest version the current constraint allows.

core_target: string            # kind: core_path only; a major (its latest release)
                               # or an exact core version. No step passes it.
complex_code: boolean          # kind: core_path only; default false. true steps one
                               # minor at a time inside a major
released_core_version: string # kind: core_path only; optional. The core version the
                               # caller confirms reached production, with a fresh
                               # production database pulled. A first run needs none.

path_pins:                     # kind: core_path only; pins this recipe created in an
  - name: string               # earlier step, as that step's report listed them
    version: string            # the exact version pinned
    restore_constraint: string # optional; the root constraint the pin replaced.
                               # Absent when the package was not a root requirement.
    pinned_for: string         # the UTC date of the core release the pin matched

held:                          # packages the project holds; never edited, any kind
  - name: string
    constraint: string         # the root constraint as it stands
    reason: string             # optional
    lift_when: string          # optional

accepted_advisories:           # advisories the project accepts
  - id: string                 # advisory ID or CVE ID
    reason: string

accepted_abandoned:            # abandoned packages the project accepts
  - name: string               # Composer name
    reason: string

critical_paths:                # pages and flows that must work after the update
  - string
```

## Sequence

If invoked in dry-run mode, run steps 1 to 3 and write nothing. For named packages and the whole site, step 3's `--dry-run` is the command that would run, and it writes neither Composer file. For a core path, the dry run prints the whole path. Its preview covers core and its dependencies only. It does not preview the contrib moves of the bare update, nor the pin lifts. Dry-run is required.

1. **Read the starting state.** Run `git status --porcelain --untracked-files=all`, `ddev drush updatedb:status` and `ddev drush config:status`. Any one printing to standard output stops the recipe. Report which, and do not fix it here. Then record `ddev composer show --locked --format=json` as the before state.
   - For a core path, run `git log --format=%s`. Compare each line, whole, with `Drupal core path step: <locked core version>`. An equal line means a run of this recipe committed the site's release. When that release differs from `released_core_version`, stop. Say the step awaits its release, or its gate failed, and point to that run's report. The rule is the same when an earlier path committed the release: the caller confirms it in `released_core_version`. The match needs the step commit's subject to reach the main branch unchanged. A squash merge that rewrites it, for example by appending a pull-request number, defeats this check.

2. **Check the foundation.** Report each finding. For a core path, the findings marked *blocks* stop the run; for the other kinds, all are reported only.
   - **Constraints.** List each root constraint narrower than a caret or tilde range, such as an exact version. List the ones not in `held` or `path_pins` as hold candidates, without a reason. A drupal/core-* constraint equal to the locked core version, when `git log --format=%s` holds that version's path-step subject, is path-written, whatever the kind: list it as that, not as a hold candidate.
   - **Project shape.** The project requires drupal/core-recommended and drupal/core-composer-scaffold. The older drupal-project or bare-core shape *blocks* a core path.
   - **Patches.** List each patch with its source, its date and its reason. Name the patch plugin's major version and whether a failed patch stops Composer. A remote merge-request URL is a finding; the fix is a local copy with its source recorded.
   - **PHP.** Report the version from `ddev drush status --field=php-version`. Composer refuses a core release whose PHP requirement it does not meet.
   - **Major moves.** A core step that crosses a major needs an Upgrade Status report from the current site. Use the latest stable Upgrade Status line that supports the site's current major. A move to Drupal 12 needs the line that supports 12, 5.0.x, which is alpha as of 2026-09-24. A missing report *blocks* the step.
   - **Custom code.** For a core step, inventory the core and contrib APIs each custom module and theme uses. Read them against the change records for the versions the step crosses. An API change can break custom code with no error.

3. **Plan the change.** Refuse a `packages` entry that names a held package with a new `constraint`. A core path stops when any drupal/core-* root requirement is held, and reports the hold.
   - **Named packages.** One `composer update` for every entry without `constraint`, all names in one command. One `composer require` for each entry with `constraint`.
   - **Whole site.** One bare `composer update`.

   Run each planned command with `--dry-run` added. When every one prints `Nothing to modify in lock file` on standard error, nothing moves: report that and stop before step 4. The stop does not apply when an entry's `constraint` differs from the current root constraint, because the run must still write it. It never applies to a core step either; the core path has its own test, below.

   - **Core path.** Read `https://updates.drupal.org/release-history/drupal/current`. Take published releases only, with no alpha, beta, rc or dev suffix. Group them by major, then by minor. Never sort the whole feed by date and pick neighbours. A release's date is the UTC calendar date of its `<date>` timestamp. The path runs from the locked core release to `core_target`, and each step is the next release this list names:
     1. **Inside a major, `complex_code` false:** the latest release of the major.
     2. **Inside a major, `complex_code` true:** the latest release of the current minor. From there, the release of the next minor of the same major published on the same date. Then the latest release of that minor, and so on to the major's latest release.
     3. **Crossing a major, whatever `complex_code` says:** from the latest release of the current major, the release of the next major published on the same date. When several minors have one, take the lowest minor.

     A `core_target` below the locked release stops the recipe: it never moves core backwards. A date with no matching release stops the recipe, with the nearest releases on each side. No step passes `core_target`. Inside a major, a step that would pass it becomes `core_target`. A crossing whose same-date release is newer than `core_target` stops the recipe: the target predates the date-matched release, and the person decides. Drupal 11 requires Drupal 10.3.0 or later, and rule 1 or 2 reaches that before rule 3 runs. This run takes the first step. The locked release equal to `core_target` means nothing to do: report that and stop before step 4.

     An intermediate step writes the exact version on each drupal/core-* root requirement. The last step writes `^<major>` for a major target, or the exact version for an exact one, and the report says so. A `path_pins` entry whose `pinned_for` date is earlier than the step release's date is lifted. Lifting writes its `restore_constraint` back, or removes the root requirement the pin added when it has none.

   The preview for a core step, whose output the recipe reports and never uses to stop, is `ddev composer require <each drupal/core-* root requirement>:<constraint> --with-all-dependencies --dry-run`.

4. **Keep the database.** Run `ddev snapshot --name pre-update-{project}-{stamp} --yes`, then `ddev snapshot restore pre-update-{project}-{stamp}`. `{project}` is the DDEV project's name, the `name` in `ddev describe -j`. In a worktree it is the same value as the `project:` line `drupal_worktree_environment` printed. `{stamp}` is the run's start time in UTC, digits only, because DDEV refuses a name that exists. DDEV prints `Failed to snapshot` and exits 0 when the snapshot itself fails. The restore changes nothing, and fails with `not found` when nothing was kept.

5. **Update the code.** Run the planned command in `ddev composer`. For a core step, write the constraints first with `--no-update`, then run a bare `ddev composer update`:
   - `ddev composer require <each drupal/core-* root requirement>:<constraint> --no-update`, with `--dev` for one in require-dev;
   - for each lifted pin, `ddev composer require <name>:<restore_constraint> --no-update`, or `ddev composer remove <name> --no-update` when it has no `restore_constraint`.

   Read the whole output:
   - A resolution failure is a stopping point. The talk "From Fear to Freedom" places the real conflict in the first or last few lines. Quote them and name the culprit package. The person fixes one conflict at a time. See `drupal/composer/composer-conflicts`.
   - A held package that blocks the resolution, or whose release does not support the step's core, is a stopping point. Name the hold and the step.
   - cweagans/composer-patches 1.x prints `Could not apply patch! Skipping.` and continues, exiting 0 unless `extra.composer-exit-on-patch-failure` or the `COMPOSER_EXIT_ON_PATCH_FAILURE` environment variable is true. That line is a stopping point. Version 2.x throws on a failed patch and the command's non-zero exit is the stopping point instead.

6. **Run the database updates.** Run `ddev drush updatedb --yes`. A non-zero exit is a stopping point.
   - **The one forced pin.** In a core step, a contrib release dated after the step's core release may claim compatibility it does not have, and break. The recipe may resolve that break only when the error names that module's code, and never for a held package. Restore the step 4 snapshot. Read the module's feed, `https://updates.drupal.org/release-history/<project>/current`. Take its release dated closest to the step's core release, not after it, whose `<core_compatibility>` includes the step's core. Run `ddev composer require <name>:<that version> --with-all-dependencies`. Record the pin: its version, the root constraint it replaced or none, its reason, and its lift condition, core passing that date. Rerun from this step. A second break stops the recipe.

7. **Run the deploy hooks.** Run `ddev drush deploy:hook --yes`. A non-zero exit is a stopping point.

8. **Export the configuration.** Run `ddev drush config:export --yes`. Read the sync directory's diff. Name each changed file and its source: an update hook, a deploy hook, or a new default. Name new default configuration a release ships for an already-installed module; the export does not carry it.

9. **Test the critical path.** Run `ddev drush status --field=bootstrap` and check each `critical_paths` entry on the served site. A failure is a stopping point.

10. **Audit and validate.** Run `ddev composer audit --locked` and `ddev composer validate --no-check-publish`. An advisory not in `accepted_advisories` is a stopping point. An abandoned package not in `accepted_abandoned` is a stopping point. An accepted one goes in the project's Composer configuration, with its reason:
    - an advisory: `policy.advisories.ignore-id` from Composer 2.10, `audit.ignore` before it;
    - an abandoned package: `policy.abandoned.ignore` from Composer 2.10, `audit.ignore-abandoned` before it.

    After that write, run both commands again; both must exit 0. The write leaves the lock file current, because Composer's content hash reads no `config` key but `platform`.

11. **Commit.** Commit every change the run made, tracked and untracked, in one commit. Step 1 proved the tree clean, so every change is the update's. The scaffold plugin runs after each `composer update`. It may rewrite scaffold files such as `.htaccess`, `robots.txt` and `default.settings.php`, and update `.gitignore` files. A core step's commit subject is `Drupal core path step: <version>`, which step 1 of the next run reads. Guide `drupal/config-management/deployment-workflows` carries the export and commit workflow.

12. **Prove the stable point.** The gate runs only where `drupal_worktree_environment` brought the site up. There, run the `## Configuration gate` of `drupal_implement_standards_and_tests`, then its put-back line. Each gate line must exit 0; a non-zero line is a stopping point, and the report says so. The gate restores the worktree's seed, the main checkout's database at bring-up. That seed is the previous version's database while the main checkout has not taken this update. Elsewhere, the gate's first line fails, so do not run it. The report says the stable point is unproved, and names the step 4 snapshot as the previous version's database.

13. **Report and hand back.** The report carries:
    - the branch, and every package that moved, old version to new, from the before state and `ddev composer show --locked --format=json` now;
    - every committed file outside `composer.json`, `composer.lock`, the sync directory and patch files, such as scaffold files and `.gitignore` files;
    - the core version, old and new;
    - each held package: its constraint before and after, unchanged, and its locked version;
    - the hold candidates, and the foundation findings;
    - the updates `updatedb` ran, the deploy hooks run, and each changed configuration file with its source;
    - each patch applied, and each skipped;
    - the audit result, the snapshot name, and the gate's output or that the stable point is unproved;
    - for a core path: the whole path, this step, the next step, and each pin created or lifted, with its reason and lift condition;
    - at a stopping point: what broke, the output that shows it, and the way back. Git restores every file the run changed, tracked and untracked: Composer files, scaffold and `.gitignore` files, the sync export. `ddev composer install` then brings `vendor/` back to the restored lock. The snapshot restores the database.

    Releasing to production is the person's. The team then pulls the code and a fresh production database. The next core step runs only after that, with this step's version as `released_core_version`. Merge the step commit without squashing, or keep its subject exactly, so step 1 of the next run can match it. A failed gate at step 12 is a stopping point, and its commit stays: the person fixes it, releases, then confirms the version.

## Data flow

```
input:  kind, packages[], core_target, complex_code, released_core_version, supplied by the caller
        path_pins[], held[], accepted_advisories[], accepted_abandoned[],
        critical_paths[]

step 1:  git status, updatedb:status, config:status,   → all empty, or stop; the before state;
         show --locked, git log (core path)              stop on an unreleased committed step
step 2:  composer.json, patches, PHP, Upgrade Status,    → foundation findings; hold candidates
         custom code, change records
step 3:  input + release-history feeds, --dry-run        → the command; for a core path, the path
step 4:  the site's database                             → snapshot pre-update-{project}-{stamp}, proved
step 5:  composer require --no-update, remove, update    → composer.json, composer.lock, vendor/
step 6:  updatedb (+ the one forced pin)                 → schema and data at the new code's level
step 7:  deploy:hook                                     → deploy hooks run
step 8:  config:export                                   → the sync directory, with what the updates changed
step 9:  status, critical_paths[]                        → the critical path works, or stop
step 10: composer audit, composer validate; accepted    → nothing unaccepted; composer.json config;
         entries written; audit and validate again          both pass again
step 11: git commit                                      → every change: Composer, sync, patch, scaffold files
step 12: configuration gate, put-back (worktree only)    → previous database + updatedb + import works
step 13: everything above                                → report; the next step for a core path
```

## State-awareness contract

The recipe reads the starting state before it writes. It stops when an update is pending or the configuration differs. It writes `composer.json`, `composer.lock`, the installed code, patch files, the scaffold files and `.gitignore` files the scaffold plugin writes, the database, the sync directory, one database snapshot and one commit, and nothing else. It never edits or pins a held package. It never imports configuration on the development site outside the gate.

Running it twice on the same input changes nothing the second time. For named packages and the whole site, step 3's dry run prints `Nothing to modify in lock file` and the run stops before the snapshot. For a core path, step 1 finds the first run's commit for the locked release. That release differs from `released_core_version`, so the run stops. Only a new `released_core_version`, equal to the locked release, lets a run take the next step. At `core_target`, a run stops with nothing to do once the caller confirms that release in `released_core_version`; before that, step 1 stops because the release awaits it.

## Verifier

Each entry is one command, run from the project root after the recipe ran. It is split on spaces and never run through a shell. A non-zero exit fails the entry, whatever `pass` says. `stdout empty` reads standard output only; a non-interactive `ddev drush` keeps Drush's messages on standard error. A stopped DDEV project prints its start-up text on standard output, so start the site before the verify run.

verifier:
  - id: composer-valid
    kind: config-assert
    run: ddev composer validate --no-check-publish
    pass: exit 0
  - id: no-advisory
    kind: config-assert
    run: ddev composer audit --locked
    pass: exit 0
  - id: no-update-pending
    kind: config-assert
    run: ddev drush updatedb:status
    pass: stdout empty
  - id: no-deploy-hook-pending
    kind: config-assert
    run: ddev drush deploy:hook-status --format=tsv
    pass: stdout empty
  - id: active-equals-export
    kind: config-assert
    run: ddev drush config:status
    pass: stdout empty
  - id: site-boots
    kind: config-assert
    run: ddev drush status --field=bootstrap
    pass: stdout contains Successful
  - id: all-committed
    kind: config-assert
    run: git status --porcelain --untracked-files=all
    pass: stdout empty

What the entries do not prove, and where the proof is:

- No single command proves a named package reached the newest version all constraints allow. Composer prints `Nothing to modify in lock file` on standard error, and a `pass` reads standard output only. The report carries each package's old and new version.
- No single command proves a held package stayed inside its constraint. The report carries it: the constraint before and after, and the locked version. `composer-valid` proves the lock file matches that constraint.
- `deploy:hook-status` prints an empty table with headers when nothing is pending. `--format=tsv` prints no header row, and one line per pending hook.
- The stable point is the configuration gate's output, from Sequence step 12, and the critical path from step 9.

## References

### Atomic guides cited

| Guide | Used for |
|---|---|
| `drupal/config-management/deployment-workflows` | Export, commit and import across environments |
| `drupal/config-management/config-import-export` | `config:export` and its `--diff` preview |
| `drupal/config-management/config-installer` | Default configuration is installed with the module, never on update |
| `drupal/config-management/update-functions` | The three kinds of update function, and their order relative to `config:import` |
| `drupal/github-actions/multi-environment-deployment` | `updatedb` before `config:import` on deploy |
| `drupal/github-actions/code-quality-checks` | `composer audit` as a build gate |
| `drupal/security/owasp-top-10-in-drupal` | Applying security updates promptly |
| `drupal/best-practices/camoa/composer-module-removal-order` | Why removal is not this recipe |
| `drupal/composer/composer-update-vs-require` | `update` against `require`, for named packages, the whole site, and a major move |
| `drupal/composer/composer-dependency-flags` | `--with-all-dependencies` against `--with-dependencies`, and `--dry-run` |
| `drupal/composer/composer-patches` | The patch plugin's major version, and whether a failed patch stops Composer |
| `drupal/composer/composer-audit` | `composer audit --locked`, and accepting an advisory or abandoned package |
| `drupal/composer/composer-conflicts` | Reading a resolution failure to the one culprit package |

### Related recipes

- `drupal_implement_standards_and_tests`: its `## Configuration gate` restores a seed database, runs `updatedb`, imports the export, and proves the export matches the commit.
- `drupal_worktree_environment`: brings up the worktree site with the seed the gate restores, and prints the `project:` value.

### External sources

| Source | What it settles |
|---|---|
| Carlos Ospina, "Simplifying Drupal Updates: A Structured Approach to Worry-Free Maintenance", 2024-10-25, https://www.adrupalcouple.us/simplifying-drupal-updates-structured-approach-worry-free-maintenance | The foundation phase, updates as their own cycle, export after `updatedb`, the custom-code API inventory against change records, one conflict at a time |
| Carlos Ospina, "From Fear to Freedom", https://www.youtube.com/watch?v=UGfrvVQjCQw | The core version path, crossing a major by release date to the lowest minor, stopping and stable points, the forced pin, the foundation, where Composer puts the real conflict |
| drupal.org release history, `https://updates.drupal.org/release-history/drupal/current` | The basis of the date rule. 8.9.20, 9.1.14 and 9.2.9 share 2021-11-17, and the talk went from 8.9.20 to 9.1.14. 10.6.0 and 11.3.0 share 2025-12-17. Each release carries `<date>` as a Unix timestamp and, for contrib, `<core_compatibility>`; `<supported_branches>` lists the supported branch prefixes |
| drupal.org, Updating Modules and Themes using Composer, https://www.drupal.org/docs/updating-drupal/updating-modules-and-themes-using-composer | `--with-all-dependencies` for modules, `require` for a major move, `updatedb`, then `config:export`, backup first |
| drupal.org, Updating Drupal core via Composer, https://www.drupal.org/docs/updating-drupal/updating-drupal-core-via-composer | `"drupal/core-*"` with `--with-all-dependencies`, `--dry-run`, export after the database update |
| drupal.org, How to upgrade from Drupal 10 to Drupal 11, https://www.drupal.org/docs/upgrading-drupal/upgrading-from-drupal-8-or-later/how-to-upgrade-from-drupal-10-to-drupal-11 | Drupal 11 requires Drupal 10.3.0 or later |
| Upgrade Status, https://www.drupal.org/project/upgrade_status | Major-upgrade readiness; 4.3.x is stable for Drupal 9 to 11, 5.0.x supports 12 and is alpha |
| Drush 13, `DeployCommands.php`, `UpdateDBCommands.php`, `DeployHookCommands.php`, `ConfigCommands.php` | The `deploy` order; `updatedb:status`, `config:status` and `deploy:hook-status` exit 0 either way; the first two print nothing on standard output when clean; `updatedb` and `deploy:hook` exit 1 on failure |
| consolidation/output-formatters 4.7, `TsvFormatter.php` | TSV prints no header row by default, so zero rows print nothing |
| Composer 2.10, CLI and config documentation, changelog, `Installer.php`, `Locker.php` | `update`, `require` and `remove` flags, `--dry-run`, `validate`; `Nothing to modify in lock file` on standard error; `audit` exits 0 or 1 from 2.10; abandoned packages fail by default from 2.7; `policy.advisories.ignore-id` and `policy.abandoned.ignore` from 2.10, `audit.ignore` and `audit.ignore-abandoned` deprecated; the lock file's content hash reads no `config` key but `platform` |
| cweagans/composer-patches 1.x, `Patches.php` and README | A failed patch prints `Could not apply patch! Skipping.` and the command succeeds, unless `extra.composer-exit-on-patch-failure` is true |
| cweagans/composer-patches 2.0.0, `src/Plugin/Patches.php` | A failed patch throws an exception, which the command's non-zero exit surfaces; there is no skip-and-continue path |
| drupal.org issue #3564942, marked Fixed 2026-02-19, auto-closed 2026-03-05 | Not a core compatibility issue: a support request. The reporter's failures came from patches missing `a/`/`b/` path prefixes and from 2.x's changed configuration and workflow — plugin options under `extra.composer-patches`, `patches.lock.json`, and `composer patches-relock` / `composer patches-repatch` after editing patches |
| Drupal core-composer-scaffold, README and `Plugin.php` | Scaffolding runs after every `composer update` and `composer install`; with `gitignore` unset it updates `.gitignore` files when the project is a git working copy that ignores `vendor` |
| Drupal core 11.4, `ModuleInstaller.php`, `ThemeInstaller.php`, `ConfigInstaller.php` | `installDefaultConfig()` runs on install only; optional configuration installs when a later install meets its dependencies |
| DDEV 1.25, `ddevapp.go` | `describe -j` carries `name` and `status_desc`; a snapshot name that exists is refused |
| Drupal core issue #3110362, https://www.drupal.org/project/drupal/issues/3110362 | Configuration an update hook changes is lost unless it is exported and committed |
