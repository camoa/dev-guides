---
# Routing block, first and in this order. Whoever is resolving reads to here and decides.
name: drupal_worktree_environment
capability: worktree-environment
description: Use when a Drupal project on DDEV gives a task's git worktree a running site of its own. Says what must be true first, how to bring the site up and seed it from the main checkout with DDEV's own worktree support, how to read its address, how to tear it down, and which tasks build on the served checkout instead.
# Metadata, read only after a match.
label: Worktree environment (Drupal)
recipe_schema_version: 1.0.0
version: 0.3.1
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

- The worktree is a sibling of the main checkout, under the same parent directory, never a
  directory inside it. Its directory name is the project's name and hostname label. A consumer that finds the worktree under the code tree refuses bring-up and
  says why, because DDEV would run every command against the main project.
- `.ddev/config.yaml` is committed with no `name:` line, so each checkout is named after its
  directory. The check below refuses bring-up while the line is there and names it; the recipe
  never edits a committed file. The remedy is the person's: delete the line and commit, and run
  `ddev config global --omit-project-name-by-default` once so DDEV stops writing it into new
  projects, as its worktree post says.
- DDEV 1.25.4 or later: the sibling-worktree snapshot restore the seed depends on was observed on
  that version.
- The main checkout's DDEV project is running: `ddev list -j` shows one row whose `approot` is the
  main checkout with `status` `running`. The snapshot is taken from that project.
- Docker has room for a second web container, a second database container and a second database
  volume. `bash` and `jq` are on the host's `PATH`, for the three scripts under `## Files`.
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

The checks a script can make are one line, run in the worktree after `## Files` is written and
before anything is committed or a token runs, as arguments and never through a shell. It must exit
0. A non-zero exit refuses the bring-up, prints the script's line, removes the files that run
wrote, and commits nothing:

```sh
bash .aida/environment/preconditions.sh {codePath}
```

The script checks, in order, that the worktree is not inside `{codePath}`, that
`.ddev/config.yaml` is there with no `name:` line, that DDEV is 1.25.4 or later, that the main
checkout is a listed project with `status` `running`, and that the worktree's directory name is
lowercase letters, digits and hyphens. One line names the first failure and what to do about it.
`bash` and `jq` need no check: the script running is the check.

## Input contract

One token the consumer holds, and three the recipe produces, each a whole argument:

```yaml
{codePath}: string         # the main checkout's path; the consumer fills it, in ## Tokens only
{mainProject}: string      # ## Tokens: the main checkout's DDEV project name
{mainFiles}: string        # ## Tokens: the main site's public files directory, absolute
{project}: string          # ## Address, the project: line; kept in the task record for ## Tear down
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

5. **Seed.** The consumer runs the `## Bring up` after `## Address`: a snapshot of the main
   project, its restore in the worktree, the main files directory imported, and a cache rebuild
   so no cached page keeps the main hostname.

6. **Record the address.** The consumer keeps the `address:` line from the same `## Address`
   output as the task's address, and every other line as a token, so `project:` is
   `{project}`. Review and `baseline` export the address as `PLAYWRIGHT_BASE_URL` for
   that task and do not ask a person for one.

7. **Tear down.** When the task is pruned, the consumer runs `## Tear down` in the worktree
   first, and only then `git worktree remove`. A tear-down that exits non-zero leaves both the
   worktree and its project in place and says so, because removing the directory then would make
   the orphan the ordering exists to prevent.

## Data flow

