---
description: "Source references and maintenance manifest for the tool api guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install

Path: not configured for this guide. Code was read from source clones at release tags (tool `1.0.0-beta11`, tool_belt `1.0.0-alpha6`, mcp_server_tool_bridge `1.0.0-beta3`, mcp_server `2.0.0-beta5`), from eca_tool `1.0.0-beta1` through the GitLab raw file API, and from a Drupal core 11.4.5 codebase with ECA 3.1 installed. Paths below are Drupal-relative.

## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Tool project page | https://www.drupal.org/project/tool | What Tool API Is, Installation and Submodules | 2026-10-01 |
| Tool release feed (1.0.0-beta11, 2026-10-01) | https://updates.drupal.org/release-history/tool/current | Header, Installation and Submodules | 2026-10-01 |
| Tool repository | https://git.drupalcode.org/project/tool | All code-based sections | 2026-10-01 |
| Tool documentation site (published from the repository's `docs/` folder; the URL answers 308 to a `pages.drupalcode.org` host) | https://project.pages.drupalcode.org/tool | All sections; same content as the docs files listed under Code Sources | 2026-10-01 |
| [META] Path to 1.0.0-rc1 (#3582978) | https://git.drupalcode.org/project/tool/-/work_items/3582978 | Preparing for Tool API 1.0.0-rc1, checkRequirements | 2026-10-01 |
| Define checkRequirements() as a configuration-time signal (#3582975, closed 2026-08-10) | https://git.drupalcode.org/project/tool/-/work_items/3582975 | checkRequirements | 2026-10-01 |
| META: make Tool's declarations introspectable over the CLI (#3582943, closed 2026-09-24) | https://git.drupalcode.org/project/tool/-/work_items/3582943 | Calling a Tool from Drush | 2026-10-01 |
| Deprecate `multiple` (#3583049) | https://git.drupalcode.org/project/tool/-/work_items/3583049 | Preparing for Tool API 1.0.0-rc1, Input Definitions | 2026-10-01 |
| Remove the output acceptance shim kept from #3583015 (#3583050, open) | https://git.drupalcode.org/project/tool/-/work_items/3583050 | Preparing for Tool API 1.0.0-rc1, Output Definitions | 2026-10-01 |
| Required outputs not enforced (#3583029, closed 2026-09-24) | https://git.drupalcode.org/project/tool/-/work_items/3583029 | Calling a Tool over MCP | 2026-10-01 |
| Tool Belt project | https://www.drupal.org/project/tool_belt | Tool Belt Catalog | 2026-10-01 |
| ECA Tool project | https://www.drupal.org/project/eca_tool | Calling a Tool from ECA | 2026-10-01 |
| ECA Tool release feed (1.0.0-beta1, 2026-09-22) | https://updates.drupal.org/release-history/eca_tool/current | Calling a Tool from ECA | 2026-10-01 |
| ECA Tool repository (tag `1.0.0-beta1`: `composer.json`, `README.md`, `src/ToolEvents.php`, `src/Plugin/ECA/Event/EcaToolEvent.php`, `src/Plugin/Action/Tool.php`, `src/Plugin/Action/ToolDeriver.php`) | https://git.drupalcode.org/project/eca_tool | Calling a Tool from ECA, checkRequirements, Operation and Destructive | 2026-10-01 |
| MCP Server Tool Bridge project | https://www.drupal.org/project/mcp_server_tool_bridge | Calling a Tool over MCP | 2026-10-01 |
| Matt Glaman, "Define the capability once; call it from anywhere" (2026-09-15). Background for the why only; its API detail is outdated for beta11: #3582943 is closed, `checkAccess()` is no longer abstract, and its `checkAccess()` sketch lacks `$return_as_object` | https://mglaman.dev/blog/define-capability-once-call-it-anywhere | What Tool API Is | 2026-10-01 |
| OWASP API Security Top 10 | https://owasp.org/API-Security/ | Security Checklist | 2026-10-01 |

## Code Sources

| Module | Relative Path | Guide Sections | Version |
|--------|---------------|----------------|---------|
| Tool (base module) | modules/contrib/tool/ | All sections | 1.0.0-beta11 |
| Tool README | modules/contrib/tool/README.md | What Tool API Is, Installation and Submodules | 1.0.0-beta11 |
| Tool docs: overview | modules/contrib/tool/docs/index.md | What Tool API Is | 1.0.0-beta11 |
| Tool docs: installation | modules/contrib/tool/docs/installation.md | Installation and Submodules | 1.0.0-beta11 |
| Tool docs: configuration and access | modules/contrib/tool/docs/configuration.md | Access Control, Installation and Submodules, Tool Explorer | 1.0.0-beta11 |
| Tool docs: developer overview and invoker sequence | modules/contrib/tool/docs/developers/index.md | Calling a Tool from PHP, Access Control | 1.0.0-beta11 |
| Tool docs: creating a tool (operations table wrong on Transform idempotency) | modules/contrib/tool/docs/developers/creating-a-tool.md | Defining a Tool, Operation and Destructive | 1.0.0-beta11 |
| Tool docs: input and output definitions | modules/contrib/tool/docs/developers/input-output-definitions.md | Input Definitions, Output Definitions | 1.0.0-beta11 |
| Tool docs: entity handles | modules/contrib/tool/docs/developers/entity-handles.md | Entity Inputs and Handles | 1.0.0-beta11 |
| Tool docs: events | modules/contrib/tool/docs/developers/events.md | Calling a Tool from PHP | 1.0.0-beta11 |
| Tool docs: Drush commands | modules/contrib/tool/docs/usage/drush.md | Calling a Tool from Drush, checkRequirements | 1.0.0-beta11 |
| Tool docs: AI function calling (map "alter hook" claim not in code) | modules/contrib/tool/docs/usage/ai-function-calling.md | Calling a Tool from the AI Module | 1.0.0-beta11 |
| Tool docs: Tool Explorer | modules/contrib/tool/docs/usage/tool-explorer.md | Tool Explorer | 1.0.0-beta11 |
| Tool docs: agent skills | modules/contrib/tool/docs/usage/agent-skills.md | Defining a Tool | 1.0.0-beta11 |
| Tool docs: modules using Tool API | modules/contrib/tool/docs/ecosystem/modules-using-tool-api.md | Calling a Tool from ECA | 1.0.0-beta11 |
| Tool docs: sources of tools | modules/contrib/tool/docs/ecosystem/sources-of-tools.md | Tool Belt Catalog | 1.0.0-beta11 |
| Tool agent skill reference (stale on `checkAccess()` and the constructor) | modules/contrib/tool/.agents/skills/create-tool-plugins/references/anatomy.md | Defining a Tool, Input Definitions | 1.0.0-beta11 |
| Tool hooks and handle docs | modules/contrib/tool/tool.api.php | Entity Inputs and Handles, Preparing for Tool API 1.0.0-rc1 | 1.0.0-beta11 |
| Tool - AI Connector | modules/contrib/tool/modules/tool_ai_connector/ | Calling a Tool from the AI Module, Entity Inputs and Handles | 1.0.0-beta11 |
| Tool Explorer | modules/contrib/tool/modules/tool_explorer/ | Tool Explorer | 1.0.0-beta11 |
| Tool Belt | modules/contrib/tool_belt/ | Tool Belt Catalog, Defining a Tool, Access Control, checkRequirements | 1.0.0-alpha6 |
| MCP Server Tool Bridge | modules/contrib/mcp_server_tool_bridge/ | Calling a Tool over MCP, Access Control, doExecute and ExecutableResult | 1.0.0-beta3 |
| MCP Server (attribute and plugin manager only) | modules/contrib/mcp_server/src/Attribute/Tool.php, modules/contrib/mcp_server/src/Plugin/ToolPluginManager.php | Tool API vs FunctionCall, MCP and ECA Tools | 2.0.0-beta5 |
| ECA Tool | modules/contrib/eca_tool/ | Calling a Tool from ECA | 1.0.0-beta1 |
| ECA base events | modules/contrib/eca/modules/base/src/BaseEvents.php | Tool API vs FunctionCall, MCP and ECA Tools | 3.1 |
| Core plugin discovery | core/lib/Drupal/Core/Plugin/DefaultPluginManager.php, core/lib/Drupal/Component/Plugin/Discovery/DerivativeDiscoveryDecorator.php | Defining a Tool | 11.4.5 |
| Core executable interface | core/lib/Drupal/Core/Executable/ExecutableInterface.php | What Tool API Is | 11.4.5 |
| Core ContextException | core/lib/Drupal/Component/Plugin/Exception/ContextException.php | Input Definitions | 11.4.5 |
