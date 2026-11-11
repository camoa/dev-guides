---
# Routing block, first and in this order. Whoever is resolving reads to here and decides.
name: python_cli_worktree_environment
capability: worktree-environment
description: Use when a Python project managed by uv gives a task's git worktree an environment of its own. Says what must be true first, how to build the worktree's own .venv from the lock file, how to read where it is, how to tell whether it is there, and how to remove it.
# Metadata, read only after a match.
label: Worktree environment (Python CLI)
recipe_schema_version: 1.0.0
version: 0.1.0
recipe_class: process
framework: python-cli
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

A task built in its own git worktree gets a Python environment of its own: a `.venv` inside the
worktree, built from the project's lock file, with the project installed from the worktree's own
source. Files ship with a branch; an environment does not. Without this, the worktree has no
`.venv/bin/pytest`, so the test runner `python-cli/test-execution.md` resolves is missing, and a
run borrowed from the main checkout's environment imports the main checkout's code. With it,
the worktree's `.venv/bin/pytest` imports the branch's code.

The sections a consumer runs are read in document order: the one line under `## Preconditions`,
then `## Bring up`, then `## Address`. `## Status` says whether the environment is there, and
`## Tear down` removes it.

## Opinion

**uv builds the environment, from the committed lock file.** `uv sync --frozen` creates `.venv`
in the project root it is run from and installs exactly what `uv.lock` pins, without resolving
again and without writing the lock file. Run in the worktree, that root is the worktree, so the
environment is the worktree's own. A project whose `pyproject.toml` declares a `[build-system]` is
installed editable from the worktree's source, so an import reaches the branch's code and not the
main checkout's. uv installs no project that declares none; only its dependencies go in.

**Nothing is shared with the main checkout's environment.** Each checkout has its own `.venv`.
uv's package cache is shared, and that is fine: it holds downloaded files, not an environment.
`UV_PROJECT_ENVIRONMENT` is the one setting that moves the environment out of the project root,
so the check refuses while it is set.

**The address is the environment's path, not a URL.** The consumer requires an `address:` line.
For a command-line tool there is nothing served, so the address is the resolved path of the
environment `.venv/bin/python` runs in. It is exported as `PLAYWRIGHT_BASE_URL` like any
address; a command surface does not read it. `root:` is the directory holding that environment,
and the consumer stops when it is not the worktree.

**Bring-up is a person's choice.** `uv sync` needs the network the first time a package is
missing from the cache, and a second environment costs disk. A task that changes only
documentation has no use for one. The commands are shown once and run on a yes.

## Preconditions

- uv is on the PATH. Nothing in this recipe installs it.
- The worktree holds a pyproject file and a committed uv lock file. A frozen sync installs from
  the lock file and never writes it, so a project with no lock file is refused rather than
  locked on the fly, which would leave the tree dirty. The remedy is to run uv lock and commit
  the lock file on the branch the worktree has checked out.
- The uv project-environment variable is unset, so the environment is built at the worktree's
  own .venv and nowhere else.
- The line runs in a task worktree, never in the main checkout, whose environment is the one a
  worktree must not touch.

A trap for whoever edits this section: the consumer records every file this prose names in
backticks that the branch has changed, and completion puts each one back to its content where
the branch started. A task that adds a dependency changes the pyproject file and the lock file.
Named in backticks here, they would be reverted at completion and the task's own change lost, so
this section names no tracked file in backticks.

The checks a script can make are one line, run in the worktree after `## Files` is written and
before anything is committed, as arguments and never through a shell. It must exit 0. A non-zero
exit refuses the bring-up, prints the script's line, removes the files that run wrote, and commits
nothing:

```sh
bash .aida/worktree-environment/preconditions.sh {codePath}
```

The script checks, in order, that the main checkout is a directory, that the line is not running
in it, that uv is on the PATH, that the pyproject file and the lock file are there, and that the
project-environment variable is unset. One line names the first failure and what to do about it.

## Input contract

One token the consumer holds, and two the recipe produces:

```yaml
{codePath}: string   # the main checkout's path; the consumer fills it, in ## Preconditions
address: string      # ## Address: the resolved path of the worktree's environment
root: string         # ## Address: the directory holding it, which must be the worktree
```

No `## Tokens` section: no command here needs a value read from the main checkout.

