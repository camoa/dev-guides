---
description: AI Test Generation — decision guides for the plan-first workflow, test plan authoring, Playwright Test Agents, and avoiding the encode-current-behavior trap.
tracks:
  - project: playwright
    registry: npm
    channel: stable
    declared: "1.56"
    verified: 2026-06-10
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
  category: testing
---

# AI Test Generation

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Decide when AI test generation pays off (and when to skip it) | [Overview](ai-testgen-overview.md) | Use AI generation when backfilling coverage on an existing site or translating a user story into tests. Skip it when you can't articulate what "correct" looks like — the agent will pick a definition for you. Always go plan-first; code without a reviewed plan skips the only review gate a non-developer can use. |
| Understand the Plan → Review → Generate → Heal cycle | [Four-Phase Pattern](ai-testgen-four-phase-pattern.md) | Every AI test generation cycle runs four phases: Plan (Planner agent writes a Markdown spec), Review (human approves), Generate (Generator writes code from the spec), Heal (Healer fixes locators when CI breaks). Never skip Plan or Review; the spec is the only artifact non-developers can review, and editing tests instead of the spec causes silent drift. |
| Author or review a Markdown test plan | [Test Plan Format](ai-testgen-plan-format.md) | Plans use a specific Markdown hierarchy: H2 = epic/area, H3 = scenario group (test.describe), H4 = single test, numbered Steps, bulleted Expected results, bulleted Negative checks. Each section has a correct detail level — steps are behavioral actions, not selector instructions. Free-form prose breaks the Generator. |
| Decide what goes in the plan vs in generated code | [Plan vs Code Boundary](ai-testgen-plan-vs-code.md) | Scenario intent, step lists, acceptance criteria, negative assertions, and field labels (user-facing) belong in the plan. CSS selectors, wait tactics, fixtures, and data construction belong in generated code or seed tests. Rule of thumb: if a manual tester could act on it by reading the rendered page, it goes in the plan. |
| Write acceptance criteria the Generator can turn into expect() calls | [Acceptance Criteria](ai-testgen-acceptance-criteria.md) | Write each criterion as an observable present-tense state ("The success message is visible") — one fact per bullet, independently checkable. The Generator emits one expect() per bullet. A scenario with 7+ criteria probably contains multiple concerns; split it. Never write code or vague prose in criteria bullets. |
| Add negative assertions to every scenario | [Negative Assertions](ai-testgen-negative-assertions.md) | Include a "Negative checks" subsection in every scenario. The AI Planner encodes what it observes — if the site has a bug, the generated assertion enshrines it. Explicit negative checks (no error messages, no console errors, no unexpected redirects) force the Planner and reviewer to think about what should NOT happen, catching the bug before it ships as ground truth. |
| Seed plan generation from the codebase | [Input: Code Analysis](ai-testgen-input-code.md) | Point the Planner at routing + form + permissions + one existing spec — not the whole codebase. For Drupal, *.routing.yml and buildForm() yield routes, field labels, and required-field negatives automatically. Always combine code analysis with live exploration — the rendered DOM (with hooks, Ajax fields, |
| Translate a user story or Jira ticket into a test plan | [Input: User Stories](ai-testgen-input-user-stories.md) | Map "As an X, I want Y so that Z" to: Preconditions = X, scenario title = imperative "X does Y", first criterion = Z made observable. When pulling from Jira, extract Acceptance Criteria and Description only — tell the Planner explicitly not to add criteria from the comment thread or related tickets. |
| Turn a vague developer prompt into a bounded plan | [Input: Raw Prompt](ai-testgen-input-raw-prompt.md) | Raw prompts ("test the checkout flow") produce over-broad crawls, hallucinated fields, and happy-path-only coverage. Prevent this by having the Planner ask five scoping questions before writing, or produce a draft plan with a "Clarifications needed" block. If scope can't be articulated, the Planner picks one representative happy path and one negative case — reviewer extends from there. |
| Scope a plan to a single flow or viewport | [Targeted Scope](ai-testgen-targeted-scope.md) | A scope-narrow prompt expresses three things: feature ("password reset"), surface ("mobile viewport 375×667, iOS Safari"), and explicit exclusions ("do not test login after reset"). Viewport goes in Preconditions (becomes test.use), not in Steps. Always plan a sibling desktop scenario — targeting only mobile misses responsive issues. |
| Use crawled-site discovery (and when not to) | [Crawled Site](ai-testgen-crawled-site.md) | Crawl-based plan generation catches forgotten surfaces on inherited projects but produces flat, unmaintainable plans on Drupal sites where infinite URL axes exist. Use it with strict path prefix restrictions, depth cap of 2, and admin/user exclusions — and treat the output as discovery material humans prune, not as production tests. |
| Combine multiple input modalities | [Hybrid Inputs](ai-testgen-hybrid-inputs.md) | When inputs conflict, user-story constraints win (define what's in/out), code analysis fills vocabulary (exact labels, routes, required fields), live exploration validates (the rendered DOM is authoritative), and crawl only fills gaps inside scope. The Planner's job is reduction, not expansion — output that covers more surface than the input requested is a Planner failure. |
| Set up Playwright Test Agents in the project | [Playwright Test Agents](ai-testgen-playwright-test-agents.md) | Playwright 1.56+ ships three agents: Planner (explores app via MCP, writes specs/feature.md), Generator (reads approved plan, writes tests/feature.spec.ts), Healer (fixes failing locators without touching assertions). Invoke via Claude Code with Playwright MCP installed. Never invoke the Generator without an approved plan, and never let the Healer rewrite assertions — only locators are the Healer's job. |
| Wire Playwright MCP into Claude Code | [Playwright MCP Setup](ai-testgen-playwright-mcp.md) | Install with `claude mcp add playwright npx @playwright/mcp@latest`, then restart Claude Code. The MCP exposes browser_navigate, browser_snapshot (accessibility-tree, ~13.7k tokens), browser_click, browser_type, and others. Use Playwright MCP for test generation; Chrome DevTools MCP for performance traces. Never run MCP against production URLs — the agent will navigate, click, and fill forms. |
| Run the full end-to-end generation loop | [End-to-End Workflow](ai-testgen-end-to-end-workflow.md) | The full loop is 10 steps: state intent, gather inputs, invoke Planner, human reviews plan, commit plan, invoke Generator, human reviews code, run tests, commit on pass (or debug/Healer on fail), then CI runs with Healer on locator drift only. Three separate reviewers for plan, generated code, and every Healer patch — same-person review of all three defeats every gate. |
| Apply the pattern with ATK or Drupal-specific tools | [Drupal & ATK Notes](ai-testgen-drupal-atk-notes.md) | For Drupal, point the Planner at *.routing.yml + buildForm() + *.permissions.yml. Use a seed test that runs drush si + recipe. If ATK is installed, set testIdAttribute:'data-qa-id' to get stable selectors for free. Always include Drupal-specific negative checks (watchdog, console errors, no unexpected /user/login redirects). Don't regenerate ATK's catalog — use ATK for generic Drupal tests, AI for project-specific feature tests. |
| Avoid the encode-current-behavior trap and other anti-patterns | [Anti-Patterns](ai-testgen-anti-patterns.md) | The top anti-pattern is encode-current-behavior: the AI Planner observes the site as-is and asserts that bugs are expected behavior, causing the suite to pass forever while shipping the bug. Mitigations are mandatory plan review, negative assertions in every scenario, draft-only status until human edits, and Healer auto-commit disabled. The triple-review rule (plan intent, generated code, every Healer patch) applies without exception. |
| Find tool URLs and install commands | [Code Reference](ai-testgen-code-reference.md) | Core toolchain is Playwright 1.56+ Test Agents (built-in Planner/Generator/Healer), @playwright/mcp MCP server, and Claude Code as the AI harness. Install with npm install -D @playwright/test@latest and claude mcp add playwright npx @playwright/mcp@latest. Community skill packs (playwright-cli-agents, qa-skills) extend the pattern with page-object awareness and multi-user flows. |
