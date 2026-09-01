---
description: "Source references and maintenance manifest for the ai test generation guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Web Sources
| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Playwright Test Agents docs | https://playwright.dev/docs/test-agents | 13, 18 | 2026-06-10 |
| Playwright MCP repo | https://github.com/microsoft/playwright-mcp | 14, 18 | 2026-06-10 |
| Planner agent prompt (source) | https://github.com/microsoft/playwright/blob/main/packages/playwright/src/agents/playwright-test-planner.agent.md | 13, 18 | 2026-06-10 |
| playwright-cli-agents (yusuftayman) | https://github.com/yusuftayman/playwright-cli-agents | 18 | 2026-06-10 |
| qa-skills (neonwatty) | https://github.com/neonwatty/qa-skills | 18 | 2026-06-10 |
| playwright-skill (lackeyjb) | https://github.com/lackeyjb/playwright-skill | 18 | 2026-06-10 |
| Spec-Driven Development with AI (javacodegeeks) | https://www.javacodegeeks.com/2026/05/spec-driven-development-with-ai-write-the-spec-first-then-prompt-the-implementation.html | 18 | 2026-06-10 |
| Writing a good spec for AI (Addy Osmani) | https://addyosmani.com/blog/good-spec/ | 18 | 2026-06-10 |
| Writing better Gherkin (Cucumber) | https://cucumber.io/docs/bdd/better-gherkin/ | 5, 18 | 2026-06-10 |

Internal cross-links to other dev-guides topics (TDD & Spec-Driven Development, ATK, Playwright E2E, Visual Regression) also appear in the guide body. They are related-guide references, not research sources, and are not listed here.

## Code Sources
| Module | Relative Path | Guide Sections | Version |
|--------|---------------|----------------|---------|
| Playwright Test Agents (Planner/Generator/Healer) | /home/camoa/node_modules/playwright/lib/agents/ | 13, 15 | 1.57.0 (npm) — guide states "1.56+"; the agent files, tool names (`planner_save_plan`), and Planner/Generator/Healer split match this installed copy |
| @playwright/test | /home/camoa/node_modules/@playwright/test/ | 14, 18 | 1.57.0 (npm) |

The Drupal-specific example code in Section 16 (`site_contact` module, `*.routing.yml`, the ATK seed script, `data-qa-id` selector hooks) is example code in the guide, not verified against an installed module. No `automated_testing_kit` or `site_contact` module exists under `/home/camoa/workspace/contrib/web`, so this pass could not confirm those specifics against a real Drupal installation. `@playwright/mcp` (the MCP server package used in Section 14) is not installed locally in this workspace; its registry version (0.0.80 at verification time) is not asserted in the guide text and is not verified in this pass.

## Version History
| Date | Change |
|------|--------|
| 2026-06-10 | Manifest reconstructed from the guide's own citations and the installed source. |
