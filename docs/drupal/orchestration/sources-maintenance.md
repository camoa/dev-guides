---
description: "Source references and maintenance manifest for the orchestration guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install

Path: not yet configured — ask user on next guide update requiring code-source lookup.

## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Orchestration project page | https://www.drupal.org/project/orchestration | What Orchestration Is, Installation and Setup | 2026-05-20 |
| Orchestration docs — index | https://project.pages.drupalcode.org/orchestration/ | What Orchestration Is, Architecture | 2026-05-20 |
| Orchestration docs — API reference | https://project.pages.drupalcode.org/orchestration/develop/api/ | Orchestration API Reference | 2026-05-20 |
| Orchestration docs — plugin authoring | https://project.pages.drupalcode.org/orchestration/develop/plugin/ | Custom Services Provider | 2026-05-20 |
| Orchestration docs — AI Agents submodule | https://project.pages.drupalcode.org/orchestration/modules/ai_agents/ | AI Agents and AI Function Providers | 2026-05-20 |
| Orchestration docs — AI Function submodule | https://project.pages.drupalcode.org/orchestration/modules/ai_function/ | AI Agents and AI Function Providers | 2026-05-20 |
| Orchestration docs — ECA submodule | https://project.pages.drupalcode.org/orchestration/modules/eca/ | ECA Services Provider | 2026-05-20 |
| Orchestration docs — Tool API submodule | https://project.pages.drupalcode.org/orchestration/modules/tool/ | Tool API Provider | 2026-05-20 |
| Dries Buytaert — Connecting Drupal with Activepieces | https://dri.es/connecting-drupal-with-activepieces | Connecting Activepieces, Installation and Setup | 2026-05-20 |
| ECA Tool event (ECA Guide) | https://ecaguide.org/plugins/eca/base/events/eca_base_eca_tool | ECA Services Provider | 2026-05-20 |
| ECA Poll by timestamp (ECA Guide) | https://ecaguide.org/plugins/orchestration_eca/events/orchestration_poll_timestamp | ECA Services Provider | 2026-05-20 |
| ECA Poll by ID (ECA Guide) | https://ecaguide.org/plugins/orchestration_eca/events/orchestration_poll_id | ECA Services Provider | 2026-05-20 |
| ECA Dispatch webhook (ECA Guide) | https://ecaguide.org/plugins/orchestration_eca/actions/orchestration_dispatch_webhook | Webhooks and Outbound Events | 2026-05-20 |
| OWASP API Security Top 10 | https://owasp.org/API-Security/ | Security Considerations | 2026-05-20 |
| OWASP SSRF | https://owasp.org/www-community/attacks/Server_Side_Request_Forgery | Security Considerations | 2026-05-20 |

## Code Sources (1.0.x branch, commit `a31a0a0`)

All paths relative to the cloned research source at `eca-src-research/orch-src/` within the dev-guides project.

