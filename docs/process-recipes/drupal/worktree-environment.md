---
# Routing block, first and in this order. Whoever is resolving reads to here and decides.
name: drupal_worktree_environment
capability: worktree-environment
description: Use when a Drupal project on DDEV gives a task's git worktree a running site of its own. Says what must be true first, how to bring the site up and seed it from the main checkout with DDEV's own worktree support, how to read its address, how to tear it down, and which tasks build on the served checkout instead.
# Metadata, read only after a match.
label: Worktree environment (Drupal)
recipe_schema_version: 1.0.0
version: 0.7.0
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

The sections a consumer runs are read in document order: `## Tokens`, then the `## Bring up` before
`## Address`, then `## Address`, then the `## Bring up` after it, and before all of them the one line under
`## Preconditions`. The second `## Bring up` is not a mistake; the address is read between the two
because it is the guard for the second.

## Opinion

**Follow DDEV's own worktree workflow, and add nothing to it.** DDEV documents how several
checkouts of one repository run as separate projects, and a worktree on a current DDEV
restores a snapshot taken in a sibling worktree without the file being copied. This recipe is that workflow
in the order a consumer runs it, plus the files directory, which DDEV does not carry across. The
pages are in `## References`; what they say is not repeated here.

**The worktree lives outside the checkout, never inside it.** DDEV treats a project directory nested
inside a registered project as belonging to the outer one until a person confirms otherwise at an
interactive `ddev start`, and `-y` keeps the outer project rather than switching. Run without a
terminal, every command in a nested worktree that does not name its project therefore reaches
the main site. A tear-down without a name then deletes the main project's containers and
database. A directory outside the checkout has no outer project, so every command in it addresses
the worktree's own. That is the layout DDEV's workflow uses, and the one this recipe requires. The
recommended layout is `<parent>/<repo>.worktrees/<repo>-<task>`; a plain sibling,
`<parent>/<repo>-<task>`, also works.

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

- The worktree is outside the main checkout, never a directory inside it. Its directory name is
  the project's name and hostname label. A consumer that finds the worktree under the code tree
  refuses bring-up and says why, because DDEV would run every command against the main project.
- `.ddev/config.yaml` is committed with no `name:` line, so each checkout is named after its
  directory. The check below refuses bring-up while the line is there and names it; the recipe
  never edits a committed file. The remedy is the person's: delete the line and commit it on the
  branch the worktree has checked out. A commit on the branch the worktree was cut from does not
  reach it until someone merges it in. That one-line change then sits in the task's diff though
  the task's contract does not name it, and the task's review should expect it. Deleting the line
  is all bring-up needs. `ddev config global --omit-project-name-by-default` is optional: DDEV's
  configuration page says it "determines whether `ddev config` updates the `name` field", so it
  only stops a later `ddev config` from writing the line back, which would fail the next bring-up.
- DDEV 1.25.4 or later: the sibling-worktree snapshot restore the seed depends on was observed on
  that version.
- The main checkout's DDEV project is running: `ddev list -j` shows one row whose `approot` is the
  main checkout with `status` `running`. The snapshot is taken from that project.
- Docker has room for a second web container, a second database container and a second database
  volume. `bash` and `jq` are on the host's `PATH`, for the seven scripts under `## Files`.
- The worktree's directory name is lowercase letters, digits and hyphens, because it becomes a
  hostname label. DDEV replaces `_` with `-` and changes nothing else, so `Add_login.v2` becomes
  the project `Add-login.v2` at `add-login.v2.ddev.site`, a name with a dot inside the label. A
  consumer that offers this recipe validates the name to this rule first.
- The worktree has a clean working tree, and the consumer commits what `## Files` writes on the
  task's branch, the way it commits what a setup recipe's install writes. Untracked files there
  fail the clean-tree check every stage runs, and `git worktree remove` refuses a tree that holds
  them.
  One known way a tree turns dirty on its own: DDEV 1.25.4 rewrites `.ddev/providers/platform.yaml`,
  a file it marks `#ddev-generated`, on `ddev start`, so a project that tracks that file fails the
  clean-tree check after the first start until the refreshed file is committed. Observed on a live
  run; commit the file once and it stays clean.
