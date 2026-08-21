---
description: Modern Web Guidance — a Google Chrome Agent Skills plugin that injects web platform best practices and Baseline compatibility data into coding agents via an offline CLI.
tracks:
  - project: modern-web-guidance
    registry: npm
    channel: stable
    declared: null
    note: no version stated in prose
    verified: 2026-06-09
guide-meta:
  concepts:
    - Modern Web Guidance
    - MWG
    - Agent Skills
    - web platform guidance
    - Baseline browser support
    - modern-web-guidance CLI
    - coding agent plugin
    - GoogleChrome plugin
    - SKILL.md
    - chrome extensions skill
  not:
    - MCP server
    - Model Context Protocol
    - Drupal AI module
    - LLM fine-tuning
  requires: []
  complements:
    - js/passkeys
    - js/forms
    - ai-tooling/figma-mcp
  specializes: ""
  category: ai-tooling
---

# Modern Web Guidance

A Google Chrome Agent Skills plugin that embeds web platform expertise, best practices, and Baseline compatibility data directly into your coding agent. It steers agents away from legacy JavaScript patterns toward native, modern browser APIs — using an offline CLI with local TensorFlow.js embeddings.

## I need to...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what MWG is and whether it's an MCP server | [What Is Modern Web Guidance](what-is-modern-web-guidance.md) | MWG is a set of Agent Skills distributed as a plugin — not an MCP server. The agent reads a SKILL.md instruction file and runs modern-web-guidance search/retrieve CLI commands offline. Covers 102 web features and 128 developer use cases. |
| Install MWG for Claude Code | [Install for Claude Code](install-claude-code.md) | Three steps: /plugin marketplace add, /plugin install, /reload-plugins. Skipping /reload-plugins means the skill does not activate. Enable AutoUpdate through /plugin settings. |
| Install MWG for another agent or IDE | [Install for Other Agents and IDEs](install-other-agents.md) | The recommended cross-agent path is npx modern-web-guidance@latest install — interactive wizard that detects your environment. Use --choose to install only the skill packs needed. |
| Configure Baseline targets, understand activation, opt out of telemetry | [Using It Effectively](using-it-effectively.md) | Set your Baseline target explicitly in CLAUDE.md — MWG defaults to Widely available if not set. Opt out of telemetry with DISABLE_TELEMETRY=1. |
| Understand how MWG relates to this repo's passkeys/forms/CSS guides | [Relationship to Dev-Guides](relationship-to-dev-guides.md) | MWG and dev-guides are complementary. MWG is the upstream web platform source (auto-activates). Dev-guides adapts the in-charter subset for Drupal/Bootstrap/our stack (explicit load). |
