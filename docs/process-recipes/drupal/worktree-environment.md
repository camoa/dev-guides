---
# Routing block, first and in this order. Whoever is resolving reads to here and decides.
name: drupal_worktree_environment
capability: worktree-environment
description: Use when a Drupal project on DDEV gives a task's git worktree a running site of its own. Says what must be true first, how to bring the site up and seed it from the main checkout with DDEV's own worktree support, how to read its address, how to tear it down, and which tasks build on the served checkout instead.
# Metadata, read only after a match.
label: Worktree environment (Drupal)
recipe_schema_version: 1.0.0
version: 0.1.0
recipe_class: process
framework: drupal
drupal_compatibility: "^10.3 || ^11"
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

A task built in its own git worktree gets a site of its own: a second DDEV project with its own
containers and database, seeded from the main checkout, reachable at an address of its own. Files
ship with a branch; a running site does not. Without this, a baseline, a review run or a browser
check made "from the worktree" reaches the main checkout's site and captures code the branch never
touched. With it, the task's `PLAYWRIGHT_BASE_URL` is the worktree's address, and every run reads
the branch.

## Opinion

**Follow DDEV's own worktree workflow, and add nothing to it.** DDEV documents how several
checkouts of one repository run as separate projects, and a worktree on a current DDEV
restores a snapshot taken in a sibling worktree without the file being copied. This recipe is that workflow
in the order a consumer runs it, plus the files directory, which DDEV does not carry across. The
pages are in `## References`; what they say is not repeated here.

**The worktree sits beside the checkout, not inside it.** DDEV treats a project directory nested
inside a registered project as belonging to the outer one until a person confirms otherwise at an
interactive `ddev start`, and `-y` keeps the outer project rather than switching. Run without a
terminal, every command in a nested worktree that does not name its project therefore reaches
the main site. A tear-down without a name then deletes the main project's containers and
database. A sibling directory has no outer project, so every command in it addresses the
worktree's own. That is the layout DDEV's workflow uses, and the one this recipe requires.

**One database per site, seeded by snapshot and never shared.** The worktree's database is a
copy taken at bring-up: a snapshot of the main project, restored in the worktree. Two sites then
drift on purpose, and a task that needs fresher data runs bring-up again.

**Bring-up is a person's choice.** A snapshot and restore is quick, but Composer, a second set of
containers and a second database volume are not free, and a task whose result is site state has no
use for them (see `## Build in place`). The commands are shown once and run on a yes; an autonomous
run never starts one. A worktree with no environment still has its files, and a consumer says so
once.

**Tear-down runs before the directory goes, and names its project.** Removing the worktree
directory first leaves DDEV's registry pointing at nothing, and the next worktree of the same name
fails `ddev start` against it. Naming the project on `ddev delete` means a repeat run, or a run
from a directory DDEV no longer knows, cannot land on another project.

## Preconditions

- The worktree is a sibling of the main checkout, `<parent of the code tree>/<task id>`, never a
  directory inside it. A consumer that finds the worktree under the code tree refuses bring-up and
  says why, because DDEV would run every command against the main project.
- `.ddev/config.yaml` is committed with no `name:` line, so each checkout is named after its
  directory. A consumer checks the file and the line, and refuses bring-up while the line is
  there, naming it; the recipe never edits a committed file.
- DDEV 1.25.4 or later: the sibling-worktree snapshot restore the seed depends on was observed on
  that version.
- The main checkout's DDEV project is running: `ddev list -j` shows one row whose `approot` is the
  main checkout with `status` `running`. The snapshot is taken from that project.
- Docker has room for a second web container, a second database container and a second database
  volume.
- The task id is lowercase letters, digits and hyphens, because it becomes a hostname. DDEV
  replaces `_` with `-` and changes nothing else, so `Add_login.v2` becomes the project
  `Add-login.v2` at `add-login.v2.ddev.site`, a name with a dot inside the label. A consumer that
  offers this recipe validates the id to this rule first.
- The worktree is a fresh checkout. On a project that ignores `vendor/` and the Composer-installed
  directories, as the Composer template for a Drupal site does once it has a `.gitignore`, bring-up installs them
  and needs the network; on a project that tracks them, that step changes nothing.

## Input contract

Three tokens the consumer fills, each a whole argument. The first two come from `ddev list -j`,
from the row whose `approot` is the main checkout's path; the third from the `## Address` output
at bring-up:

```yaml
{mainProject}: string      # that row's name: the main checkout's DDEV project name
{mainFiles}: string        # that row's approot, then its docroot, then sites/default/files:
                           #   the main site's public files directory as an absolute path
{worktreeProject}: string  # .raw.name from ddev describe -j in the worktree, kept in the task record
```