- The worktree is a fresh checkout. On a project that ignores `vendor/` and the Composer-installed
  directories, as the Composer template for a Drupal site does once it has a `.gitignore`, bring-up installs them
  and needs the network; on a project that tracks them, that step changes nothing.
  Until bring-up has run, such a worktree holds no site to test. The `{custom_root}` token of
  `drupal/test-execution.md` looks for a folder named modules/custom, which the standard layout keeps
  in git. It prints nothing in two cases: the project's custom modules are Composer-installed
  (`type:drupal-custom-module`) and bring-up has not run, or the project has no custom module yet.
  An empty value there is one of those, not a wrong command. Run bring-up before passing
  `--value custom_root=<path>`, because a folder that does not exist yet fails the same way.

The checks a script can make are one line, run in the worktree after `## Files` is written and
before anything is committed or a token runs, as arguments and never through a shell. It must exit
0. A non-zero exit refuses the bring-up, prints the script's line, removes the files that run
wrote, and commits nothing:

```sh
bash .aida/worktree-environment/preconditions.sh {codePath}
```

The script checks, in order, that the worktree is not inside `{codePath}`, that
`.ddev/config.yaml` is there with no `name:` line, that DDEV is 1.25.4 or later, that the main
checkout is a listed project with `status` `running`, that the worktree's directory name is
lowercase letters, digits and hyphens, and that no `main-seed-` snapshot from an earlier bring-up
is still in the main checkout. One line names the first failure and what to do about it.
`bash` and `jq` need no check: the script running is the check.

## Input contract

One token the consumer holds, and three the recipe produces, each a whole argument:

```yaml
{codePath}: string         # the main checkout's path; the consumer fills it, in ## Preconditions, ## Tokens and ## Tear down
{mainProject}: string      # ## Tokens: the main checkout's DDEV project name
{mainFiles}: string        # ## Tokens: the main site's public files directory, absolute
{project}: string          # ## Address, the project: line; kept in the task record for the second ## Bring up, ## Tear down and the configuration gate
```

DDEV addresses a project by name and never by path, so the main checkout's path on its own cannot
name it. The `## Tokens` commands turn the path into the name and the files directory by reading
DDEV's project list. Every other command here runs in the worktree, and DDEV resolves the
worktree's own project from there.

## Sequence

1. **Show.** After `git worktree add`, the consumer prints the `## Preconditions` prose and the
   line it will run, so a person sees what is checked and why.

2. **Offer.** The consumer prints the `## Bring up` lines with the tokens by name, and the
   `## Build in place` prose, and asks once. A no writes nothing: the worktree keeps its files and
   has no site, and the task record says so. An autonomous run takes the no.

3. **Write, check, commit, fill.** On a yes, the consumer writes the `## Files` where absent,
   then runs the `## Preconditions` line with `{codePath}` filled. A non-zero exit refuses the
   bring-up with the script's line, removes the files that run wrote, and commits nothing. On exit
   0 it commits the files on the task's branch, runs each `## Tokens` command the same way, and
   takes the first line each prints as the token's value. A command that prints nothing or exits
   non-zero refuses the bring-up by the token's name.

4. **Start and confirm the project.** The consumer runs the `## Bring up` before `## Address`,
   then the `## Address` command, and reads its `root:` line. A value that is not the
   worktree's path means DDEV resolved another project, and the consumer stops before anything is
   written to a database. The check costs one command and is the whole guard against the nested
   layout the first precondition rules out.

5. **Record the address.** The consumer keeps the `address:` line from the same `## Address`
   output as the task's address, and every other line as a token, so `project:` is
   `{project}`. Review and `baseline` export the address as `PLAYWRIGHT_BASE_URL` for
   that task and do not ask a person for one.

6. **Seed.** The consumer runs the `## Bring up` after `## Address`: a snapshot of the main
   project, its restore in the worktree, the main checkout's copy removed, the main files
   directory imported, a cache rebuild so no cached page keeps the main hostname, and then, after
   every snapshot the worktree held before is removed, two snapshots of the seeded database under
   the worktree's own names, `seed-{project}` and `gate-{project}`, for the
   `## Configuration gate` of `drupal/standards-and-tests.md`.

7. **Tear down.** When the task is pruned, the consumer runs `## Tear down` in the worktree
   first, and only then `git worktree remove`. A tear-down that exits non-zero leaves both the
   worktree and its project in place and says so, because removing the directory then would make
   the orphan the ordering exists to prevent.

## Data flow