## Sequence

1. **Show.** After `git worktree add`, the consumer prints the `## Preconditions` prose and the
   line it will run.

2. **Offer.** The consumer prints the `## Bring up` and `## Tear down` lines and the
   `## Build in place` prose, and asks once. A no writes nothing, and the task record says so.
   An autonomous run takes the no.

3. **Write, check, commit.** On a yes, the consumer writes the `## Files` where absent, then runs
   the `## Preconditions` line with `{codePath}` filled. A non-zero exit refuses the bring-up,
   removes the files that run wrote, and commits nothing. On exit 0 it commits the files on the
   task's branch.

4. **Build.** The consumer runs `## Bring up` in the worktree.

5. **Record and confirm.** The consumer runs `## Address`, stops when `root:` is not the
   worktree, and records `address:` as the task's address.

6. **Tear down.** When the task is pruned, the consumer runs `## Tear down` in the worktree, then
   `git worktree remove`.

## Data flow

```
input:  {codePath}                       held by the consumer

files (written where absent, committed after the check passes):
        .aida/worktree-environment/preconditions.sh, address.sh, status.sh

preconditions (in the worktree, before the commit):
        preconditions.sh {codePath}       → exit 0, or one line naming the first failure

bring up (in the worktree):
        uv sync --frozen                  → .venv, from uv.lock; the project installed editable
                                            when it declares a [build-system]

address (in the worktree):
        address.sh                        → address: <worktree>/.venv; root: <worktree>, checked

status (in the worktree):
        status.sh                         → exit 0 when .venv/bin/python runs from <worktree>/.venv

tear down (in the worktree, before git worktree remove):
        rm -rf .venv                      → the worktree's environment gone; files stay
```

## State-awareness contract

`uv sync --frozen` can run twice: on an environment that already matches the lock file it changes
nothing, and on one that drifts it brings it back to the lock file. Running `up` again is how a
task refreshes its environment after the lock file changes on the branch.

A worktree that already holds a working `.venv` when `up` first runs is adopted, not synced: the
`## Status` line exits 0, so the consumer records the address and runs no precondition and no
bring-up line, and a later `down` lets go of the environment instead of removing it. For a full
bring-up, remove that `.venv` first.

Adoption is the likely path, not an edge case: `uv run` in the worktree creates `.venv` on its
own. Run `up` before any `uv run`, or remove `.venv` first. Prune refuses an adopted tree until a
person removes `.venv` and runs `down` again; that second `down` runs `## Status`, which exits 1,
and the mark goes.

uv writes the environment inside `.venv` and no tracked file; the frozen sync never writes
`uv.lock`. A build backend that writes metadata into the source tree on an editable install, such
as setuptools' `*.egg-info`, leaves untracked files unless the project ignores them.

The three `## Files` are written once, where absent, and committed on the task's branch once the
`## Preconditions` line has exited 0. Completion removes them again before the branch merges,
because they did not exist where the branch started.

`## Tear down` removes `.venv` and exits 0 when there is none, so a repeat run changes nothing.

## Verifier

In the worktree, with uv on the PATH:

1. Before bring-up, `bash .aida/worktree-environment/preconditions.sh <main checkout>` prints
   nothing and exits 0. Run from the main checkout, with the uv project-environment variable set,
   with uv off the PATH, with a main checkout path that does not exist, or with no `uv.lock`, it
   prints one line saying which and exits 1.
2. Before bring-up, `bash .aida/worktree-environment/status.sh` prints that the environment is
   absent and exits 1.
3. After `uv sync --frozen`, `bash .aida/worktree-environment/address.sh` prints `address:`, the
   worktree's `.venv`, and `root:`, the worktree; `status.sh` exits 0.
4. `.venv/bin/pytest` runs the suite, and, on a project with a `[build-system]`,
   `.venv/bin/python -c "import <package>; print(<package>.__file__)"` prints a path inside the
   worktree.
5. `git status --short` in the worktree prints nothing, on a project that ignores `__pycache__/`
   and its build metadata. Step 4's import writes `__pycache__/` under the source tree.
6. After `## Tear down`, `status.sh` exits 1, and a second tear-down exits 0.

## Status

One command, run before a consumer's verify lines.

```sh
bash .aida/worktree-environment/status.sh
```

