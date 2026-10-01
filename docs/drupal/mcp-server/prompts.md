---
description: "Ship reusable MCP prompts as mcp_prompt_config config entities: YAML shape, placeholder substitution, roles, content types and completion providers"
tldr: "Ship reusable prompt templates as mcp_prompt_config entities with arguments and placeholder substitution. Gotcha: prompts have no access check and access mcp server prompts is never checked, so keep secrets out of prompt text."
drupal_version: "^10 || ^11"
---

# Prompts

**Version:** mcp_server 2.0.0-beta5.

## When to Use

> Use prompts to ship reusable message templates an agent can fetch with arguments. Prompts are config entities, so they export with config.

## Decision

| If the agent needs... | Use |
|---|---|
| A reusable instruction template with arguments | A prompt (this page) |
| Data to read | A [resource](resources-and-resource-templates.md) |
| An action with side effects | A [tool](native-tool-plugins.md) |

## Pattern

Entity type `mcp_prompt_config`; config name `mcp_server.mcp_prompt_config.<id>`. `mcp_server` defines only a delete form. Create and edit prompts through config import or the `mcp_server_ui` project. From the test fixture `mcp_server.mcp_prompt_config.test_with_args.yml`, with its test-only completion provider removed:

```yaml
id: analysis
label: Analysis Prompt
title: 'Analysis'
description: 'Analyze a topic given a skill level and context'
status: true
arguments:
  - label: 'Skill Level'
    machine_name: skill_level
    description: 'Audience skill level'
    required: true
  - label: 'Context'
    machine_name: context
    description: 'Additional context'
    required: false
messages:
  - role: user
    content:
      - type: text
        text: 'Analyze for {{skill_level}} with context {{context}}'
```

## Behavior

From `src/Capability/Handler/PromptConfigHandler.php` and `McpServerFactory::registerPrompts()`:

- Only `status: true` prompts are registered. The prompt name is the entity `id` (pattern `^[a-z0-9_]+$`).
- `{{ name }}` placeholders are replaced in every string of each content item. Unknown placeholders stay as written.
- Message roles: `user` or `assistant`. Content types: `text`, `image`, `audio`, `resource`.
- An argument with `completion_providers` accepts only exact values from that provider; otherwise `PromptGetException`.
- Completion providers are plugin type `mcp_server.argument_completion_provider` in `src/Plugin/mcp_server/ArgumentCompletionProvider/`. `mcp_server` ships none.

## Common Mistakes

- Relying on `access mcp server prompts`. Nothing checks it; every enabled prompt is served to anyone who reaches the server.
- Putting secrets or internal URLs in prompt text. Prompts have no access check.
- Treating completion validation as injection defense. It checks values against a list; free-text arguments are inserted as-is.
- Expecting `{{ }}` to be Twig. It is a plain regex substitution.

## See Also

- [Resources and Resource Templates](resources-and-resource-templates.md) → (shares completion providers)
- Reference: `modules/contrib/mcp_server/src/Entity/McpPromptConfig.php`, `src/Capability/Handler/PromptConfigHandler.php`, `config/schema/mcp_server.schema.yml`, `tests/modules/mcp_server_test/config/install/`