```
input:  {codePath}                       held by the consumer

files (written where absent, committed after the check passes):
        .aida/worktree-environment/preconditions.sh, main-row.sh, main-project.sh, main-files.sh, address.sh, status.sh, main-seed-cleanup.sh

preconditions (in the worktree, before the commit):
        preconditions.sh {codePath}       → exit 0, or one line naming the first failure

tokens (in the worktree, before bring-up):
        main-project.sh {codePath}        → {mainProject}, the name field of the checkout's ddev list -j row
        main-files.sh {codePath}          → {mainFiles}, the checkout's resolved path, its docroot field, sites/default/files

bring up, before ## Address (in the worktree):
        ddev start                        → the worktree's containers, named after the directory
        ddev composer install             → vendor/ and the installed directories, from the lock file

address (in the worktree):
        address.sh                        → root: checked; address: recorded; project: → {project}

bring up, after ## Address (in the worktree):
        ddev snapshot {mainProject} --name main-seed-{project} --yes
                                          → <main>/.ddev/db_snapshots/main-seed-{project}-<db>.zst, DDEV-ignored
        ddev snapshot restore main-seed-{project}
                                          → the worktree database, from that snapshot
        ddev snapshot {mainProject} --cleanup --name main-seed-{project} --yes
                                          → the main checkout's copy removed by name
        ddev import-files --source {mainFiles}
                                          → the worktree's sites/default/files, replaced
        ddev drush cr                     → caches rebuilt under the worktree's hostname
        ddev snapshot --cleanup --yes     → the worktree's own earlier snapshots removed, none is fine
        ddev snapshot --name seed-{project} --yes
                                          → <worktree>/.ddev/db_snapshots/seed-{project}-<db>.zst, the seed by name
        ddev snapshot --name gate-{project} --yes
                                          → gate-{project}-<db>.zst beside it, the name the configuration gate retakes

tear down (in the worktree, before git worktree remove):
        ddev delete --omit-snapshot --yes {project}
                                          → containers, volume, registry entry gone; files stay
        main-seed-cleanup.sh {codePath} {mainProject} {project}
                                          → a main-seed-{project} a failed bring-up left, removed; none is fine
```

## State-awareness contract

Every `## Bring up` line can run twice. `ddev start` on a running project restarts it.
`ddev composer install` changes nothing when the lock file is satisfied. `ddev snapshot --name
main-seed-{project}` takes a snapshot under that name and is refused with exit 0 if the name is
already there; the cleanup line right after it removes that snapshot by name, so a normal run
leaves nothing to collide with the next one. `ddev snapshot restore main-seed-{project}` replaces
the worktree's database with that one snapshot, by name rather than by newest file. `ddev
import-files` replaces the destination directory, and `ddev drush cr`
is a cache rebuild. `ddev snapshot --cleanup --yes` with no name removes the worktree's own
snapshots, for the reason `## Bring up` gives, and is what lets the two named snapshots after it
run again. Running bring-up
again is how a task refreshes its copy from the main checkout. The refresh replaces the two
named snapshots and loses whatever the worktree's database held since, which is the branch's
content, so a task that has built on the site does not refresh without a person's yes.

Each bring-up takes one named snapshot in the main checkout's `.ddev/db_snapshots/`,
`main-seed-{project}`, and removes it by name right after the restore, so nothing accumulates
there. A bring-up that fails before that removal leaves the snapshot behind. `## Preconditions`
refuses the next bring-up on that worktree until the person removes it, using the command the
refusal prints, and `## Tear down` removes it too. The worktree's own `.ddev/db_snapshots/` holds `seed-{project}` and
`gate-{project}`; the cleanup line clears it at each bring-up, and `git worktree remove` takes the
directory with it, because `ddev delete` leaves the `.ddev` folder alone.

The seven `## Files` are written once, where absent, and refused where a file exists with other
content, the rule every setup recipe's files follow. The consumer commits them on the task's
branch once the `## Preconditions` line has exited 0 and before a token runs, so the tree is
clean for the stages that check it, and a refused bring-up leaves no file behind. Task completion
takes them off the branch before it merges, as `## Tear down` says.

Beyond those, nothing here writes a tracked file. `.ddev/db_snapshots/` is ignored by DDEV's own
`.ddev/.gitignore`; the worktree's `sites/default/files` is ignored by the same rule that ignores
the main checkout's. A `settings.ddev.php` DDEV writes at `ddev start` is one the main checkout
already ignores.

`## Tear down` names the project, so a repeat run reports the project as deleted and touches
nothing else; DDEV does not fail on a name it has already removed. A consumer runs the tear-down
only for a task whose record carries an address from a bring-up. An address recorded for a site
that was already up marks no bring-up, as the next paragraphs say.

