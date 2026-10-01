---
description: "Drupal Tool API (drupal/tool) — define a typed operation once as a #[Tool] plugin and call it from Drush, PHP, the AI module, ECA and MCP"
tracks:
  - project: tool
    channel: alpha
    reason: no stable release exists; 1.0.x is beta-only
    declared: "1.0.0-beta11"
    verified: 2026-10-01
guide-meta:
  concepts:
    - Tool API
    - drupal/tool
    - "#[Tool] attribute"
    - ToolBase
    - ToolManager
    - plugin.manager.tool
    - ToolOperation
    - destructive
    - InputDefinition
    - EntityInputDefinition
    - ListInputDefinition
    - MapInputDefinition
    - OutputDefinition
    - InputDefinitionRefinerInterface
    - ExecutableResult
    - FailureCategory
    - doExecute
    - checkAccess
    - checkRequirements
    - RequirementsException
    - Invoker
    - InvokerCapability::EntitiesAsHandles
    - entity handles
    - getFormattedResult
    - drush tool:run
    - drush tool:list
    - drush generate plugin:tool
    - tool_explorer
    - tool_ai_connector
    - tool_belt
    - eca_tool
    - mcp_server_tool_bridge
    - 1.0.0-rc1 deprecations
  not:
    - MCP Server native tool plugins (Drupal\mcp_server\Attribute\Tool — see drupal/mcp-server)
    - AI module FunctionCall plugins (see drupal/ai-module)
    - Core Action plugins
    - ECA eca_base.tool event (see drupal/orchestration)
    - Orchestration orchestration_tool provider (see drupal/orchestration)
  requires:
    - drupal/plugins
  complements:
    - drupal/ai-module
    - drupal/orchestration
    - drupal/mcp-server
    - drupal/eca
  category: drupal
---

