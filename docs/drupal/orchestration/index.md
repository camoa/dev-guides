---
description: Drupal Orchestration 1.0.x — expose ECA workflows, AI agents, and Tool API plugins as callable HTTP services for external automation platforms (Activepieces, n8n, Make, Zapier)
guide-meta:
  concepts:
    - Orchestration module
    - drupal/orchestration
    - orchestration_eca
    - orchestration_ai_agents
    - orchestration_ai_function
    - orchestration_tool
    - ServicesProviderInterface
    - ServicesProviderManager
    - Service value object
    - ServiceConfig
    - Webhooks service
    - webhook register
    - webhook unregister
    - orchestration_dispatch_webhook
    - orchestration poll
    - PollEventTimestamp
    - PollEventId
    - Activepieces
    - iPaaS
    - external automation platform
    - DXP 2.0
    - use orchestration connect
  not:
    - JSON:API (data CRUD — see drupal/jsonapi)
    - ECA plugin development (see drupal/eca)
    - Drupal AI module configuration (see drupal/ai-module)
  requires:
    - drupal/eca
    - drupal/services
  complements:
    - drupal/eca
    - drupal/modeler-api
  specializes: ""
  category: drupal
tracks:
  - project: orchestration
    channel: stable
    declared: 1.0.x
    verified: 2026-05-20
---

# Orchestration

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what Orchestration does and when to use it | [What Orchestration Is](what-orchestration-is.md) | Use Orchestration when you want external automation platforms (Activepieces, Zapier, n8n) to invoke Drupal workflows, AI agents, or business logic via HTTP. JSON:API handles data CRUD; Orchestration handles behavior. ECA is the internal half; Orchestration is the external half. |
| Understand the internal architecture | [Architecture](architecture.md) | Orchestration has three layers: the Connect controller (REST endpoints), ServicesProviderManager (collects tagged providers), and the Webhooks service. Providers register as Symfony services tagged `orchestration_services_provider` — no plugin annotation system. Service UUID format is `provider_id::service_id` (double colon). |
| Install and enable the module | [Installation and Setup](installation-and-setup.md) | Require `drupal/orchestration`, enable `basic_auth` and `orchestration` core module, then enable only the submodules matching your use case. Create a dedicated service account user with the single `use orchestration connect` permission. Run `drush cache-rebuild` after enabling submodules. |
| Expose ECA models to external platforms | [ECA Services Provider](eca-services-provider.md) | Use orchestration_eca to make ECA models callable from external platforms. The model must subscribe to the `eca_base.tool` event and define an `arguments` YAML field — those become the service's callable parameters. Service UUID format is `eca::{wildcard}`. |
| Expose AI Agents or AI Function Call plugins | [AI Agents and AI Function Providers](ai-agents-and-ai-function-providers.md) | Use orchestration_ai_agents to invoke AI Agent config entities from external platforms (service UUID: `ai_agent::{machine_name}`). Use orchestration_ai_function only for custom `ai.function_calls` plugins not covered by other providers — it auto-deduplicates against eca, ai_agents, and tool providers. |
| Expose Tool API plugins | [Tool API Provider](tool-api-provider.md) | Use orchestration_tool to let external platforms call `drupal/tool` plugins directly. Service UUID is `tool::{plugin_id}`; entity-typed inputs expect the entity's numeric ID (resolved internally before execute()). The Tool API is explicitly marked early-stage — treat orchestration_tool as similarly unstable. |
| Register and manage webhooks | [Webhooks and Outbound Events](webhooks-and-outbound-events.md) | Webhooks are stored in Drupal's KeyValue store (`orchestration` collection). Register via admin UI (`remote: false`) or via `/orchestration/webhook/register` API (`remote: true`). Dispatch using the `orchestration_dispatch_webhook` ECA action. Failed deliveries are silently discarded in 1.0.0 — monitor at the receiving platform. |
| Understand the REST endpoints and request/response shapes | [Orchestration API Reference](orchestration-api-reference.md) | Five REST endpoints, all requiring Basic Auth + `use orchestration connect`. Service UUIDs use double colon (`provider::id`). Unknown service IDs return HTTP 500, not 404. Sending both `timestamp` and `id` to the poll endpoint silently uses `timestamp`. Always send `Content-Type: application/json`. |
| Understand authentication and permissions | [Authentication and Permissions](authentication-and-permissions.md) | There is one permission: `use orchestration connect`. It gates all five API endpoints and the admin UI — no per-service granularity in 1.0.0. Use Basic Auth with a dedicated service account user. Always enforce HTTPS in production; Basic Auth credentials travel Base64-encoded in every request. |
| Connect Drupal to Activepieces | [Connecting Activepieces](connecting-activepieces.md) | Activepieces is the only platform with a built Drupal connector (as of May 2026). It uses JSON:API for content CRUD and the Orchestration API for workflow/agent/tool invocation. Activepieces Cloud cannot reach a `localhost` Drupal site; use self-hosted Docker or ngrok for local development. |
| Write a custom services provider | [Custom Services Provider](custom-services-provider.md) | Implement `ServicesProviderInterface` and register the class as a Symfony service tagged `orchestration_services_provider`. No plugin annotation needed. Provider ID must not contain colons — the UUID is `{provider_id}::{service_id}`. `execute()` must return `array\|string`. |
| Understand security risks and mitigations | [Security Considerations](security-considerations.md) | Orchestration exposes an HTTP API that executes arbitrary Drupal logic. Enforce HTTPS (Basic Auth credentials are Base64 in every header), use a minimal-permission dedicated service account, enable only needed submodules, and never assign `use orchestration connect` to the authenticated role. Failed webhook deliveries are silently discarded in 1.0.0. |