**A site that is already up.** A worktree can run a site before any bring-up of this task, for
example when a later task takes over an earlier task's worktree. Bring-up must not run on that
site, because its second `## Bring up` replaces the database with the main checkout's and loses
the branch's content. The site may be recorded as it stands. A consumer that adopts it writes
the `## Files`, runs `## Address` with its `root:` check, and records the address. It runs no
`## Preconditions`, `## Tokens` or `## Bring up` line.

The site must still be this worktree's own project. Of the `## Preconditions` checks, the DDEV
version, the running main checkout and the stale `main-seed-` snapshot guard the seed, and none
applies to a site nobody seeds. The `name:` check and the nested-layout check guard which project
a command reaches, and the `root:` check alone does not cover them. `ddev describe` reports the
`approot` of the directory it was run from, while it finds the containers by project name. So
`status.sh` checks both: the project resolved from the worktree is rooted at the worktree, and
its name is the worktree's directory name. A site that fails either check is not adopted. The
consumer then takes the bring-up path, and `## Preconditions` refuses it before anything is
written to a database. A pinned `name:` line, or a directory name with an `_` or an uppercase
letter, ends there. A person resolves it, and runs no bring-up over a database the branch needs.

An adopted site has no seed this recipe took. Never take `seed-{project}` from the adopted site
itself. That database already holds the branch's change, so the configuration gate would import
onto it, change nothing and prove nothing. The only true seed is the main checkout's database. Check
for a seed at adoption, not first at the gate. Run `ddev snapshot --list` in the worktree and look
for `seed-{project}`; the list includes snapshots in sibling worktrees of the same repository. A seed
that is listed was taken from the main checkout at an earlier bring-up, of unknown age. When
no bring-up took `gate-{project}` either, the gate's first line fails on that missing snapshot.
With that name put back, a missing seed fails the fourth line. Either stop comes before the
database changes. The way to a true seed is a person's choice between two remedies:

- Run bring-up, after exporting the database with `ddev export-db` to a file outside the
  worktree. Bring-up replaces the site's content.
- Take `ddev snapshot {mainProject} --name seed-{project} --yes` in the main checkout while it
  runs. The gate's restore by name finds it there. That copy of the main database then stays in
  the main checkout until a person removes it with
  `ddev snapshot {mainProject} --cleanup --name seed-{project} --yes`.

An adopted site is never torn down by a consumer, as `## Tear down` says.

## Verifier

In the worktree, with the main checkout running:

1. Before bring-up, `bash .aida/worktree-environment/preconditions.sh <main checkout>` prints nothing and
   exits 0, including for a main checkout whose DDEV `docroot` is empty because its Drupal root
   is the repository root. Run from a directory inside the checkout, from a project whose `.ddev/config.yaml`
   has a `name:` line, with a main checkout that is no listed project, or from a directory named
   `Bad_Name`, it prints one line saying which and exits 1.

After bring-up:

2. `ddev list -j` shows two rows with the main checkout's `approot` and the worktree's, each
   `running`, with different `name` and `primary_url` values.
3. `bash .aida/worktree-environment/address.sh` prints three lines, `address:`, `project:` and `root:`, the
   root being the worktree's path and the address `https://<worktree name>.ddev.site`; `curl -sSI`
   on that address returns `HTTP/2 200`.
4. `ddev drush status --field=uri` prints the worktree's address, and
   `ddev drush config:get system.site name` prints the same site name the main checkout does,
   which shows the database came across. `ddev snapshot --list` in the worktree lists
   `seed-{project}` and `gate-{project}` among its rows.
5. A file added under the worktree's docroot is served at the worktree's address and answers 404
   at the main checkout's.
6. `git status --short` in the worktree and in the main checkout print nothing.
7. After `## Tear down`, `ddev list -j` shows the main row only, the worktree directory still
   exists and `git worktree list` in the main checkout still lists it; a second tear-down run
   exits 0 and leaves the main row running; then `git worktree remove` takes the directory.

