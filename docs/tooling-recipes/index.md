---
description: Tooling recipes — one tool per framework, saying what the tool is, how to install it, and how to run it. Nothing about the project's pages, layers, or design.
---

# Tooling Recipes

> A **separate class** from [process recipes](../process-recipes/index.md) and [agentic (task) recipes](../agentic-recipes/index.md). A **tooling recipe** puts one tool on disk for one framework and says how to invoke it. That is its whole scope.

The other two classes name their tools constantly and assume they are already there. A project with no test runner cannot observe a failing test, so test-first is unfalsifiable. A review that wants a static-analysis reading with no analyser present reports the tool as absent, permanently, because nothing installs it. This class closes that gap and nothing else.

A tooling recipe is named for its tool, and whatever needs the tool refers to it by that name. It knows nothing about the project's pages, its layers, or its design.

## Why three headings

| Heading | What it holds |
|---|---|
| `Goal` | What the tool is, and what a project gets by having it |
| `Install` | The commands that add it, in order |
| `Run` | The command that invokes it, and where the result appears |

**Run is also the check.** Whoever needs the tool runs the Run command, and a "not found" is the answer that the tool is missing — install, then run it again. Nothing records whether a tool is present, because a stored answer goes stale the moment someone removes the package.

**There is no preconditions section.** If an install step needs Composer and Composer is absent, the step fails with Composer's own message, which is more useful than anything written here in advance and one less thing to keep true.

## How install steps run

Each step runs as arguments, never through a shell. A step containing a shell metacharacter is refused rather than run to mean something its author did not intend — write two steps instead of joining them with `&&`.

Every step is safe to run twice, because a project may already have part of what the tool needs.

## Catalog

| Framework | Tool | Recipe |
|---|---|---|
| `drupal` | `phpcs` | [PHP_CodeSniffer](drupal/phpcs.md) |
| `drupal` | `phpstan` | [PHPStan](drupal/phpstan.md) |
