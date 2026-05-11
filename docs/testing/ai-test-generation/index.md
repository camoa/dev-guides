---
description: AI Test Generation — decision guides for the plan-first workflow, test plan authoring, Playwright Test Agents, and avoiding the encode-current-behavior trap.
guide-meta:
  concepts:
    - AI test generation
    - Playwright Test Agents
    - Planner agent
    - Generator agent
    - Healer agent
    - Playwright MCP
    - "@playwright/mcp"
    - test plan
    - specs/ directory
    - plan-first
    - plan review
    - encode-current-behavior
    - negative assertions
    - negative checks
    - acceptance criteria
    - four-phase pattern
    - plan vs code boundary
    - crawled site discovery
    - hybrid inputs
    - user story to test
    - Jira to test plan
    - seed test
    - Drupal test generation
    - ATK test generation
  not:
    - toHaveScreenshot (see testing/visual-regression/playwright)
    - visual regression (see testing/visual-regression)
    - ATK full catalog (see testing/atk)
    - Playwright locators fundamentals (see testing/playwright)
    - PHPUnit (see drupal/tdd)
  requires:
    - testing/playwright
  complements:
    - testing/atk
    - testing/playwright
    - testing/visual-regression/playwright
    - testing/visual-regression/workflow
  specializes: ""
  category: testing
---

# AI Test Generation

| I need to... | Guide | Summary |
|---|---|---|
| Decide when AI test generation pays off (and when to skip it) | [Overview](ai-testgen-overview.md) | Use AI generation when backfilling coverage on an existing site or translating a user story into tests. Skip it when you can't articulate what "correct" looks like — the agent will pick a definition for you. Always go plan-first; code without a reviewed plan skips the only review gate a non-developer can use. |
| Understand the Plan → Review → Generate → Heal cycle | [Four-Phase Pattern](ai-testgen-four-phase-pattern.md) | Every AI test generation cycle runs four phases: Plan (Planner writes a Markdown spec), Review (human approves), Generate (Generator writes code from the spec), Heal (Healer fixes locators when CI breaks). Never skip Plan or Review; editing tests instead of the spec causes silent drift. |
| Author or review a Markdown test plan | [Test Plan Format](ai-testgen-plan-format.md) | Plans use a specific Markdown hierarchy: H2 = epic, H3 = scenario group (test.describe), H4 = single test, numbered Steps, bulleted Expected results, bulleted Negative checks. Free-form prose breaks the Generator. |
| Decide what goes in the plan vs in generated code | [Plan vs Code Boundary](ai-testgen-plan-vs-code.md) | Scenario intent, step lists, acceptance criteria, negative assertions, and field labels belong in the plan. CSS selectors, wait tactics, fixtures, and data construction belong in generated code. If a manual tester could act on it by reading the rendered page, it goes in the plan. |
| Write acceptance criteria the Generator can turn into expect() calls | [Acceptance Criteria](ai-testgen-acceptance-criteria.md) | Write each criterion as an observable present-tense state ("The success message is visible") — one fact per bullet, independently checkable. The Generator emits one expect() per bullet. 7+ criteria in one scenario usually means split it. |
| Add negative assertions to every scenario | [Negative Assertions](ai-testgen-negative-assertions.md) | Include a "Negative checks" subsection in every scenario. The AI Planner encodes what it observes — explicit negative checks force the Planner and reviewer to think about what should NOT happen, catching bugs before they become enshrined as ground truth. |
| Seed plan generation from the codebase | [Input: Code Analysis](ai-testgen-input-code.md) | Point the Planner at routing + form + permissions + one existing spec — not the whole codebase. For Drupal, *.routing.yml and buildForm() yield routes, field labels, and required-field negatives automatically. Always combine code analysis with live exploration. |
| Translate a user story or Jira ticket into a test plan | [Input: User Stories](ai-testgen-input-user-stories.md) | Map "As an X, I want Y so that Z" to Preconditions = X, scenario title = "X does Y", first criterion = Z made observable. Extract Acceptance Criteria and Description only from Jira — tell the Planner explicitly not to add criteria from comments or related tickets. |
| Turn a vague developer prompt into a bounded plan | [Input: Raw Prompt](ai-testgen-input-raw-prompt.md) | Raw prompts produce over-broad crawls, hallucinated fields, and happy-path-only coverage. Have the Planner ask five scoping questions first, or produce a draft with a "Clarifications needed" block. |
| Scope a plan to a single flow or viewport | [Targeted Scope](ai-testgen-targeted-scope.md) | A scope-narrow prompt expresses: feature, surface (viewport + user agent), and explicit exclusions. Viewport goes in Preconditions, not Steps. Always plan a sibling desktop scenario — targeting only mobile misses responsive issues. |
| Use crawled-site discovery (and when not to) | [Crawled Site](ai-testgen-crawled-site.md) | Crawl-based discovery catches forgotten surfaces on inherited projects but produces flat, unmaintainable plans on Drupal sites. Use with strict path prefix restrictions, depth cap of 2, and admin/user exclusions — and treat output as discovery material, not production tests. |
| Combine multiple input modalities | [Hybrid Inputs](ai-testgen-hybrid-inputs.md) | When inputs conflict: user-story constraints win, code analysis fills vocabulary, live exploration validates, crawl only fills gaps inside scope. The Planner's job is reduction — output covering more surface than the input asked for is a Planner failure. |
| Set up Playwright Test Agents in the project | [Playwright Test Agents](ai-testgen-playwright-test-agents.md) | Playwright 1.56+ ships three agents: Planner (writes specs/feature.md), Generator (writes tests/feature.spec.ts from approved plan), Healer (fixes failing locators without touching assertions). Invoke via Claude Code with Playwright MCP installed. |
| Wire Playwright MCP into Claude Code | [Playwright MCP Setup](ai-testgen-playwright-mcp.md) | Install with `claude mcp add playwright npx @playwright/mcp@latest`, then restart Claude Code. Use Playwright MCP for test generation; Chrome DevTools MCP for performance traces. Never run against production URLs. |
| Run the full end-to-end generation loop | [End-to-End Workflow](ai-testgen-end-to-end-workflow.md) | The full loop is 10 steps from intent to CI. Three separate reviewers for plan, generated code, and every Healer patch — same-person review of all three defeats every gate. Includes review checklists for plans and generated code. |
| Apply the pattern with ATK or Drupal-specific tools | [Drupal & ATK Notes](ai-testgen-drupal-atk-notes.md) | For Drupal, point the Planner at routing + buildForm() + permissions. Use ATK's catalog for generic Drupal tests; AI generation for project-specific features. Set testIdAttribute:'data-qa-id' for stable selectors when ATK is installed. |
| Avoid the encode-current-behavior trap and other anti-patterns | [Anti-Patterns](ai-testgen-anti-patterns.md) | The AI Planner encodes what it observes — including bugs — as expected behavior. Mitigations: mandatory plan review, negative assertions, draft-only status, Healer auto-commit disabled. The triple-review rule (plan, code, Healer patch) applies without exception. |
| Find tool URLs and install commands | [Code Reference](ai-testgen-code-reference.md) | Core toolchain: Playwright 1.56+ Test Agents, @playwright/mcp, Claude Code. Install commands, key documentation URLs, and community skill packs. |
