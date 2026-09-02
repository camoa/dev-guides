---
description: Prompt system — config entities for reusable prompts with variable substitution
tldr: "Use the prompt system when you need reusable, deployable prompts with variable substitution. For one-off prompts in code, string interpolation is simpler."
drupal_version: "11.x"
---

# Prompt System

## When to Use

> Use the prompt system when you need reusable, deployable prompts with variable substitution. For one-off prompts in code, string interpolation is simpler.

The AI module provides a config entity system for managing reusable prompts with variable substitution.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Reusable, site-configurable prompts | `ai.ai_prompt.*` config entities | Deployable via config sync; overridable per environment |
| Define prompt variables/schema | `ai.ai_prompt_type.*` config entities | Named variables for substitution |
| Modify prompts without code | `ai.prompt_manager` service | Loads and renders prompts with variable values |

## Prompt Config Entities

- `ai.ai_prompt_type.*` — defines prompt types with named variables
- `ai.ai_prompt.*` — individual prompt instances with text content

## Service: `ai.prompt_manager`

```php
$promptManager = \Drupal::service('ai.prompt_manager');
// Load and render a prompt with variables
```

## Variables

Prompts support Twig-style conditionals and placeholder variables:

- `{variableName}` — simple substitution
- `{% if variableName %}...{% endif %}` — conditional blocks

## Example (AI Translate Default Prompt)

```
You are a helpful translator.
{% if sourceLangName %}Translate from {sourceLangName} {% endif %}to {destLangName}.
Preserve all HTML tags. Translate alt and title attributes.
{inputText}
```

## Common Mistakes

- **Wrong**: Hardcoding prompts in PHP strings → **Right**: Use prompt config entities so prompts are deployable and configurable without code changes

## See Also

- [AI Assistant API](ai-assistant-api.md)
- [AI Translate](ai-translate.md)
- Reference: `web/modules/contrib/ai/src/Entity/AiPrompt.php`
