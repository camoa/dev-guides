---
description: AI Agents — ReAct loop, config entities, tool usage, orchestration, and security
tldr: "Use this guide when building autonomous AI agents that make decisions. Use [AI Automators](ai-automators.md) for fixed field-population workflows that don't need autonomous decision-making."
drupal_version: "11.x"
---

# AI Agents

## When to Use

> Use this guide when building autonomous AI agents that make decisions. Use [AI Automators](ai-automators.md) for fixed field-population workflows that don't need autonomous decision-making. Use [AI Assistant API](ai-assistant-api.md) to expose an agent as a standard assistant.

AI Agents (separate contrib module: `drupal/ai_agents`) provide autonomous decision-making via a ReAct loop. The agent decides which tools to use and when — unlike automators which follow fixed steps.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Fixed content generation workflow | Automators | Simpler, lower cost, no reasoning loop |
| Dynamic decision-making | Agents | Agent decides which tools to use |
| Expose agent to chat UI | Config entity + Assistant | `ai_agent` field on `ai_assistant` entity |
| Multi-step orchestration | Agents-as-tools | Sub-agents have isolated memory |
| High-stakes production site | Avoid MCP tools | Tool description injection risk |

## Agent Loop

```
System prompt + instructions + tools + memory
    -> LLM decides: use tool OR write final response
    -> If tool: execute, store result in memory, loop again
    -> If text: return to caller, stop
```

## Agent Types

| Type | Definition | Best For |
|------|------------|----------|
| Config Entity | YAML + UI at `/admin/config/ai/agents` | Site builders, tool-based |
| Code-Based | PHP plugin + prompt files | Complex workflows |

## Configuration

| Field | Purpose |
|-------|---------|
| Title | Identifier; also used as tool label when used as sub-agent |
| Description | Critical — orchestrating agents read this to decide when to call |
| Max Loops | Default 3; prevents runaway loops |
| Agent Instructions | System prompt (supports tokens); be verbose |
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
| Override Description | Replace tool description for this agent's prompt |
| Use Artifact Storage | Store in artifact token (not history) to reduce tokens |
| Property Restrictions | `Allow all` / `Only allow` / `Force value` |

## Orchestration (Agents-as-Tools)

Any agent can be used as a tool by another agent. Each sub-agent invocation has its own isolated memory. The orchestrator receives only the sub-agent's final output.

## Programmatic Usage

```php
$agent = \Drupal::service('plugin.manager.ai_agents')->createInstance('field_agent');
$input = new ChatInput([new ChatMessage('user', 'Create a Tags vocabulary')]);
$agent->setChatInput($input);
$agent->determineSolvability();
$output = $agent->solve();

// Get tool results
$results = $agent->getToolResults(FALSE);
$specific = $agent->getToolResultsByPluginId('entity_create_tool');
```

## Progress Polling

```php
$agent->setProgressThreadId('unique-id');
$agent->setDetailedProgressTracking([
  AiAgentStatusItemTypes::Started,
  AiAgentStatusItemTypes::ToolStarted,
]);
$agent->solve();

// Poll progress
$progress = \Drupal::service('ai_agents.agent_status_poller')
  ->getLatestStatusUpdates('unique-id');
```

## Security Considerations

1. **Tools without permissions** — always check `hasPermission()` in tools
2. **Tools too widely scoped** — use Property Restrictions to lock entity types/bundles
3. **Loose instructions** — write 4+ sentences per tool describing what agent can/cannot do
4. **Prompt injection** — any user content is a vector; use Guardrails; separate high-privilege agents
5. **MCP tools** — do NOT use on critical sites (tool description injection risk)

## Common Mistakes

| Mistake | Why it's wrong |
|---------|---------------|
| Setting `max_loops` too high (>10) | Runaway cost risk; 3-5 is safe for most use cases |
| Using agents when automators suffice | Agents are for genuine decision-making; fixed workflows use automators |
| Not setting Property Restrictions on dangerous tools | Agent could write to any entity type; restrict to intended scope |

## See Also

- [AI Assistant API](ai-assistant-api.md)
- [AI Automators](ai-automators.md)
- [Function Calling](function-calling.md)
- [Security](security.md)
- Reference: `drupal/ai_agents` (separate contrib project)