# Tool API

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Know what Tool API is and why it is not core Actions | [What Tool API Is](what-tool-api-is.md) | Use a Tool API plugin when one operation must be callable from Drush, PHP, AI function calling, ECA and MCP. A tool extends ToolBase with the #[Tool] attribute. Gotcha: the module is beta and ships no tools of its own. |
| Tell a Tool API tool from FunctionCall, MCP and ECA tools | [Tool API vs FunctionCall, MCP and ECA Tools](which-tool-this-guide-means.md) | The word tool names five Drupal mechanisms. A Tool API tool uses the #[Tool] attribute from the tool module and extends ToolBase. Gotcha: mcp_server ships its own #[Tool] attribute, and ECA 3.1 removed eca_base.tool. |
| Install the module and pick submodules | [Installation and Submodules](installation-and-submodules.md) | Require drupal/tool pinned to the beta, enable the base module, then only the submodules whose callers you need. Gotcha: the two permissions gate only Tool Explorer; each tool's own access rule gates execution. |
| Write a tool plugin and fill in `#[Tool]` | [Defining a Tool](defining-a-tool.md) | A tool lives in src/Plugin/tool/Tool, carries #[Tool] and extends ToolBase; inject services by overriding create(). Gotcha: one tool with no permission and no checkAccess() override breaks discovery for every tool. |
| Pick the right `operation` and decide on `destructive` | [Operation and Destructive](operation-and-destructive.md) | Set operation by the tool's worst side effect: Write or Trigger for anything that modifies state, plus destructive: TRUE for deletes. Gotcha: both are metadata; Tool API enforces neither, so enforce safety in access and code. |
| Declare inputs: types, required, constraints, lists, maps | [Input Definitions](input-definitions.md) | Declare inputs with the typed-data definition classes; they drive validation, forms and the JSON Schema callers see. Gotcha: required defaults to TRUE, and an empty list or map still passes required; add NotBlank or Count. |
| Declare outputs and know what reaches the caller | [Output Definitions](output-definitions.md) | Declare every returned key with an output definition class. Gotchas: required defaults to TRUE, so a missing output turns success into a Runtime failure, and undeclared result keys still reach Drush, AI and MCP callers raw. |
| Take or return an entity | [Entity Inputs and Handles](entity-inputs-and-handles.md) | An entity input receives the loaded entity; AI and MCP invokers with EntitiesAsHandles pass handle:<uuid> strings instead. Gotcha: Drush cannot pass entities, so a tool for scripts should take an entity type and ID. |
| Write `doExecute()` and return a result | [doExecute and ExecutableResult](doexecute-and-executableresult.md) | doExecute() receives validated values and returns ExecutableResult::success() or failure() with a FailureCategory. Gotcha: failure() defaults to Input, which tells a model to retry; never return exception messages to callers. |
| Control who may run a tool | [Access Control](access-control.md) | Declare permission for account-level rules and override checkAccess() for rules on input values; access() runs permission, then validation, then checkAccess(). Gotcha: the override must keep the return_as_object parameter. |
| Report missing configuration | [checkRequirements](checkrequirements.md) | Throw RequirementsException from checkRequirements() for missing deployment config such as a module or API key. Gotcha: it is a configuration-time signal; execute() and access() never call it, so re-check blockers in doExecute(). |
| Scaffold a tool with Drush | [Scaffolding with drush generate](scaffolding-with-drush-generate.md) | Run drush generate plugin:tool to write the plugin plus unit and kernel tests. Gotcha: the generated checkAccess() throws LogicException until you define access, and the generated catch returns exception messages to callers. |
| Call a tool from Drush | [Calling a Tool from Drush](calling-a-tool-from-drush.md) | Use tool:list, tool:search and tool:info to inspect tools, and tool:run with --input and --json to run one. Gotcha: tool:run runs as anonymous unless you pass --uid, and the drush invoker cannot pass entity inputs. |
| Call a tool from PHP or a controller | [Calling a Tool from PHP](calling-a-tool-from-php.md) | Call checkPermission(), setInputValue(), validateInputs(), access() and execute() in that order, then read getResult() or getFormattedResult(). Gotcha: execute() does not check access; your code is the gate. |
| Expose tools to the AI module | [Calling a Tool from the AI Module](calling-a-tool-from-the-ai-module.md) | Enable tool_ai_connector to turn every tool into an AI function named tool__ plus the ID with colons replaced by __. Gotcha: it exposes every tool and ignores operation, destructive and requirements; scope agent tool lists. |
| Run tools from ECA | [Calling a Tool from ECA](calling-a-tool-from-eca.md) | Install drupal/eca_tool to run tools as ECA actions (eca_tool:<tool_id>) and to expose ECA models as tools through its Tool event. Gotcha: it needs core 11.3 or later, and its Tool event defaults to a destructive write. |
| Make a tool ready for MCP | [Calling a Tool over MCP](calling-a-tool-over-mcp.md) | MCP exposure is opt-in per tool through an mcp_tool_config entity, and content entities travel as handles. Gotcha: the bridge does not pre-check the declared permission, so keep refiners and input transforms free of side effects. |
| Browse and run tools in the admin UI | [Tool Explorer](tool-explorer.md) | Enable tool_explorer to browse tools at /admin/config/tool/explorer and run one from a form. Gotcha: the execute form skips validateInputs(), so invalid input reads as access denied, and it never shows outputs. |
| Use ready-made tools instead of writing my own | [Tool Belt Catalog](tool-belt-catalog.md) | Check tool_belt 1.0.0-alpha6 before writing a tool for a common core task; it ships 58 tools in eight submodules. Gotcha: tool_belt:entity_save saves without entity validation; use entity_create or entity_update. |
| Prepare for 1.0.0-rc1 | [Preparing for Tool API 1.0.0-rc1](what-changes-at-rc1.md) | Before updating drupal/tool, replace multiple: TRUE with List definitions, declare outputs with output classes, rename the adapter alter hook and drop ExecutableResultInterface. Gotcha: rc1 removes the conversion shims. |
| Review a tool for security | [Security Checklist](security-best-practices.md) | Before exposing tools to AI, MCP or scripts, check access rules, failure messages, undeclared outputs, entity validation, honest operation labels and who holds administer tool. Gotcha: operation Read is not enforced. |
| Keep tools fast | [Performance Checklist](performance-best-practices.md) | Keep create() and checkRequirements() cheap, filter catalogs with static checkPermission(), cache expensive Read tools inside doExecute() and page list tools. Gotcha: Tool API never caches tool results. |
| Check sources and versions | [Sources & Maintenance Manifest](sources-maintenance.md) | Source references and maintenance manifest for the tool api guides — web sources, code sources, and version history |
