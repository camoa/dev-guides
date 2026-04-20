---
description: AI Agents — ReAct loop, config entities, tool usage, orchestration, and security
tldr: "Use this guide when building autonomous AI agents that make decisions. Use [AI Automators](ai-automators.md) for fixed field-population workflows that don't need autonomous decision-making."
drupal_version: "11.x"
---

# AI Agents

## When to Use

> Use this guide when building autonomous AI agents that make decisions. Use [AI Automators](ai-automators.md) for fixed field-population workflows that don't need autonomous decision-making. Use [AI Assistant API](ai-assistant-api.md) to expose an agent as a standard assistant.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Fixed content generation workflow | Automators | Simpler, lower cost, no reasoning loop |
| Dynamic decision-making | Agents | Agent decides which tools to use |
| Expose agent to chat UI | Config entity + Assistant | `ai_agent` field on `ai_assistant` entity |
| Multi-step orchestration | Agents-as-tools | Sub-agents have isolated memory |
| High-stakes production site | Avoid MCP tools | Tool description injection risk |

## Pattern

```php
$agent = \Drupal::service('plugin.manager.ai_agents')->createInstance('field_agent');
$input = new ChatInput([new ChatMessage('user', 'Create a Tags vocabulary')]);
$agent->setChatInput($input);
$agent->determineSolvability();
$output = $agent->solve();

// Get tool results.
$results = $agent->getToolResults(FALSE);
$specific = $agent->getToolResultsByPluginId('entity_create_tool');
```

## Agent Loop

```
System prompt + instructions + tools + memory
  -> LLM decides: use tool OR write final response
  -> If tool: execute, store result in memory, loop again
  -> If text: return to caller, stop
```

## Configuration

| Field | Purpose |
|-------|---------|
| Description | Critical — orchestrating agents read this to decide when to call |
| Max Loops | Default 3; prevents runaway loops; use 3-5 for most cases |
| Agent Instructions | System prompt (supports tokens); write 4+ sentences |
| Default Information Tools | Auto-run each loop without LLM decision (YAML config) |
| Tools | Available tools + other agents (agents-as-tools) |

## Default Information Tools YAML

```yaml
site_context:
  label: 'Current site info'
  description: 'Provides site context'
  tool: 'site_info_tool'
  parameters:
    format: 'summary'
  available_on_loop: [1]  # Only run on first loop
```

## Tool Usage Settings

| Setting | Effect |
|---------|--------|
| Return Directly | Skip text generation; return raw tool output |
| Require Usage | Force tool to be called at least once |
| Property Restrictions | `Allow all` / `Only allow` / `Force value` |
| Use Artifact Storage | Store in artifact token to reduce tokens |

## Progress Polling

```php
$agent->setProgressThreadId('unique-id');
$agent->setDetailedProgressTracking([
  AiAgentStatusItemTypes::Started,
  AiAgentStatusItemTypes::ToolStarted,
]);
$agent->solve();

$progress = \Drupal::service('ai_agents.agent_status_poller')
  ->getLatestStatusUpdates('unique-id');
```

## Security Checklist

- Tools must check `$this->currentUser->hasPermission()` before operations
- Use Property Restrictions to lock entity types/bundles
- Write explicit instructions about what the agent can and cannot do
- Use Guardrails for user-facing agents
- Do not use MCP tools on critical production sites (tool description injection risk)
- Separate high-privilege agents from user-facing ones

## Common Mistakes

- **Wrong**: Setting `max_loops` too high (>10) → **Right**: Runaway cost risk; 3-5 is safe for most use cases
- **Wrong**: Using agents for fixed workflows → **Right**: Automators handle fixed workflows; agents are for genuine decision-making
- **Wrong**: No Property Restrictions on dangerous tools → **Right**: Agent could write to any entity type; restrict to intended scope

## See Also

- [AI Assistant API](ai-assistant-api.md)
- [AI Automators](ai-automators.md)
- [Function Calling](function-calling.md)
- [Security](security.md)
- Reference: `drupal/ai_agents` (separate contrib project)
