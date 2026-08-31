---
description: Full end-to-end AI test generation loop — 10-step workflow, plan review checklist, code review checklist, and reviewer assignment guide.
tldr: "The full loop is 10 steps: state intent, gather inputs, invoke Planner, human reviews plan, commit plan, invoke Generator, human reviews code, run tests, commit on pass (or debug/Healer on fail), then CI runs with Healer on locator drift only. Three separate reviewers for plan, generated code, and every Healer patch — same-person review of all three defeats every gate."
---

# End-to-End Workflow

## When to Use

> Use this when running the full loop for a new feature from intent to CI.

## Pattern: 10-step workflow

```
1. State intent          → "Test the contact form per JIRA-1234"
2. Gather inputs         → user story + code paths + style reference
3. Invoke Planner        → produces specs/contact-form.md
4. Review plan (human)   → PM/dev/QA reads; approves/edits
5. Commit plan           → git add specs/contact-form.md
6. Invoke Generator      → produces tests/contact-form.spec.ts
7. Review code (human)   → developer reads. A tweak may fix a locator, a fixture or a name; it may not change what the test asserts. An assertion that looks wrong is a plan change, not a code edit.
8. Run tests             → npx playwright test contact-form
9. If pass → commit code → git add tests/contact-form.spec.ts
   If fail → debug:
   - Plan wrong? Edit plan, regenerate code
   - Site bug?   Open ticket, mark test fixme
   - Locator drift? Invoke Healer
10. CI runs forever      → Healer on locator drift only
```

## Pattern: review checklist for plans

- [ ] Title is a single imperative scenario
- [ ] Preconditions describe state only, not procedure
- [ ] Steps are 3–10 numbered behavioral actions
- [ ] Each expected result is observable
- [ ] Negative checks are present and specific
- [ ] Out-of-scope is explicit
- [ ] No selectors in plan
- [ ] No hallucinated fields (cross-check against live site or code)
- [ ] No invented acceptance criteria — every bullet traces to intent
- [ ] Clarifications block resolved before approval

## Pattern: review checklist for generated code

- [ ] Each `test()` maps to one scenario in the plan
- [ ] Each `test.step()` maps to one numbered step
- [ ] Each `expect()` maps to one bullet under Expected/Negative
- [ ] Selectors use `getByRole` / `getByLabel` / `getByTestId` — not class chains
- [ ] No `page.waitForTimeout(...)` — auto-wait or `waitForResponse`
- [ ] Helpers and fixtures used where appropriate (not inlined)
- [ ] `// spec:` and `// seed:` comments trace back to source artifacts

## Decision: who reviews what

| Artifact | Reviewer |
|---|---|
| Plan | PM / designer / QA / dev — anyone who understands the intent |
| Generated code | Developer — checks technical correctness |
| Healer patch | Developer — checks locator stability |

## Common Mistakes

- **Wrong**: Same person writes the plan, generates the code, and approves both → **Right**: no real review gate
- **Wrong**: Plan committed without running the Generator → **Right**: plan reviewed but not validated to be code-generable
- **Wrong**: Tests committed without re-running → **Right**: Generator output not verified to actually pass

## See Also

- [The Four-Phase Pattern](ai-testgen-four-phase-pattern.md)
- [Playwright Test Agents](ai-testgen-playwright-test-agents.md)
- [Anti-Patterns](ai-testgen-anti-patterns.md)
