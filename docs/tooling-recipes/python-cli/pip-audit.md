---
# Routing block, first and in this order. Whoever is resolving reads to here and decides.
name: python_cli_pip_audit_tooling
capability: pip-audit
description: Use when a Python CLI project needs pip-audit installed in its own virtual environment to audit its dependencies for known vulnerabilities. Says how to install it and how to run it.
# Metadata, read only after a match.
label: pip-audit (Python CLI)
recipe_schema_version: 1.0.0
version: 0.1.0
recipe_class: tooling
framework: python-cli
authors:
  - name: camoa
license: GPL-2.0-or-later
---

# pip-audit (Python CLI)

## Goal

pip-audit checks installed Python distributions against the Python Packaging
Advisory Database and reports each one with a known vulnerability. Run with no
arguments, it audits the environment it is installed in. With it installed,
`python-cli/checks.md`'s `security` row has a binary to run.

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
.venv/bin/python -m pip install pip-audit
```

pip-audit 2.10.1 brings 27 packages of its own into a fresh environment,
among them `requests`, `rich` and `cyclonedx-python-lib`. The audit reads them
along with the project's own dependencies, because they are installed in the
same environment.

The audit also reads the pip the first step put there. `ensurepip` installs the
pip bundled with the interpreter, which can be old. On a `uv venv` under Python
3.11.15 it installed pip 24.0 and setuptools 79.0.1, and pip-audit 2.10.1
reported `Found 15 known vulnerabilities in 2 packages` and exited 1.

With no `.venv` in the project root, the first step fails with the shell's own
not-found message. Create the environment the way the project already does,
then install again.

On a project that `uv` manages, these steps last only until the next
`uv sync`. Verified on uv 0.13.7: `uv sync` removes every package
`pyproject.toml` does not declare, pip-audit and pip included. Such a project
declares pip-audit in its dev dependency group instead, which `uv sync` then
keeps:

```text
uv add --dev pip-audit
```

## Run

```sh
.venv/bin/pip-audit --version
```

`python-cli/checks.md`'s `security` row runs this same binary,
`.venv/bin/pip-audit`, so this check proves the row has its tool. Neither looks
on `PATH`, where a pip-audit installed elsewhere would audit the environment it
lives in, not the project's.

Exit 0 with a line reading `pip-audit <version>` means the project's
environment holds pip-audit. Verified on pip-audit 2.10.1, installed with pip
26.2.2 under Python 3.15.2.

The row itself runs `.venv/bin/pip-audit` with no arguments. In the throwaway
project it printed `No known vulnerabilities found` and exited 0. It exits 1
when it finds a known vulnerability. It needs network access to reach the
advisory data.

If `.venv/bin/pip-audit` is absent, the command exits 127: install, then run
it again.
