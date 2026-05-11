---
description: AI test generation tool inventory, install commands, key references, and links to related guides.
tldr: Core toolchain is Playwright 1.56+ Test Agents (built-in Planner/Generator/Healer), @playwright/mcp MCP server, and Claude Code as the AI harness. Install with npm install -D @playwright/test@latest and claude mcp add playwright npx @playwright/mcp@latest. Community skill packs (playwright-cli-agents, qa-skills) extend the pattern with page-object awareness and multi-user flows.
---

# Code Reference

## Tool Inventory

| Tool | Type | Purpose |
|---|---|---|
| Playwright Test Agents (1.56+) | Built-in | Planner / Generator / Healer agents |
| `@playwright/mcp` | MCP server | Browser control for AI agents |
| Claude Code with MCP | AI harness | Runs the agents |
| Cursor / Copilot agent | AI harness | Alternative harnesses |
| `playwright-cli-agents` (yusuftayman) | Community skill pack | Page-Object-aware agents — fork-starter |
| `qa-skills` (neonwatty) | Community skill pack | Multi-user flows + QA agents |
| `playwright-skill` (lackeyjb) | Community skill | Single-skill simpler starter |

## Install Commands

```bash
# Playwright 1.56+
npm install -D @playwright/test@latest
npx playwright install --with-deps

# Playwright MCP for Claude Code
claude mcp add playwright npx @playwright/mcp@latest

# Restart Claude Code
```

## Key References

| Resource | URL |
|---|---|
| Playwright Test Agents docs | https://playwright.dev/docs/test-agents |
| Playwright MCP repo | https://github.com/microsoft/playwright-mcp |
| Planner agent prompt (source) | https://github.com/microsoft/playwright/blob/main/packages/playwright/src/agents/playwright-test-planner.agent.md |
| playwright-cli-agents | https://github.com/yusuftayman/playwright-cli-agents |
| qa-skills | https://github.com/neonwatty/qa-skills |
| playwright-skill | https://github.com/lackeyjb/playwright-skill |
| Spec-Driven Development with AI | https://www.javacodegeeks.com/2026/05/spec-driven-development-with-ai-write-the-spec-first-then-prompt-the-implementation.html |
| Writing a good spec for AI (Addy Osmani) | https://addyosmani.com/blog/good-spec/ |
| Writing better Gherkin (Cucumber) | https://cucumber.io/docs/bdd/better-gherkin/ |

## See Also

- [Playwright (E2E)](../playwright/) — the runner the Generator targets; locators, web-first assertions, fixtures, auth
- [Playwright for Visual Regression](../visual-regression/playwright/) — setup, config, Drupal/DDEV plumbing
- [Visual Regression Workflow](../visual-regression/workflow/) — adjacent workflow guide (pre-AI baseline strategies that still matter)
- [Automated Testing Kit (ATK)](../atk/) — Drupal-specific test catalog; integration patterns
- [HTML Report](../visual-regression/html-report/) — triage UI for generated test failures
