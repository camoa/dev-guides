---
description: "Source references and maintenance manifest for the ai module guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install

Path: local Drupal research install with `web/modules/contrib/ai` (1.3.x dev checkout — services.yml and plugin files verified against this)

## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Drupal AI project page | https://www.drupal.org/project/ai | All | 2026-05-19 |
| Releases list | https://www.drupal.org/project/ai/releases | All | 2026-05-19 |
| Release notes 1.3.0 | https://www.drupal.org/project/ai/releases/1.3.0 | core-architecture, function-calling, deprecated-modules | 2026-05-19 |
| Release notes 1.3.1 | https://www.drupal.org/project/ai/releases/1.3.1 | provider-system | 2026-05-19 |
| Release notes 1.3.2 | https://www.drupal.org/project/ai/releases/1.3.2 | ai-chatbot-deepchat, ai-ckeditor | 2026-05-19 |
| Release notes 1.3.3 | https://www.drupal.org/project/ai/releases/1.3.3 | function-calling, provider-system, guardrails-system | 2026-05-19 |
| Release notes 1.3.4 | https://www.drupal.org/project/ai/releases/1.3.4 | core-architecture, ai-automators | 2026-05-19 |
| Release notes 1.3.5 | https://www.drupal.org/project/ai/releases/1.3.5 | ai-api-explorer, guardrails-system | 2026-05-19 |
| Release notes 1.4.0-rc1 | https://www.drupal.org/project/ai/releases/1.4.0-rc1 | core-architecture, guardrails-system, events-system, enums-and-dtos, function-calling | 2026-05-19 |
| Release notes 1.4.2 | https://www.drupal.org/project/ai/releases/1.4.2 | core-architecture, provider-system, operation-types, guardrails-system, ai-chatbot-deepchat, ai-automators, enums-and-dtos | 2026-06-10 |
| Official developer docs | https://project.pages.drupalcode.org/ai/1.3.x/ | All | 2026-05-19 |
| AI module git repo (1.3.x) | https://git.drupalcode.org/project/ai/-/tree/1.3.x | All | 2026-05-19 |
| AI module git repo (1.4.x) | https://git.drupalcode.org/project/ai/-/tree/1.4.x | core-architecture, guardrails-system, events-system | 2026-05-19 |
| AI module git tag 1.4.2 | https://git.drupalcode.org/project/ai/-/tree/1.4.2 | core-architecture, provider-system, operation-types, guardrails-system, ai-chatbot-deepchat, ai-automators, enums-and-dtos | 2026-06-10 |
| ai_translate deprecation issue | https://www.drupal.org/node/3570275 | deprecated-modules, ai-translate | 2026-05-19 |

## Code Sources

| Module | Relative Path | Guide Sections | Version |
|--------|---------------|----------------|---------|
| AI core module | `web/modules/contrib/ai/` | core-architecture, provider-system, operation-types, guardrails-system, events-system, exceptions, enums-and-dtos, security | 1.4.2 |
| ai_assistant_api | `web/modules/contrib/ai/modules/ai_assistant_api/` | ai-assistant-api | 1.4.2 |
| ai_chatbot | `web/modules/contrib/ai/modules/ai_chatbot/` | ai-chatbot-deepchat | 1.4.2 |
| ai_automators | `web/modules/contrib/ai/modules/ai_automators/` | ai-automators | 1.4.2 |
| ai_ckeditor | `web/modules/contrib/ai/modules/ai_ckeditor/` | ai-ckeditor | 1.4.2 |
| ai_search | `web/modules/contrib/ai/modules/ai_search/` | ai-search-vector-rag | 1.4.2 |
| ai_translate | `web/modules/contrib/ai/modules/ai_translate/` | ai-translate, deprecated-modules | 1.4.2 |
| ai_observability | `web/modules/contrib/ai/modules/ai_observability/` | ai-observability | 1.4.2 |
| ai_logging | `web/modules/contrib/ai/modules/ai_logging/` | ai-logging, deprecated-modules | 1.4.2 |
| ai_api_explorer | `web/modules/contrib/ai/modules/ai_api_explorer/` | ai-api-explorer | 1.4.2 |
| ai_validations | `web/modules/contrib/ai/modules/ai_validations/` | ai-validations, deprecated-modules | 1.4.2 |
| ai_content_suggestions | `web/modules/contrib/ai/modules/ai_content_suggestions/` | deprecated-modules | 1.4.2 |
| ai_external_moderation | `web/modules/contrib/ai/modules/ai_external_moderation/` | deprecated-modules, guardrails-system | 1.4.2 |
| ai_eca | `web/modules/contrib/ai/modules/ai_eca/` | deprecated-modules | 1.4.2 |
| field_widget_actions | `web/modules/contrib/ai/modules/field_widget_actions/` | field-widget-actions | 1.4.2 |
