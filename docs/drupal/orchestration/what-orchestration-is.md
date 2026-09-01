---
description: What the Orchestration module does, when to use it, and how it relates to ECA and JSON:API
tldr: "Use Orchestration when you want external automation platforms (Activepieces, Zapier, n8n) to invoke Drupal workflows, AI agents, or business logic via HTTP. JSON:API handles data CRUD; Orchestration handles behavior. ECA is the internal half; Orchestration is the external half."
drupal_version: "11.x"
---

# What Orchestration Is

## When to Use

> Use Orchestration when external platforms need to trigger Drupal behavior (ECA models, AI agents, Tool plugins). Use JSON:API when external platforms need to read or mutate Drupal content. Use ECA alone when the automation is entirely internal.

## Decision

| If you want to... | Use... | Why |
|---|---|---|
| Let an external platform query or mutate Drupal content | Core **JSON:API** | Standard REST CRUD; Orchestration does not replace this |
| Let an external platform trigger a Drupal ECA workflow | **Orchestration + orchestration_eca** | Exposes ECA Tool-event models as callable services |
| Let an external platform invoke a Drupal AI Agent | **Orchestration + orchestration_ai_agents** | Wraps `drupal/ai_agents` agents as Orchestration services |
| Let an external platform call a Tool API plugin | **Orchestration + orchestration_tool** | Wraps `drupal/tool` plugins as Orchestration services |
| Let Drupal entity events trigger external workflows | **Orchestration webhooks + ECA dispatch action** | ECA observes the entity event; webhook action fires outbound HTTP |
| Automate purely internal Drupal workflows | **ECA alone** | Orchestration is the external half; ECA is the internal half |

## Context: DXP 2.0

This module is the practical implementation of Dries Buytaert's "DXP 2.0" vision articulated at DrupalCon Vienna Oct 2025 and DrupalCon Chicago Mar 2026: Drupal as a composable platform wired into the broader automation ecosystem rather than a siloed CMS. The Activepieces integration is the first expression of this.

## Pattern

The mental model: JSON:API handles **data**; Orchestration handles **behavior**.

```
External platform sends request
  → Orchestration routes to matching provider
    → Drupal executes (ECA model, AI agent, Tool plugin)
      → Response returned to platform
```

Orchestration is a **thin bridge** — it provides no functionality by itself. Everything comes from enabled submodules (`orchestration_eca`, `orchestration_ai_agents`, `orchestration_ai_function`, `orchestration_tool`).

## Common Mistakes

- **Wrong**: Using Orchestration for content CRUD → **Right**: Use JSON:API (core) for data access
- **Wrong**: Installing all four submodules → **Right**: Enable only the providers matching your use case
- **Wrong**: Expecting Orchestration to work without a supported platform → **Right**: As of May 2026, only Activepieces has a built connector; other platforms require manual API implementation
- **Wrong**: Conflating ECA with Orchestration → **Right**: ECA is internal automation; Orchestration is the external API bridge

## See Also

- [Architecture](architecture.md)
- [ECA Services Provider](eca-services-provider.md)
- Reference: https://project.pages.drupalcode.org/orchestration/
