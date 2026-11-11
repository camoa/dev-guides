---
# Routing block, first and in this order. Whoever is resolving reads to here and decides.
name: python_cli_ruff_tooling
capability: ruff
description: Use when a Python CLI project needs the Ruff linter and formatter installed in its own virtual environment. Says how to install it and how to run it.
# Metadata, read only after a match.
label: Ruff (Python CLI)
recipe_schema_version: 1.0.0
version: 0.1.0
recipe_class: tooling
framework: python-cli
authors:
  - name: camoa
license: GPL-2.0-or-later
---

# Ruff (Python CLI)

## Goal

Ruff lints and formats Python from one binary, configured from one `[tool.ruff]`
section of `pyproject.toml`. `ruff check` reports each place the code breaks a
selected rule, and `ruff format --check` lists each file it would reformat
without writing it. With it installed, `python-cli/checks.md`'s
`coding-standards` row has a binary to run.

## Install

The Python CLI recipes keep the project's tools in a virtual environment at
`.venv/` in the project root, and assume nothing about what created it. A
`.venv` made by `uv venv` holds no pip, so the first step puts pip there. On a
`.venv` that already has pip, it prints `Requirement already satisfied` and
exits 0.

```sh
.venv/bin/python -m ensurepip
```

```sh
.venv/bin/python -m pip install ruff
```

With no `.venv` in the project root, the first step fails with the shell's own
not-found message. Create the environment the way the project already does,
then install again.

On a project that `uv` manages, these steps last only until the next
`uv sync`. Verified on uv 0.13.7: `uv sync` removes every package
`pyproject.toml` does not declare, Ruff and pip included. Such a project
declares Ruff in its dev dependency group instead, which `uv sync` then keeps:

```text
uv add --dev ruff
```

## Run

```sh
.venv/bin/ruff --version
```

`python-cli/checks.md`'s `coding-standards` row runs this same binary,
`.venv/bin/ruff`, so this check proves the row has its tool. Neither looks on
`PATH`: in the throwaway project this recipe was verified in, a user-wide
`ruff` printed `ruff 0.15.0` while `.venv/bin/ruff --version` printed
`ruff 0.17.4`.

Exit 0 with a line reading `ruff <version>` means the project's environment
holds Ruff. Verified on Ruff 0.17.4, installed with pip 26.2.2 under Python
3.15.2.

If `.venv/bin/ruff` is absent, the command exits 127: install, then run it
again.