```
input:  {codePath}                       held by the consumer

files (written where absent, committed after the check passes):
        .aida/environment/preconditions.sh, main-row.sh, main-project.sh, main-files.sh, address.sh

preconditions (in the worktree, before the commit):
        preconditions.sh {codePath}       → exit 0, or one line naming the first failure

tokens (in the worktree, before bring-up):
        main-project.sh {codePath}        → {mainProject}, from ddev list -j
        main-files.sh {codePath}          → {mainFiles}, from the same row

bring up, before ## Address (in the worktree):
        ddev start                        → the worktree's containers, named after the directory
        ddev composer install             → vendor/ and the installed directories, from the lock file

address (in the worktree):
        address.sh                        → root: checked; address: recorded; project: → {project}

bring up, after ## Address (in the worktree):
        ddev snapshot {mainProject}       → <main>/.ddev/db_snapshots/<main>_<time>-<db>.zst, DDEV-ignored
        ddev snapshot restore --latest    → the worktree database, from that sibling snapshot
        ddev import-files {mainFiles}     → the worktree's sites/default/files, replaced
        ddev drush cr                     → caches rebuilt under the worktree's hostname

tear down (in the worktree, before git worktree remove):
        ddev delete --omit-snapshot --yes {project}
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

The five `## Files` are written once, where absent, and refused where a file exists with other
content, the rule every setup recipe's files follow. The consumer commits them on the task's
branch once the `## Preconditions` line has exited 0 and before a token runs, so the tree is
clean for the stages that check it, and a refused bring-up leaves no file behind. A worktree made
after that branch merges carries them already.

Beyond those, nothing here writes a tracked file. `.ddev/db_snapshots/` is ignored by DDEV's own
`.ddev/.gitignore`; the worktree's `sites/default/files` is ignored by the same rule that ignores
the main checkout's. A `settings.ddev.php` DDEV writes at `ddev start` is one the main checkout
already ignores.

`## Tear down` names the project, so a repeat run reports the project as deleted and touches
nothing else; DDEV does not fail on a name it has already removed. A consumer runs the tear-down
only for a task whose record carries an address, which is the mark that bring-up ran.

## Verifier

In the worktree, with the main checkout running:

1. Before bring-up, `bash .aida/environment/preconditions.sh <main checkout>` prints nothing and
   exits 0. Run from a directory inside the checkout, from a project whose `.ddev/config.yaml`
   has a `name:` line, with a main checkout that is no listed project, or from a directory named
   `Bad_Name`, it prints one line saying which and exits 1.

After bring-up:

2. `ddev list -j` shows two rows with the main checkout's `approot` and the worktree's, each
   `running`, with different `name` and `primary_url` values.
3. `bash .aida/environment/address.sh` prints three lines, `address:`, `project:` and `root:`, the
   root being the worktree's path and the address `https://<worktree name>.ddev.site`; `curl -sSI`
   on that address returns `HTTP/2 200`.
4. `ddev drush status --field=uri` prints the worktree's address, and
   `ddev drush config:get system.site name` prints the same site name the main checkout does,
   which shows the database came across.
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
second bring-up left a second timestamped snapshot, and `--latest` picked it.

## Tokens

One fenced `sh` block per token, the token's name as the fence's second word, one command. The
consumer runs each in the worktree before the first `## Bring up`, as arguments and never through a
shell, with `{codePath}` filled whole, and takes the first line of standard output as the value. A
command that prints nothing, or exits non-zero, refuses the bring-up and names the token.

```sh mainProject
bash .aida/environment/main-project.sh {codePath}
```

```sh mainFiles
bash .aida/environment/main-files.sh {codePath}
```

Both scripts read the main checkout's row of DDEV's project list through `main-row.sh`, because
a pipe and a filter are more than one argument can say. A checkout that is not a listed project
prints nothing and exits 4, which is the refusal.

## Files

Five scripts, written where absent, the path as the fence's second word. They hold every DDEV and
`jq` invocation the checks, the tokens and the address need, so the consumer runs them and knows
neither. Paths are compared as the filesystem resolves them, in one place, because DDEV lists a
checkout under the path it was started from, and a consumer may hold that path with a trailing
slash or through a link.

