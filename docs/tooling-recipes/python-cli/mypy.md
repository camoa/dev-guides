---
# Routing block, first and in this order. Whoever is resolving reads to here and decides.
name: python_cli_mypy_tooling
capability: mypy
description: Use when a Python CLI project needs the mypy type checker installed in its own virtual environment. Says how to install it and how to run it.
# Metadata, read only after a match.
label: mypy (Python CLI)
recipe_schema_version: 1.0.0
version: 0.1.0
recipe_class: tooling
framework: python-cli
authors:
  - name: camoa
license: GPL-2.0-or-later
---

# mypy (Python CLI)

## Goal

mypy reads Python's type annotations without running the code and reports each
place a value cannot have the type its use requires. It reads what to check, and
how strictly, from `[tool.mypy]` in `pyproject.toml`. With it installed,
`python-cli/checks.md`'s `static-analysis` row has a binary to run.

mypy belongs in the project's own environment, not beside it. It follows each
import into the installed package it names, so a mypy outside the environment
cannot see the project's dependencies and reports them as missing.

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
.venv/bin/python -m pip install mypy
```

With no `.venv` in the project root, the first step fails with the shell's own
not-found message. Create the environment the way the project already does,
then install again.

On a project that `uv` manages, these steps last only until the next
`uv sync`. Verified on uv 0.13.7: `uv sync` removes every package
`pyproject.toml` does not declare, mypy and pip included. Such a project
declares mypy in its dev dependency group instead, which `uv sync` then keeps:

```text
uv add --dev mypy
```

## Run

```sh
.venv/bin/mypy --version
```

`python-cli/checks.md`'s `static-analysis` row runs this same binary,
`.venv/bin/mypy`, so this check proves the row has its tool. Neither looks on
`PATH`, where a mypy installed elsewhere could not import the project's
dependencies.

Exit 0 with a line reading `mypy <version> (compiled: yes)` means the
project's environment holds mypy. Verified on mypy 2.4.1, installed with pip
26.2.2 under Python 3.15.2.

The row itself runs `.venv/bin/mypy` with no arguments, which reads `files`
and `strict` from `[tool.mypy]`. In the throwaway project, with
`files = ["src"]` declared, it printed `Success: no issues found in 1 source
file`.

If `.venv/bin/mypy` is absent, the command exits 127: install, then run it
again.