Observed on 2026-09-13 against a fresh Drupal 11.4 standard install on DDEV 1.25.4 with Docker on
Linux, twice, on 0.1.0 and on 0.2.0. The main checkout sat in a directory with no `name:` line,
the worktree beside it, and every command ran without a terminal. Steps 2 to 5 held as written on
both runs. The token scripts printed their values, and nothing with exit 4 for a path that is no
project. Steps 6 and 7 held on 0.1.0, which wrote no files. On 0.2.0 the three `## Files` were
written and not committed, and both failed: `git status` showed `.aida/` untracked, and
`git worktree remove` refused the tree with exit 128. That is why the commit is a step; a run with
the commit made is not yet observed. Step 1 was run on 2026-09-14 against a running project with a
pinned `name:`, a nested directory, a directory with no `.ddev/`, a main checkout that is no
project, a directory named `Bad_Name`, and a passing sibling: each refusal printed its one line
and exit 1, and the passing case printed nothing and exit 0. The token scripts were run with the
checkout's path plain, with a trailing slash, and through a symbolic link, and printed the same
name and files directory each time; DDEV itself lists a project under the path `ddev start` was
run from, link included, which is why the scripts compare resolved paths. Bring-up took about 75 seconds, 35 of them the restore. A
second bring-up left a second timestamped snapshot, and `--latest` picked it. The three lines added
on 2026-09-22, the cleanup and the two named snapshots, are read from DDEV 1.25.4's source
(`pkg/ddevapp/snapshot.go` and `cmd/ddev/cmd/snapshot.go`) and not yet run. What was read: a
cleanup with no name lists the project's own snapshot directory and deletes each entry, so an
empty directory exits 0. A cleanup with a name that does not exist exits 1. A failure inside a
snapshot prints a warning and exits 0, so step 4's listing is the check that both names exist.

The three lines changed on 2026-09-30, naming the main checkout's seed snapshot
`main-seed-{project}` and deleting it by name right after the restore, match DDEV 1.25.4's
documented `snapshot`, `snapshot restore` and `snapshot --cleanup --name` commands and are not yet
run end to end.

The tear-down guard added on 2026-11-11 is read from DDEV 1.25.5's source and not yet run. A
cleanup with a name passes it to `DeleteSnapshot`, which returns an error when no file matches,
and the command then exits 1 (`cmd/ddev/cmd/snapshot.go:208-211`, `pkg/ddevapp/snapshot.go:81-84`).

The 0.4.1 scripts were run on 2026-09-24 with bash 5.2.21 against a stub `ddev` that printed a
fixed project list; no DDEV ran. The list held a project with an empty `docroot`, one with `web`,
and one with no `docroot` key at all. Each checkout was given plain, with a trailing slash, and
through a symbolic link. The empty-docroot project read `status` `running` and its files
directory as the checkout's own `sites/default/files`, where 0.4.0's loop had read `status` empty
and the files directory as `<checkout>/running/sites/default/files`. The project with no
`docroot` key read an empty docroot rather than `null`, which is what the `// ""` in
`main-row.sh` is for. A directory that is no listed project, and one that does not exist, both
exited 4 from all three scripts. A run against a real project whose Drupal root is the repository
root is not yet observed.

The root and name checks added to `status.sh` in 0.7.0 are read from DDEV 1.25.5's source and
were run only against a stub `ddev`. `ddev describe` loads the project from the nearest
`.ddev/config.yaml` at or above the directory (`pkg/ddevapp/utils.go:162-176`), and `app.Init`
finds its web container by the project's name (`pkg/ddevapp/ddevapp.go:203-217`).

## Status

One command, run before a consumer's verify lines, because `ddev drush` and `ddev exec` silently
start a stopped project and print start-up text that fails every `stdout empty` check.

```sh
bash .aida/worktree-environment/status.sh
```

Exit 0 means the worktree's own project is up. That is the project DDEV resolves from the
worktree, rooted at the worktree and named after its directory. A non-zero exit prints which
condition failed and stops the step, which the consumer reports as `task environment <id> up`.
A consumer also runs this line to decide whether a worktree already runs a site it may adopt,
as `## State-awareness contract` says. Without the root and name checks, a project resolved
somewhere else would read as up.

## Tokens

One fenced `sh` block per token, the token's name as the fence's second word, one command. The
consumer runs each in the worktree before the first `## Bring up`, as arguments and never through a
shell, with `{codePath}` filled whole, and takes the first line of standard output as the value. A
command that prints nothing, or exits non-zero, refuses the bring-up and names the token.

```sh mainProject
bash .aida/worktree-environment/main-project.sh {codePath}
```

```sh mainFiles
bash .aida/worktree-environment/main-files.sh {codePath}
```

Both scripts ask `main-row.sh` for one field of the main checkout's row of DDEV's project list,
because a pipe and a filter are more than one argument can say. A checkout that is not a listed
project prints nothing and exits 4, which is the refusal. The script never splits the row on
tabs. A tab is whitespace to `read`, so an empty field between two tabs vanishes. A project whose
Drupal root is the repository root lists an empty `docroot`, and every field after it then moves
one place to the left.

## Files

