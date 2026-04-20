---
description: Short-term memory plugins — manage conversation context within a session
tldr: "Use short-term memory plugins when you need to manage conversation context within a session beyond the default history mechanism in `ai_assistant_api`. For most cases, set `allow_history` on the `ai_assistant` config entity instead."
drupal_version: "11.x"
---

# Short-Term Memory

## When to Use

> Use short-term memory plugins when you need to manage conversation context within a session beyond the default history mechanism in `ai_assistant_api`. For most cases, set `allow_history` on the `ai_assistant` config entity instead.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Standard conversation history | `allow_history` on assistant | Built-in; no custom code needed |
| Custom context storage | Custom `AiShortTermMemory` plugin | Full control over context management |

## Pattern

```php
use Drupal\ai\Attribute\AiShortTermMemory;

#[AiShortTermMemory(
  id: 'my_memory',
  label: new TranslatableMarkup('My Memory'),
  description: new TranslatableMarkup('Custom memory management'),
)]
class MyMemory extends AiShortTermMemoryPluginBase {
  // Store/retrieve conversation context.
}
```

**ID convention:** Same as guardrails — must match or be prefixed by group.

## Service

`plugin.manager.ai.short_term_memory` — discovers and manages memory plugins.

## Common Mistakes

- **Wrong**: Building a custom memory plugin for basic history → **Right**: Use `allow_history: session` on the `ai_assistant` config entity
- **Wrong**: ID that doesn't match group prefix → **Right**: Same ID convention as guardrails (must match or be prefixed by group)

## See Also

- [AI Assistant API](ai-assistant-api.md)
- [Guardrails System](guardrails-system.md)
- Reference: `web/modules/contrib/ai/src/Plugin/AiShortTermMemory/`