Exit 0 means the worktree's own environment is there and its interpreter runs. A non-zero exit
prints why.

## Files

Three scripts in `.aida/worktree-environment/`, written where absent, the path as the fence's
second word. They hold every command that needs a quote or a substitution, so each line the
consumer runs stays plain arguments.

```sh .aida/worktree-environment/preconditions.sh
#!/usr/bin/env bash
# Checks what must be true before this worktree gets a Python environment. $1 is the main checkout.
# One line names the first failure and exits 1; silence and exit 0 when everything holds.
main="$(cd "$1" 2>/dev/null && pwd -P)" || { echo "the main checkout $1 is not a directory"; exit 1; }
here="$(pwd -P)"
[ "$here" != "$main" ] || { echo "$here is the main checkout, not a task worktree; run this from the worktree"; exit 1; }
command -v uv >/dev/null || { echo "uv is not on PATH; install it as https://docs.astral.sh/uv/getting-started/installation/ says"; exit 1; }
[ -f pyproject.toml ] || { echo "no pyproject.toml in $here; this recipe is for a Python project uv manages"; exit 1; }
[ -f uv.lock ] || { echo "no uv.lock in $here; run uv lock and commit uv.lock on the branch this worktree has checked out"; exit 1; }
[ -z "${UV_PROJECT_ENVIRONMENT:-}" ] || { echo "UV_PROJECT_ENVIRONMENT is set to $UV_PROJECT_ENVIRONMENT, so uv would build the environment there and not in $here/.venv; unset it"; exit 1; }
```

```sh .aida/worktree-environment/address.sh
#!/usr/bin/env bash
# Prints the environment the worktree's .venv/bin/python runs in, as address:, and the directory
# holding it, as root:. Both are resolved, so a .venv that links to another checkout names that one.
prefix="$(.venv/bin/python -c 'import sys; print(sys.prefix)')" || exit 1
prefix="$(cd "$prefix" && pwd -P)" || exit 1
printf 'address: %s\nroot: %s\n' "$prefix" "$(dirname "$prefix")"
```

```sh .aida/worktree-environment/status.sh
#!/usr/bin/env bash
# Exits 0 when this worktree's own .venv holds a Python that runs; otherwise says why and exits 1.
here="$(pwd -P)"
[ -x .venv/bin/python ] || { echo "no environment: $here/.venv/bin/python is absent"; exit 1; }
prefix="$(.venv/bin/python -c 'import sys; print(sys.prefix)' 2>/dev/null)" || { echo "$here/.venv/bin/python does not run"; exit 1; }
[ "$(cd "$prefix" 2>/dev/null && pwd -P)" = "$here/.venv" ] || { echo "$here/.venv runs from $prefix, not from this worktree"; exit 1; }
```

## Bring up

The consumer reads every fenced block tagged `sh` under `## Bring up`, one command per line, and
runs each as arguments from the worktree, never through a shell.

```sh
uv sync --frozen
```

It installs the default dependency groups, which include `dev`, where a uv project keeps pytest
and the review tools. A project that keeps them in another group declares it as a default group
in `pyproject.toml`.

## Address

One command, run in the worktree. Its standard output is `key: value` lines:

```sh
bash .aida/worktree-environment/address.sh
```

## Tear down

Run in the worktree, before `git worktree remove`:

```sh
rm -rf .venv
```

On a `.venv` that is a link, it removes the link and not what it points to.

## Build in place

Every task on a Python command-line tool produces files on a branch, so none needs the main
checkout's environment. A task that changes no Python code, such as one on documentation alone,
has no use for an environment, and the person may decline the offer for it.

## References

| Reference | Why |
|---|---|
| [uv: Project environments and `uv sync`](https://docs.astral.sh/uv/concepts/projects/sync/) | `--frozen` installs from the lock file without checking or writing it; the environment is `.venv` in the project root |
| [uv: Environment variables](https://docs.astral.sh/uv/reference/environment/) | `UV_PROJECT_ENVIRONMENT` moves the project environment out of `.venv` |
| [uv: Dependency groups](https://docs.astral.sh/uv/concepts/projects/dependencies/#dependency-groups) | `dev` is synced by default; `default-groups` changes which groups are |
| `python-cli/test-execution.md` | Resolves the runner as `.venv/bin/pytest`, which this environment provides |
