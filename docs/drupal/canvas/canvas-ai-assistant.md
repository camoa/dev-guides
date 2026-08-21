---
description: "How the Canvas AI assistant (canvas_ai submodule) works, setup requirements, and how component metadata affects AI-driven page building."
tldr: "Use this when you want content editors to build or modify Canvas pages using natural language prompts. The Canvas AI assistant (`canvas_ai` submodule) is an optional feature targeted at editorial workflows, not developer workflows."
drupal_version: "11.x"
---

# Canvas AI Assistant

## When to Use

> Use this when you want content editors to build or modify Canvas pages using natural language prompts. The Canvas AI assistant (`canvas_ai` submodule) is an optional feature targeted at editorial workflows, not developer workflows.

## Decision

| Situation | Choose | Why |
|---|---|---|
| Editors building pages via prompts | Enable `canvas_ai` submodule | AI selects + configures existing components from prompt |
| Developer-built components | Write good `description`, `title`, `examples` | AI reads metadata to select and configure components correctly |
| New component generation on demand | Not supported (primary workflow) | AI primarily places existing approved components |

## Pattern

**Architecture — how it works:**

1. The editor writes a prompt in the Canvas AI chat interface
2. The orchestrator analyzes the prompt to determine intent (place existing components vs. generate new components)
3. The `canvas_page_builder_agent` retrieves all enabled components and uses them as context
4. AI selects components from the approved library and configures their props
5. Components are placed on the Canvas page with AI-generated content

**Prompt intent routing:**
- Prompts with "place", "use", "add" → routes to page builder agent (uses existing components)
- Prompts with "create", "generate", "build" → may trigger component creation (behavior depends on Canvas version)

**Setup:**

```
1. Enable canvas_ai submodule
2. Install an AI Provider module (e.g., OpenAI, Anthropic) that supports function calling
3. Configure the provider at /admin/config/ai/settings
4. Enable the provider for all Chat operation types
```

The AI provider must support function calling/tool use — the orchestrator uses structured function calls to select and configure components.

**Making components AI-friendly** — the AI uses `name`, `description`, and prop `title`/`description` from `*.component.yml` as context:

```yaml
name: Hero Banner
description: 'Full-width hero section for landing pages with headline, body text, and a call-to-action button.'

props:
  type: object
  properties:
    headline:
      type: string
      title: Headline
      description: 'Main heading text for the hero section.'
      examples:
        - 'Transform Your Business Today'
    body:
      type: string
      title: Body
      description: 'Supporting paragraph text below the headline.'
      examples:
        - 'Start your journey with our platform.'
```

## Common Mistakes

- **Wrong**: Enabling `canvas_ai` without a function-calling-capable AI provider → **Right**: The AI will fail to use tools and will not work
- **Wrong**: Expecting AI to generate new Code Components on demand → **Right**: The AI primarily selects and configures existing approved components; code generation is a separate workflow
- **Wrong**: Providing no `description` on components → **Right**: The AI has no signal for when to select the component
- **Wrong**: Expecting the AI to override the design system → **Right**: The AI is constrained to the available approved components; it cannot place arbitrary HTML

## See Also

- Canvas AI docs: https://project.pages.drupalcode.org/canvas/ai-assistant/
- XB AI Assistant module: https://www.drupal.org/project/xb_ai_assistant
- Bonnici article on Canvas AI: https://www.bonnici.co.nz/blog/drupal-ai-native-page-building-canvas-ai-context