DDEV addresses a project by name and never by path, so the main checkout's path on its own cannot
name it; the `name` field of its row can. Every other command here runs in the worktree, and DDEV
resolves the worktree's own project from there.

## Sequence

1. **Check.** After `git worktree add`, the consumer confirms the worktree is not under the code
   tree, reads `.ddev/config.yaml` in the worktree for a `name:` line, and refuses with the reason
   when either fails. It shows the rest of `## Preconditions` as things a person confirms.

2. **Offer.** The consumer prints the `## Bring up` lines with both tokens filled and the
   `## Build in place` prose, and asks once. A no leaves a worktree with files and no site, and the
   task record says so. An autonomous run takes the no.

3. **Start and confirm the project.** On a yes, the consumer runs the first `## Bring up` block,
   then the `## Address` command, and reads `.raw.approot` from its output. A value that is not the
   worktree's path means DDEV resolved another project, and the consumer stops before anything is
   written to a database. The check costs one command and is the whole guard against the nested
   layout the first precondition rules out.

4. **Seed.** The consumer runs the second `## Bring up` block: a snapshot of the main project,
   its restore in the worktree, the main files directory imported, and a cache rebuild so no
   cached page keeps the main hostname.

5. **Record the address.** The consumer reads `.raw.primary_url` from the same `## Address`
   output and writes it into the task record. Review and `baseline` export it as
   `PLAYWRIGHT_BASE_URL` for that task and do not ask a person for one.

6. **Tear down.** When the task is pruned, the consumer runs `## Tear down` in the worktree
   first, and only then `git worktree remove`. A tear-down that exits non-zero leaves both the
   worktree and its project in place and says so, because removing the directory then would make
   the orphan the ordering exists to prevent.

## Data flow

```
input:  {mainProject}, {mainFiles}       from ddev list -j, the main checkout's row
        {worktreeProject}                 from ddev describe -j in the worktree, at bring-up

bring up, first block (in the worktree):
        ddev start                        → the worktree's containers, named after the directory
        ddev composer install             → vendor/ and the installed directories, from the lock file

address (in the worktree):
        ddev describe -j                  → .raw.approot checked, .raw.primary_url recorded

bring up, second block (in the worktree):
        ddev snapshot {mainProject}       → <main>/.ddev/db_snapshots/<main>_<time>-<db>.zst, DDEV-ignored
        ddev snapshot restore --latest    → the worktree database, from that sibling snapshot
        ddev import-files {mainFiles}     → the worktree's sites/default/files, replaced
        ddev drush cr                     → caches rebuilt under the worktree's hostname

tear down (in the worktree, before git worktree remove):
        ddev delete --omit-snapshot --yes {worktreeProject}
                                          → containers, volume, registry entry gone; files stay
```

## State-awareness contract

Every `## Bring up` line is safe to run twice. `ddev start` on a running project restarts it.
`ddev composer install` changes nothing when the lock file is satisfied. `ddev snapshot` takes a
new snapshot each time, and `ddev snapshot restore --latest` replaces the database with the
newest one. `ddev import-files` replaces the destination directory, and `ddev drush cr` is a
cache rebuild. Running bring-up again is how a task refreshes its copy from the main checkout.

Each bring-up leaves one snapshot in the main checkout's `.ddev/db_snapshots/`, named with its
time. `ddev snapshot --list` there shows them, and removing them is a person's call in the main
checkout, never this recipe's.

Nothing here writes a tracked file. `.ddev/db_snapshots/` is ignored by DDEV's own
`.ddev/.gitignore`; the worktree's `sites/default/files` is ignored by the same rule that ignores
the main checkout's. A `settings.ddev.php` DDEV writes at `ddev start` is one the main checkout
already ignores.

`## Tear down` names the project, so a repeat run reports the project as deleted and touches
nothing else; DDEV does not fail on a name it has already removed. A consumer runs the tear-down
only for a task whose record carries an address, which is the mark that bring-up ran.

## Verifier

In the worktree, after bring-up, with the main checkout still running:

1. `ddev list -j` shows two rows with the main checkout's `approot` and the worktree's, each
   `running`, with different `name` and `primary_url` values.
2. `ddev describe -j` prints JSON whose `.raw.approot` is the worktree's path and whose
   `.raw.primary_url` is `https://<worktree name>.ddev.site`; `curl -sSI` on that address returns
   `HTTP/2 200`.