```sh .aida/environment/preconditions.sh
#!/usr/bin/env bash
# Checks what must be true before this worktree gets a site. $1 is the main checkout.
# One line per failure, exit 1 at the first; silence and exit 0 when everything holds.
main="$(cd "$1" 2>/dev/null && pwd -P)" || { echo "the main checkout $1 is not a directory"; exit 1; }
here="$(pwd -P)"
case "$here" in
  "$main"/*) echo "the worktree $here is inside the checkout $main; DDEV hands a nested project to the outer one, so make the worktree a sibling: git worktree add ../<name>"; exit 1 ;;
esac
[ -f .ddev/config.yaml ] || { echo "no .ddev/config.yaml in $here; this recipe is for a DDEV project"; exit 1; }
line="$(grep -n '^name:' .ddev/config.yaml | head -1 | cut -d: -f1)"
if [ -n "$line" ]; then
  echo ".ddev/config.yaml:$line pins the project name, so every worktree would collide with it; delete that line and commit, and run 'ddev config global --omit-project-name-by-default' once so DDEV stops writing it"
  exit 1
fi
command -v ddev >/dev/null || { echo "ddev is not on PATH"; exit 1; }
version="$(ddev --version | sed 's/^ddev version v//')"
IFS=. read -r major minor patch <<<"${version%%-*}"
if [ "${major:-0}" -lt 1 ] || { [ "$major" -eq 1 ] && [ "${minor:-0}" -lt 25 ]; } || { [ "$major" -eq 1 ] && [ "$minor" -eq 25 ] && [ "${patch:-0}" -lt 4 ]; }; then
  echo "DDEV $version is older than 1.25.4, the version that restores a snapshot from a sibling worktree"
  exit 1
fi
status="$(bash "$(dirname "$0")/main-row.sh" "$1" | cut -f4)"
[ "$status" = "running" ] || { echo "the main checkout $1 is not a running DDEV project (status: ${status:-not listed}); run ddev start there first"; exit 1; }
name="$(basename "$here")"
case "$name" in
  *[!a-z0-9-]*) echo "the worktree directory name '$name' becomes a hostname label; use lowercase letters, digits and hyphens"; exit 1 ;;
esac
```

```sh .aida/environment/main-row.sh
#!/usr/bin/env bash
# Prints the DDEV project row for the checkout at $1 as "approot<TAB>name<TAB>docroot<TAB>status".
# Paths are compared as the filesystem resolves them, so a trailing slash or a symlink on either
# side still matches. Prints nothing and exits 4 when no listed project is that checkout.
want="$(cd "$1" 2>/dev/null && pwd -P)" || exit 4
while IFS=$'\t' read -r root name docroot status; do
  if [ "$(cd "$root" 2>/dev/null && pwd -P)" = "$want" ]; then
    printf '%s\t%s\t%s\t%s\n' "$root" "$name" "$docroot" "$status"
    exit 0
  fi
done < <(ddev list -j | jq -r '.raw[] | [.approot, .name, .docroot, .status] | @tsv')
exit 4
```

```sh .aida/environment/main-project.sh
#!/usr/bin/env bash
# Prints the DDEV project name of the checkout at $1.
bash "$(dirname "$0")/main-row.sh" "$1" | cut -f2
exit "${PIPESTATUS[0]}"
```

```sh .aida/environment/main-files.sh
#!/usr/bin/env bash
# Prints the public files directory of the checkout at $1: its approot, its docroot, sites/default/files.
row="$(bash "$(dirname "$0")/main-row.sh" "$1")" || exit $?
IFS=$'\t' read -r root _ docroot _ <<<"$row"
printf '%s/sites/default/files\n' "${root}${docroot:+/$docroot}"
```

```sh .aida/environment/address.sh
#!/usr/bin/env bash
# Prints the worktree project's address, name and root, one key per line, from where it is run.
ddev describe -j | jq -r '.raw | "address: \(.primary_url)\nproject: \(.name)\nroot: \(.approot)"'
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
bash .aida/environment/address.sh
```

`address:` is the site's address, for example `https://add-login.ddev.site`, which review and
`baseline` export as `PLAYWRIGHT_BASE_URL`. `root:` is the directory DDEV resolved the project
from, and must be the worktree; the consumer stops here when it is not. `project:` is the
worktree's DDEV project name, kept as `{project}` for `## Tear down`.

## Bring up

This second heading runs after `## Address` has confirmed the project.

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

## Tear down

Run in the worktree, before `git worktree remove`. The last argument is `{project}`, the
`project:` line `## Address` printed at bring-up:

```sh
ddev delete --omit-snapshot --yes {project}
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