Seven scripts in `.aida/worktree-environment/`, written where absent, the path as the fence's
second word. They hold every DDEV and `jq` invocation the checks, the tokens, the address and the
tear-down guard need, so the consumer runs them and knows neither. Paths are compared as the filesystem resolves them, in one place, because DDEV lists a
checkout under the path it was started from, and a consumer may hold that path with a trailing
slash or through a link.

Until 0.4.1 the scripts lived in `.aida/environment/`. A file that exists with different content
refuses the whole bring-up, so a project that had committed the 0.4.0 scripts would refuse the
corrected ones at the same paths until a person removed the old files. At the new paths they are
absent and are written. The old directory is no longer read, and a person may delete it.

```sh .aida/worktree-environment/preconditions.sh
#!/usr/bin/env bash
# Checks what must be true before this worktree gets a site. $1 is the main checkout.
# One line per failure, exit 1 at the first; silence and exit 0 when everything holds.
main="$(cd "$1" 2>/dev/null && pwd -P)" || { echo "the main checkout $1 is not a directory"; exit 1; }
here="$(pwd -P)"
case "$here" in
  "$main"/*) echo "the worktree $here is inside the checkout $main; DDEV hands a nested project to the outer one, so put it outside the checkout: git worktree add ../<repo>.worktrees/<repo>-<name>"; exit 1 ;;
esac
[ -f .ddev/config.yaml ] || { echo "no .ddev/config.yaml in $here; this recipe is for a DDEV project"; exit 1; }
line="$(grep -n '^name:' .ddev/config.yaml | head -1 | cut -d: -f1)"
if [ -n "$line" ]; then
  echo ".ddev/config.yaml:$line pins the project name, so every worktree would collide with it; delete that line and commit it on the branch this worktree has checked out, since a commit on the branch it was cut from does not reach it"
  exit 1
fi
command -v ddev >/dev/null || { echo "ddev is not on PATH"; exit 1; }
version="$(ddev --version | sed 's/^ddev version v//')"
IFS=. read -r major minor patch <<<"${version%%-*}"
if [ "${major:-0}" -lt 1 ] || { [ "$major" -eq 1 ] && [ "${minor:-0}" -lt 25 ]; } || { [ "$major" -eq 1 ] && [ "$minor" -eq 25 ] && [ "${patch:-0}" -lt 4 ]; }; then
  echo "DDEV $version is older than 1.25.4, the version that restores a snapshot from a sibling worktree"
  exit 1
fi
status="$(bash "$(dirname "$0")/main-row.sh" "$1" status)"
[ "$status" = "running" ] || { echo "the main checkout $1 is not a running DDEV project (status: ${status:-not listed}); run ddev start there first"; exit 1; }
name="$(basename "$here")"
case "$name" in
  *[!a-z0-9-]*) echo "the worktree directory name '$name' becomes a hostname label; use lowercase letters, digits and hyphens"; exit 1 ;;
esac
shopt -s nullglob
found=("$main"/.ddev/db_snapshots/main-seed-"$name"-{mariadb,mysql,postgres}_*.{zst,gz,mbstream,xbstream})
if [ "${#found[@]}" -gt 0 ]; then
  stale="${found[0]}"
  mainName="$(bash "$(dirname "$0")/main-row.sh" "$1" name)"
  echo "$stale is left from a bring-up that did not finish; remove it first: ddev snapshot $mainName --cleanup --name main-seed-$name --yes"
  exit 1
fi
```

```sh .aida/worktree-environment/main-row.sh
#!/usr/bin/env bash
# Prints one field of the DDEV project row for the checkout at $1; $2 names it: name, docroot or status.
# One path is read per line, so an empty field cannot shift the others. Paths are compared as the
# filesystem resolves them, so a trailing slash or a symlink on either side still matches.
# Prints nothing and exits 4 when no listed project is that checkout.
want="$(cd "$1" 2>/dev/null && pwd -P)" || exit 4
list="$(ddev list -j)" || exit 4
while IFS= read -r root; do
  if [ "$(cd "$root" 2>/dev/null && pwd -P)" = "$want" ]; then
    jq -r --arg root "$root" --arg field "$2" 'first(.raw[] | select(.approot == $root)) | .[$field] // ""' <<<"$list"
    exit 0
  fi
done < <(jq -r '.raw[].approot' <<<"$list")
exit 4
```

```sh .aida/worktree-environment/main-project.sh
#!/usr/bin/env bash
# Prints the DDEV project name of the checkout at $1.
exec bash "$(dirname "$0")/main-row.sh" "$1" name
```

