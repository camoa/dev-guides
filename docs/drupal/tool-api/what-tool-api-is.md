---
description: "What Drupal Tool API is: a plugin type plus a runtime that declares one operation once for Drush, PHP, AI, ECA and MCP callers, and why it is not core Actions"
tldr: "Use a Tool API plugin when one operation must be callable from Drush, PHP, AI function calling, ECA and MCP. A tool extends ToolBase with the #[Tool] attribute. Gotcha: the module is beta and ships no tools of its own."
drupal_version: "^10.5 || ^11"
---

# What Tool API Is

## When to Use

> Read this first to decide whether an operation belongs in a Tool API plugin. A tool declares one operation once, with typed inputs, typed outputs and an access rule, and every caller runs that same declaration.
>
> **Version:** applies to `drupal/tool` 1.0.0-beta11 (beta; no security advisory coverage). Paths are under `modules/contrib/tool/`.

## Decision

Tool API is a **plugin type plus a runtime**. A tool is a class with the `#[Tool]` attribute that extends `ToolBase`. The runtime validates inputs, checks access, runs the tool and shapes the result for the caller. Deterministic callers (Drush, your own PHP), non-deterministic callers (AI function calling) and remote callers (MCP) all run the same plugin (tool 1.0.0-beta11 `README.md`, `docs/index.md`).

| If you need... | Use... | Why |
|---|---|---|
| One operation callable from Drush, PHP, AI function calling, ECA and MCP | A Tool API plugin | One definition carries typed inputs, typed outputs, an access rule and a result message |
| A bulk operation for Views bulk operations or an action config entity | A core Action plugin | Those core systems consume Action plugins, not tools |
| A function that only makes sense inside the AI module | An AI module `#[FunctionCall]` plugin | Recommendation: prefer a tool when any non-AI caller could use it, because `tool_ai_connector` exposes tools to the AI module anyway |
| Ready-made tools for common core tasks | `drupal/tool_belt` | See [Tool Belt Catalog](tool-belt-catalog.md) |

## Why Not Core Actions

The project page names two gaps in core Actions: "Input is loosely defined; outputs do not exist" and "Inputs, forms and configuration are defined separately, with nothing binding them together" (https://www.drupal.org/project/tool). Core's `ExecutableInterface::execute()` is still untyped in core 11.4.5 (`core/lib/Drupal/Core/Executable/ExecutableInterface.php`), so `ToolInterface` declares its own `execute(): static` ([#3582964](https://git.drupalcode.org/project/tool/-/work_items/3582964)).

What a tool has that an Action does not: typed input definitions validated before execution, declared outputs, an `operation` that says whether the tool modifies state, per-invocation access that sees the input values, and a result object with a message and a failure category.

## Common Mistakes

- Treating Tool API as stable. It is beta and the API changes until rc1 → pin the version in `composer.json` and read [Preparing for Tool API 1.0.0-rc1](what-changes-at-rc1.md) before each update
- Expecting the module to ship tools. It ships none → install a catalog such as `tool_belt` or write your own

## See Also

- [Tool API vs FunctionCall, MCP and ECA Tools](which-tool-this-guide-means.md) → terminology
- [Defining a Tool](defining-a-tool.md) → the plugin itself
- Background: Matt Glaman, "Define the capability once; call it from anywhere" (2026-09-15), on why a new plugin type beat extending Actions; parts of its API detail are outdated for beta11
- Reference: `modules/contrib/tool/README.md`, `modules/contrib/tool/docs/index.md`, `modules/contrib/tool/src/Tool/ToolInterface.php`, https://www.drupal.org/project/tool