| File | Relative Path | Guide Sections | Module Version |
|---|---|---|---|
| Core module info | `orchestration.info.yml` | What Orchestration Is, Installation and Setup | 1.0.0 |
| Core services | `orchestration.services.yml` | Architecture, Custom Services Provider | 1.0.0 |
| Core routing | `orchestration.routing.yml` | Orchestration API Reference, Authentication and Permissions | 1.0.0 |
| Core permissions | `orchestration.permissions.yml` | Authentication and Permissions, Security Considerations | 1.0.0 |
| Core install (update hooks) | `orchestration.install` | Webhooks and Outbound Events | 1.0.0 |
| Composer requirements | `composer.json` | Installation and Setup | 1.0.0 |
| Connect controller | `src/Controller/Connect.php` | Orchestration API Reference, Architecture | 1.0.0 |
| Orchestration controller | `src/Controller/Orchestration.php` | Webhooks and Outbound Events, Orchestration API Reference | 1.0.0 |
| ServicesProviderInterface | `src/ServicesProviderInterface.php` | Custom Services Provider, Architecture | 1.0.0 |
| ServicesProviderManager | `src/ServicesProviderManager.php` | Architecture | 1.0.0 |
| Service value object | `src/Service.php` | Custom Services Provider, Architecture, Orchestration API Reference | 1.0.0 |
| ServiceConfig value object | `src/ServiceConfig.php` | Custom Services Provider, Orchestration API Reference | 1.0.0 |
| Webhooks service | `src/Webhooks.php` | Webhooks and Outbound Events, Security Considerations | 1.0.0 |
| Webhook form | `src/Form/Webhook.php` | Webhooks and Outbound Events | 1.0.0 |
| PollEventBase | `src/Event/PollEventBase.php` | ECA Services Provider, Orchestration API Reference | 1.0.0 |
| PollEventTimestamp | `src/Event/PollEventTimestamp.php` | ECA Services Provider, Orchestration API Reference | 1.0.0 |
| PollEventId | `src/Event/PollEventId.php` | ECA Services Provider, Orchestration API Reference | 1.0.0 |
| ECA submodule info | `modules/eca/orchestration_eca.info.yml` | ECA Services Provider, Installation and Setup | 1.0.0 |
| ECA submodule services | `modules/eca/orchestration_eca.services.yml` | ECA Services Provider, Architecture | 1.0.0 |
| ECA schema | `modules/eca/config/schema/orchestration_eca.schema.yml` | ECA Services Provider | 1.0.0 |
| ECA ServicesProvider | `modules/eca/src/ServicesProvider.php` | ECA Services Provider | 1.0.0 |
| ECA Poll event plugin | `modules/eca/src/Plugin/ECA/Event/Poll.php` | ECA Services Provider | 1.0.0 |
| ECA Poll deriver | `modules/eca/src/Plugin/ECA/Event/PollDeriver.php` | ECA Services Provider | 1.0.0 |
| ECA AddItemToPollResultBase | `modules/eca/src/Plugin/Action/AddItemToPollResultBase.php` | ECA Services Provider | 1.0.0 |
| ECA AddItemToPollResultTimestamp | `modules/eca/src/Plugin/Action/AddItemToPollResultTimestamp.php` | ECA Services Provider | 1.0.0 |
| ECA AddItemToPollResultId | `modules/eca/src/Plugin/Action/AddItemToPollResultId.php` | ECA Services Provider | 1.0.0 |
| ECA Dispatch Webhook action | `modules/eca/src/Plugin/Action/Webhook.php` | Webhooks and Outbound Events | 1.0.0 |
| AI Agents submodule info | `modules/ai_agents/orchestration_ai_agents.info.yml` | AI Agents and AI Function Providers | 1.0.0 |
| AI Agents submodule services | `modules/ai_agents/orchestration_ai_agents.services.yml` | Architecture, AI Agents | 1.0.0 |
| AI Agents ServicesProvider | `modules/ai_agents/src/ServicesProvider.php` | AI Agents and AI Function Providers | 1.0.0 |
| AI Function submodule info | `modules/ai_function/orchestration_ai_function.info.yml` | AI Agents and AI Function Providers | 1.0.0 |
| AI Function submodule services | `modules/ai_function/orchestration_ai_function.services.yml` | Architecture, AI Function | 1.0.0 |
| AI Function ServicesProvider | `modules/ai_function/src/ServicesProvider.php` | AI Agents and AI Function Providers | 1.0.0 |
| Tool submodule info | `modules/tool/orchestration_tool.info.yml` | Tool API Provider, Installation and Setup | 1.0.0 |
| Tool submodule services | `modules/tool/orchestration_tool.services.yml` | Architecture, Tool API | 1.0.0 |
| Tool ServicesProvider | `modules/tool/src/ServicesProvider.php` | Tool API Provider | 1.0.0 |
| Module docs index | `docs/index.md` | What Orchestration Is, Installation and Setup | 1.0.0 |
| API docs | `docs/develop/api.md` | Orchestration API Reference | 1.0.0 |
| Plugin docs | `docs/develop/plugin.md` | Custom Services Provider | 1.0.0 |
| ECA module docs | `docs/modules/eca/index.md` | ECA Services Provider | 1.0.0 |
| AI Agents module docs | `docs/modules/ai_agents/index.md` | AI Agents and AI Function Providers | 1.0.0 |
| AI Function module docs | `docs/modules/ai_function/index.md` | AI Agents and AI Function Providers | 1.0.0 |
| Tool module docs | `docs/modules/tool/index.md` | Tool API Provider | 1.0.0 |

<!-- END PARTITION: sources-maintenance -->