```sh .aida/worktree-environment/main-files.sh
#!/usr/bin/env bash
# Prints the public files directory of the checkout at $1: its resolved path, its docroot, sites/default/files.
root="$(cd "$1" 2>/dev/null && pwd -P)" || exit 4
docroot="$(bash "$(dirname "$0")/main-row.sh" "$1" docroot)" || exit $?
printf '%s/sites/default/files\n' "${root}${docroot:+/$docroot}"
```

```sh .aida/worktree-environment/address.sh
#!/usr/bin/env bash
# Prints the worktree project's address, name and root, one key per line, from where it is run.
ddev describe -j | jq -r '.raw | "address: \(.primary_url)\nproject: \(.name)\nroot: \(.approot)"'
```

```sh .aida/worktree-environment/status.sh
#!/usr/bin/env bash
# Exits 0 when the DDEV project resolved from here is running, is rooted here and is named after
# this directory; otherwise prints which and exits 1. describe reports the approot of the directory
# it ran in but finds containers by name, so the name check is what ties the containers to here.
command -v jq >/dev/null || { echo "jq is not installed"; exit 1; }
here="$(pwd -P)"
raw="$(ddev describe -j 2>/dev/null | jq -c '.raw // empty')"
status="$(jq -r '.status // empty' <<<"$raw")"
[ "$status" = "running" ] || { echo "the worktree's DDEV project is not running (status: ${status:-not a DDEV project})"; exit 1; }
root="$(jq -r '.approot // empty' <<<"$raw")"
[ -n "$root" ] && [ "$(cd "$root" 2>/dev/null && pwd -P)" = "$here" ] \
  || { echo "DDEV resolved the project at ${root:-no folder}, not this worktree $here, so a command here reaches another project"; exit 1; }
name="$(jq -r '.name // empty' <<<"$raw")"
[ "$name" = "$(basename "$here")" ] \
  || { echo "the project here is named ${name:-nothing}, not $(basename "$here") after this directory; a name: line in .ddev/config.yaml or an _ in the directory name does that"; exit 1; }
```

```sh .aida/worktree-environment/main-seed-cleanup.sh
#!/usr/bin/env bash
# Removes main-seed-$3 from the main checkout at $1, whose DDEV project is $2, when a bring-up
# that did not finish left it. Exits 0 when there is none, because DDEV's cleanup of a name
# that does not exist exits 1. The pattern is DDEV's own snapshot file name, so a sibling
# worktree's main-seed-$3-<more> is never matched.
main="$(cd "$1" 2>/dev/null && pwd -P)" || { echo "the main checkout $1 is not a directory"; exit 1; }
shopt -s nullglob
found=("$main"/.ddev/db_snapshots/main-seed-"$3"-{mariadb,mysql,postgres}_*.{zst,gz,mbstream,xbstream})
[ "${#found[@]}" -gt 0 ] || exit 0
exec ddev snapshot "$2" --cleanup --name "main-seed-$3" --yes
```

## Bring up

The consumer reads every fenced block tagged `sh` under a `## Bring up` heading, in document order,
one command per line, and runs each as arguments from the worktree, never through a shell. This
first heading runs before `## Address`.

```sh
ddev start
ddev composer install
```

The worktree tracks `composer.lock` and, on most projects, not what it installs, so the site has no
code to serve until Composer runs.

## Address

One command, run in the worktree. Its standard output is `key: value` lines:

```sh
bash .aida/worktree-environment/address.sh
```

`address:` is the site's address, for example `https://add-login.ddev.site`, which review and
`baseline` export as `PLAYWRIGHT_BASE_URL`. `root:` is the directory DDEV resolved the project
from, and must be the worktree; the consumer stops here when it is not. `project:` is the
worktree's DDEV project name, kept as `{project}` for the second `## Bring up`, `## Tear down`
and the configuration gate of `drupal/standards-and-tests.md`.

## Bring up

This second heading runs after `## Address` has confirmed the project.

```sh
ddev snapshot {mainProject} --name main-seed-{project} --yes
ddev snapshot restore main-seed-{project}
ddev snapshot {mainProject} --cleanup --name main-seed-{project} --yes
ddev import-files --source {mainFiles}
ddev drush cr
ddev snapshot --cleanup --yes
ddev snapshot --name seed-{project} --yes
ddev snapshot --name gate-{project} --yes
```

