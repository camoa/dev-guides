---
description: "How the Canvas AI assistant (canvas_ai submodule) works, setup requirements, and how component metadata affects AI-driven page building."
tldr: "Use this when you want content editors to build or modify Canvas pages using natural language prompts. The Canvas AI assistant (`canvas_ai` submodule) is an optional feature targeted at editorial workflows, not developer workflows."
drupal_version: "11.x"
---

# Canvas AI Assistant

## When to Use

> You want content editors to be able to build or modify Canvas pages using natural language prompts — describing what they want ("Add a hero with a blue background and a contact us button") and having AI select and configure components automatically. The Canvas AI assistant is an optional submodule targeted at editorial workflows, not developer workflows.

## Decision

| Situation | Choose | Why |
|---|---|---|
| Editors building pages via prompts | Enable `canvas_ai` submodule | AI selects + configures existing components from prompt |
| Developer-built components | Write good `description`, `title`, `examples` | AI reads metadata to select and configure components correctly |
| New component generation on demand | Not supported (primary workflow) | AI primarily places existing approved components |

## Architecture

The Canvas AI assistant is the `canvas_ai` submodule (also known historically as `xb_ai_assistant`). It operates as an orchestration layer:

1. **The editor writes a prompt** in the Canvas AI chat interface
2. **The orchestrator analyzes the prompt** to determine intent (place existing components vs. generate new components)
3. **The `canvas_page_builder_agent`** retrieves all enabled components and uses them as context
4. **AI selects components** from the approved library and configures their props
5. **Components are placed** on the Canvas page with AI-generated content

**Prompt intent routing:**
- Prompts with "place", "use", "add" → routes to page builder agent (uses existing components)
- Prompts with "create", "generate", "build" → may trigger component creation (behavior depends on Canvas version)

## Setup

```
1. Enable canvas_ai submodule
2. Install an AI Provider module (e.g., OpenAI, Anthropic) that supports function calling
3. Configure the provider at /admin/config/ai/settings
4. Enable the provider for all Chat operation types
```

**Requirements**: The AI provider must support function calling/tool use — the orchestrator uses structured function calls to select and configure components.

## Implications for Component Developers

The AI assistant uses your component's `name`, `description`, and prop `title`/`description` fields from `*.component.yml` as its context. **Good metadata = better AI selection and configuration.**

Best practices for AI-friendly components:
- Write clear `description` in `*.component.yml` — the AI reads this to decide when to use the component
- Write descriptive `title` and `description` on every prop — the AI uses these to configure prop values correctly
- Provide `examples` in prop definitions — these guide the AI on appropriate values
- Use meaningful `group` values — the AI can reason about component categories

## Common Mistakes

- Enabling `canvas_ai` without a function-calling-capable AI provider — the AI will fail to use tools and will not work
- Expecting AI to generate new Code Components on demand — the AI primarily selects and configures existing approved components; code generation is a separate workflow
- Providing no `description` on components — the AI has no signal for when to select the component
- Expecting the AI to override the design system — the AI is constrained to the available approved components; it cannot place arbitrary HTML

## See Also

- Canvas AI docs: https://project.pages.drupalcode.org/canvas/ai-assistant/
- XB AI Assistant module: https://www.drupal.org/project/xb_ai_assistant
- Bonnici article on Canvas AI: https://www.bonnici.co.nz/blog/drupal-ai-native-page-building-canvas-ai-context
