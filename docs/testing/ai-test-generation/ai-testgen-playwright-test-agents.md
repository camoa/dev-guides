---
description: Playwright Test Agents (1.56+) — the Planner, Generator, and Healer agents and how to invoke each via Claude Code.
tldr: "Playwright 1.56+ ships three agents: Planner (explores app via MCP, writes specs/feature.md), Generator (reads approved plan, writes tests/feature.spec.ts), Healer (fixes failing locators without touching assertions). Invoke via Claude Code with Playwright MCP installed. Never invoke the Generator without an approved plan, and never let the Healer rewrite assertions — only locators are the Healer's job."
---

# Playwright Test Agents

## When to Use

> Playwright 1.56+ ships three official agents. This is the canonical Plan-Generate-Heal toolchain.

## The Three Agents

**Planner** — explores the app via Playwright MCP, writes a Markdown test plan with `planner_save_plan` tool. Output: `specs/<feature>.md`.

**Generator** — reads an approved plan, writes Playwright code. Output: `tests/<feature>.spec.ts`.

**Healer** — reads a failing test, opens the app, finds new locators, patches the code. Tests cite `// spec:` and `// seed:` headers so regenerations stay traceable.

## Decision

| Use Test Agents | Hand-write |
|---|---|
| Net-new test coverage on existing site | One-off test for a tricky integration |
| Refresh after major UI redesign | Edge case the Planner can't articulate |
| User-story-driven feature work | Single-purpose smoke test |

### Required Setup

| Requirement | Why |
|---|---|
| Playwright 1.56+ | When Test Agents shipped |
| Playwright MCP server | How agents interact with the browser |
| Claude Code / Cursor / Copilot agent | Runs the agent prompts via MCP |
| Node/TS project | Java pending as of 2026-05 |

## Pattern: invoke Planner

Through Claude Code with Playwright MCP installed:

```
Use the Playwright Planner to write a test plan for the contact form.
Read web/modules/custom/site_contact/ for vocabulary.
Save the plan to specs/contact-form.md.
Scope: anonymous user submitting valid + invalid messages.
Out of scope: authenticated submissions, spam protection.
```

## Pattern: invoke Generator

```
Use the Playwright Generator to convert specs/contact-form.md
into tests/contact-form.spec.ts.
Seed: tests/seed.spec.ts.
Use playwright-bdd-style descriptions for test.step() if helpful.
```

## Pattern: invoke Healer

```
The test tests/contact-form.spec.ts:42 is failing in CI.
Use the Playwright Healer to update locators while preserving the plan.
Do not change assertions — only locators.
```

## Common Mistakes

- **Invoking the Generator without an approved plan** — defeats the review gate
- **Letting the Healer rewrite assertions** — assertions are the plan's contract; only locators are the Healer's job
- **Skipping the seed test** — every scenario needs a deterministic starting state

## See Also

- [Playwright MCP Setup](ai-testgen-playwright-mcp.md)
- [The Four-Phase Pattern](ai-testgen-four-phase-pattern.md)
- [End-to-End Workflow](ai-testgen-end-to-end-workflow.md)
- Reference: https://playwright.dev/docs/test-agents
