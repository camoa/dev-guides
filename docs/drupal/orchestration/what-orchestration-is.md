---
description: What the Orchestration module does, when to use it, and how it relates to ECA and JSON:API
tldr: "Use Orchestration when you want external automation platforms (Activepieces, Zapier, n8n) to invoke Drupal workflows, AI agents, or business logic via HTTP. JSON:API handles data CRUD; Orchestration handles behavior. ECA is the internal half; Orchestration is the external half."
drupal_version: "11.x"
---

# What Orchestration Is

## When to Use

> Use Orchestration when external platforms need to trigger Drupal behavior (ECA models, AI agents, Tool plugins). Use JSON:API when external platforms need to read or mutate Drupal content. Use ECA alone when the automation is entirely internal.

Read this first. It explains the purpose of the module and its relationship to ECA, JSON:API, and external automation platforms so you can decide whether it belongs in your architecture.

## Decision

Orchestration is a **thin bridge** — it exposes Drupal's internal workflow, AI, and business logic capabilities as a callable HTTP API for external automation platforms (iPaaS tools like Activepieces, Zapier, n8n, Make). It provides no functionality by itself; everything comes from the submodules.

| If you want to... | Use... | Why |
|---|---|---|
| Let an external platform query or mutate Drupal content | Core **JSON:API** | Standard REST CRUD; Orchestration does not replace this |
| Let an external platform trigger a Drupal ECA workflow | **Orchestration + orchestration_eca** | Exposes ECA Tool-event models as callable services |
| Let an external platform invoke a Drupal AI Agent | **Orchestration + orchestration_ai_agents** | Wraps `drupal/ai_agents` agents as Orchestration services |
| Let an external platform call a Tool API plugin | **Orchestration + orchestration_tool** | Wraps `drupal/tool` plugins as Orchestration services |
| Let Drupal entity events trigger external workflows | **Orchestration webhooks + ECA dispatch action** | ECA observes the entity event; webhook action fires outbound HTTP |
| Automate purely internal Drupal workflows | **ECA alone** | Orchestration is the external half; ECA is the internal half |

**The mental model**: JSON:API handles data; Orchestration handles *behavior*. External platform sends a request → Orchestration routes it to the right internal capability → Drupal executes → response returns.

Orchestration is the **external** half of Drupal automation. ECA is the **internal** half. They are complementary: ECA models fire when Drupal events happen internally; Orchestration lets external platforms invoke those same models (and vice versa, letting ECA fire outbound webhooks). You will almost always use both together.

## Context: DXP 2.0

This module is the practical implementation of Dries Buytaert's "DXP 2.0" vision articulated at DrupalCon Vienna Oct 2025 and DrupalCon Chicago Mar 2026: Drupal as a composable platform wired into the broader automation ecosystem rather than a siloed CMS. The Activepieces integration is the first expression of this.

## Pattern

```
External platform sends request
  → Orchestration routes to matching provider
    → Drupal executes (ECA model, AI agent, Tool plugin)
      → Response returned to platform
```

Orchestration provides no functionality by itself — everything comes from enabled submodules (`orchestration_eca`, `orchestration_ai_agents`, `orchestration_ai_function`, `orchestration_tool`).

## Common Mistakes

- **Using Orchestration for JSON:API CRUD work** — JSON:API (core) handles that natively and is more appropriate
- **Installing all four submodules when you only need one** — enable only the providers matching your use case
- **Expecting Orchestration to work without a supported external platform** — currently only Activepieces has a built connector; using the raw API with other platforms requires manual implementation
- **Conflating ECA (internal automation) with Orchestration (external bridge)** — they solve different halves of the same problem

## See Also

- [Architecture](architecture.md) → for how the bridge and provider system works
- [ECA Services Provider](eca-services-provider.md) → for the most common integration pattern
- Reference: https://project.pages.drupalcode.org/orchestration/
