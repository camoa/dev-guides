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
| Understand what MWG is and whether it's an MCP server | [What Is Modern Web Guidance](what-is-modern-web-guidance.md) | MWG is a set of Agent Skills distributed as a plugin — not an MCP server. The agent reads a SKILL.md instruction file and runs modern-web-guidance search/retrieve CLI commands offline (TensorFlow.js local embeddings, no API keys). Covers 102 web features and 128 developer use cases across CSS, HTML, JS, passkeys, performance, and accessibility. |
| Install MWG for Claude Code | [Install for Claude Code](install-claude-code.md) | Three steps in Claude Code — /plugin marketplace add GoogleChrome/modern-web-guidance, /plugin install modern-web-guidance@googlechrome, /reload-plugins. Skipping /reload-plugins means the skill does not activate. Enable AutoUpdate through /plugin settings — MWG adds new guides frequently. |
| Install MWG for another agent or IDE | [Install for Other Agents and IDEs](install-other-agents.md) | The recommended cross-agent path is npx modern-web-guidance@latest install — runs an interactive wizard that detects your agent. Use --choose to install only the skill packs you need. Use --auto-update where available to keep guides current as MWG adds new content frequently. |
| Configure Baseline targets, understand activation, opt out of telemetry | [Using It Effectively](using-it-effectively.md) | Set your Baseline target explicitly in CLAUDE.md — MWG defaults to Widely available if not set, which may be more conservative than your project allows. The skill activates automatically on relevant web tasks. If it misses a task, manually direct the agent to run modern-web-guidance search. Opt out of telemetry with DISABLE_TELEMETRY=1 in your shell profile. |
| Understand how MWG relates to this repo's passkeys/forms/CSS guides | [Relationship to Dev-Guides](relationship-to-dev-guides.md) | MWG and dev-guides are complementary, not redundant. MWG is the upstream source of truth for web platform patterns (automatic, 128 task guides). Dev-guides adapts the in-charter subset for Drupal/Bootstrap/our stack (explicit load, opinionated patterns). MWG will not activate for Drupal Form API; dev-guides will not replace MWG for cutting-edge CSS questions. |