The snapshot is taken in the main project under the name `main-seed-{project}` and restored in the
worktree by that name, without a path between them, which is DDEV's worktree support doing the
copy. The third line deletes it from the main checkout by name, right after the restore, before
`import-files` and the rest run. A bring-up that fails between the first line and the third can
leave `main-seed-{project}` in the main checkout. `## Preconditions` then refuses the next
bring-up until it is removed. An unnamed snapshot, restored with `--latest`, left one full copy of the main database in
the main checkout's `.ddev/db_snapshots/` on every bring-up, because nothing deleted it; two were
found and removed by hand. `--latest` also risked restoring whatever snapshot was newest across
every sibling worktree, which could be one the person had taken themselves, not the one bring-up
just took. `main-seed-{project}` is a different name from the worktree's own `seed-{project}`, so a
restore by name cannot pick up the wrong one from a sibling worktree's snapshot list. The cache
rebuild runs before the first request, because the restored cache tables were built under the main
hostname.

The last three lines keep the seeded database under the worktree's own names. The worktree
restores by name without reaching into the main checkout for a dated file, and the third line
then removes the main copy. The cleanup takes no name, so it
touches only the worktree's own snapshots and exits 0 when there are none; it removes the copies a
previous bring-up left, and the two snapshots that follow are never refused. `seed-{project}` is
the seed the configuration gate of `drupal/standards-and-tests.md` restores. `gate-{project}` is
the name that gate removes and retakes on every run; bring-up leaves it so the gate's first line,
which removes it by name, has something to remove and fails on a worktree not brought up this
way. The names carry `{project}`, the `project:` line `## Address` printed, for the reason the
gate gives: a bare name is looked up in sibling worktrees too. Apart from `main-seed-{project}`,
which bring-up names and removes, nothing in the main checkout is touched.

## Tear down

Run in the worktree, before `git worktree remove`. The last argument is `{project}`, the
`project:` line `## Address` printed at bring-up:

```sh
ddev delete --omit-snapshot --yes {project}
bash .aida/worktree-environment/main-seed-cleanup.sh {codePath} {mainProject} {project}
```

The second line removes `main-seed-{project}` from the main checkout when a bring-up failed
before its third line, so a task pruned and never brought up again leaves no copy of the main
database behind. It is a script, not `ddev snapshot {mainProject} --cleanup --name
main-seed-{project} --yes` on its own, because that command exits 1 when no such snapshot exists,
which is the normal case, and the consumer stops a tear-down at the first line that fails. A
line runs as arguments, so `|| true` is not available. It runs after `ddev delete` because it
needs only the main project and the worktree's files, which `ddev delete` leaves in place. A
worktree brought up before 0.6.1 does not hold the script: its project is deleted, then the
second line fails. Commit the script from `## Files` on the branch and tear down again, or
remove the snapshot by hand with the command above.

`--omit-snapshot` skips DDEV's pre-delete snapshot because the database is a copy the main
checkout still has. The worktree's files stay for `git worktree remove`.

An adopted site, one that was up before any bring-up of this task, is not torn down by a
consumer. Its database is no copy of the main checkout's, so `--omit-snapshot` is wrong for it,
and a snapshot DDEV takes on delete sits in the worktree's `.ddev/db_snapshots/`, which
`git worktree remove` deletes. A person decides whether that database may go. If they keep it,
they export it with `ddev export-db` to a file outside the worktree first, and then run the first
line. No bring-up of this task took `main-seed-{project}`, so `{mainProject}` has no value for
the second line. Run that line only when the main checkout holds that snapshot, with the main
project's name filled in by hand.

None of this may reach trunk. Merged without the `name:` line, the main checkout's DDEV project
is renamed to its folder name, only when that differs from the pinned name. The renamed project
gets a new, empty database. Merged with the scripts, trunk carries files only a worktree's
bring-up uses. The consumer's task completion handles both before the merge. It tears the site
down first, while the project still has the worktree's name. Then it commits on the branch each
file bring-up recorded, back at its content where the branch started. That puts the `name:` line
back in `.ddev/config.yaml` and removes the `## Files` scripts in `.aida/worktree-environment/`.

A person still acts in three cases:

- An order changed one of those files after bring-up, or one holds an uncommitted change.
  Completion then puts nothing back, and its warning names the files.
- The task records no point where the branch started. Completion's warning says so.
- The site was adopted. Completion leaves it up and still takes the `## Files` scripts off the
  branch. Adoption recorded no `name:` change, so a person checks `.ddev/config.yaml` by hand.
  The PR body names the adoption.

In the first two cases the person puts the files back by hand before the merge. A site adopted or kept up
comes down only by the person's choice, as above.

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