3. `ddev drush status --field=uri` prints the worktree's address, and
   `ddev drush config:get system.site name` prints the same site name the main checkout does,
   which shows the database came across.
4. A file added under the worktree's docroot is served at the worktree's address and answers 404
   at the main checkout's.
5. `git status --short` in the worktree and in the main checkout print nothing.
6. After `## Tear down`, `ddev list -j` shows the main row only, the worktree directory still
   exists and `git worktree list` in the main checkout still lists it; a second tear-down run
   exits 0 and leaves the main row running; then `git worktree remove` takes the directory.

Observed on 2026-09-13 against a fresh Drupal 11.4 standard install on DDEV 1.25.4 with Docker on
Linux. The main checkout sat in a directory with no `name:` line, the worktree beside it, and
every command ran without a terminal. Steps 1 to 6 held as written. Bring-up took about 75
seconds, 35 of them the restore. A second bring-up left a second timestamped snapshot, and
`--latest` picked it.

## Bring up

The consumer reads every fenced block tagged `sh` under this heading, in order, one command per
line, and runs each as arguments from the worktree, never through a shell. The two tokens are
filled whole; no other argument varies. Between the two blocks the consumer runs `## Address` and
checks `.raw.approot`, as `## Sequence` step 3 says.

```sh
ddev start
ddev composer install
```

The worktree tracks `composer.lock` and, on most projects, not what it installs, so the site has no
code to serve until Composer runs.

```sh
ddev snapshot {mainProject} --yes
ddev snapshot restore --latest
ddev import-files --source {mainFiles}
ddev drush cr
```

The snapshot is taken in the main project and restored in the worktree without a path between
them, which is DDEV's worktree support doing the copy. It carries no `--name`: DDEV names it with
the time, and `--latest` restores the one just taken. A fixed name would not do, because a second
snapshot under a name that exists is refused with exit 0, and the restore would then load the
first seed again with nothing to show for it. The cache rebuild runs before the first request,
because the restored cache tables were built under the main hostname.

## Address

One command, run in the worktree, and the fields to read from its output:

```sh
ddev describe -j
```

The address is `.raw.primary_url` in the JSON on standard output, for example
`https://add-login.ddev.site`; `.raw.approot` is the directory DDEV resolved the project from, and
must be the worktree. Review and `baseline` export the address as `PLAYWRIGHT_BASE_URL`.

## Tear down

Run in the worktree, before `git worktree remove`. The last argument is the worktree's project
name, which is its directory name with `_` replaced by `-`, and is also `.raw.name` in the
`## Address` output:

```sh
ddev delete --omit-snapshot --yes {worktreeProject}
```

`--omit-snapshot` skips DDEV's pre-delete snapshot because the database is a copy the main
checkout still has. The worktree's files stay for `git worktree remove`.

## Build in place

A task whose result is files on a branch belongs in a worktree with an environment of its own: a
module's code, a theme's templates, a test suite, configuration exported as YAML. A task whose
result is site state does not. Requiring a module with Composer and enabling it, importing
configuration, building a theme's assets, running a migration: each of these produces enabled
modules, schema, rows or built files that downstream work must see, and a copy nobody serves is
where nothing downstream looks. Those tasks build on the served checkout, with a person present,
and skip this recipe. A consumer shows this paragraph at the point of choice, and the person
decides which kind of task this is.

## References

| Reference | Why |
|---|---|
| [DDEV: Git worktrees for contributors](https://ddev.com/blog/git-worktree-contributor-training/) | The workflow this recipe follows: worktrees beside the checkout, `name:` omitted, one project per worktree |
| [DDEV configuration: `name`, `omit_project_name_by_default`](https://docs.ddev.com/en/stable/users/configuration/config/) | A project with no `name:` takes its directory's name; the global option DDEV suggests for worktree users |
| [DDEV commands: `snapshot`, `snapshot restore`](https://docs.ddev.com/en/stable/users/usage/commands/#snapshot) | Snapshots from sibling worktrees of the same repository are listed and restorable by name |
| [DDEV commands: `import-files`, `delete`](https://docs.ddev.com/en/stable/users/usage/commands/#import-files) | The files import replaces the destination; `delete` takes project names and `--omit-snapshot` |
| [DDEV FAQ](https://docs.ddev.com/en/stable/users/usage/faq/) | Several checkouts of one project as distinct names; nested projects are to be avoided |
| `drupal/e2e-setup-atk.md`, `drupal/visual-regression-setup.md` | The suites that read `PLAYWRIGHT_BASE_URL`, which `## Address` supplies for a worktree |
| `drupal/checks.md`, `## Surface commands` | The rows review runs against that address |
